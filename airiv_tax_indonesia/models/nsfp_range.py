# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AirivNsfpRange(models.Model):
    _name = 'airiv.nsfp.range'
    _description = 'DJP Nomor Seri Faktur Pajak (NSFP) Pool'
    _order = 'year desc, start_number asc'

    name = fields.Char(string="Reference / SK DJP", required=True)
    year = fields.Char(string="Tax Year", size=4, required=True, default=lambda self: str(fields.Date.today().year))
    prefix = fields.Char(string="Prefix / Code", size=8, default="000", help="e.g. 000 for standard or 001")
    start_number = fields.Integer(string="Start Serial (8 Digits)", required=True)
    end_number = fields.Integer(string="End Serial (8 Digits)", required=True)
    current_number = fields.Integer(string="Next Serial to Assign", required=True)
    active = fields.Boolean(default=True)
    notes = fields.Text(string="Notes")

    total_quota = fields.Integer(string="Total Quota", compute="_compute_quota", store=True)
    used_quota = fields.Integer(string="Used", compute="_compute_quota", store=True)
    remaining_quota = fields.Integer(string="Remaining", compute="_compute_quota", store=True)

    @api.depends('start_number', 'end_number', 'current_number')
    def _compute_quota(self):
        for record in self:
            record.total_quota = (record.end_number - record.start_number + 1) if record.end_number >= record.start_number else 0
            record.used_quota = (record.current_number - record.start_number) if record.current_number >= record.start_number else 0
            record.remaining_quota = max(record.total_quota - record.used_quota, 0)

    def allocate_next_nsfp(self):
        self.ensure_one()
        if self.current_number > self.end_number:
            raise UserError(_("NSFP Quota Depleted for range %s (%s)! Please request a new range on e-Nofa Coretax.", self.name, self.year))
        
        serial_str = f"{self.current_number:08d}"
        allocated_nsfp = f"{self.prefix}-{self.year[-2:]}.{serial_str}"
        self.current_number += 1
        return allocated_nsfp
