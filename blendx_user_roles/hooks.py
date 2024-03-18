# -*- coding: utf-8 -*-

def post_init_hook(cr, registry):
    """
    Introduced to update views after initializing the app
    """
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})
    env["res.groups"]._update_security_role_view()
