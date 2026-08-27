# Indonesia DJP Coretax & e-Faktur Tax Compliance (PPN 12%, DPP Nilai Lain, 16-Digit NPWP/NIK)

[![License: LGPL-3](https://img.shields.io/badge/License-LGPL--3-blue.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![Odoo: 18.0 Community](https://img.shields.io/badge/Odoo-18.0%20Community-purple.svg)](https://www.odoo.com)
[![Price: Free ($0.00)](https://img.shields.io/badge/Price-%240.00%20(Free)-green.svg)](https://airiv.id)
[![Target: DJP Coretax](https://img.shields.io/badge/Compliance-DJP%20Coretax%20%26%20e--Faktur-gold.svg)](https://airiv.id)

A comprehensive commercial taxation and VAT compliance engine developed specifically for **Odoo 18.0 Community Edition**. Built to support the latest Directorate General of Taxes (**Direktorat Jenderal Pajak - DJP**) regulations, including **UU HPP No. 7/2021** (statutory PPN 12%), **PMK 136/2023** (16-Digit NPWP & NIK integration), DPP Nilai Lain mechanisms, automated NSFP (Nomor Seri Faktur Pajak) quota pooling, and DJP e-Faktur 4.0 / Coretax CSV batch exports.

---

## Detailed Statutory Features

### 1. Statutory PPN 12% & DPP Nilai Lain Architecture
* **PPN 12% Statutory Rate**: Pre-configured standard sales (Keluaran) and purchase (Masukan) VAT fixtures.
* **DPP Nilai Lain Engine**: Supports transactions utilizing deemed tax bases (such as freight forwarding, logistics, or delivery services) with statutory effective rates:
  $$\text{DPP Nilai Lain} = \text{Gross Amount} \times \frac{11}{12}$$
  $$\text{Effective PPN Payable} = \text{DPP Nilai Lain} \times 12\% = \text{Gross Amount} \times 11\%$$
* **Transaction Code Mapping**: Full support for standard DJP transaction prefixes:
  * `01`: Penyerahan BKP/JKP kepada Pihak Bukan Pemungut PPN.
  * `02`: Penyerahan kepada Pemungut Bendaharawan Pemerintah.
  * `03`: Penyerahan kepada Pemungut BUMN / Badan Usaha Tertentu.
  * `04`: Penyerahan menggunakan DPP Nilai Lain.
  * `05`: Penyerahan Besaran Tertentu (Pasal 9A UU PPN).
  * `07`: Penyerahan yang PPN-nya Tidak Dipungut (Kawasan Berikat).
  * `08`: Penyerahan yang Dibebaskan dari Pengenaan PPN.

### 2. 16-Digit NPWP & NIK Validation (Coretax / PMK 136/2023)
* **WPOP Integration**: Automatic validation of 16-digit Indonesian National Identity Numbers (NIK) functioning as the primary Tax ID for individual taxpayers (*Wajib Pajak Orang Pribadi*).
* **WP Badan & NITKU**: Enforces 16-digit corporate NPWP validation alongside 22-digit Nomor Identitas Tempat Kegiatan Usaha (NITKU) for branch offices.
* **Retail & Non-NPWP Handling**: Supports zero-padded identifiers (`0000000000000000`) for end-consumer transactions.

### 3. NSFP Serial Number Management & Auto-Allocation
* **e-Nofa Allocation Pools**: Register tax serial ranges granted by DJP (Start Serial, End Serial, Year).
* **Sequential Auto-Assignment**: Invoices automatically draw the next sequential NSFP upon invoice validation.
* **Quota Tracking**: Real-time progress tracking of used versus remaining serial quota.

### 4. DJP e-Faktur 4.0 & Coretax CSV Batch Exporter
* **FK (Faktur Pajak Header)**: Header metadata, transaction codes, invoice dates, NPWP, SPPKP names, DPP, and PPN values.
* **LT (Lawan Transaksi)**: Customer tax profile address records.
* **OF (Objek Faktur)**: Line-item product code, unit price, quantity, DPP, and VAT details formatted for direct batch upload into DJP e-Faktur desktop application and Coretax web portal.

---

## Installation & Configuration Guide

1. **Deploy Module**:
   Place `airiv_tax_indonesia` inside your Odoo `custom_addons` directory.

2. **Activate Module**:
   * Navigate to **Apps > Update Apps List**.
   * Search for `Indonesia DJP Coretax & e-Faktur Tax Engine` and click **Activate**.

3. **Configure NSFP Serial Pool**:
   * Open the **Indonesian Taxation** app from the App Drawer.
   * Go to **Configuration > NSFP Serial Pools**.
   * Create a new pool with your e-Nofa decision letter reference, tax year, start serial, and end serial.

4. **Assign Taxes to Products / Invoices**:
   * Apply **PPN Keluaran 12%** or **PPN DPP Nilai Lain** to sales quotations and customer invoices.
   * Post the invoice; the system automatically allocates the next official NSFP.

5. **Export to e-Faktur**:
   * Go to **Faktur Pajak & Coretax > Export e-Faktur CSV**.
   * Select your tax period and click **Generate & Download CSV**.
   * Upload the generated file directly to DJP e-Faktur / Coretax.

---

## Module Specifications

| Specification | Details |
| :--- | :--- |
| **Framework Version** | Odoo 18.0 Community Edition (OWL client & App Drawer compliant) |
| **License** | GNU Lesser General Public License v3.0 (LGPL-3) |
| **Price** | Free ($0.00) |
| **Dependencies** | `account`, `base` |
| **Server Overhead** | Zero (Native ORM, direct CSV stream, no middleware) |
| **DJP Specifications** | UU HPP No. 7/2021, PMK 136/2023, DJP e-Faktur 4.0 |
