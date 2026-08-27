# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_id_faktur_pajak_number = fields.Char(string="Nomor Faktur Pajak (NSFP)", copy=False, tracking=True)
    l10n_id_tax_transaction_code = fields.Selection([
        ('01', '01 - Kepada Pihak Bukan Pemungut PPN (Standard)'),
        ('02', '02 - Kepada Pemungut Bendaharawan Pemerintah'),
        ('03', '03 - Kepada Pemungut BUMN / Badan Usaha Tertentu'),
        ('04', '04 - DPP Nilai Lain (Effective 11% / 12% Rates)'),
        ('05', '05 - Besaran Tertentu (Pasal 9A UU PPN)'),
        ('07', '07 - Penyerahan yang PPN-nya Tidak Dipungut (Kawasan Berikat)'),
        ('08', '08 - Penyerahan yang Dibebaskan dari Pengenaan PPN'),
        ('09', '09 - Penyerahan Aktiva Pasal 16D UU PPN'),
    ], string="Kode Transaksi Faktur Pajak", default='01', tracking=True)

    l10n_id_faktur_date = fields.Date(string="Tanggal Faktur Pajak", default=fields.Date.context_today)
    l10n_id_efaktur_status = fields.Selection([
        ('unassigned', 'Belum Ada NSFP'),
        ('assigned', 'NSFP Assigned'),
        ('exported', 'Exported to e-Faktur CSV'),
        ('approved', 'Approved DJP Coretax'),
        ('cancelled', 'Dibatalkan'),
    ], string="Status e-Faktur", default='unassigned', copy=False, tracking=True)

    l10n_id_is_dpp_nilai_lain = fields.Boolean(string="Apply DPP Nilai Lain", default=False)
    l10n_id_dpp_factor = fields.Float(string="DPP Factor Ratio", default=0.9166666667, digits=(12, 10))

    def action_assign_nsfp(self):
        for move in self:
            if move.move_type not in ('out_invoice', 'out_refund'):
                continue
            if move.l10n_id_faktur_pajak_number:
                continue
            
            pool = self.env['airiv.nsfp.range'].search([('active', '=', True), ('remaining_quota', '>', 0)], limit=1)
            if not pool:
                raise UserError(_("No active NSFP pool with remaining quota found! Please configure NSFP ranges under Indonesian Tax > NSFP Pool."))
            
            raw_serial = pool.allocate_next_nsfp()
            full_nsfp = f"{move.l10n_id_tax_transaction_code}.{raw_serial}"
            move.write({
                'l10n_id_faktur_pajak_number': full_nsfp,
                'l10n_id_efaktur_status': 'assigned',
                'l10n_id_faktur_date': move.invoice_date or fields.Date.today(),
            })

    def action_post(self):
        res = super(AccountMove, self).action_post()
        for move in self:
            if move.move_type in ('out_invoice', 'out_refund') and not move.l10n_id_faktur_pajak_number:
                pool = self.env['airiv.nsfp.range'].search([('active', '=', True), ('remaining_quota', '>', 0)], limit=1)
                if pool:
                    move.action_assign_nsfp()
        return res
