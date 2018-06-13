import os
import random

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import tcms_api
from tcms.tests.factories import UserFactory
from tcms.tests.factories import ProductFactory
from tcms.tests.factories import VersionFactory
from tcms.tests.factories import TagFactory
from tcms.tests.factories import ComponentFactory
from tcms.tests.factories import TestCaseRunFactory
from tcms.tests.factories import CategoryFactory

from tcms.testcases.models import BugSystem
from tcms.core.contrib.auth.backends import initiate_user_with_default_setups


class BaseAPIClient_TestCase(StaticLiveServerTestCase):
    """
        Bring up a local Django instance and
        prepare test data - create Test Cases, Test Plans and Test Runs
    """

    # reload data which came from migrations like standard
    # groups Admin and Tester
    serialized_rollback = True

    # how many test objects to create
    num_cases = 1
    num_plans = 1
    num_runs = 1

    # NOTE: we setup the required DB data and API objects here
    # because this method is executed *AFTER* setUpClass() and the
    # serialized rollback is not yet available during setUpClass()
    # execution
    def _fixture_setup(self):
        # restore the serialized data from initial migrations
        # this includes default groups and permissions
        super(BaseAPIClient_TestCase, self)._fixture_setup()

        # reset connection to server b/c the address changes for
        # every test and the client caches this as a class attribute
        tcms_api.TCMS._connection = None
        # also the config is a singleton so reset that too
        # to force config reload
        tcms_api.Config._instance = None

        # API user
        self.api_user, _ = User.objects.get_or_create(
            username='api-tester',
            email='api@example.com')
        self.api_user.set_password('testing')
        initiate_user_with_default_setups(self.api_user)

        # WARNING: for now we override the config file
        # until we can pass the testing configuration
        # TODO: change config values instead of overwriting files on disk
        conf_path = os.path.expanduser('~/.tcms.conf')
        conf_fh = open(conf_path, 'w')
        conf_fh.write("""[tcms]
url = %s/xml-rpc/
username = %s
password = %s
""" % (self.live_server_url, self.api_user.username, 'testing'))
        conf_fh.close()

        self.rpc_client = tcms_api.TCMS()._server

        # create the product first so we can fetch it via API
        f_product = ProductFactory()
        self.product = self.rpc_client.Product.filter(name=f_product.name)[0]

        f_version = VersionFactory(product=f_product)
        self.version = self.rpc_client.Version.filter(product=self.product,
                                                      version=f_version.value)[0]

        self.plantype = self.rpc_client.PlanType.filter(name="Function")[0]

        CategoryFactory(name='Security', product=f_product)
        CategoryFactory(name='Sanity', product=f_product)
        f_category = CategoryFactory(product=f_product)
        self.category = self.rpc_client.Category.filter(category=f_category.name,
                                                        product=self.product)[0]

        f_component = ComponentFactory(product=f_product)
        self.component = self.rpc_client.Component.filter(name=f_component.name,
                                                          product=self.product)[0]

        self.CASESTATUS = self.rpc_client.TestCaseStatus.filter(name="CONFIRMED")[0]
        self.build = self.rpc_client.Build.filter(product=self.product, build="unspecified")[0]

        f_tags = [TagFactory() for i in range(20)]
        self.tags = [self.rpc_client.Tag.filter(pk=t.pk)[0] for t in f_tags]

        f_users = [UserFactory() for i in range(50)]
        self.TESTERS = [self.rpc_client.User.filter(pk=u.pk)[0] for u in f_users]

        # Create test cases
        self.cases = []
        for case_count in range(self.num_cases):
            testcase = self.rpc_client.TestCase.create(
                category=self.category['pk'],
                product=self.product['pk'],
                summary="Test Case {0}".format(case_count + 1),
                status=self.CASESTATUS['pk'])
            # Add a couple of random tags and the default tester
            for counter in range(10):
                tag = random.choice(self.tags)  # nosec:B311:blacklist
                self.rpc_client.TestCase.add_tag(testcase['pk'], tag['name'])

            default_tester = random.choice(self.TESTERS)['pk']  # nosec:B311:blacklist
            self.rpc_client.TestCase.update(default_tester=default_tester)
            self.cases.append(testcase)

        # Create master test plan (parent of all)
        self.master = self.rpc_client.TestPlan.create(
            name="API client Test Plan",
            text='Master TP created from API',
            product=self.product['pk'],
            version=self.version['pk'],
            type=self.plantype['pk'],
            owner=self.api_user.pk)

        for case in self.cases:
            self.rpc_client.TestPlan.add_case(self.master['pk'], case['pk'])

        # Create child test plans
        self.testruns = []
        for plan_count in range(self.num_plans):
            testplan = self.rpc_client.TestPlan.create(
                name="Test Plan {0}".format(plan_count + 1),
                text='Child TP created from API',
                product=self.product['pk'],
                version=self.version['pk'],
                parent=self.master['pk'],
                type=self.plantype['pk'])
            # Link all test cases to the test plan
            for case in self.cases:
                self.rpc_client.TestPlan.add_case(testplan['pk'], case['pk'])

            # Create test runs
            for run_count in range(self.num_runs):
                testrun = self.rpc_client.TestRun.create(
                    testplan=testplan['pk'],
                    build=self.build['pk'],
                    product=self.product['pk'],
                    summary="Test Run {0}".format(run_count + 1),
                    version=self.version.name)
                self.testruns.append(testrun)

        # Create a TestCaseRun object
        self.caserun = TestCaseRunFactory()
        self.caserun.add_bug(1234, BugSystem.objects.first().pk)
