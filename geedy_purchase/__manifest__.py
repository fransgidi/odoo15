# -*- coding: utf-8 -*-
# Copyright (C) 2020-Geedy System

{
    'name': 'Full Purchase',
    'version': '15.0.1.1',
    'category': 'Purchase',
    'summary': """
    """,
    'description': """
    """,
    'author': 'Geedy System',
    # 'website': "",
    'company': 'Geedy System',
    'maintainer': 'Geedy System',
    'depends': ['purchase', 'product', 'purchase_stock'],
    'data': [
        "security/purchase_request.xml",
        "security/ir.model.access.csv",
        "data/purchase_request_sequence.xml",
        "data/purchase_request_data.xml",
        "report/report_purchase_request.xml",
        "wizard/purchase_request_line_make_purchase_order_view.xml",
        "views/purchase_request_view.xml",
        "views/purchase_request_line_view.xml",
        "views/purchase_request_report.xml",
        "views/product_template.xml",
        "views/purchase_order_view.xml",
        "views/stock_move_views.xml",
        "views/stock_picking_views.xml",
    ],
    'qweb': [],
    'demo': [
        "demo/purchase_request_demo.xml"
    ],
    'license': 'LGPL-3',
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
