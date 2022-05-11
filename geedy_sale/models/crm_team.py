# -*- coding: utf-8 -*-
# Copyright (C) 2020-Geedy System

from odoo import api, fields, models, SUPERUSER_ID, _

class CrmTeam(models.Model):
    _inherit = "crm.team"

    leader_commission_id = fields.Many2one('commission.periods', string='Leader Commission')
    member_commission_id = fields.Many2one('commission.periods', string='Members Commission')
