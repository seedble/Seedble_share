/** @odoo-module **/

const { patch } = require('web.utils');
const { onWillStart } = owl;
import { CustomFilterItem } from "@web/search/filter_menu/custom_filter_item";
import { useService } from "@web/core/utils/hooks";

patch(CustomFilterItem.prototype, "CustomFilterItemPatchBits", {
    setup() {
        this._super();
        this.orm = useService("orm");
        onWillStart(async () => {
        const res = await this.orm.call("access.management", "get_hidden_field", [
            "",
            this?.env?.searchModel?.resModel,
        ]);
        this.fields = this.fields.filter((ele) => !res.includes(ele.name));
        });
    }
})