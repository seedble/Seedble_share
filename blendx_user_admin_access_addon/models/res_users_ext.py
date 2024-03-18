# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ResUsersExt(models.Model):
    """ Extend res users """
    _inherit = 'res.users'

    work_phone = fields.Char(string="Work Phone")
    location_code = fields.Char(string="Location Code")
    work_country = fields.Char(string="Work Country")
    birth_date = fields.Date(string="Birth Date")
    gender = fields.Many2one('res.users.gender', string="Gender")
    job_family_id = fields.Many2one('res.users.job.family', string="Job Family")
    job_family_group_id = fields.Many2one('res.users.job.family', string="Job Family Group")
    management_level_id = fields.Many2one('res.users.management.level', string="Management Level")
    employee_type_id = fields.Many2one('res.users.employee.type', string="Employee Type")
    length_service = fields.Char(string="Length of Service ")
    seniority_date = fields.Date(string="Seniority Date")
    location = fields.Char(string="Location")
    level_03_manager = fields.Char(string="Level 03 Manager")
    level_03_manager_id = fields.Char(string="Level 03 Manager ID")
    level_04_manager = fields.Char(string="Level 04 Manager")
    level_04_manager_id = fields.Char(string="Level 04 Manager ID")
    res_company_id = fields.Many2one('res.company', string="Company")
    division_id = fields.Many2one('res.users.division', string="Division")

    ds_uuid = fields.Char(string="Device UUID")
    ds_current_country_name = fields.Char(string="Current Country Name")
    ds_current_operator_name = fields.Char(string="Current Operator Name")
    ds_device_owner = fields.Char(string="Device Owner")
    ds_email = fields.Char(string="Email Address")
    ds_home_country_name = fields.Char(string="Home Country Name")
    ds_language = fields.Char(string="Language")
    ds_last_check_in = fields.Char(string="Last Check-In")
    ds_manufacturer = fields.Char(string="Manufacturer")
    ds_model = fields.Char(string="Model")
    ds_platform_name = fields.Char(string="Platform Name")
    ds_registration_date = fields.Date(string="Registration Date")
    ds_status = fields.Char(string="Status")
