# -*- coding: utf-8 -*-


def uninstall_hook_method(cr, registry):
    """ Upgrade blendx_user_roles module after uninstall this module. """
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})
    blendx_user_roles_module = env["ir.module.module"].search([('name', '=', 'blendx_user_roles')])
    if blendx_user_roles_module.state == 'installed':
        blendx_user_roles_module.button_upgrade()
