from odoo import models, fields


class IrModuleCategoryExt(models.Model):
    _inherit = 'ir.module.category'

    is_managed_with_blendx_user_roles = fields.Boolean(string='Managed with Blendx User Roles', default=True,
                                                       help="If this set will visible on Access Rights tab of the User roles.")
    blendx_intent_id = fields.Many2one('blendx.intent', string='Intent')

    def write(self, values):
        """ Over-ride this method to update the view for user roles when is_managed_with_blendx_user_roles update."""
        res = super().write(values)
        if "is_managed_with_blendx_user_roles" in values or "blendx_intent_id" in values:
            self.env["res.groups"]._update_user_groups_view()
        return res
