from odoo import models, fields,api
from odoo.exceptions import Warning, ValidationError, UserError

class access_domain_ah(models.Model):
    _name = 'access.domain.ah'
    _description = 'Access Domain'


    model_id = fields.Many2one(
        'ir.model', string='Model', index=True, required=True, ondelete='cascade')
    model_name = fields.Char(string='Model Name', related='model_id.model', readonly=True, store=True)
    apply_domain = fields.Boolean('Apply Filter')
    domain = fields.Char(string='Filter', default='[]')

    access_management_id = fields.Many2one('access.management','Access Management')

    read_right = fields.Boolean('Read',default=True)
    create_right = fields.Boolean('Create')
    write_right = fields.Boolean('Write')
    delete_right = fields.Boolean('Delete')

    @api.onchange('apply_domain')
    def _check_domain(self):
        for rec in self:
            if not rec.apply_domain:
                rec.domain = False

    @api.onchange('read_right')
    def _check_read(self):
        for rec in self:
            if not rec.read_right:
                rec.create_right = False
                rec.write_right = False
                rec.delete_right = False
                rec.apply_domain = True
                rec.domain = '[["id","=",False]]'


    @api.onchange('create_right')
    def _check_create(self):
         for rec in self:
            if rec.create_right:
                rec.read_right = True
            else:
                rec.delete_right = False    

    @api.onchange('write_right')
    def _check_write(self):
         for rec in self:
            if rec.write_right:
                rec.read_right = True
            else:
                rec.delete_right = False

    @api.onchange('delete_right')
    def _check_delete(self):
         for rec in self:
            if rec.delete_right:
                rec.read_right = True
                rec.write_right = True

