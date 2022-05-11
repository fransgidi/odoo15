# -*- coding: utf-8 -*-
# Copyright (C) 2020-Geedy System

import time
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools.safe_eval import safe_eval
from datetime import date, datetime, timedelta

# class SaleOrder(models.Model):
#     _inherit = "sale.order"

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    discount_type = fields.Selection([
        # ('percent', 'Percentage'),
        ('multi', 'Multi Percentage'),
        ('fix', 'Fix Discount')
    ], string='Discount Lines Type', default='multi')
    multi_discount = fields.Char(string='Multi (%) Discount', readonly=True, states={'draft': [('readonly', False)]})
    fix_discount = fields.Float('Fix Discount', copy=False, digits='Fix Discount', default=0.0, readonly=True, states={'draft': [('readonly', False)]})

    @api.onchange('discount_type')
    def _onchange_discount_type(self):
        for line in self:
            line.update({
                'multi_discount': '',
                'fix_discount': 0.0,
                'discount': 0.0,
            })

    @api.depends('product_uom_qty', 'discount_type', 'fix_discount', 'multi_discount', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        res = super(SaleOrderLine, self)._compute_amount()
        for line in self:
            if line.discount_type == 'multi' and line.multi_discount:
                persentage = line.multi_discount.split('+')
                disc = 1
                for persent in persentage:
                    persent2 = float(persent)
                    if isinstance(persent2, float):
                        disc = disc - (disc * (persent2/100))
                discount = (1 - disc) * 100
                price = line.price_unit * (1 - discount / 100.0)
                taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
                line.update({
                    'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'],
                    'discount': discount,
                })
            if line.discount_type == 'fix' and line.fix_discount > 0:
                if line.price_unit > 0:
                    discount = (line.fix_discount/line.price_unit) * 100
                else:
                    discount = 0.0
                price = line.price_unit - line.fix_discount
                taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
                line.update({
                    'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'],
                    'discount': discount,
                })
