# -*- coding: utf-8 -*-
import logging
from odoo.http import request
from odoo import api, fields, models, tools,_
from odoo.exceptions import Warning, ValidationError,AccessError
_logger = logging.getLogger(__name__)

class ir_model_access(models.Model):
    _inherit = 'ir.model.access'



    # The context parameter is useful when the method translates error messages.
    # But as the method raises an exception in that case,  the key 'lang' might
    # not be really necessary as a cache key, unless the `ormcache_context`
    # decorator catches the exception (it does not at the moment.)
    @api.model
    @tools.ormcache_context('self.env.uid', 'self.env.su', 'model', 'mode', 'raise_exception', keys=('lang',))
    def check(self, model, mode='read', raise_exception=True):
        if model == 'mail.thread':
            return True
        if self.env.su or model == 'ir.model':
            # User root have all accesses
            return True

        assert isinstance(model, str), 'Not a model name: %s' % (model,)
        assert mode in ('read', 'write', 'create', 'unlink'), 'Invalid access mode'

        # TransientModel records have no access rights, only an implicit access rule
        if model not in self.env:
            _logger.error('Missing model %s', model)


        
        """
            This part is writen to by pass base access rule and apply dynamic rule of access management rule,
            In case of any record found in access management.
        """
        value = self._cr.execute("""SELECT value from ir_config_parameter where key='uninstall_simplify_access_management' """)
        value = self._cr.fetchone()
        if not value:
            if model:
                self._cr.execute("SELECT id FROM ir_model WHERE model='" + model + "'")
                model_numeric_id = self._cr.fetchone()[0]
                if model_numeric_id and isinstance(model_numeric_id,int) and self.env.user:
                    try:
                        self._cr.execute("""
                                        SELECT dm.id
                                        FROM access_domain_ah as dm
                                        WHERE dm.model_id=%s AND dm.access_management_id 
                                        IN (SELECT am.id 
                                            FROM access_management as am 
                                            WHERE active='t' AND am.id 
                                            IN (SELECT amusr.access_management_id
                                                FROM access_management_users_rel_ah as amusr
                                                WHERE amusr.user_id=%s))
                                        """,[model_numeric_id, self.env.user.id])
                    except:
                        pass                    
                    access_domain_ah_ids = self.env['access.domain.ah'].browse(row[0] for row in self._cr.fetchall()).filtered(lambda line: self.env.company in line.access_management_id.company_ids)
                    if access_domain_ah_ids:
                        return True


        # We check if a specific rule exists
        self._cr.execute("""SELECT MAX(CASE WHEN perm_{mode} THEN 1 ELSE 0 END)
                              FROM ir_model_access a
                              JOIN ir_model m ON (m.id = a.model_id)
                              JOIN res_groups_users_rel gu ON (gu.gid = a.group_id)
                             WHERE m.model = %s
                               AND gu.uid = %s
                               AND a.active IS TRUE""".format(mode=mode),
                         (model, self._uid,))
        r = self._cr.fetchone()[0]

        if not r:
            # there is no specific rule. We check the generic rule
            self._cr.execute("""SELECT MAX(CASE WHEN perm_{mode} THEN 1 ELSE 0 END)
                                  FROM ir_model_access a
                                  JOIN ir_model m ON (m.id = a.model_id)
                                 WHERE a.group_id IS NULL
                                   AND m.model = %s
                                   AND a.active IS TRUE""".format(mode=mode),
                             (model,))
            r = self._cr.fetchone()[0]

        if not r and raise_exception:
            groups = '\n'.join('\t- %s' % g for g in self.group_names_with_access(model, mode))
            document_kind = self.env['ir.model']._get(model).name or model
            msg_heads = {
                # Messages are declared in extenso so they are properly exported in translation terms
                'read': _("You are not allowed to access '%(document_kind)s' (%(document_model)s) records.", document_kind=document_kind, document_model=model),
                'write':  _("You are not allowed to modify '%(document_kind)s' (%(document_model)s) records.", document_kind=document_kind, document_model=model),
                'create': _("You are not allowed to create '%(document_kind)s' (%(document_model)s) records.", document_kind=document_kind, document_model=model),
                'unlink': _("You are not allowed to delete '%(document_kind)s' (%(document_model)s) records.", document_kind=document_kind, document_model=model),
            }
            operation_error = msg_heads[mode]

            if groups:
                group_info = _("This operation is allowed for the following groups:\n%(groups_list)s", groups_list=groups)
            else:
                group_info = _("No group currently allows this operation.")

            resolution_info = _("Contact your administrator to request access if necessary.")

            _logger.info('Access Denied by ACLs for operation: %s, uid: %s, model: %s', mode, self._uid, model)
            msg = """{operation_error}

{group_info}

{resolution_info}""".format(
                operation_error=operation_error,
                group_info=group_info,
                resolution_info=resolution_info)

            raise AccessError(msg)

        try:
            read_value = True
            self._cr.execute("SELECT state FROM ir_module_module WHERE name='simplify_access_management'")
            data = self._cr.fetchone() or False
            if data and data[0] != 'installed':
                read_value = False
            if self.env.user.id and read_value and request.httprequest.cookies.get('cids'):
                a = "select access_management_id from access_management_comapnay_rel where company_id = " + str(request.httprequest.cookies.get('cids') and request.httprequest.cookies.get('cids').split(',')[0] or request.env.company.id)
                self._cr.execute(a)
                a = self._cr.fetchall()
                if a:    
                    a = "select access_management_id from access_management_users_rel_ah where user_id = " + str(self.env.user.id) + " AND access_management_id in " + str(tuple([i[0] for i in a]+[0]))
                    self._cr.execute(a)
                    a = self._cr.fetchall()
                    if a:
                        a = "SELECT id FROM access_management WHERE active='t' AND id in " + str(tuple([i[0] for i in a]+[0])) + " and readonly = True"
                        self._cr.execute(a)
                        a = self._cr.fetchall()
                if bool(a):
                    if mode != 'read':  
                        return False
        except:
            pass


        return bool(r)
