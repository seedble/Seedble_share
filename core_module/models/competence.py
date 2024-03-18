# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CmCompetence(models.Model):
    _name = 'cm.competence'
    _description = 'Competence'

    name = fields.Char(
        string='Name',
        required=True
    )

    deprecated = fields.Boolean(
        string='Deprecated'
    )
