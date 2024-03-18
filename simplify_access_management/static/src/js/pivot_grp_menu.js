/** @odoo-module **/

const { patch } = require('web.utils');
const { onWillStart } = owl;
import { GroupByMenu } from "@web/search/group_by_menu/group_by_menu";
import { useService } from "@web/core/utils/hooks";

patch(GroupByMenu.prototype, "GoupMenuPatchBits", {
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