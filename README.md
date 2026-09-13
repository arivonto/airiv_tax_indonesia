# Indonesia DJP Coretax & e-Faktur Tax Engine

[![Odoo](https://img.shields.io/badge/Odoo-18.0-714B67.svg)](https://www.odoo.com/)
[![License](https://img.shields.io/badge/License-LGPL--3-0f766e.svg)](LICENSE)
[![Author](https://img.shields.io/badge/Author-AIRIV-0891b2.svg)](https://airiv.id)
[![GitHub Actions](https://github.com/arivonto/airiv_tax_indonesia/actions/workflows/odoo-appstore-ci.yml/badge.svg?branch=18.0)](https://github.com/arivonto/airiv_tax_indonesia/actions)
[![Apps Store Ready](https://img.shields.io/badge/Odoo%20Apps%20Store-ready-22c55e.svg)](https://apps.odoo.com/)

`airiv_tax_indonesia` is an Indonesian commercial taxation layer for Odoo 18 Community. It adds DJP Coretax and e-Faktur oriented fields, PPN 12% tax definitions, DPP Nilai Lain support, 16-digit NPWP/NIK validation, NSFP allocation, and CSV export workflows.

The module is designed for practical Indonesian accounting operations where invoices, customer identity, Faktur Pajak numbers, and e-Faktur export evidence need to stay inside Odoo.

## Core Capabilities

- Indonesian PPN 12% and DPP Nilai Lain tax records.
- PPh 23 service withholding tax record.
- Indonesian taxpayer type on contacts: individual taxpayer, company taxpayer, collector, or non-NPWP retail buyer.
- NPWP 16 / NIK 16 validation for Coretax identity readiness.
- NITKU, official tax name, and official tax address fields on partners.
- Customer invoice tax transaction code.
- Faktur Pajak number and e-Faktur status on invoices.
- NSFP pool management with range, current number, total quota, used quota, and remaining quota.
- Automatic NSFP assignment for posted customer invoices when an active pool is available.
- e-Faktur/Coretax CSV export wizard with FK and OF rows.
- AIRIV OS-ready app identity, iconography, and Apps Store packaging.

## Architecture

```text
Indonesian Tax Master Data
  |
  |-- PPN 12%
  |-- DPP Nilai Lain
  |-- PPh 23
  v
Partner Tax Identity Layer
  |
  |-- taxpayer type
  |-- NPWP/NIK 16 digit
  |-- NITKU
  |-- tax name and address
  v
Invoice Tax Control
  |
  |-- transaction code
  |-- NSFP allocation pool
  |-- Faktur Pajak number
  |-- e-Faktur status
  v
DJP Export Workflow
  |
  |-- date filtered invoices
  |-- FK rows
  |-- OF item rows
  |-- CSV download
```

The module stays native to Odoo. It uses Odoo models, invoice extensions, partner extensions, access rules, XML views, and wizard-based CSV generation without requiring an external tax server.

## Feature & Workflow Automation

### 1. Tax Master Setup

The module installs Indonesian tax records for:

- PPN Keluaran 12%,
- PPN Masukan 12%,
- PPN DPP Nilai Lain effective 11%,
- PPh Pasal 23 service withholding.

### 2. Partner Coretax Identity

Contacts can store:

- Indonesian taxpayer type,
- NPWP 16 / NIK 16,
- NITKU,
- official tax name,
- official tax address.

NPWP/NIK values are validated as 16 numeric digits for applicable taxpayer types.

### 3. NSFP Allocation

Accounting users can maintain DJP NSFP ranges with:

- tax year,
- prefix,
- start serial,
- end serial,
- next serial,
- remaining quota.

Customer invoices can receive sequential Faktur Pajak numbers from the active NSFP pool.

### 4. Invoice e-Faktur Control

Customer invoices store:

- tax transaction code,
- Faktur Pajak number,
- Faktur Pajak date,
- e-Faktur status,
- DPP Nilai Lain flag,
- DPP factor ratio.

### 5. e-Faktur/Coretax Export

The export wizard selects invoices by date range and generates downloadable CSV data with:

- FK invoice rows,
- OF line item rows,
- partner tax identity,
- DPP and PPN amounts,
- updated invoice export status.

## Technical Specifications

| Area | Specification |
| --- | --- |
| Odoo version | 18.0 Community |
| Module name | `airiv_tax_indonesia` |
| Version | 18.0.1.0.0 |
| License | LGPL-3 |
| Author | AIRIV |
| Website | https://airiv.id |
| Repository | https://github.com/arivonto/airiv_tax_indonesia |
| Main models | `airiv.nsfp.range`, `airiv.efaktur.export.wizard`, `account.move`, `res.partner` |
| Tax domain | Indonesian DJP Coretax, e-Faktur, PPN, DPP Nilai Lain, and NSFP operations |
| Export format | DJP e-Faktur/Coretax CSV with FK and OF rows |
| Dependencies | `account`, `base`, `airiv_os_core` |
| Store assets | `static/description/icon.png`, `static/description/banner.png`, `static/description/index.html` |

## Installation Guidance

1. Clone the repository on branch `18.0`.

```bash
git clone --branch 18.0 git@github.com:arivonto/airiv_tax_indonesia.git
```

2. Add the module folder to your Odoo addons path.

```text
airiv_tax_indonesia/airiv_tax_indonesia
```

3. Restart Odoo and update the apps list.

4. Install **Indonesia DJP Coretax & e-Faktur Tax Engine** from Apps.

5. Review installed Indonesian tax records and adjust them to your accounting policy when needed.

6. Fill partner tax identity data before generating invoice export files.

7. Create an active NSFP pool before posting customer invoices that require Faktur Pajak numbers.

## Configuration Checklist

- Confirm Indonesian tax records are installed and available.
- Fill taxpayer type, NPWP/NIK 16 digit, NITKU, tax name, and tax address on relevant partners.
- Create active NSFP range records with correct year, prefix, and serial range.
- Review customer invoice transaction code before assigning NSFP.
- Confirm invoice Faktur Pajak number and e-Faktur status before export.
- Run e-Faktur/Coretax CSV export for a controlled date range.
- Review CSV output before uploading to any official tax system.

## Repository Layout

```text
airiv_tax_indonesia/
  __manifest__.py
  data/
    tax_data.xml
  models/
    account_move.py
    nsfp_range.py
    res_partner.py
  security/
    ir.model.access.csv
  static/description/
    icon.png
    banner.png
    index.html
  views/
    account_move_views.xml
    nsfp_range_views.xml
    res_partner_views.xml
    tax_menu_views.xml
  wizard/
    efaktur_export_wizard.py
    efaktur_export_wizard_views.xml
```

## Contact Info

| Field | Details |
| --- | --- |
| Author | AIRIV |
| Website | https://airiv.id |
| GitHub | https://github.com/arivonto |
| Module repository | https://github.com/arivonto/airiv_tax_indonesia |
| Odoo series | 18.0 |

## Quality Gate

This repository includes an Odoo Apps Store CI audit through GitHub Actions. The audit checks manifest metadata, required store assets, import safety, README presence, and Apps Store packaging readiness on branch `18.0`.
