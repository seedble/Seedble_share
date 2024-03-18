# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CmRole(models.Model):
    _name = 'cm.role'
    _description = 'Role'

    name = fields.Char(
        string='Name',
        required=True
    )

    deprecated = fields.Boolean(
        string='Deprecated'
    )
