from odoo import api, fields, models


class ResBlendxJob(models.Model):
    """ Blendx Job """
    _name = 'res.blendx.job'
    _description = "Blendx Job"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean('Active', default=True)


class ResBlendxSeniorityLevel(models.Model):
    """ Seniority Level """
    _name = 'res.blendx.seniority'
    _description = "Seniority Level"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean('Active', default=True)
