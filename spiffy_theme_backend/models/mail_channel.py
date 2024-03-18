# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.
# Developed by Bizople Solutions Pvt. Ltd.

from odoo import models
import requests
import logging
from bs4 import BeautifulSoup
import re
_logger = logging.getLogger(__name__)

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'
    

    def _notify_thread(self, message, msg_vals=False, **kwargs):
        print('============call notif thread-------')
        rdata = super(MailThread, self)._notify_thread(message, msg_vals=msg_vals, **kwargs)
        self._notify_record_firebase(message, rdata, msg_vals, **kwargs)
        return rdata
    
    def _notify_record_firebase(self, message, rdata, msg_vals=False, **kwargs):
        """ We want to send a Cloud notification for every mentions of a partner
        and every direct message. We have to take into account the risk of
        duplicated notifications in case of a mention in a channel of `chat` type.
        """
        
        notif_pids = [r['id'] for r in rdata if r['active']]
        _logger.info('notif_pids ------------------------------------ %s', notif_pids)
        no_inbox_pids = [r['id'] for r in rdata if r['active'] and r['notif'] != 'inbox']
        if not notif_pids:
            return

        msg_vals = dict(msg_vals or {})
        msg_sudo = message.sudo()
        msg_type = msg_vals.get('message_type') or msg_sudo.message_type
        author_id = [msg_vals.get('author_id')] if 'author_id' in msg_vals else msg_sudo.author_id.ids
        if msg_type in ('comment', 'wa_message'):
            pids = set(notif_pids) - set(author_id)

            _logger.info('if comment pids ------------------------------------ %s', pids)

            for id in pids:
                user_obj = self.env['res.users'].search([('partner_id','=',int(id))])     
                device_ids = user_obj.mail_firebase_tokens.mapped('token') if user_obj else False
                self._prepare_firebase_notifications(message,device_ids)
        elif msg_type in ('notification', 'user_notification'):
            pids = (set(no_inbox_pids) - set(author_id))

            _logger.info('elsee wa_message pids ------------------------------------ %s', pids)

            for id in pids:
                user_obj = self.env['res.users'].search([('partner_id','=',int(id))])     
                device_ids = user_obj.mail_firebase_tokens.mapped('token') if user_obj else False
                self._prepare_firebase_notifications(message,device_ids)
        

    def _prepare_firebase_notifications(self, message, device_ids):
        message_json = {
            'author_id': message['author_id'],
            'body': message['body'],
            'body_html': message['body'],
            'res_id':message['res_id'],
            'model':message['model']
        }
        _logger.info('_prepare_firebase_notifications device_ids ------------------------------------ %s', device_ids)
        
        self._mail_channel_firebase_notifications(message_json, device_ids)

    def _mail_channel_firebase_notifications(self, message, device_ids):
        """
            Send notifications via Firebase Cloud
        """
        if not device_ids:
            _logger.info('device_ids not found ------------------------------------')
            return
        key = self.env.company.firebase_server_key
        if not key:
            _logger.info('key not found ------------------------------------')
            return
        url = 'https://fcm.googleapis.com/fcm/send'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key={}'.format(key)
        }
        _logger.info('===message==>>>>>',message)
        action = self.env.ref('mail.action_discuss')
        menu = self.env.ref('mail.menu_root_discuss')
        menu_item_obj = self.env['push.notification.menu'].search([('model_name','=',message['model'])])
        
        
        _logger.info('====mesage model==>>>>>>> %s',message['model'])
        if message['model'] == 'mail.channel':
            channel_url = f'/web?bg_color=True&tool_color_id=1#menu_id={str(menu.id)}&default_active_id=mail.box_inbox&action={str(action.id)}&active_id=mail.channel_{str(message["res_id"])}'
        elif message['model'] == 'whatsapp.chatroom':
            whatsapp_chatroom_obj = self.env['whatsapp.chatroom'].search([('id','=',message['res_id'])])
            active_waba_id = whatsapp_chatroom_obj.wa_business_acc_id.id if whatsapp_chatroom_obj else False
            active_action = self.env.ref('whatsapp_integration_bs_chatroom.bs_whatsapp_chatroom')
            active_action_id = active_action.id if active_action else False
            _logger.info('------active waba id and action id-----',active_waba_id,active_action_id)
            if active_action_id and active_waba_id:
                channel_url = f'/web?bg_color=True&tool_color_id=1#action={active_action_id}&active_waba_id={active_waba_id}&active_id=mail.box_inbox'
            else:
                channel_url = f'/web?bg_color=True&tool_color_id=1#default_active_id=mail.box_inbox&action={str(action.id)}&menu_id={str(menu.id)}&active_id=mail.box_inbox'
        elif menu_item_obj:
            menu_id = menu_item_obj.menu_id.id
            action_id = menu_item_obj.action_id.id
            object_id = message['res_id']
            channel_url = f'/web?bg_color=True&tool_color_id=1#id={str(object_id)}&menu_id={str(menu_id)}&action={str(action_id)}&model={message["model"]}&view_type=form&active_id=mail.box_inbox'
        else:
            channel_url = f'/web?bg_color=True&tool_color_id=1#default_active_id=mail.box_inbox&action={str(action.id)}&menu_id={str(menu.id)}&active_id=mail.box_inbox'
        _logger.info('===channel url====>>>>>>>> %s',channel_url)
        
        parse_message = BeautifulSoup(message['body'], 'html.parser')
        msg_without_tags = parse_message.get_text()
        text_without_spaces = re.sub(r'\s+', ' ', msg_without_tags).strip()
        lines = text_without_spaces.split('\n')
        message_body = '\n'.join(lines)
        
        if len(device_ids) > 1:
            data = {
                "notification": {
                    'title': message['author_id'].name,
                    'body': message_body,
                    'sound': "default",
                    'badge': None,
                },
                'dry_run': False,
                'priority': 'high',
                'content_available': True,
                "data": {
                    "body_html": message['body_html'],
                    'res_id':message['res_id'],
                    'click_action':channel_url,

                },
                "registration_ids": device_ids,
            }
        else:
            data = {
                "notification": {
                    'title': message['author_id'].name,
                    'body': message_body,
                    'res_id':message['res_id'],
                    'sound': "default",
                    'badge': None,
                },
                'dry_run': False,
                'priority': 'high',
                'content_available': True,
                "data": {
                    "body_html": message['body_html'],
                    'click_action':channel_url,
                },
                "to": ''.join(device_ids),
            }
        resonse_data = requests.post(url, json=data, headers=headers)
        _logger.info('_mail_channel_firebase_notifications resonse_data ------------------------------------ %s', resonse_data)
        
        


class Channel(models.Model):
    _inherit = 'mail.channel'


    def _notify_record_firebase(self, message, rdata, msg_vals=False, **kwargs):
        """ Specifically handle channel members. """
        chat_channels = self.filtered(lambda channel: channel.channel_type == 'chat')
        channel_channels = self.filtered(lambda channel: channel.channel_type == 'channel')
        if chat_channels:
            # modify rdata only for calling super. Do not deep copy as we only
            # add data into list but we do not modify item content
            channel_rdata = rdata.copy()
            channel_rdata += [
                {'id': partner.id,
                 'share': partner.partner_share,
                 'active': partner.active,
                 'notif': 'ocn',
                 'type': 'customer',
                 'groups': [],
                }
                for partner in chat_channels.mapped("channel_partner_ids")
            ]
        elif channel_channels:
            channel_rdata = rdata.copy()
            channel_rdata += [
                {'id': partner.id,
                 'share': partner.partner_share,
                 'active': partner.active,
                 'notif': 'ocn',
                 'type': 'customer',
                 'groups': [],
                }
                for partner in channel_channels.mapped("channel_partner_ids")
            ]
        else:
            channel_rdata = rdata
        return super(Channel, self)._notify_record_firebase(message, channel_rdata, msg_vals=msg_vals, **kwargs)