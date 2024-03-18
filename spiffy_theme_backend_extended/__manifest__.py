# -*- coding: utf-8 -*-
{
    'name': 'Spiffy Theme Backend Extended',
    'version': '16.0.1.0.1',
    'author': 'Seedble s.r.l.',
    'website': 'https://seedble.com',
    'summary': 'Spiffy Theme Backend Extended',
    'description': """Spiffy Theme Backend Extended""",
    'depends': ['spiffy_theme_backend'],
    'data': [
        'data/backend_config_data.xml',
        'views/backend_configurator_template.xml',
        'views/backend_configurator_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/spiffy_theme_backend_extended/static/src/scss/bookmarks.scss',
            '/spiffy_theme_backend_extended/static/src/scss/common_view.scss',
            '/spiffy_theme_backend_extended/static/src/scss/controlpannel.scss',
            '/spiffy_theme_backend_extended/static/src/scss/custom_varibles.scss',
            '/spiffy_theme_backend_extended/static/src/scss/list_view.scss',
            '/spiffy_theme_backend_extended/static/src/scss/search_panel.scss',
            '/spiffy_theme_backend_extended/static/src/js/color_pallet.js',
            '/spiffy_theme_backend_extended/static/src/js/menu.js',
            ('remove','/spiffy_theme_backend/static/src/js/dialog.js')
        ],
    },
    'installable': True,
}
