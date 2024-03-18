# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    def _default_access_pack(self):
        default_user_id = self.env['ir.model.data']._xmlid_to_res_id('base.default_user', raise_if_not_found=False)
        return self.env['res.users'].browse(default_user_id).sudo().access_management_ids if default_user_id else []

    access_management_ids = fields.Many2many(
        comodel_name='access.management',
        relation='access_management_users_rel_ah',
        column1='user_id',
        column2='access_management_id',
        string='Access Pack',
        default=_default_access_pack
    )
