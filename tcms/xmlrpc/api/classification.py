 # -*- coding: utf-8 -*-

 from modernrpc.core import rpc_method

 from tcms.testcases.models import Classification

 @rpc_method(name='Classification.filter')
 def filter(query):
     """
     .. function:: XML-RPC Classification.filter(query)

         Search and return Classification objects matching query.

         :param query: Field lookups for :class:`tcms.testcases.models.Classification`
         :type query: dict
         :return: List of serialized :class:`tcms.testcases.models.Classification` objects
         :rtype: list(dict)
     """
     return Classification.to_xmlrpc(query)

 @permissions_required('management.add_classification')
 @rpc_method(name='Classification.create')
 def create(values, **kwargs):
     """
         function:: XML-RPC Classification.create(values)
         Create a new Classification object and store it in the database.

         :param values: Field values for class `tcms.management.models.Classification`
         :type values: dict
         :return Serialized :class:`tcms.management.models.Classification` object
         :rtype: dict
         :raises: PermissionDenied if missing *management.add_product* permission
         :raises: ValueError if a value already exists for the associated  property

         Minimal Classification parameters::
             >>> values = {
                     'name': 'ProductName',
                     'description': 'Product description',
                     'sortkey': 'integer'
                     }
     """
     new_classification = Classification.create(values)
     if not new_classification:
         raise ValueError(('The classification "{}" already exists').format(values['name']))
     result = new_classification.serialize()
     return result
