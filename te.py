#!/usr/bin/env python3.6

from tcms_api.base import TCMS

if __name__ == "__main__":
    tcms = TCMS()
    # print(tcms._server.Env.Property.filter({'name': 'prop5'}))
    # tcms._server.Env.Value.create(
    #     {'value': 'value20', 'property': 'prop5', 'is_active': True})
    # print(tcms._server.Env.Value.filter({'property__name': 'prop5'}))
    #print(tcms._server.Env.Value.filter({'id__gt': 0}))
    # tcms._server.Env.Property.create({'name': 'prop8', 'is_active': True})
    #print(tcms._server.Env.Property.filter({'id__gt': 0}))
    #tcms._server.Env.Group.create(
     #   {'name': 'group4', 'property': ['prop8', 'prop6'], 'is_active': True}
    #)
    print(tcms._server.Classification.create(
        {'name':'roo', 'description':'tee', 'sortkey':'1'}
        )
    )
    print(tcms._server.Product.create(
        {'name': 'group4', 'classification': 'roo', 'description': 'erwrg'}
        )
    )
