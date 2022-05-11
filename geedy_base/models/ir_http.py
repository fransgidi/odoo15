# -*- coding: utf-8 -*-
# Copyright (C) 2020-Geedy System

from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):

    _inherit = "ir.http"

    def session_info(self):
        result = super(IrHttp, self).session_info()
        company = request.session.uid and request.env.user.company_id
        blend_mode = company and company.background_blend_mode or False
        result.update(
            theme_background_blend_mode=blend_mode or "normal",
            theme_has_background_image=bool(company and company.background_image)
        )
        return result
