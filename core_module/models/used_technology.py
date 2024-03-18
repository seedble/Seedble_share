# -*- coding: utf-8 -*-

from odoo import models, fields, api


class UsedTechnology(models.Model):
    _name = 'used.technology'
    _description = 'Used Technology'

    name = fields.Char(
        string='Name',
        required=True
    )

    deprecated = fields.Boolean(
        string='Deprecated'
    )
