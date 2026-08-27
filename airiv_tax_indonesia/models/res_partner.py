# -*- coding: utf-8 -*-
import re
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    l10n_id_tax_type = fields.Selection([
        ('wpop', 'WPOP (Orang Pribadi - NIK 16 Digit)'),
        ('badan', 'WP Badan (Badan Usaha - NPWP 16 Digit)'),
        ('pemungut', 'Pemungut Instansi Pemerintah / BUMN'),
        ('non_npwp', 'Non-NPWP / Pembeli Retail (0000000000000000)'),
    ], string="Indonesian Tax Entity Type", default='badan')

    l10n_id_npwp16 = fields.Char(string="NPWP 16 / NIK (Coretax)", size=16, help="16-digit Single Identity Tax Number (NIK for individual or NPWP 16 for entities)")
    l10n_id_nitku = fields.Char(string="NITKU (22 Digit)", size=22, help="Nomor Identitas Tempat Kegiatan Usaha (22 digits for branch offices)")
    l10n_id_tax_name = fields.Char(string="Nama Wajib Pajak (SPPKP)", help="Official registered tax entity name")
    l10n_id_tax_address = fields.Char(string="Alamat Faktur Pajak", help="Official address registered in DJP Master File")

    @api.constrains('l10n_id_npwp16', 'l10n_id_tax_type')
    def _check_l10n_id_npwp16(self):
        for record in self:
            if not record.l10n_id_npwp16:
                continue
            cleaned = re.sub(r'\D', '', record.l10n_id_npwp16)
            if record.l10n_id_tax_type == 'non_npwp':
                continue
            if len(cleaned) != 16:
                raise ValidationError(_("Invalid Coretax Identification! NPWP 16 / NIK must be exactly 16 numeric digits. Provided: %s", record.l10n_id_npwp16))
