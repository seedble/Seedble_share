# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ReferenceSector(models.Model):
    _name = 'reference.sector'
    _description = 'Reference Sector'

    name = fields.Char(
        string='Name',
        required=True
    )

    deprecated = fields.Boolean(
        string='Deprecated'
    )
