/* @odoo-module */

import { FormRenderer } from "@web/views/form/form_renderer";
import { ListController } from "@web/views/list/list_controller";
import { FormController } from "@web/views/form/form_controller";
import { ListRenderer } from "@web/views/list/list_renderer";
import { session } from "@web/session";
const { patch } = require("web.utils");
const { onMounted, onPatched } = owl;
var rpc = require("web.rpc");

patch(
    ListRenderer.prototype,
    "simplify_access_management/static/src/js/hide_export.js",
    {
        setup() {
            this._super();

            onMounted(async () => {
                var hash = window.location.hash.replace("#", '').split("&");
                let cids;
                if(hash.findIndex(ele => ele.includes("cid")) == -1)
                    cids = session.company_id;
                else {
                    cids = hash.filter(ele => ele.includes("cid"))[0].split("=")[1].split(",");
                    cids = cids.length > 0? parseInt(cids[0]): session.company_id;
                }
                let model = hash.filter(ele=>ele.includes("model"))?.[0];
                model = model? model.split("=")?.[1].split(",")?.[0]: model;
                if(cids && model) {
                    this.isExportAvailable = await rpc.query({
                        model: "access.management",
                        method: "is_export_hide",
                        args: [
                            session.user_id,
                            cids,
                            model,
                        ],
                    });
                }
                if (this.isExportAvailable) {
                    if ($(".o_list_export_xlsx").length) {
                        $(".o_list_export_xlsx").attr(
                            "style",
                            "display: none !important;"
                        );
                    }
                }
            });

            onPatched(async (nextProps) => {
                if (this.isExportAvailable) {
                    if ($(".o_list_export_xlsx").length) {
                        $(".o_list_export_xlsx").attr(
                            "style",
                            "display: none !important;"
                        );
                    }
                }
            });
        },
    }
);