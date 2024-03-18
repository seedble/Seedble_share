# -*- coding: utf-8 -*-
{
    'name': 'BlendX Settings(User-Admin Access)',
    'version': '0.2.3',  # 16c
    'category': 'Custom',
    'license': 'LGPL-3',
    'summary': """BlendX Settings - Blendx User Admin Access""",
    'author': "Seedble",
    'website': "https://seedble.com",
    'description': """
    BlendX Settings - Blendx User Admin Access
    > This module contains Users(Blendx) and Access rights for Blendx Settings, Blendx User Admin.
    > Blendx Department
    """,
    "depends": ["blendx_user_roles", "auth_signup"],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",

        "views/blendx_settings_view.xml",
        "views/blendx_res_users_view.xml",
        "views/res_blendx_job_views.xml",
        "views/blendx_department_view.xml"
    ],
    "uninstall_hook": 'uninstall_hook_method'
}
