# -*- coding: utf-8 -*-

from modernrpc.core import rpc_method

from tcms.management.models import EnvProperty
from tcms.xmlrpc.utils import parse_bool_value

from tcms.xmlrpc.decorators import permissions_required


@rpc_method(name='Env.Property.filter')
def filter(query):
    """
    .. function:: XML-RPC Env.Property.filter(query)

        Performs a search and returns the resulting list of environment properties.

        :param query: Field lookups for :class:`tcms.management.models.EnvProperty`
        :type query: dict
        :returns: List of serialized :class:`tcms.management.models.EnvProperty` objects
        :rtype: list(dict)
    """
    if 'is_active' in query:
        query['is_active'] = parse_bool_value(query['is_active'])
    return EnvProperty.to_xmlrpc(query)


@permissions_required("management.add_envproperty")
@rpc_method(name='Env.Property.create')
def create(values, **kwargs):
        """
        .. function:: XML-RPC Env.Property.create(values, **kwargs)

            Create a new EnvProperty and store it in the database

            :param values: Field values for class `tcms.management.models.EnvProperty`
            :type values: dict
            :return: Serialized :class:`tcms.management.models.EnvProperty` object
            :rtype: dict
            :raises: PermissionDenied if missing *management.add_envvalue* permission
            :raises: ValueError if a value already exists for the associated property

            Minimal env value parameters::
                >>> values = {
                    'value': 'x86_64',
                    'property': 'OS',
                    'property_id': 2,
                    'is_active': True,
                }
        """
        new_env_property = EnvProperty.create(values)
        if not new_env_property:
            raise ValueError(('The env property'
                              '"{}" already exists').format(values['name']))

        result = new_env_property.serialize()
        return result
