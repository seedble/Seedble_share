import logging

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class DepartmentTeamRole(models.Model):
    _name = "department.team.role"
    _description = "Blendx Department Team Role"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean('Active', default=True)
    operational = fields.Boolean('Operational', default=False)
    organizational = fields.Boolean('Organizational', default=False)


class BlendxDepartmentCompany(models.Model):
    _name = "blendx.department.company"
    _description = "Blendx Department Company"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean('Active', default=True)
    parent_id = fields.Many2one('blendx.department.company', string='Parent Department')


class BlendxDepartment(models.Model):
    """ Blendx Department """
    _name = 'blendx.department'
    _description = "Blendx Department"
    _rec_name = 'name'

    # _sql_constraints = [
    #     ('manager_id_uniq', 'UNIQUE (manager_id)', 'Manager must be unique')
    # ]

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Department Description")
    active = fields.Boolean('Active', default=True)
    parent_id = fields.Many2one('blendx.department', string='Superior Department')
    department_company_id = fields.Many2one('blendx.department.company', string='Company')
    manager_id = fields.Many2one('res.users', string='Manager')
    team_ids = fields.One2many('blendx.department.team', 'blendx_department_id', string='Teams')
    organization_typology = fields.Selection([('operational', 'Operational'), ('organizational', 'Organizational')],
                                             string="Organization Typology", default='operational', store=True)

    @api.constrains('manager_id')
    def _check_manager_id_unique(self):
        if self.organization_typology != 'organizational':
            return
        department_ids = self.search_count([('manager_id', '=', self.manager_id.id), ('id', '!=', self.id),
                                            ('organization_typology', '=', 'organizational')])
        if department_ids <= 0:
            return
        raise ValidationError("Manager must be unique in each department!")


class BlendxDepartmentTeam(models.Model):
    """ Blendx Department Team"""
    _name = 'blendx.department.team'
    _description = "Blendx Department Team"
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean('Active', default=True)
    team_member_id = fields.Many2one('res.users', string="Team Member")
    blendx_department_id = fields.Many2one('blendx.department', string="Blendx Department")

    @api.constrains('team_member_id', 'team_role_id')
    def _check_team_member_unique(self):
        """ Constrains to select team member and team role. """
        if self.blendx_department_id.organization_typology != 'organizational':
            return
        department_teams = self.search_count(
            [('team_role_id', '=', self.team_role_id.id), ('team_member_id', '=', self.team_member_id.id),
             ('id', '!=', self.id), ('blendx_department_id.organization_typology', '=', 'organizational')])
        if department_teams <= 0:
            return
        raise ValidationError("Team member and Team role must be unique in each department!")

    @api.onchange('blendx_department_id')
    def set_domain_team_role_id(self):
        """ Onchange method on department to set domain on team role. """
        domain = []
        if self.blendx_department_id.organization_typology == 'operational':
            domain = [('operational', '=', True)]
        elif self.blendx_department_id.organization_typology == 'organizational':
            domain = [('organizational', '=', True)]
        return {'domain': {'team_role_id': domain}}

    team_role_id = fields.Many2one('department.team.role', string="Team Role")
