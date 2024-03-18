from odoo import fields, models, api


class ResUsersDivision(models.Model):
    _name = "res.users.division"
    _description = "Res Users Division"
    _rec_name = "div_name"

    div_name = fields.Char(string="Name")


class ResUsersEmployeeType(models.Model):
    _name = "res.users.employee.type"
    _description = "Res Users Employee Type"
    _rec_name = "et_name"

    et_name = fields.Char(string="Name", required=True)


class ResUsersManagementLevel(models.Model):
    _name = "res.users.management.level"
    _description = "Res Users Management Level"
    _rec_name = "ml_name"

    ml_name = fields.Char(string="Name", required=True)


class ResUsersJobFamily(models.Model):
    _name = "res.users.job.family"
    _description = "Res Users Job Family"
    _rec_name = "jf_name"

    jf_name = fields.Char(string="Name", required=True)
    parent_id = fields.Many2one('res.users.job.family', string="Job Family Group")


class ResUsersGender(models.Model):
    _name = 'res.users.gender'
    _description = 'Res Users Gender'
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
