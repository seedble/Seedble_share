/** @odoo-module **/

import {useService} from '@web/core/utils/hooks';
import {FormController} from '@web/views/form/form_controller';
import { usePager } from "@web/search/pager_hook";
import {SplitViewStatusIndicator} from './split_view_components';
import {beforeSplitViewOpenchange} from "./split_view_components";

export class SplitViewController extends FormController {

    setup() {
        super.setup();
        this.actionService = useService('action');
        console.log('side form controller thiss ---------------------------------- ', this)
        beforeSplitViewOpenchange(this.saveButtonClicked.bind(this))
        usePager(() => {
            if (!this.model.root.isVirtual) {
                const resIds = this.props.resIds;
                return {
                    offset: resIds.indexOf(this.props.resId),
                    limit: 1,
                    total: resIds.length,
                    onUpdate: ({ offset }) => this.onPagerUpdate({ offset, resIds }),
                };
            };
        });
    }

    async onPagerUpdate({ offset, resIds }) {
        await this.model.root.askChanges(); // ensures that isDirty is correct
        let canProceed = true;
        if (this.model.root.isDirty) {
            canProceed = await this.model.root.save({
                stayInEdition: true,
                useSaveErrorDialog: true,
            });
        }
        if (canProceed) {
            return this.model.load({ resId: resIds[offset] });
        }
    }

    async save () {
        const changedFields = await this._super(...arguments);
        // $('.tree_form_split > .o_view_controller > .o_control_panel .reload_view').click()
        return changedFields;
    }
    // async saveButtonClicked(params = {}) {
    //     // const saved = await this._super(...arguments);
    //     const saved = await super.saveButtonClicked(...arguments);
    //     // $('.tree_form_split > .o_view_controller > .o_control_panel .reload_view').click()
    //     console.log('saved sideform view')
    //     return saved;
    // }

    getActionMenuItems() {
        const ActionMenuItems = super.getActionMenuItems(...arguments);
        $('.spiffy_list_view > .o_list_renderer .o_data_row[resid="'+this.props.resId+'"]').addClass('side-selected')
        return ActionMenuItems;
    }

}

SplitViewController.template = 'spiffy_split_view.SplitViewForm';

SplitViewController.components = {
    ...FormController.components,
    SplitViewStatusIndicator,
}