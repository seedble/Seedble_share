/** @odoo-module **/

import {archParseBoolean} from '@web/views/utils';
import {ListArchParser} from '@web/views/list/list_arch_parser';
import {patch} from '@web/core/utils/patch';
import {FormControlPanel} from '@web/views/form/control_panel/form_control_panel';
import {FormStatusIndicator} from '@web/views/form/form_status_indicator/form_status_indicator'
import { WithSearch, SEARCH_KEYS } from '@web/search/with_search/with_search';
export const beforeSplitViewOpen = []



patch(ListArchParser.prototype, 'spiffy_split_view', {
    parse(arch, models, modelName) {
        const result = this._super.apply(this, arguments);
        const xmlDoc = this.parseXML(arch);
        result.splitView = archParseBoolean(xmlDoc.getAttribute('split_view') || '');
        return result
    }
})

export class SplitViewControlPanel extends FormControlPanel {
}
export class SplitViewStatusIndicator extends FormStatusIndicator {
}

export function beforeSplitViewOpenchange(func) {
    beforeSplitViewOpen.push(func)
}

SEARCH_KEYS.push('resId')
WithSearch.props.resId = { type: [Number, { value: null }, { value: false }], optional: true }

SplitViewControlPanel.template = 'spiffy_split_view.SplitViewControlPanel';
SplitViewStatusIndicator.template = 'spiffy_split_view.SplitViewStatusIndicator';

