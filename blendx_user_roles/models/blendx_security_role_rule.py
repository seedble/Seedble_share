# -*- coding: utf-8 -*-

from odoo import _, api, models, fields


class BlendxSecurityRoleRule(models.Model):
    """
    The model to keep security rights combined in a role
    """
    _name = "blendx.security.role.rule"
    _description = "Blendx Role Rule"

    @api.depends_context("tz", "lang")
    @api.depends("rule_type", "period_ids", "period_ids.period_start", "period_ids.period_end")
    def _compute_name(self):
        """
        Compute method for name
        """
        for rule in self:
            ttype = rule.rule_type == "activate" and _("Activate for:") or _("Block for:")
            periods = "\n".join(rule.period_ids.mapped(lambda pe: pe.name))
            rule.name = "{}\n{}".format(ttype, periods)

    name = fields.Text(string="Name", compute=_compute_name)
    user_id = fields.Many2one(
        "res.users",
        string="User",
        required=True,
        ondelete="cascade",
    )
    role_id = fields.Many2one(
        "blendx.security.role",
        string="Role",
        required=True,
        ondelete="cascade",
    )
    rule_type = fields.Selection(
        [
            ("activate", "Temporary Activation"),
            ("block", "Temporary Blocking"),
        ],
        string="Action",
        default="activate",
        required=True,
    )
    period_ids = fields.One2many(
        "blendx.security.role.rule.period",
        "rule_id",
        string="Periods",
        required=True,
    )

    _order = "user_id, id"

    _sql_constraints = [(
        "role_id_id_uniq", "unique(user_id, role_id)", _("The rule should be unique per user and role!"),
    )]

    @api.model_create_multi
    def create(self, vals_list):
        """
        Re-write to update role users if necessary
        """
        rule_ids = super(BlendxSecurityRoleRule, self).create(vals_list)
        for rule in rule_ids:
            rule.role_id.action_refresh_blockings()
        return rule_ids

    def write(self, vals):
        """
        Re-write to update role users if necessary
        """
        res = super(BlendxSecurityRoleRule, self).write(vals)
        for rule in self:
            rule.role_id.action_refresh_blockings()
        return res

    def unlink(self):
        """
        Re-write to update role users if necessary
        """
        role_ids = self.mapped("role_id")
        res = super(BlendxSecurityRoleRule, self).unlink()
        for role in role_ids:
            role.action_refresh_blockings()
        return res
