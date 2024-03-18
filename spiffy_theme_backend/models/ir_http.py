# -*- coding: utf-8 -*-
# Developed by Bizople Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details

from odoo import api, models
from odoo.http import request

class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        # Show company change option even if single company available 
        is_bg_color = self.env.user.table_color
        res = super(Http, self).session_info()
        # user = request.env.user
        company = self.env.company
        
        session_sid = request.session.sid
        if self.env.user.image_1920:
            image = self.env.user.image_1920.decode('utf-8')
        else:
            image = ''
        res.update({'bg_color':is_bg_color,'user_image':image,'session_sid':session_sid,'spiffy_installed':True})

        if 'device_token' and 'device_name' in self.env.context:
            device_token = self.env.context.get('device_token')
            device_name = self.env.context.get('device_name')
            user_obj = self.env['mail.firebase'].search([('user_id','=',res['uid']),('token','=',device_token)])
            if not user_obj:
                self.env['mail.firebase'].create({'user_id':res['uid'],'os':device_name,'token':device_token})

        if self.env.user.has_group('base.group_user'):
            res.update({
                "display_switch_company_menu": True,
                "prevent_auto_save_warning_msg": company.prevent_auto_save_warning if company.prevent_auto_save_warning else '',
            })
            
        return res