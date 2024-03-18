from . import models
# from . import wizard
from . import controllers



from odoo import api, SUPERUSER_ID

def uninstall_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['ir.config_parameter'].search([('key','=','uninstall_check')]).unlink()

def post_install_action_dup_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    action_data_obj = env['action.data']
    for action in env['ir.actions.actions'].search([]):
        action_data_obj.create({'name':action.name,'action_id':action.id})