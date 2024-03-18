# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
# Developed by Bizople Solutions Pvt. Ltd.

from odoo import models, fields

class MailFirebase(models.Model):
    _name = "mail.firebase"
    _description = "Mail Firebase"

    user_id = fields.Many2one('res.users', string="User", readonly=True)
    os = fields.Char(string="Device OS", readonly=True)
    token = fields.Char(string="Device firebase token", readonly=True)

    _sql_constraints = [
        ('token', 'unique(token, os, user_id)', 'Token must be unique per user!'),
        ('token_not_false', 'CHECK (token IS NOT NULL)', 'Token must be not null!'),
    ]

    def remove_firebase_record(self,device_token,userid):
        firebase_obj = self.env['mail.firebase'].search([('token','=',device_token),('user_id','=',int(userid))])
        if firebase_obj:
            firebase_obj.unlink()