# -*- coding: utf-8 -*-
{
    'name': 'Users (BlendX) Add-on',
    'version': '0.1.2',  # 16c
    'category': 'Custom',
    'license': 'LGPL-3',
    'summary': """Users (BlendX) Add-on - Extension of BlendX Settings(User-Admin Access) module.""",
    'author': "Seedble",
    'website': "https://seedble.com",
    'description': """This module contains extra fields of BlendX Settings(User-Admin Access).""",
    "depends": ["blendx_user_admin_access"],
    "data": [
        "security/ir.model.access.csv",

        "views/res_users_gender_view.xml",
        "views/res_users_job_family_view.xml",
        "views/res_users_management_level_view.xml",
        "views/res_users_division_view.xml",
        "views/res_users_employee_type_view.xml",
        "views/res_users_view_ext.xml"
    ]
}
