# -*- coding: utf-8 -*-
# Copyright (C) 2020-Geedy System

{
    'name': 'Base Module',
    'version': '15.0.1.1',
    'category': 'Base',
    'summary': """
    """,
    'description': """
    """,
    'author': 'Geedy System',
    # 'website': "",
    'company': 'Geedy System',
    'maintainer': 'Geedy System',
    'depends': [
        'base_setup',
        'web_editor',
        'mail',
    ],
    'excludes': ['web_enterprise'],
    'data': [
       'templates/webclient.xml',
       'views/res_config_settings_view.xml',
       'views/res_users.xml',
    ],
    'assets': {
        'web.assets_qweb': [
            'geedy_base/static/src/**/*.xml',
        ],
        'web._assets_primary_variables': [
            'geedy_base/static/src/colors.scss',
        ],
        'web._assets_backend_helpers': [
            'geedy_base/static/src/variables.scss',
            'geedy_base/static/src/mixins.scss',
        ],
        'web.assets_backend': [
            'geedy_base/static/src/webclient/**/*.scss',
            'geedy_base/static/src/webclient/**/*.js',
            'geedy_base/static/src/search/**/*.scss',
            'geedy_base/static/src/search/**/*.js',
            'geedy_base/static/src/legacy/**/*.scss',
            'geedy_base/static/src/legacy/**/*.js',
        ],
    },
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
    'uninstall_hook': '_uninstall_reset_changes',
}
