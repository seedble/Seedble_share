# -*- coding: utf-8 -*-

{
    'name': 'Core Module',
    'version': '16.0.1.0.1',
    'category': 'Blendx',
    'license': 'LGPL-3',
    'summary': 'Core Module',
    'author': 'Seedble s.r.l.',
    'website': 'https://seedble.com',
    'description': """
        Core Mdule
    """,
    'depends': ['base', 'blendx_base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/reference_sector_view.xml',
        'views/competence_view.xml',
        'views/category_view.xml',
        'views/used_technology_view.xml',
        'views/keyword_view.xml',
        'views/target_view.xml',
        'views/role_view.xml',
        'views/dashboard_view.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
