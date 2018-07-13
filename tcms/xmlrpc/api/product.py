# -*- coding: utf-8 -*-

from modernrpc.core import rpc_method

from tcms.management.models import Product
from tcms.xmlrpc.decorators import permissions_required

@rpc_method(name='Product.filter')
def filter(query):
    """
    .. function:: XML-RPC Product.filter(query)

        Perform a search and return the resulting list of products.

        :param query: Field lookups for :class:`tcms.management.models.Product`
        :type query: dict
        :return: Serialized list of :class:`tcms.management.models.Product` objects
        :rtype: dict

    Example::

        # Get all of products named 'Red Hat Enterprise Linux 5'
        >>> Product.filter({'name': 'Red Hat Enterprise Linux 5'})
    """
    return Product.to_xmlrpc(query)

@permissions_required('management.add_product')
@rpc_method(name='Product.create')
def create(values, **kwargs):
    """
        function:: XML-RPC Product.create(values)
        Create a new Product object and store it in the database.

        :param values: Field values for class `tcms.management.models.Product`
        :type values: dict
        :return Serialized :class:`tcms.management.models.Product` object
        :rtype: dict
        :raises: PermissionDenied if missing *management.add_product* pewrmission
        :raises: ValueError if a value already exists for the associated property

        Minimal Product parameters::
            >>> values = {
                    'name': 'ProductName',
                    'classification': 'ClassificationName',
                    'description': 'Product description',
                    }
    """
    new_product = Product.create(values)
    if not new_product:
        raise ValueError(('The product"{}" already exists').format(values['name']))
    result = new_product.serialize()
    return result
