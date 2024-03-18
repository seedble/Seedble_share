# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
# Developed by Bizople Solutions Pvt. Ltd.
from odoo import models,fields

class PushNotification(models.Model):
    _name = 'push.notification.menu'
    _description = "Push Notification Menu"
    _rec_name = "model_name"
    
    model_name = fields.Many2one('ir.model',string="Model",domain=[('model','!=','whatsapp.chatroom')])
    menu_id = fields.Many2one('ir.ui.menu',string="Menu")  
    action_id = fields.Many2one('ir.actions.actions',string="Action",domain=[('type','=','ir.actions.act_window')])  