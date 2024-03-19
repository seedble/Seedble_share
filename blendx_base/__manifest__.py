# -*- coding: utf-8 -*-

{
    'name': 'Blendx Base Module',
    'version': '16.0.1.0.0',
    'category': 'Blendx',
    'license': 'LGPL-3',
    'summary': 'Blendx Base Module',
    'author': 'Seedble s.r.l.',
    'website': 'https://seedble.com',
    'description': """
        Blendx Base Module
    """,
    'depends': ['web'],
    'data': [
    ],
    'assets': {
        'web.assets_backend': [
            'blendx_base/static/src/views/**/*',
        ]
    },
    'application': True,
    'installable': True,
    'auto_install': True,
}
