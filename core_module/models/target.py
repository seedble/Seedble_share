# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CmTarget(models.Model):
    _name = 'cm.target'
    _description = 'Target'

    name = fields.Char(
        string='Name',
        required=True
    )

    deprecated = fields.Boolean(
        string='Deprecated'
    )
