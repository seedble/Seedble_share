# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class CmDashboard(models.Model):
    _name = 'cm.dashboard'
    _description = 'Dashboard'
    _order = 'name'

    name = fields.Char(
        string='Name',
        required=True
    )

    menu_id = fields.Many2one(
        comodel_name='ir.ui.menu',
        string='Menu',
        required=True,
        domain=lambda self: [('parent_id', '=', self.env.ref('core_module.core_module_config_menu').id)],
        help='Link Card to Menu Item'
    )

    rec_count = fields.Integer(
        string='Record Count',
        compute='compute_rec_count'
    )

    @api.onchange('menu_id')
    def onchange_menu_id(self):
        self.name = self.menu_id.name

    @api.constrains('menu_id')
    def check_duplicate_menu(self):
        for rec in self:
            rec_ids = rec.search([('menu_id', '=', rec.menu_id.id)]) - rec
            if rec_ids:
                raise UserError('Record for menu already exist.')

    def action_create_record(self):
        return {
            'res_model': self.menu_id.action.res_model,
            'type': 'ir.actions.act_window',
            'views': [(False, 'form')],
        }

    def open_menu_action(self):
        action = self.menu_id.action.sudo().read()[0]
        return action

    def compute_rec_count(self):
        for rec in self:
            rec.rec_count = self.env[rec.menu_id.action.res_model].search_count([])
