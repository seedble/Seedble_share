from odoo.exceptions import UserError
from odoo import api, fields, models, _

# For Monkey-patch
from odoo.addons.blendx_user_roles.models.res_users import ResUsersInherit

USER_ADMIN_SELF_WARNING = _("""This operation is not possible since after that your user would not have rights to change 
user access rights.""")


class ResPartnerExt(models.Model):
    """ Inherit the res partner to Fix the error while create user from BlendX Admin user. """
    _inherit = 'res.partner'

    signup_expiration = fields.Datetime(copy=False,
                                        groups="base.group_erp_manager,blendx_user_admin_access.group_blendx_settings_admin")
    signup_token = fields.Char(copy=False,
                               groups="base.group_erp_manager,blendx_user_admin_access.group_blendx_settings_admin")
    signup_type = fields.Char(string='Signup Token Type', copy=False,
                              groups="base.group_erp_manager,blendx_user_admin_access.group_blendx_settings_admin")


class ResUsersExt(models.Model):
    """ Extend res users """
    _inherit = 'res.users'

    job_title_id = fields.Many2one('res.blendx.job', string="Job title")
    seniority_level_id = fields.Many2one('res.blendx.seniority', string="Seniority Level")
    blendx_department_id = fields.Many2one('blendx.department',
                                           string="BlendX Department")  # TODO: Need to remove in future

    # blendx.department.team
    blendx_department_team_ids = fields.Many2many(
        comodel_name='blendx.department.team',
        relation='rel_blendx_department_team_res_users',
        column1='blendx_department_team_id',
        column2='res_users_id',
        string='Blendx Department Team'
    )

    def _inverse_security_role_ids(self):
        """ This method is monkey-patch of _inverse_security_role_ids from blendx_user_roles module.
        Inverse method for security_role_ids

        Extra info:
         * it use roles are changed from its form, we do not allow empty user rights (they are considered as "manual")
           The reason is that in this case manual grpups changes would be applied
           Otherwise, full deletion would be possible (empty_rights_possible in context)
        """
        access_settings_group = self.env.ref("base.group_erp_manager")
        if self.env.su or self.env.user.has_group("base.group_erp_manager") or self.env.user.has_group(
                "blendx_user_admin_access.group_blendx_settings_admin"):
            for user in self:
                if user.security_role_ids:
                    all_groups = user.security_role_ids.mapped("group_ids")
                    if self.env.user == user and access_settings_group not in (all_groups + all_groups.implied_ids):
                        raise UserError(USER_ADMIN_SELF_WARNING)
                    else:
                        user.sudo().groups_id = [(6, 0, all_groups.ids)]
                elif self._context.get("empty_rights_possible"):
                    if self.env.user == user:
                        raise UserError(USER_ADMIN_SELF_WARNING)
                    else:
                        user.sudo().groups_id = [(6, 0, [])]
        else:
            raise UserError(_("Sorry you are not allowed to change this role"))

    # Monkey-patch of _inverse_security_role_ids of res.users
    ResUsersInherit._inverse_security_role_ids = _inverse_security_role_ids

    # Over-write this field to not call from blendx_user_roles module.
    security_role_ids = fields.Many2many(
        "blendx.security.role",
        "blendx_security_role_res_users_rel_table",
        "security_role_id",
        "res_users_id",
        string="Roles",
        inverse=_inverse_security_role_ids,
    )

    def write(self, vals):
        """ Over-ride this method to check the access right of Blendx User Admin. If current user is only Blendx User
            than can not select Blendx admin.
        """
        if self.user_has_groups('blendx_user_admin_access.group_blendx_user') and not self.user_has_groups(
                'blendx_user_admin_access.group_blendx_admin'):
            field_str = "sel_groups_" + str(self.env.ref('blendx_user_admin_access.group_blendx_user').id) + '_' + str(
                self.env.ref('blendx_user_admin_access.group_blendx_admin').id)
            if field_str in vals and vals[field_str] == self.env.ref('blendx_user_admin_access.group_blendx_admin').id:
                raise UserError(
                    "You can not select BlendX Admin as you are Blendx User.\nPlease contact you administrator.")
        return super(ResUsersExt, self).write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        """ Over-ride this method to check the access right of Blendx User Admin. If current user is only Blendx User
            than can not select Blendx admin.
        """
        if self.user_has_groups('blendx_user_admin_access.group_blendx_user') and not self.user_has_groups(
                'blendx_user_admin_access.group_blendx_admin'):
            field_str = "sel_groups_" + str(self.env.ref('blendx_user_admin_access.group_blendx_user').id) + '_' + str(
                self.env.ref('blendx_user_admin_access.group_blendx_admin').id)
            for val_list in vals_list:
                if field_str in val_list and val_list[field_str] == self.env.ref(
                        'blendx_user_admin_access.group_blendx_admin').id:
                    raise UserError(
                        "You can not select BlendX Admin as you are Blendx User.\nPlease contact you administrator.")
        return super(ResUsersExt, self).create(vals_list)
