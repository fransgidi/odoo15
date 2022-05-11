# -*- coding: utf-8 -*-
# Copyright (C) 2020-Geedy System

from odoo import api, models, _

class PartnerLedgerReport(models.AbstractModel):
    _name = 'report.geedy_accounting.partner_ledger'

    @api.model
    def _get_report_values(self, docids, data=None):
        if self.env.context.get('partner_ledger_pdf_report'):

            if data.get('report_data'):
                data.update({'account_data': data.get('report_data')['report_lines'],
                             'Filters': data.get('report_data')['filters'],
                             'company': self.env.company,
                             })
        return data
