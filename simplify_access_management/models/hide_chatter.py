from odoo import fields, models, api, _
from lxml import etree


class hide_chatter(models.Model):
    _name = 'hide.chatter'
    _description = "Chatter Rights"

    access_management_id = fields.Many2one('access.management', 'Access Management')
    model_id = fields.Many2one('ir.model', 'Model')

    hide_chatter = fields.Boolean('Chatter')
    hide_send_mail = fields.Boolean('Send Message')
    hide_log_notes = fields.Boolean('Log Notes')
    hide_schedule_activity = fields.Boolean('Schedule Activity')
