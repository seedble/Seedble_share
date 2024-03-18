from odoo import fields, models, api, _
from odoo.http import request

class ir_ui_menu(models.Model):
    _inherit = 'ir.ui.menu'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        ids = super(ir_ui_menu, self).search(args, offset=0, limit=None, order=order, count=False)
        user = self.env.user
        # user.clear_caches()
        # cids = request.httprequest.cookies.get('cids') and request.httprequest.cookies.get('cids').split(',')[0] or self.env.company.id
        cids = self.env.company.id
        for menu_id in user.access_management_ids.filtered(lambda line: int(cids) in line.company_ids.ids).mapped('hide_menu_ids'):
            if menu_id in ids:
                ids = ids - menu_id
        if offset:
            ids = ids[offset:]
        if limit:
            ids = ids[:limit]
        return len(ids) if count else ids

