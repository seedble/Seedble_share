/** @odoo-module **/

import {Component} from '@odoo/owl';
import {useService} from '@web/core/utils/hooks';
import {SplitViewController} from "./split_view_controller";
import {SplitViewControlPanel} from './split_view_components';
import {SplitViewForm} from './split_view_form';

const {useEffect, useRef, useChildSubEnv} = owl;

export class SplitviewContainer extends Component {

    setup() {
        super.setup();
        this.formviewPanel = useRef('formview-panel')
        this.formviewContainer = useRef('formview-container')
        this.actionService = useService('action');
        useChildSubEnv({
            config: {
                ...this.env.config,
                ControlPanel: SplitViewControlPanel,
                Controller: SplitViewController,
            },
        })
        useEffect(() => {
            this.updateSlipViewForm();
            this.addDraggableSlider();
        }, () => [this.props.resId])
    }

    addDraggableSlider() {
        var self = this
        if (!this.formviewPanel.el) {
            return
        }
        console.log('this formviewPanel ----------------- ', this)
        $('#separator').remove()
        
        $('.tree_form_split_view > .o_action_manager').addClass('tree_form_split')
        $('.tree_form_split_view > .o_action_manager > .o_view_controller').addClass('split-screen-tree-viewer')
        $(this.formviewPanel.el).addClass('tree-form-viewer')
        $(this.formviewPanel.el).before('<div id="separator" class="split_view_separator"></div>')


        $('.o_action_manager.tree_form_split > .split-screen-tree-viewer > .o_control_panel .reload_view').click()

        var options = {
            containment: 'parent',
            helper: 'clone'
        }
        Object.assign(options, {
            axis: 'x',
            start: function(event, ui) {
                $(this).attr('start_offset', $(this).offset().left);
                $(this).attr('start_next_height', $(this).next().width());
            },
            drag: function(event, ui) {
                var prev_element = $(this).prev();
                prev_element.width(ui.offset.left - prev_element.offset().left);
            }
        })
        $('#separator').draggable(options);
        $('#separator').on("dragstop", function(event, ui) {
            $('.custom_seperator').css({
                'opacity': '1'
            })
        });
    }

    updateSlipViewForm() {
        const slip_view_form = this.formviewContainer.el?.querySelector('.o_form_view')
        if (slip_view_form) {
            slip_view_form.classList.remove('o_xxl_form_view')
        }
    }

    get formViewProps() {
        const props = {
            context: {
                ...this.props.context,
            },
            loadActionMenus: true,
            display: {
                controlPanel: true,
            },
            viewId: this.props.viewId,
            className: 'o_xxs_form_view',
            resModel: this.props.resModel,
            resId: this.props.resId,
            resIds: this.props.resIds,
        }
        return props
    }

}

SplitviewContainer.template = 'spiffy_split_view.SplitviewContainer';
SplitviewContainer.props = {
    context: {
        type: Object,
        optional: true,
    },
    viewId: {
        type: Number,
        optional: true,
    },
    record: {
        type: Object,
    },
    resModel: {
        type: String,
    },
    resId: {
        type: Number,
    },
    resIds: {
        type: Array,
    },
    mode: {
        type: String,
        optional: true,
    },
}
SplitviewContainer.components = {
    SplitViewForm,
};
