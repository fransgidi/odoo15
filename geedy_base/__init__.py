# -*- coding: utf-8 -*-
# Copyright (C) 2020-Geedy System

from . import models

from odoo import api, SUPERUSER_ID


def _uninstall_reset_changes(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['web_editor.assets'].reset_asset(
        '/geedy_base/static/src/colors.scss',
        'web._assets_primary_variables'
    )
