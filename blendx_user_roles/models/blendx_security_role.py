# -*- coding: utf-8 -*-

from itertools import chain, repeat
from collections import defaultdict

from odoo import api, models, fields

from odoo.addons.base.models.res_users import name_boolean_group, name_selection_groups, is_boolean_group, \
    is_selection_groups, is_reified_group, get_boolean_group, get_selection_groups, parse_m2m
from odoo.tools import partition


class BlendxSecurityRole(models.Model):
    """
    The model to keep security rights combined in a role
    """
    _name = "blendx.security.role"
    _description = "Blendx User Role"

    def _default_group_ids(self):
        """
        Default method for group_ids: taken from default user
        """
        default_user_id = self.env["ir.model.data"]._xmlid_to_res_id("base.default_user", raise_if_not_found=False)
        return self.env["res.users"].browse(default_user_id).sudo().groups_id if default_user_id else []

    name = fields.Char(string="Name", required=True)
    group_ids = fields.Many2many(
        "res.groups",
        "blendx_res_groups_security_role_rel_table",
        "res_group_id",
        "security_role_id",
        string="Security groups",
        default=_default_group_ids,
    )
    user_ids = fields.Many2many(
        "res.users",
        "blendx_security_role_res_users_rel_table",
        "res_users_id",
        "security_role_id",
        string="Users",
    )
    rule_ids = fields.One2many(
        "blendx.security.role.rule",
        "role_id",
        string="Rules",
    )
    active = fields.Boolean(string="Active", default=True)
    color = fields.Integer(string="Color index", default=10)
    # blendx_intent_ids = fields.Many2one('blendx.intent', string='Intent')

    @api.model_create_multi
    def create(self, vals_list):
        """
        Re-write to process dummy groups fields

        Methods:
         * _remove_reified_groups
         * _inverse_security_role_ids of res.users
        """
        new_vals_list = []
        for values in vals_list:
            new_vals_list.append(self._remove_reified_groups(values))
        roles = super(BlendxSecurityRole, self).create(new_vals_list)
        roles.user_ids.with_context(empty_rights_possible=True)._inverse_security_role_ids()
        return roles

    def write(self, vals):
        """
        Re-write to process dummy groups fields
        
        Methods:
         * _remove_reified_groups
         * _inverse_security_role_ids of res.users
        """

        def update_users():
            if force_roles_update or vals.get("user_ids") is not None or vals.get("active") is not None \
                    or vals.get("group_ids") is not None:
                all_user_ids = old_user_ids | self.mapped("user_ids")
                all_user_ids.with_context(empty_rights_possible=True)._inverse_security_role_ids()

        force_roles_update = self._context.get("force_roles_update")
        vals = self._remove_reified_groups(vals)
        old_user_ids = self.mapped("user_ids")
        res = super(BlendxSecurityRole, self).write(vals)
        update_users()
        return res

    @api.model
    def new(self, values={}, origin=None, ref=None):
        """
        Re-write to process dummy groups fields
        
        Methods:
         * _remove_reified_groups
         * _inverse_security_role_ids of res.users
        """
        values = self._remove_reified_groups(values)
        role = super().new(values=values, origin=origin, ref=ref)
        return role

    def unlink(self):
        """
        Re-write to trigger roles re-calculations
        
        Methods:
         * _remove_reified_groups
         * _inverse_security_role_ids of res.users
        """
        all_user_ids = self.mapped("user_ids")
        res = super(BlendxSecurityRole, self).unlink()
        all_user_ids.with_context(empty_rights_possible=True)._inverse_security_role_ids()
        return res

    def read(self, fields=None, load="_classic_read"):
        """
        Re-write to process dummy groups fields
         1. determine required group fields
         2. read regular fields and add group_ids if necessary
         3. add reified group fields

        Methods:
         * fields_get
         * is_reified_group
         * super of read
         * _add_reified_groups
        """
        # 1
        fields1 = fields or list(self.fields_get())
        group_fields, other_fields = partition(is_reified_group, fields1)
        # 2
        drop_group_ids = False
        if group_fields and fields:
            if "group_ids" not in other_fields:
                other_fields.append("group_ids")
                drop_group_ids = True
        else:
            other_fields = fields
        res = super(BlendxSecurityRole, self).read(other_fields, load=load)
        # 3
        if group_fields:
            for values in res:
                self._add_reified_groups(group_fields, values)
                if drop_group_ids:
                    values.pop("group_ids", None)
        return res

    @api.model
    def default_get(self, fields):
        """
        Re Title: 863gv5xnu: Add the tab task inside the user story and sprint -write

        Methods:
         * is_reified_group
         * super of default_get
         * _add_reified_groups
        """
        group_fields, fields = partition(is_reified_group, fields)
        fields1 = (fields + ["group_ids"]) if group_fields else fields
        values = super(BlendxSecurityRole, self).default_get(fields1)
        self._add_reified_groups(group_fields, values)
        return values

    def onchange(self, values, field_name, field_onchange):
        """
        Re-write

        Methods:
         * is_reified_group
         * super
         * _add_reified_groups
        """
        field_onchange["group_ids"] = ""
        result = super().onchange(values, field_name, field_onchange)
        if not field_name:
            self._add_reified_groups(
                filter(is_reified_group, field_onchange),
                result.setdefault("value", {})
            )
        return result

    def _remove_reified_groups(self, values):
        """
        The method to return values without reified group fields

        Args:
         * values - dict of values

        Methods:
         * is_boolean_group
         * get_boolean_group
         * is_selection_groups
         * get_selection_groups

        Returns:
         * dict of updated values
        """
        add, rem = [], []
        values1 = {}
        for key, val in values.items():
            if is_boolean_group(key):
                (add if val else rem).append(get_boolean_group(key))
            elif is_selection_groups(key):
                rem += get_selection_groups(key)
                if val:
                    add.append(val)
            else:
                values1[key] = val
        if "group_ids" not in values and (add or rem):
            values1["group_ids"] = list(chain(
                zip(repeat(3), rem),
                zip(repeat(4), add)
            ))
        return values1

    def _add_reified_groups(self, fields, values):
        """
        The method to add reified group fields to values

        Args:
         * fields
         * values

        Methods:
         * parse_m2m
         * is_boolean_group
         * get_boolean_group
         * get_selection_groups
        """
        gids = set(parse_m2m(values.get("group_ids") or []))
        for f in fields:
            if is_boolean_group(f):
                values[f] = get_boolean_group(f) in gids
            elif is_selection_groups(f):
                sel_groups = self.env["res.groups"].sudo().browse(get_selection_groups(f))
                sel_order = {g: len(g.trans_implied_ids & sel_groups) for g in sel_groups}
                sel_groups = sel_groups.sorted(key=sel_order.get)
                selected = [gid for gid in sel_groups.ids if gid in gids]
                if self.env.ref("base.group_user").id in selected:
                    values[f] = self.env.ref("base.group_user").id
                else:
                    values[f] = selected and selected[-1] or False

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """
        Re-write to get dummy group fields

        Method:
         * super of fields_get
         * get_groups_by_application
         * name_selection_groups
         * name_boolean_group
        """
        res = super(BlendxSecurityRole, self).fields_get(allfields, attributes=attributes)
        Group = self.env["res.groups"].sudo()
        for app, kind, gs, category_name in Group.get_groups_by_application():
            if kind == "selection":
                selection_vals = [(False, "")]
                if app.xml_id == "base.module_category_user_type":
                    selection_vals = []
                field_name = name_selection_groups(gs.ids)
                if allfields and field_name not in allfields:
                    continue
                # selection group field
                tips = ["%s: %s" % (g.name, g.comment) for g in gs if g.comment]
                res[field_name] = {
                    "type": "selection",
                    "string": app.name or _("Other"),
                    "selection": selection_vals + [(g.id, g.name) for g in gs],
                    "help": "\n".join(tips),
                    "exportable": False,
                    "selectable": False,
                }
            else:
                # boolean group fields
                for g in gs:
                    field_name = name_boolean_group(g.id)
                    if allfields and field_name not in allfields:
                        continue
                    res[field_name] = {
                        "type": "boolean",
                        "string": g.name,
                        "help": g.comment,
                        "exportable": False,
                        "selectable": False,
                    }
        return res

    def action_create_user(self):
        """
        The method to open a user form view with pre-filled groups

        Returns:
         * ir.actions.window

        Extra info:
         * Expected singletom
        """
        action = self.sudo().env.ref("blendx_user_roles.action_res_users_only_form").read()[0]
        action["context"] = {
            "default_groups_id": [(6, 0, self.group_ids.ids)],
            "default_security_role_ids": [(6, 0, self.ids)],
            "form_view_ref": "base.view_users_form",
        }
        return action

    @api.model
    def action_block_or_activate_users(self):
        """
        The method to find all rules that migth potentially influence role users and force required action
        Primarily designed for the cron job

        Methods:
         * _get_all_active_periods of blendx.security.role.rule.period
         * _refresh_blocking
        """
        period_ids = self.env["blendx.security.role.rule.period"]._get_all_active_periods()
        role_ids = self.env["blendx.security.role"].search([])
        for role in role_ids:
            role._refresh_blocking(period_ids)

    def action_refresh_blockings(self):
        """
        The method to acticate/block users based on the advanced rules
        
        Methods:
         * _get_all_active_periods of blendx.security.role.rule.period
         * _refresh_blocking

        Extra info:
         * Expected singleton
        """
        period_ids = self.env["blendx.security.role.rule.period"]._get_all_active_periods(self)
        self._refresh_blocking(period_ids)

    def _refresh_blocking(self, period_ids):
        """
        The method to check this role blocking/activation rules and amend users correspondinly

        Args:
         * period_ids - blendx.security.role.rule.period recordset (so, period which requires the action)

        Extra info:
         * Expected singleton
        """
        user_commands = []
        for rule in self.rule_ids:
            rule_user_id = rule.user_id
            user_active = rule_user_id in self.user_ids
            rule_active = rule.period_ids & period_ids and True or False
            if rule.rule_type == "activate":
                if rule_active:
                    # found at least a single rule to activate > a user should be activated
                    if not user_active:
                        # otherwise the user should be activated, but he is already
                        user_commands.append((4, rule_user_id.id))
                else:
                    # no rule to activate > a user should be blocked
                    if user_active:
                        # otherwise the user should be blocked, but he is already
                        user_commands.append((3, rule_user_id.id))
            else:
                if rule_active:
                    # found at least a single rule to block > a user should be blocked
                    if user_active:
                        # otherwise the user should be blocked, but he is already
                        user_commands.append((3, rule_user_id.id))
                else:
                    # no rule to block > a user should be active
                    if not user_active:
                        # otherwise the user should be activated, but he is already
                        user_commands.append((4, rule_user_id.id))

        if user_commands:
            self.write({"user_ids": user_commands})
