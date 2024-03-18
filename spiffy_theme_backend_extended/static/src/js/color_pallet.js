odoo.define('spiffy_theme_backend_extended.color_pallate', function (require) {
    'use strict';
    var Widget = require('web.Widget')
    var ColorPallet = require('spiffy_theme_backend.ColorPalletJS');

    ColorPallet.include({
        pallet_1: function() {
            $(':root').css({
                "--light-theme-primary-color": "#1ea8e7",
                "--light-theme-primary-btn-color": "#1ea8e7",
                "--light-theme-primary-text-color": "#ffffff",
                "--primary-rgba": '#1ea8e7b3',
            });
        },

        pallet_2: function() {
            $(':root').css({
                "--light-theme-primary-color": "#75ab38",
                "--light-theme-primary-btn-color": "#75ab38",
                "--light-theme-primary-text-color": "#ffffff",
                "--primary-rgba": '#75ab38b3',
            });
        },

        pallet_3: function() {
            $(':root').css({
                "--light-theme-primary-color": "#ed6789",
                "--light-theme-primary-btn-color": "#ed6789",
                "--light-theme-primary-text-color": "#ffffff",
                "--primary-rgba": '#ed6789b3',
            });
        },

        pallet_4: function() {
            $(':root').css({
                "--light-theme-primary-color": "#a772cb",
                "--light-theme-primary-btn-color": "#a772cb",
                "--light-theme-primary-text-color": "#ffffff",
                "--primary-rgba": '#a772cbb3',
            });
        },

        pallet_5: function() {
            $(':root').css({
                "--light-theme-primary-color": "#eb5858",
                "--light-theme-primary-btn-color": "#eb5858",
                "--light-theme-primary-text-color": "#ffffff",
                "--primary-rgba": '#eb5858b3',
            });
        },

        pallet_6: function() {
            $(':root').css({
                "--light-theme-primary-color": "#8c6f46",
                "--light-theme-primary-btn-color": "#8c6f46",
                "--light-theme-primary-text-color": "#ffffff",
                "--primary-rgba": '#8c6f46b3',
            });
        },

        pallet_7: function() {
            $(':root').css({
                "--light-theme-primary-color": "#007a5a",
                "--light-theme-primary-btn-color": "#007a5a",
                "--light-theme-primary-text-color": "#ffffff",
                "--primary-rgba": '#007a5ab3',
            });
        },

        pallet_8: function() {
            $(':root').css({
                "--light-theme-primary-color": "#cc8631",
                "--light-theme-primary-btn-color": "#cc8631",
                "--light-theme-primary-text-color": "#ffffff",
                "--primary-rgba": '#cc8631b3',
            });
        },

        pallet_9: function() {
            $(':root').css({
                "--light-theme-primary-color": "#0097a7",
                "--light-theme-primary-btn-color": "#0097a7",
                "--light-theme-primary-text-color": "#ffffff",
                "--primary-rgba": '#0097a7b3',
            });
        },

        custom_color_pallet: function(record_dict) {
            $(':root').css({
                "--light-theme-primary-color": record_dict.light_primary_bg_color,
                "--light-theme-primary-btn-color": record_dict.light_primary_btn_color,
                "--light-theme-primary-text-color": record_dict.light_primary_text_color,
                "--primary-rgba": record_dict.light_primary_bg_color+'b3',
            });
        },
    });
});