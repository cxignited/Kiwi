# -*- coding: utf-8 -*-

from modernrpc.core import rpc_method

from tcms.management.models import EnvValue
from tcms.xmlrpc.utils import parse_bool_value
from tcms.xmlrpc.decorators import permissions_required


@rpc_method(name='Env.Value.filter')
def filter(query):  # pylint: disable=invalid-name
    """
    .. function:: XML-RPC Env.Value.filter(query)

        Performs a search and returns the resulting list of environment values.

        :param query: Field lookups for :class:`tcms.management.models.EnvValue`
        :type query: dict
        :returns: List of serialized :class:`tcms.management.models.EnvValue` objects
        :rtype: list(dict)
    """
    if 'is_active' in query:
        query['is_active'] = parse_bool_value(query['is_active'])
    return EnvValue.to_xmlrpc(query)


@permissions_required('management.add_envvalue')
@rpc_method(name='Env.Value.create')
def create(values, **kwargs):
    """
    .. function:: XML-RPC Env.Value.create(values)
        Create a new EnvValue object and store it in the database.

        :param values: Field values for class `tcms.management.models.EnvValue`
        :type values: dict
        :return: Serialized :class:`tcms.management.models.EnvValue` object
        :rtype: dict
        :raises: PermissionDenied if missing *management.add_envvalue* permission
        :raises: ValueError if a value already exists for the associated property

        Minimal env value parameters::
            >>> values = {
                'value': 'x86_64',
                'property': 'OS',
                'is_active': True,
            }
            >>> EnvValues.create(values)
    """
    new_env_val = EnvValue.create(values)
    print("ENVVVVV: {}".format(new_env_val))
    if not new_env_val:
        raise ValueError(('The env value "{}" already exists '
                          'for the env property "{}"').format(values['value'], values['property']))

    result = new_env_val.serialize()
    return result
