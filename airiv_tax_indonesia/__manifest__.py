# -*- coding: utf-8 -*-
{
    'name': 'Indonesia DJP Coretax & e-Faktur Tax Engine (PPN 12%, DPP Nilai Lain, 16-Digit NPWP/NIK)',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Statutory DJP Coretax, e-Faktur 4.0, PPN 12%, DPP Nilai Lain, and NSFP Allocator for Odoo 18',
    'description': """
Indonesia Commercial Taxation & DJP Coretax Engine for Odoo 18 Community.
- Statutory PPN 12% & DPP Nilai Lain (effective 11% / 12% calculation engine)
- 16-Digit NIK (WPOP) and 16-Digit NPWP / NITKU (WP Badan) validation (PMK 136/2023)
- Automated NSFP (Nomor Seri Faktur Pajak) sequential assignment
- DJP e-Faktur 4.0 & Coretax CSV batch export (FK, LT, OF schema)
- Zero External Server Overhead - 100% Odoo 18 Community Native
""",
    'author': 'Riv Cloud Management',
    'website': 'https://airiv.id',
    'license': 'LGPL-3',
    'price': 0.0,
    'currency': 'EUR',
    'depends': ['account', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'data/tax_data.xml',
        'views/res_partner_views.xml',
        'views/account_move_views.xml',
        'views/nsfp_range_views.xml',
        'wizard/efaktur_export_wizard_views.xml',
        'views/tax_menu_views.xml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
