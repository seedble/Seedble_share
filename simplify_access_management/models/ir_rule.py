# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import Warning, ValidationError, UserError
from odoo.tools import config
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval
from odoo.http import request
from odoo.addons.advanced_web_domain_widget.models.domain_prepare import prepare_domain_v2


class ir_rule(models.Model):
    _inherit = 'ir.rule'

    @api.model
    @tools.conditional(
        'xml' not in config['dev_mode'],
        tools.ormcache('self.env.uid', 'self.env.su', 'model_name', 'mode',
                       'tuple(self._compute_domain_context_values())'),
    )
    def _compute_domain(self, model_name, mode="read"):
        res = super(ir_rule, self)._compute_domain(model_name, mode)

        read_value = True
        self._cr.execute("SELECT state FROM ir_module_module WHERE name='simplify_access_management'")
        data = self._cr.fetchone() or False

        self._cr.execute("SELECT id FROM ir_module_module WHERE state IN ('to upgrade', 'to remove','to install')")
        all_data = self._cr.fetchone() or False

        if data and data[0] != 'installed':
            read_value = False
        model_list = ['mail.activity', 'res.users.log', 'res.users', 'mail.channel', 'mail.alias', 'bus.presence',
                      'res.lang']
        if self.env.user.id and read_value and not all_data:
            if model_name not in model_list:
                self._cr.execute("""SELECT am.id FROM access_management as am
                                    WHERE active='t' AND readonly = True AND am.id 
                                    IN (SELECT au.access_management_id 
                                        FROM access_management_users_rel_ah as au 
                                        WHERE user_id = %s AND am.id 
                                        IN (SELECT ac.access_management_id
                                            FROM access_management_comapnay_rel as ac
                                            WHERE ac.company_id=%s))""" % (self.env.user.id, self.env.company.id))
                # a = "select access_management_id from access_management_comapnay_rel where company_id = " + str(self.env.company.id)
                # self._cr.execute(a)
                # a = self._cr.fetchall()
                # if a:   
                #     a = "select access_management_id from access_management_users_rel_ah where user_id = " + str(self.env.user.id) + " AND access_management_id in " + str(tuple([i[0] for i in a]+[0]))
                #     self._cr.execute(a)
                #     a = self._cr.fetchall()
                #     if a:
                #         a = "SELECT id FROM access_management WHERE active='t' AND id in " + str(tuple([i[0] for i in a]+[0])) + " and readonly = True"
                #         self._cr.execute(a)
                #         a = self._cr.fetchall()
                a = self._cr.fetchall()
                if bool(a):
                    if mode != 'read' and model_name not in ['mail.channel.partner']:
                        raise UserError(
                            _('%s is a read-only user. So you can not make any changes in the system!') % self.env.user.name)

        value = self._cr.execute(
            """SELECT value from ir_config_parameter where key='uninstall_simplify_access_management' """)
        value = self._cr.fetchone()
        if not value:
            value = self._cr.execute("""select state from ir_module_module where name = 'simplify_access_management'""")
            value = self._cr.fetchone()
            value = value and value[0] or False
            if model_name and value == 'installed':
                # if model_name:
                self._cr.execute("SELECT id FROM ir_model WHERE model='" + model_name + "'")
                model_numeric_id = self._cr.fetchone()
                model_numeric_id = model_numeric_id and model_numeric_id[0] or False
                if model_numeric_id and isinstance(model_numeric_id, int) and self.env.user:
                    try:
                        self._cr.execute("""
                                        SELECT dm.id
                                        FROM access_domain_ah as dm
                                        WHERE dm.model_id=%s AND dm.apply_domain AND dm.access_management_id 
                                        IN (SELECT am.id 
                                            FROM access_management as am 
                                            WHERE active='t' AND am.id 
                                            IN (SELECT amusr.access_management_id
                                                FROM access_management_users_rel_ah as amusr
                                                WHERE amusr.user_id=%s))
                                        """, [model_numeric_id, self.env.user.id])
                    except:
                        pass
                    access_domain_ah_ids = self.env['access.domain.ah'].browse(
                        row[0] for row in self._cr.fetchall()).filtered(
                        lambda line: self.env.company in line.access_management_id.company_ids)
                    # access_domain_ah_ids = access_domain_ah_ids.filtered(lambda line: self.env.company in line.access_management_id.company_ids)
                    if access_domain_ah_ids:
                        domain_list = []
                        if model_name == 'res.partner':
                            # jo aya user related jetala partner 6 ana access alag thi apididha 6 error no ave atle
                            self._cr.execute("""SELECT partner_id FROM res_users""")
                            partner_ids = [row[0] for row in self._cr.fetchall()]
                            domain_list = ['|', ('id', 'in', partner_ids)]
                        eval_context = self._eval_context()
                        # only domain records
                        length = len(access_domain_ah_ids.sudo()) if access_domain_ah_ids.sudo() else 0
                        for access in access_domain_ah_ids.sudo():
                            dom = safe_eval(access.domain, eval_context) if access.domain else []
                            if dom:
                                dom = expression.normalize_domain(dom)
                                for dom_tuple in dom:
                                    if isinstance(dom_tuple, tuple):
                                        left_value = dom_tuple[0]
                                        operator_value = dom_tuple[1]
                                        right_value = dom_tuple[2]
                                        left_value_split_list = left_value.split('.')
                                        model_string = model_name
                                        left_user = False
                                        left_company = False
                                        for field in left_value_split_list:
                                            left_user = False
                                            left_company = False
                                            model_obj = self.env[model_string]
                                            field_type = model_obj.fields_get()[field]['type']
                                            if field_type in ['many2one', 'many2many', 'one2many']:
                                                field_relation = model_obj.fields_get()[field]['relation']
                                                model_string = field_relation
                                                if model_string == 'res.users':
                                                    left_user = True
                                                if model_string == 'res.company':
                                                    left_company = True

                                        if left_user:
                                            if operator_value in ['in', 'not in']:
                                                if isinstance(right_value, list) and 0 in right_value:
                                                    zero_index = right_value.index(0)
                                                    right_value[zero_index] = self.env.user.id

                                        if left_company:
                                            if operator_value in ['in', 'not in']:
                                                if isinstance(right_value, list) and 0 in right_value:
                                                    zero_index = right_value.index(0)
                                                    right_value[zero_index] = self.env.company.id

                                        if operator_value == 'date_filter':
                                            domain_list += prepare_domain_v2(dom_tuple)
                                        else:
                                            domain_list.append(dom_tuple)
                                    else:
                                        domain_list.append(dom_tuple)
                                if length > 1:
                                    domain_list.insert(0, '|')
                                    length -= 1
                        if domain_list:
                            return domain_list

        return res
