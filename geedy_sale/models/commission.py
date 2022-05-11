# -*- coding: utf-8 -*-
# Copyright (C) 2020-Geedy System

import time
from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

class CommissionSettlement(models.Model):
    _name = "commission.settlement"

    name =  fields.Char(string='Number', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]})
    base_on = fields.Selection([
        ('invoice', 'Invoice'),
        ('payment', 'Payment'),
        ], string='Base On', readonly=True, states={'draft': [('readonly', False)]}, default='invoice')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('settle', 'Settlement'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    leader_include_team_sales = fields.Boolean(string="Sales leader accumulated by team sales",
        help="Set true, if this commission is leader commissions and commission scheme sales are calculated by members team total sales.")
    comm_sale_line = fields.One2many('commission.sale', 'commission_id', string='Commission Scheme Sales', readonly=True, states={'draft': [('readonly', False)]})

    def unlink(self):
        for me in self:
            if me.state == 'settle':
                raise UserError(_('You can not delete a settle commission.'))
        return super(CommissionSettlement, self).unlink()

    def action_confirm(self):
        self.write({'state': 'settle'})

class CommissionSales(models.Model):
    _name = "commission.sale"

    commission_id = fields.Many2one('commission.settlement', string='Commission Settlement')
    min_target = fields.Float(string='Minimum')
    max_target = fields.Float(string='Maximum')
    type = fields.Selection([
        ('percent', 'Percentage Amount'),
        ('fix', 'Fix Amount'),
        ], string='Commission Type', default='percent')
    amount = fields.Float(string='Amount')

class CommissionPeriods(models.Model):
    _name = "commission.periods"

    name = fields.Char(string='Periods Name', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]})
    start_date = fields.Date(string='Start Date', readonly=True, copy=False, states={'draft': [('readonly', False)]}, default=fields.Datetime.now)
    end_date = fields.Date(string='End Date', readonly=True, copy=False, states={'draft': [('readonly', False)]}, default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('settle', 'Settlement'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    periods_line = fields.One2many('commission.periods.line', 'periods_id', string='Commission Periods Scheme', readonly=True, states={'draft': [('readonly', False)]})

    def unlink(self):
        for me in self:
            if me.state == 'settle':
                raise UserError(_('You can not delete a settle commission periods.'))
        return super(CommissionPeriods, self).unlink()

    def action_confirm(self):
        for line in self.periods_line:
            if line.start_date < self.start_date or line.end_date > self.end_date:
                raise UserError(_('You have to set start date and end date in line arrage between %s and %s.') % (self.start_date, self.end_date))
        self.write({'state': 'settle'})

    def create_monthly(self):
        interval = 1
        for me in self:
            self.env['commission.periods.line'].search([('periods_id','=',me.id)]).unlink()
            ds = me.start_date
            while ds < me.end_date:
                de = ds + relativedelta(months=interval, days=-1)
                if de > me.end_date:
                    de = me.end_date
                vals = {
                    'start_date': ds,
                    'end_date': de,
                    'comm_settle_id': self.env['commission.settlement'].search([], limit=1).id,
                    'periods_id': me.id
                }
                self.env['commission.periods.line'].create(vals)
                ds = ds + relativedelta(months=interval)

class CommissionPeriodsLine(models.Model):
    _name = "commission.periods.line"

    periods_id = fields.Many2one('commission.periods', string='Commission Periods')
    start_date = fields.Date(string='Start Date', default=fields.Datetime.now)
    end_date = fields.Date(string='End Date', default=fields.Datetime.now)
    comm_settle_id = fields.Many2one('commission.settlement', string='Commission Settlement')

class CommissionCommission(models.Model):
    _name = "commission.commission"

    salesperson = fields.Many2one('res.users', string='Salesperson')
    sales_team = fields.Many2one('crm.team', string='Sales Team')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    amount_reach = fields.Float(string='Total Sales Amount')
    commission_amount = fields.Float(string='Commission')

    def unlink(self):
        for me in self:
            raise UserError(_('Forbidden to delete report.'))
        return super(CommissionCommission, self).unlink()
