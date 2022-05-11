# -*- coding: utf-8 -*-
# Copyright (C) 2020-Geedy System

{
    'name': 'Full Sale',
    'version': '15.0.1.1',
    'category': 'Sale',
    'summary': """
    """,
    'description': """
    """,
    'author': 'Geedy System',
    # 'website': "",
    'company': 'Geedy System',
    'maintainer': 'Geedy System',
    'depends': ['sale','sales_team'],
    'data': [
        "security/ir.model.access.csv",
        "views/sale_order_view.xml",
        "views/menu_view.xml",
        "views/commission_settle_view.xml",
        "views/commission_periods_view.xml",
        "views/crm_team_view.xml",
        "views/commission_commission_view.xml",
    ],
    'qweb': [],
    'demo': [
    ],
    'license': 'LGPL-3',
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
