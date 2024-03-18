/** @odoo-module **/
// import DocumentViewer from '@mail/component/document_viewer';
import view_registry from 'web.view_registry';
import ActionMenus from 'web.ActionMenus';
var spiffyDocumentViewer = require("spiffy_theme_backend.spiffyDocumentViewer");
import { ListRenderer } from "@web/views/list/list_renderer";
import { registerPatch } from '@mail/model/model_core';
import "@mail/models/file_uploader";
import { useService } from "@web/core/utils/hooks";

import { registry } from "@web/core/registry";
import { divertColorItem } from "./apps_menu";
import session from "web.session";

import {SplitviewContainer} from './split_view/split_view_container';
import {beforeSplitViewOpen} from "./split_view/split_view_components";

const serviceRegistry = registry.category("services");
const userMenuRegistry = registry.category("user_menuitems");


    var ajax = require("web.ajax");
    var core = require("web.core");
    var dom = require("web.dom");
    var _t = core._t;
    var { patch } = require("web.utils");
    var { onMounted, onWillStart, useState, useChildSubEnv } = owl;


    // TODO add list view document here , old way will not work
    patch(ListRenderer.prototype, "spiffy_theme_backend.ListRenderer", {
      setup() {
          this._super();
          var self = this
          this.rpc = useService("rpc");
          this.actionService = useService('action');
          this.viewService = useService('view');
          this.userService = useService('user');

          self.showattachment = false
          if ($('body').hasClass('show_attachment')) {
            self.showattachment = true
          }
          var rec_ids = []
          this.notificationService = useService("notification");
          var records = this.props.list.records
          var model = this.props.list.resModel
          records.map(record => rec_ids.push(record.resId))

          onWillStart(async () => {
              this.biz_attachment_data = await this.rpc("/get/attachment/data", { model, rec_ids });
          });
          // split view code

          this.SplitViewForm = useState({
              show: false,
              id: 0,
          })

          const formViewId = this.getFormViewId()
          useChildSubEnv({
              config: {
                  ...this.env.config,
                  isX2Many: this.isX2Many,
                  views: [[formViewId, 'form']],
                  close: this.closeSplitViewForm.bind(this),
              },
          });
      },

      _loadattachmentviewer: function (ev) {
        var attachment_id = parseInt($(ev.currentTarget).data("id"));
        var rec_id = parseInt($(ev.currentTarget).data("rec_id"));
        var attachment_mimetype = $(ev.currentTarget).data("mimetype");
        var mimetype_match = attachment_mimetype.match("(image|application/pdf|text|video)");
        var attachment_data = this.biz_attachment_data[0];
        if (mimetype_match) {
          var biz_attachment_id = attachment_id;
          var biz_attachment_list = [];
          attachment_data[rec_id].forEach((attachment) => {
            if (attachment.attachment_mimetype.match("(image|application/pdf|text|video)")) {
              biz_attachment_list.push({
                id: attachment.attachment_id,
                filename: attachment.attachment_name,
                name: attachment.attachment_name,
                url: "/web/content/"+attachment.attachment_id+"?download=true",
                type: attachment.attachment_mimetype,
                mimetype: attachment.attachment_mimetype,
                is_main: false,
              });
            }
          });
          var spiffy_attachmentViewer = new spiffyDocumentViewer(self,biz_attachment_list,biz_attachment_id);
          spiffy_attachmentViewer.appendTo($(".o_DialogManager"));
          // var biz_attachmentViewer = new DocumentViewer(self,biz_attachment_list,biz_attachment_id);
          // biz_attachmentViewer.appendTo($("body"));

        } else{
            this.notificationService.add(this.env._t("Preview for this file type can not be shown"), {
              title: this.env._t("File Format Not Supported"),
              type: 'danger',
              sticky: false
          });
        }
      },

      // split view functions

      getFormViewId() {
          return this.env.config.views.find(view => view[1] === 'form')?.[0] || false
      },

      getSplitviewContainerProps() {
            const resIds = this.props.list.records.map((record) => record.resId); 
          const props = {
            context: {
                ...this.SplitViewFormRecord.context,
            },
            record: this.SplitViewFormRecord,
            resModel: this.props.list.resModel,
            resId: this.SplitViewForm.id,
            resIds: resIds,
          }
          const viewId = this.getFormViewId()
          if (viewId) {
              props.viewId = viewId
          }
          return props
      },

      async callbeforeSplitViewOpen() {
          return await Promise.all(beforeSplitViewOpen.map(func => func()))
      },

      async onCellClicked(record, column, ev) {
          var split_view_enabled = $('body').hasClass('tree_form_split_view')
          console.log('this onCellClicked ----------------------- ', this)

          if ((!this.isX2Many && !split_view_enabled) || (this.isX2Many && !this.props.archInfo.splitView) || (this.props.archInfo.editable)) {
              this._super.apply(this, arguments);
              return;
          }
          if (ev.target.special_click) {
              return;
          }
          if (record.resId && this.SplitViewForm.id !== record.resId && !this.props.archInfo.editable) {
              await this.callbeforeSplitViewOpen();
              this.SplitViewForm.id = record.resId;
              this.SplitViewForm.show = true;
              this.SplitViewFormRecord = record;
              this.recordDatapointID = record.id;
          }
      },

    async closeSplitViewForm() {
        await this.callbeforeSplitViewOpen();
        this.SplitViewForm.show = false;
        this.SplitViewForm.id = false;
        $('.tree_form_split > .o_view_controller > .o_content > .spiffy_list_view > #separator').remove()
        // $('.tree_form_split > .o_view_controller > .o_content > .spiffy_list_view > .close_form_view').remove()
        $('.o_action_manager.tree_form_split').removeClass('tree_form_split')
        $('.spiffy_list_view').attr('style','')
        $('.o_list_table .o_data_row').removeClass('side-selected')
        console.log('close side for mview')
    },

    });

    const getAttachmentNextTemporaryId = (function () {
      let tmpId = 0;
      return () => {
          tmpId -= 1;
          return tmpId;
      };
    })();
    
    registerPatch({
      name: 'FileUploader',
      recordMethods:{
          /**
           * @private
           * @override
           * @param {Object} param0
           * @param {FileList|Array} param0.files
           * @returns {Promise}
           */
          async _performUpload({ files }) {
            const webRecord = this.activityListViewItemOwner && this.activityListViewItemOwner.webRecord;
            const composer = this.composerView && this.composerView.composer; // save before async
            const thread = this.thread; // save before async
            const chatter = (
                (this.chatterOwner) ||
                (this.attachmentBoxView && this.attachmentBoxView.chatter) ||
                (this.activityView && this.activityView.activityBoxView.chatter)
            ); // save before async
            const activity = (
                this.activityView && this.activityView.activity ||
                this.activityListViewItemOwner && this.activityListViewItemOwner.activity
            ); // save before async
            const uploadingAttachments = new Map();
            for (const file of files) {
                uploadingAttachments.set(file, this.messaging.models['Attachment'].insert({
                    composer,
                    filename: file.name,
                    id: getAttachmentNextTemporaryId(),
                    isUploading: true,
                    mimetype: file.type,
                    name: file.name,
                    originThread: (!composer && thread) ? thread : undefined,
                }));
            }
            const attachments = [];
            for (const file of files) {
                const uploadingAttachment = uploadingAttachments.get(file);
                if (!uploadingAttachment.exists()) {
                    // This happens when a pending attachment is being deleted by user before upload.
                    continue;
                }
                if ((composer && !composer.exists()) || (thread && !thread.exists())) {
                    return;
                }
                try {
                  var response;
                  if (session.bg_color) {
                    response = await (composer || thread).messaging.browser.fetch('/app/attachment/upload', {
                        method: 'POST',
                        body: this._createFormData({ composer, file, thread }),
                        signal: uploadingAttachment.uploadingAbortController.signal,
                    });
                  }else{
                    response = await (composer || thread).messaging.browser.fetch('/mail/attachment/upload', {
                        method: 'POST',
                        body: this._createFormData({ composer, file, thread }),
                        signal: uploadingAttachment.uploadingAbortController.signal,
                    });
                  }
                    
                    const attachmentData = await response.json();
                    if (uploadingAttachment.exists()) {
                        uploadingAttachment.delete();
                    }
                    if ((composer && !composer.exists()) || (thread && !thread.exists())) {
                        return;
                    }
                    const attachment = this._onAttachmentUploaded({ attachmentData, composer, thread });
                    attachments.push(attachment);
                } catch (e) {
                    if (e.name !== 'AbortError') {
                        throw e;
                    }
                }
            }
            if (activity && activity.exists()) {
                await activity.markAsDone({ attachments });
            }
            if (webRecord) {
                webRecord.model.load({ resId: thread.id });
            }
            if (chatter && chatter.exists() && chatter.shouldReloadParentFromFileChanged) {
                chatter.reloadParentView();
            }
        },
      }
    })

    registerPatch({
      name: 'Attachment',
      recordMethods:{
        /**
         * Handles click on download icon.
         *
         * @param {MouseEvent} ev
         */
        onClickDownload(ev) {
          if(session.bg_color){
            var attach_id = this.id
            ajax.jsonRpc("/attach/get_data", "call", {
              id:attach_id
            }).then(function (data) {
              if (data){
                window.flutter_inappwebview.callHandler('blobToBase64Handler', btoa(data['pdf_data']),data['attach_type'],data['attach_name']);
              }
            });
          }else{
            this._super.apply(this, arguments);
          }
        },
      }
    })

    registerPatch({
      name:'AttachmentViewerViewable',
      recordMethods:{
        download() {
          console.log('=======attch=>>>>>>',this.attachmentOwner.id)
          if(session.bg_color){
            var attach_id = this.attachmentOwner.id
            ajax.jsonRpc("/attach/get_data", "call", {
              id:attach_id
            }).then(function (data) {
              if (data){
                window.flutter_inappwebview.callHandler('blobToBase64Handler', btoa(data['pdf_data']),data['attach_type'],data['attach_name']);
              }
            });
          }else{
            this._super.apply(this, arguments);
          }
       },
      }
    })

    registerPatch({
      name: 'AttachmentImage',
      recordMethods:{
        /**
         * Called when clicking on download icon.
         *
         * @param {MouseEvent} ev
         */
        onClickDownload(ev) {
          if(session.bg_color){
            var attach_id = this.attachment.id
            ajax.jsonRpc("/attach/get_data", "call", {
              id:attach_id
            }).then(function (data) {
              if (data){
                window.flutter_inappwebview.callHandler('blobToBase64Handler', btoa(data['pdf_data']),data['attach_type'],data['attach_name']);
              }
            });
          }else{
            this._super.apply(this, arguments);
          }
        }
      }
    })

    const bg_colorService = {
      start() {       
          var is_body_color = session.bg_color
          if (is_body_color) {
              userMenuRegistry.remove('log_out');
              userMenuRegistry.remove('odoo_account');
              userMenuRegistry.remove('documentation');
              userMenuRegistry.remove('support');
  
              userMenuRegistry.add("divert.account", divertColorItem);
          }
      },
    };
    serviceRegistry.add("bg_color", bg_colorService);

    ListRenderer.components = {
        ...ListRenderer.components,
        SplitviewContainer,
    };
