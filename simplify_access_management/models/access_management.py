from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.http import request


class access_management(models.Model):
    _name = 'access.management'
    _description = "Access Management"

    name = fields.Char('Name')
    user_ids = fields.Many2many('res.users', 'access_management_users_rel_ah', 'access_management_id', 'user_id',
                                'Users')

    readonly = fields.Boolean('Read-Only')
    active = fields.Boolean('Active', default=True)

    hide_menu_ids = fields.Many2many('ir.ui.menu', 'access_management_menu_rel_ah', 'access_management_id', 'menu_id',
                                     'Hide Menu')
    hide_field_ids = fields.One2many('hide.field', 'access_management_id', 'Hide Field', copy=True)

    remove_action_ids = fields.One2many('remove.action', 'access_management_id', 'Remove Action', copy=True)

    access_domain_ah_ids = fields.One2many('access.domain.ah', 'access_management_id', 'Access Domain', copy=True)
    hide_view_nodes_ids = fields.One2many('hide.view.nodes', 'access_management_id', 'Button/Tab Access', copy=True)

    self_module_menu_ids = fields.Many2many('ir.ui.menu', 'access_management_ir_ui_self_module_menu',
                                            'access_management_id', 'menu_id', 'Self Module Menu',
                                            compute="_get_self_module_info")
    self_model_ids = fields.Many2many('ir.model', 'access_management_ir_model_self', 'access_management_id', 'model_id',
                                      'Self Model', compute="_get_self_module_info")
    total_rules = fields.Integer('Access Rules', compute="_count_total_rules")

    # Chatter
    hide_chatter_ids = fields.One2many('hide.chatter', 'access_management_id', 'Hide Chatters', copy=True)

    hide_chatter = fields.Boolean('Hide Chatter')
    hide_send_mail = fields.Boolean('Hide Send Message')
    hide_log_notes = fields.Boolean('Hide Log Notes')
    hide_schedule_activity = fields.Boolean('Hide Schedule Activity')

    hide_export = fields.Boolean()
    hide_import = fields.Boolean()
    disable_login = fields.Boolean('Disable Login')


    disable_debug_mode = fields.Boolean('Disable Developer Mode')

    company_ids = fields.Many2many('res.company', 'access_management_comapnay_rel', 'access_management_id',
                                   'company_id', 'Companies', required=True, default=lambda self: self.env.company)

    hide_filters_groups_ids = fields.One2many('hide.filters.groups', 'access_management_id', 'Hide Filters/Group By',
                                              copy=True)

    def _count_total_rules(self):
        for rec in self:
            rule = 0
            rule = rule + len(rec.hide_menu_ids) + len(rec.hide_field_ids) + len(rec.remove_action_ids) + len(
                rec.access_domain_ah_ids) + len(rec.hide_view_nodes_ids)
            rec.total_rules = rule

    def action_show_rules(self):
        pass

    def _get_self_module_info(self):
        access_menu_id = self.env.ref('simplify_access_management.main_menu_simplify_access_management')
        model_list = ['access.management', 'access.domain.ah', 'action.data', 'hide.field', 'hide.view.nodes',
                      'store.model.nodes', 'remove.action', 'view.data']
        models_ids = self.env['ir.model'].search([('model', 'in', model_list)])
        for rec in self:
            rec.self_module_menu_ids = False
            rec.self_model_ids = False
            if access_menu_id:
                rec.self_module_menu_ids = [(6, 0, access_menu_id.ids)]
            if models_ids:
                rec.self_model_ids = [(6, 0, models_ids.ids)]

    def toggle_active_value(self):
        for record in self:
            record.write({'active': not record.active})
        return True

    @api.model_create_multi
    def create(self, vals_list):
        res = super(access_management, self).create(vals_list)
        # for user in self.env['res.users'].sudo().search([('share','=',False)]):
        # user.clear_caches()
        self.clear_caches()
        for record in res:
            if record.readonly:
                for user in record.user_ids:
                    if user.has_group('base.group_system') or user.has_group('base.group_erp_manager'):
                        raise UserError(_('Admin user can not be set as a read-only..!'))
        return res

    def unlink(self):
        res = super(access_management, self).unlink()
        self.clear_caches()
        # for user in self.env['res.users'].sudo().search([('share','=',False)]):
        #     user.clear_caches()
        return res

    def write(self, vals):
        res = super(access_management, self).write(vals)

        if self.readonly:
            for user in self.user_ids:
                if user.has_group('base.group_system') or user.has_group('base.group_erp_manager'):
                    raise UserError(_('Admin user can not be set as a read-only..!'))
        # for user in self.env['res.users'].sudo().search([('share','=',False)]):
        #     user.clear_caches()
        self.clear_caches()
        return res

    def get_remove_options(self, model):
        restrict_export = self.env['access.management'].search([('company_ids', 'in', self.env.company.id),
                                                                ('active', '=', True),
                                                                ('user_ids', 'in', self.env.user.id),
                                                                ('hide_export', '=', True)], limit=1).id
        remove_action = self.env['remove.action'].sudo().search(
            [('access_management_id.company_ids', 'in', self.env.company.id),
             ('access_management_id', 'in', self.env.user.access_management_ids.ids), ('model_id.model', '=', model)])
        options = []
        added_export = False
        if restrict_export:
            options.append('export')
            added_export = True

        for action in remove_action:
            if not added_export and action.restrict_export:
                options.append('export')
            if action.restrict_archive_unarchive:
                options.append('archive')
                options.append('unarchive')
            if action.restrict_duplicate:
                options.append('duplicate')
        return options

    @api.model
    def get_chatter_hide_details(self, user_id, company_id, model=False):
        hide_send_mail = True
        hide_log_notes = True
        hide_schedule_activity = True

        access_ids = self.search([('user_ids', 'in', user_id), ('company_ids', 'in', company_id)])
        for access in access_ids:
            if access.hide_chatter:
                hide_send_mail = False
                hide_log_notes = False
                hide_schedule_activity = False
                break

            if access.hide_send_mail:
                hide_send_mail = False

            if access.hide_log_notes:
                hide_log_notes = False

            if access.hide_schedule_activity:
                hide_schedule_activity = False

        if model and hide_send_mail or hide_log_notes or hide_schedule_activity:
            hide_ids = self.env['hide.chatter'].search([('access_management_id.company_ids', 'in', company_id),
                                                        ('access_management_id.active', '=', True),
                                                        ('access_management_id.user_ids', 'in', user_id),
                                                        ('model_id.model', '=', model)])

            if hide_ids:
                if hide_send_mail and hide_ids.filtered(lambda x: x.hide_send_mail):
                    hide_send_mail = False

                if hide_log_notes and hide_ids.filtered(lambda x: x.hide_log_notes):
                    hide_log_notes = False

                if hide_schedule_activity and hide_ids.filtered(lambda x: x.hide_schedule_activity):
                    hide_schedule_activity = False

        return {
            'hide_send_mail': hide_send_mail,
            'hide_log_notes': hide_log_notes,
            'hide_schedule_activity': hide_schedule_activity
        }

    @api.model
    def is_export_hide(self, user_id, company_id, model=False):
        hide_export = False
        access_ids = self.search(
            [('user_ids', 'in', user_id), ('company_ids', 'in', company_id), ('active', '=', True)])

        for access in access_ids:
            if access.hide_export:
                hide_export = True
                break

        if not hide_export and model:
            if self.env['remove.action'].search([('access_management_id', 'in', access_ids.ids),
                                                 ('model_id.model', '=', model),
                                                 ('restrict_export', '=', True)]):
                hide_export = True

        return hide_export

    def get_hidden_field(self, model=False):
        if model:
            hidden_fields = []
            hide_field_obj = self.env['hide.field'].sudo()
            for hide_field in hide_field_obj.search(
                        [('access_management_id.company_ids', 'in', self.env.company.id),
                         ('model_id.model', '=', model), ('access_management_id.active', '=', True),
                         ('access_management_id.user_ids', 'in', self._uid), ('invisible', '=', True)]):
                for field in hide_field.field_id:
                    if field.name:
                        hidden_fields.append(field.name)
            return hidden_fields
        return []