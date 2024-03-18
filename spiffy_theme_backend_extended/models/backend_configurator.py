# -*- coding: utf-8 -*-

from odoo import api, fields, models

class BackendConfigInherit(models.Model):
	_inherit = 'backend.config'

	light_primary_btn_color = fields.Char(string="Primary Button Color for light",default="#0097a7")
