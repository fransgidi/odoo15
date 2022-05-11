# -*- coding: utf-8 -*-
# Copyright (C) 2020-Geedy System

from odoo import models


class AccountTaxReport(models.TransientModel):
    _inherit = "account.common.report"
    _name = 'kit.account.tax.report'
    _description = 'Tax Report'

    def _print_report(self, data):
        return self.env.ref(
            'geedy_accounting.action_report_account_tax').report_action(
            self, data=data)
