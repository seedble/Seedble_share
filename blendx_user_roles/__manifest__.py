# -*- coding: utf-8 -*-
{
    'name': 'Blendx Security User Roles',
    'version': '0.1.7',  # 16c
    'category': 'Custom',
    'license': 'LGPL-3',
    'summary': """The tool combines users in roles and simplifies security group assigning.
               Access group management. Users mass updating. Access groups management.
               Access organizational structure. Odoo user rights. Access rights. 
               User security roles""",
    'author': "Seedble",
    'website': "https://seedble.com",
    'description': """
        Blendx Security User Roles
        """,
    "depends": [
        "base",
        "blendx_base"
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/cron.xml",
        "views/res_users.xml",
        "views/blendx_security_role.xml",
        "views/blendx_intent_views.xml",
        "views/ir_module_category_views.xml",
    ],
    "application": True,
    "installable": True,
    "auto_install": False,
}
