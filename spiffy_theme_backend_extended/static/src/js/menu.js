odoo.define('spiffy_theme_backend_extended.MenuJs', function (require) {
    'use strict';

    var {fuzzyLookup} = require("@web/core/utils/search");
    var ajax = require('web.ajax');
    var core = require('web.core');
    var qweb = core.qweb;
    const config = require("web.config");

    var { NavBar } = require("@web/webclient/navbar/navbar");
    var { patch } = require("web.utils");
    const { useListener } = require("@web/core/utils/hooks");

    var { browser } = require("@web/core/browser/browser");
    var { useService } = require("@web/core/utils/hooks");

    var { loadCSS, loadJS } = require("@web/core/assets");

    const {useExternalListener, onMounted } = owl;


    patch(NavBar.prototype, "spiffy_theme_backend_extended.MenuJs", {
        async setup(parent, menuData) {
             this._super();
             var self = this
             this._getModeDataExt();
             $(document).on("click", ".selected_value", function(ev){self._setBtnColor(ev)});
        },

        _setBtnColor: function() {
            var self = this
            console.log("=============");
            var light_primary_btn_color = $("input[id='primary_btn']").val()
             ajax.rpc('/color/pallet/btn/', {
                 'light_primary_btn_color': light_primary_btn_color,
             })
        },

        _getModeDataExt: function() {
            var self = this
            ajax.rpc('/get/dark/mode/data').then(function(rec) {
                 var dark_mode = rec
                 self._ChangeThemeModeExt(dark_mode)
            })
        },

        _ChangeThemeModeExt: function (darkmode) {
            if (darkmode){
                $(':root').css('--biz-theme-btn-color','var(--dark-theme-primary-btn-color)');
            }
            else{
                $(':root').css('--biz-theme-btn-color','var(--light-theme-primary-btn-color)');
            }
        },

    });
 });