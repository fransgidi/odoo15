# -*- coding: utf-8 -*-
# Copyright (C) 2020-Geedy System

{
    'name': 'Full Accounting',
    'version': '15.0.1.1',
    'category': 'Accounting',
    'summary': """
    """,
    'description': """
    """,
    'author': 'Geedy System',
    # 'website': "",
    'company': 'Geedy System',
    'maintainer': 'Geedy System',
    'depends': ['base', 'account', 'sale', 'account_check_printing'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/account_financial_report_data.xml',
        'data/cash_flow_data.xml',
        'data/account_pdc_data.xml',
        'data/followup_levels.xml',
        'data/account_asset_data.xml',
        'data/recurring_entry_cron.xml',
        'data/multiple_invoice_data.xml',
        'views/account_analytic_account_views.xml',
        'views/account_budget_views.xml',
        'views/assets.xml',
        'views/dashboard_views.xml',
        'views/reports_config_view.xml',
        'views/accounting_menu.xml',
        'views/account_group.xml',
        'views/credit_limit_view.xml',
        'views/account_configuration.xml',
        'views/account_payment_view.xml',
        'views/res_config_view.xml',
        'views/recurring_payments_view.xml',
        'views/account_followup.xml',
        'views/followup_report.xml',
        'views/views.xml',
        # 'views/kit_menus.xml',
        'wizard/asset_depreciation_confirmation_wizard_views.xml',
        'wizard/asset_modify_views.xml',
        'views/account_asset_views.xml',
        'views/account_move_views.xml',
        'views/account_asset_templates.xml',
        'views/product_template_views.xml',
        'views/payment_matching.xml',
        'views/multiple_invoice_layout_view.xml',
        'views/multiple_invoice_form.xml',
        'wizard/financial_report.xml',
        'wizard/general_ledger.xml',
        'wizard/partner_ledger.xml',
        'wizard/tax_report.xml',
        'wizard/account_lock_date.xml',
        'wizard/trial_balance.xml',
        'wizard/aged_partner.xml',
        'wizard/journal_audit.xml',
        'wizard/cash_flow_report.xml',
        'wizard/account_bank_book_wizard_view.xml',
        'wizard/account_cash_book_wizard_view.xml',
        'wizard/account_day_book_wizard_view.xml',
        'report/report_financial.xml',
        'report/general_ledger_report.xml',
        'report/report_journal_audit.xml',
        'report/report_aged_partner.xml',
        'report/report_trial_balance.xml',
        'report/report_tax.xml',
        'report/report_partner_ledger.xml',
        'report/cash_flow_report.xml',
        'report/account_bank_book_view.xml',
        'report/account_cash_book_view.xml',
        'report/account_day_book_view.xml',
        'report/account_asset_report_views.xml',
        'report/report.xml',
        'report/multiple_invoice_layouts.xml',
        'report/multiple_invoice_report.xml',
        'report/trial_balance.xml',
        'report/general_ledger.xml',
        'report/financial_report_template.xml',
        'report/partner_ledger.xml',
        'report/ageing.xml',
        'report/daybook.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'geedy_accounting/static/src/scss/style.scss',
            'geedy_accounting/static/src/scss/account_asset.scss',
            'geedy_accounting/static/lib/bootstrap-toggle-master/css/bootstrap-toggle.min.css',
            'geedy_accounting/static/src/js/account_dashboard.js',
            'geedy_accounting/static/src/js/account_asset.js',
            'geedy_accounting/static/src/js/payment_model.js',
            'geedy_accounting/static/src/js/payment_render.js',
            'geedy_accounting/static/src/js/payment_matching.js',
            'geedy_accounting/static/lib/Chart.bundle.js',
            'geedy_accounting/static/lib/Chart.bundle.min.js',
            'geedy_accounting/static/lib/Chart.min.js',
            'geedy_accounting/static/lib/Chart.js',
            'geedy_accounting/static/lib/bootstrap-toggle-master/js/bootstrap-toggle.min.js',

            'geedy_accounting/static/src/css/report.css',
            'geedy_accounting/static/src/js/action_manager.js',
            'geedy_accounting/static/src/js/general_ledger.js',
            'geedy_accounting/static/src/js/trial_balance.js',
            'geedy_accounting/static/src/js/cash_flow.js',
            'geedy_accounting/static/src/js/financial_reports.js',
            'geedy_accounting/static/src/js/partner_ledger.js',
            'geedy_accounting/static/src/js/ageing.js',
            'geedy_accounting/static/src/js/daybook.js',

        ],
        'web.assets_qweb': [
            'geedy_accounting/static/src/xml/template.xml',
            'geedy_accounting/static/src/xml/payment_matching.xml',

            'geedy_accounting/static/src/xml/general_ledger_view.xml',
            'geedy_accounting/static/src/xml/trial_balance_view.xml',
            'geedy_accounting/static/src/xml/cash_flow_view.xml',
            'geedy_accounting/static/src/xml/financial_reports_view.xml',
            'geedy_accounting/static/src/xml/partner_ledger_view.xml',
            'geedy_accounting/static/src/xml/ageing.xml',
            'geedy_accounting/static/src/xml/daybook.xml',
        ],
    },
    'license': 'LGPL-3',
    'images': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
