# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CmCategory(models.Model):
    _name = 'cm.category'
    _description = 'Category'

    name = fields.Char(
        string='Name',
        required=True
    )

    deprecated = fields.Boolean(
        string='Deprecated'
    )
