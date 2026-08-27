# -*- coding: utf-8 -*-
import base64
import io
import csv
import re
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AirivEfakturExportWizard(models.TransientModel):
    _name = 'airiv.efaktur.export.wizard'
    _description = 'DJP e-Faktur 4.0 & Coretax Batch CSV Exporter'

    date_from = fields.Date(string="Start Date", required=True, default=lambda self: fields.Date.today().replace(day=1))
    date_to = fields.Date(string="End Date", required=True, default=fields.Date.today)
    invoice_ids = fields.Many2many('account.move', string="Target Invoices", domain="[('move_type', '=', 'out_invoice'), ('state', '=', 'posted')]")
    csv_file = fields.Binary(string="Generated e-Faktur CSV", readonly=True)
    filename = fields.Char(string="File Name", readonly=True)

    @api.onchange('date_from', 'date_to')
    def _onchange_dates(self):
        if self.date_from and self.date_to:
            self.invoice_ids = self.env['account.move'].search([
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
                ('invoice_date', '>=', self.date_from),
                ('invoice_date', '<=', self.date_to),
            ])

    def action_generate_csv(self):
        self.ensure_one()
        if not self.invoice_ids:
            raise UserError(_("No posted customer invoices found in the selected period."))

        output = io.StringIO()
        writer = csv.writer(output, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Standard DJP e-Faktur 4.0 Header
        writer.writerow(["FK", "KD_JENIS_TRANSAKSI", "FG_PENGGANTI", "NOMOR_FAKTUR", "MASA_PAJAK", "TAHUN_PAJAK", "TANGGAL_FAKTUR", "NPWP", "NAMA", "ALAMAT_LENGKAP", "JUMLAH_DPP", "JUMLAH_PPN", "JUMLAH_PPNBM", "ID_KETERANGAN_TAMBAHAN", "FG_UANG_MUKA", "UANG_MUKA_DPP", "UANG_MUKA_PPN", "UANG_MUKA_PPNBM", "REFERENSI", "KODE_DOKUMEN_PENDUKUNG"])
        writer.writerow(["LT", "NPWP", "NAMA", "JALAN", "BLOK", "NOMOR", "RT", "RW", "KECAMATAN", "KELURAHAN", "KABUPATEN", "PROPINSI", "KODE_POS", "NOMOR_TELEPON"])
        writer.writerow(["OF", "KODE_OBJEK", "NAMA", "HARGA_SATUAN", "JUMLAH_BARANG", "HARGA_TOTAL", "DISKON", "DPP", "PPN", "TARIF_PPNBM", "PPNBM"])

        exported_moves = self.env['account.move']

        for move in self.invoice_ids:
            partner = move.partner_id
            npwp = re.sub(r'\D', '', partner.l10n_id_npwp16 or partner.vat or '0000000000000000')
            if len(npwp) < 16:
                npwp = npwp.zfill(16)
            
            clean_nsfp = re.sub(r'[^0-9]', '', move.l10n_id_faktur_pajak_number or '')
            if len(clean_nsfp) >= 13:
                clean_nsfp = clean_nsfp[-13:]
            else:
                clean_nsfp = f"00026{move.id:08d}"

            invoice_date = move.invoice_date or fields.Date.today()
            masa_pajak = invoice_date.month
            tahun_pajak = invoice_date.year

            dpp_total = sum(move.invoice_line_ids.mapped('price_subtotal'))
            ppn_total = sum(move.invoice_line_ids.mapped('price_total')) - dpp_total
            if ppn_total <= 0:
                ppn_total = int(round(dpp_total * 0.12))

            # 1. Write FK
            writer.writerow([
                "FK",
                move.l10n_id_tax_transaction_code or "01",
                "0",
                clean_nsfp,
                masa_pajak,
                tahun_pajak,
                invoice_date.strftime("%d/%m/%Y"),
                npwp,
                partner.l10n_id_tax_name or partner.name,
                partner.l10n_id_tax_address or partner.contact_address or "Indonesia",
                int(round(dpp_total)),
                int(round(ppn_total)),
                0,
                "",
                "0",
                0,
                0,
                0,
                move.name,
                ""
            ])

            # 2. Write OF
            for line in move.invoice_line_ids.filtered(lambda l: not l.display_type):
                price_subtotal = int(round(line.price_subtotal))
                line_ppn = int(round(price_subtotal * 0.12))
                writer.writerow([
                    "OF",
                    line.product_id.default_code or f"PROD-{line.product_id.id}",
                    line.name.replace('\n', ' ')[:100],
                    int(round(line.price_unit)),
                    line.quantity,
                    price_subtotal,
                    0,
                    price_subtotal,
                    line_ppn,
                    0,
                    0
                ])

            exported_moves |= move

        exported_moves.write({'l10n_id_efaktur_status': 'exported'})

        csv_data = output.getvalue().encode('utf-8')
        self.write({
            'csv_file': base64.b64encode(csv_data),
            'filename': f"eFaktur_DJP_Export_{fields.Date.today().strftime('%Y%m%d')}.csv"
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f"/web/content/?model=airiv.efaktur.export.wizard&id={self.id}&field=csv_file&download=true&filename={self.filename}",
            'target': 'self',
        }
