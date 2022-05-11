# -*- coding: utf-8 -*-
# Copyright (C) 2020-Geedy System

from odoo import fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    budget_line = fields.One2many('budget.lines', 'analytic_account_id', 'Budget Lines')
