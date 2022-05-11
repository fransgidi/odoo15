# -*- coding: utf-8 -*-
# Copyright (C) 2020-Geedy System

from odoo import api, fields, models, SUPERUSER_ID, _

class AccountMove(models.Model):
    _inherit = "account.move"

    def entitle_commission(self):
        if self.invoice_user_id and self.team_id and self.invoice_user_id != self.team_id.user_id and self.invoice_user_id in self.team_id.member_ids and self.team_id.member_commission_id:
            for periods in self.team_id.member_commission_id.periods_line:
                if periods.start_date <= self.invoice_date <= periods.end_date:
                    if periods.comm_settle_id.base_on == 'invoice':
                        self._commission_base_invoice('members')
                    else:
                        self._commission_base_payment('members')
        if self.invoice_user_id and self.team_id and self.invoice_user_id == self.team_id.user_id and self.invoice_user_id not in self.team_id.member_ids and self.team_id.leader_commission_id:
            for periods in self.team_id.leader_commission_id.periods_line:
                if periods.start_date <= self.invoice_date <= periods.end_date:
                    if periods.comm_settle_id.base_on == 'invoice':
                        self._commission_base_invoice('leader')
                    else:
                        self._commission_base_payment('leader')

    def action_post(self):
        res = super(AccountMove, self).action_post()
        self.entitle_commission()
        return res

    def _commissions(self,period_id,start_d=fields.Datetime.now,end_d=fields.Datetime.now,status='inv'):
        domain = [('invoice_date','>=',start_d),
                ('invoice_date','<=',end_d),
                ('state','=','posted'),
                ]
        if period_id.comm_settle_id.leader_include_team_sales == True:
            users = self.team_id.member_ids.ids
            if self.invoice_user_id.id not in users:
                users.append(self.invoice_user_id.id)
            domain += [('invoice_user_id','in',users)]
        else:
            domain += [('invoice_user_id','=',self.invoice_user_id.id)]
        if status != 'inv':
            domain += [('payment_state','=','paid')]
        inv_ids = self.search(domain)
        amount_total = 0.0
        for inv in inv_ids:
            amount_total += inv.amount_total
        commission_id = self.env['commission.commission'].search([('salesperson','=',self.invoice_user_id.id),
                                    ('sales_team','=',self.team_id.id),
                                    ('start_date','=',start_d),
                                    ('end_date','=',end_d),
                                ])
        if not commission_id:
            commission_id = self.env['commission.commission'].create({
                            'salesperson': self.invoice_user_id.id,
                            'sales_team': self.team_id.id,
                            'start_date': start_d,
                            'end_date': end_d,
                            'amount_reach': 0.0,
                            'commission_amount': 0.0,
                        })
        commission_id.write({'amount_reach': amount_total})
        for sale in period_id.comm_settle_id.comm_sale_line:
            if sale.min_target <= amount_total <= sale.max_target:
                if sale.type == 'fix':
                    commission_id.write({'commission_amount': sale.amount})
                else:
                    commission_id.write({'commission_amount': (amount_total * ( sale.amount / 100 ))})

    def _commission_base_invoice(self, person='members'):
        if person == 'members':
            for periods in self.team_id.member_commission_id.periods_line:
                if periods.start_date <= self.invoice_date <= periods.end_date:
                    self._commissions(periods, periods.start_date, periods.end_date, 'inv')

        if person == 'leader':
            for periods in self.team_id.leader_commission_id.periods_line:
                if periods.start_date <= self.invoice_date <= periods.end_date:
                    self._commissions(periods, periods.start_date, periods.end_date, 'inv')

    def _commission_base_payment(self, person='members'):
        if person == 'members':
            for periods in self.team_id.member_commission_id.periods_line:
                if periods.start_date <= self.invoice_date <= periods.end_date:
                    self._commissions(periods, periods.start_date, periods.end_date, 'pay')

        if person == 'leader':
            for periods in self.team_id.leader_commission_id.periods_line:
                if periods.start_date <= self.invoice_date <= periods.end_date:
                    self._commissions(periods, periods.start_date, periods.end_date, 'pay')
