# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class SecurityRoleRulePeriod(models.Model):
    """
    The model to keep security rights combined in a role
    """
    _name = "blendx.security.role.rule.period"
    _description = "Role Rule Period"
    _rec_name = "name"

    @api.depends_context("tz", "lang")
    @api.depends("period_start", "period_end")
    def _compute_name(self):
        """
        Compute method for name

        Methods: 
         * _return_lang_date_format
        """

        def get_in_tz(c_date):
            """
            The method to convert datetime to a proper tz
            """
            local_datetime = c_date and fields.Datetime.context_timestamp(self, c_date) or False
            return local_datetime and local_datetime.strftime(lang_format) or "∞"

        dt_now = fields.Datetime.now()
        lang_format = self._return_lang_date_format()
        for period in self:
            period_start = period.period_start
            period_end = period.period_end
            fit_now = (not period_start or period_start <= dt_now) and (not period_end or period_end >= dt_now)
            period.name = "{} - {}{}".format(get_in_tz(period_start), get_in_tz(period_end), fit_now and "   ⚡" or "")

    name = fields.Char(string="Periods", compute=_compute_name)
    rule_id = fields.Many2one(
        "blendx.security.role.rule",
        string="Rule",
        required=True,
        ondelete="cascade",
    )
    role_id = fields.Many2one(related="rule_id.role_id", store=True)
    period_start = fields.Datetime(string="Period Start", index=True)
    period_end = fields.Datetime(string="Period End", index=True)

    _order = "rule_id, period_start desc, period_end desc, id"

    @api.constrains('period_start', 'period_end')
    def _check_start_date(self):
        for rec in self:
            if rec.period_start and rec.period_end and rec.period_end < rec.period_start:
                raise ValidationError(_('End Date must be greater than start date.'))

    @api.model_create_multi
    def create(self, vals_list):
        """
        Re-write to update role users if necessary
        """
        period_ids = super(SecurityRoleRulePeriod, self).create(vals_list)
        for period in period_ids:
            period.rule_id.role_id.action_refresh_blockings()
        return period_ids

    def write(self, vals):
        """
        Re-write to update role users if necessary
        """
        res = super(SecurityRoleRulePeriod, self).write(vals)
        for period in self:
            period.rule_id.role_id.action_refresh_blockings()
        return res

    def unlink(self):
        """
        Re-write to update role users if necessary
        """
        role_ids = self.mapped("rule_id").mapped("role_id")
        res = super(SecurityRoleRulePeriod, self).unlink()
        for role in role_ids:
            role.action_refresh_blockings()
        return res

    @api.model
    def _get_all_active_periods(self, role_id=None):
        """
        The method to get all periods where rule should become active
        
        Args:
         * role_id - blendx.security.role object (optional)

        Returns:
         * blendx.security.role.rule.period recordset
        """
        datetime_now = fields.Datetime.now()
        is_inside_domain = [
            "|",
            ("period_start", "<=", datetime_now),
            ("period_start", "=", False),
            "|",
            ("period_end", ">=", datetime_now),
            ("period_end", "=", False),
        ]
        if role_id:
            is_inside_domain.append(("role_id", "=", role_id.id))
        period_ids = self.env["blendx.security.role.rule.period"].search(is_inside_domain)
        return period_ids

    @api.model
    def _return_lang_date_format(self):
        """
        The method to return date format for js

        Returns:
         * str
        """
        lang = self._context.get("lang") or self.env.user.lang
        lang_date_format = "%m/%d/%Y %H:%M:%S"
        if lang:
            record_lang = self.env["res.lang"].search([("code", "=", lang)], limit=1)
            lang_date_format = "{} {}".format(record_lang.date_format, record_lang.time_format)
        return lang_date_format
