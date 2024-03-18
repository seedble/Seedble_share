/**@odoo-module */

import { evalDomain } from "@web/views/utils";
import { FormLabel } from "@web/views/form/form_label";


import {patch} from 'web.utils';
patch(FormLabel.prototype, 'form_label.js', {
   get className() {
        let className = this._super();
        const modifiers = this.props.fieldInfo.modifiers || {};
        const required = evalDomain(modifiers.required, this.props.record.evalContext);
        const classes = this.props.className ? [this.props.className] : [];
        if (required) {
            className += " o_required_label";
        }
        return className;
    }
});
