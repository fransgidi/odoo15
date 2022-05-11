# -*- coding: utf-8 -*-
# Copyright (C) 2020-Geedy System

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    purchase_request = fields.Boolean(
        help="Check this box to generate Purchase Request instead of "
        "generating Requests For Quotation from procurement.",
        company_dependent=True,
    )
