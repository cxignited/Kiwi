# -*- coding: utf-8 -*-

from modernrpc.core import rpc_method, REQUEST_KEY

from tcms.management.models import EnvGroup
from tcms.xmlrpc.utils import parse_bool_value

from tcms.xmlrpc.decorators import permissions_required


@rpc_method(name='Env.Group.filter')
def filter(query):  # pylint: disable=invalid-name
    """
    .. function:: XML-RPC Env.Group.filter(query)

        Perform a search and return the resulting list of
        :class:`tcms.management.models.EnvGroup` objects.

        :param query: Field lookups for :class:`tcms.management.models.EnvGroup`
        :type query: dict
        :returns: List of serialized :class:`tcms.management.models.EnvGroup` objects
        :rtype: list(dict)
    """
    if 'is_active' in query:
        query['is_active'] = parse_bool_value(query['is_active'])
    return EnvGroup.to_xmlrpc(query)


@permissions_required("management.add_envgroup")
@rpc_method(name='Env.Group.create')
def create(values, **kwargs):
    """
    .. function:: XML-RPC Env.Group.create(values)

        Create a new EnvGroup object and store in the database

        :param values: Field values for :class:`tcms.management.models.EnvGroup`
        :type values: dict
        :return: Serialized :class: `tcsm.management.models.EnvGroup` object
        :rtype: dict
        :raises PermissionDenied if missing *management.add_envgroup* permission
        :raises ValueError if the envGroup already exists

        Mininal test case parameters::

            >>> values = {
                'name': 'group1',
                'property': ['prop1','prop2'],
                'is_active':True
            }
            >>> EnvGroup.create(values)
    """
    author = kwargs.get(REQUEST_KEY).user
    values.update({'manager': author, 'modified_by': author})
    new_env_group = EnvGroup.create(values)
    if not new_env_group:
        raise ValueError('The env group "{}"'
                         ' already exists'.format(values['name']))
