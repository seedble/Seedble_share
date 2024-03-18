# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CmKeyword(models.Model):
    _name = 'cm.keyword'
    _description = 'Keyword'

    name = fields.Char(
        string='Name',
        required=True
    )

    deprecated = fields.Boolean(
        string='Deprecated'
    )
