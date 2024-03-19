/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Many2OneField } from "@web/views/fields/many2one/many2one_field";
import { Component } from "@odoo/owl";

export class Many2OneAvatarLeft extends Component {
    get relation() {
        return this.props.relation;
    }
}

Many2OneAvatarLeft.template = "blendx_base.Many2OneAvatarLeft";
Many2OneAvatarLeft.components = {
    Many2OneField,
};
Many2OneAvatarLeft.props = {
    ...Many2OneField.props,
};

Many2OneAvatarLeft.supportedTypes = ["many2one"];
Many2OneAvatarLeft.extractProps = Many2OneField.extractProps;
registry.category("fields").add("many2one_avatar_left", Many2OneAvatarLeft);
