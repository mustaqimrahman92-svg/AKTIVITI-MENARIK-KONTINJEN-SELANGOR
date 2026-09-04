# PROMPT: Web Application & Data Entry Form for Selangor Contingent "Aktiviti Menarik Perhatian" Report Generator

## Objective
Build a web-based reporting system and data entry form tailored for the Royal Malaysia Police (PDRM) Selangor Contingent. The app should allow officers to input scheduled events/activities, group them automatically by district/IPD, and generate a standardized, clean report ready for printing or exporting to PDF.

---

## 1. Structure & Fields for Data Entry Form (Borang Input)

The data entry form must strictly include the following official items/fields per event entry:

1. **Daerah / IPD (Police District Header):**
   - Field Type: Dropdown Select
   - Options (Selangor IPDs): SHAH ALAM, SEPANG, SUBANG JAYA, SERDANG, AMPANG JAYA, PETALING JAYA, KLANG UTARA, KLANG SELATAN, KUALA SELANGOR, HULU SELANGOR, SABAK BERNAM, KUALA LANGAT, KAJANG.

2. **Tarikh & Masa (Date & Time Column):**
   - Field Type: Text Input / Date-Time Picker
   - Placeholder Example: "04 SEP 2026 @ 1900 HRS HINGGA SELESAI"

3. **Program / Anjuran (Program & Organizer Column):**
   - Field Type: Multi-line Text Area
   - Input Structure:
     - Program Name (e.g., "KONSERT AKHIR KITA ASLI BATTLE OF THE BAND")
     - Organizer Name (e.g., "PEMADIAM NEGERI SELANGOR")

4. **Lokasi & Kehadiran (Location & Attendance Column):**
   - Location Name/Address (Text Input, e.g., "AUDITORIUM DEWAN JUBLI PERAK SUK")
   - Attendance / Target Audience (Text Input, e.g., "2000 ORANG")

5. **VIP / Individu Dikenali (Key Figures / VIPs Column):**
   - Dynamic List Input (Allow adding multiple VIPs per event: A, B, C, D...)
   - Sub-fields for each VIP:
     - VIP Name (e.g., "DATO' SERI ANWAR BIN IBRAHIM")
     - VIP Title / Designation (e.g., "PERDANA MENTERI MALAYSIA")

---

## 2. Table Output & Layout Requirements

1. **Overall Report Header:**
   - Title: `AKTIVITI MENARIK PERHATIAN`
   - Date Subtitle: Customizable text input (e.g., `4 HINGGA 6 SEPT 2026 (JUMAAT HINGGA AHAD)`)

2. **Table Header Columns:**
   - `BIL.` (Auto-incremented integer across all events)
   - `TARIKH @ JAM`
   - `PROGRAM / ANJURAN`
   - `LOKASI / KEHADIRAN`
   - `VIP / INDIVIDU DIKENALI`

3. **District Banners & Grouping:**
   - Events must be automatically grouped under their respective District / IPD banner (e.g., `SHAH ALAM`, `SEPANG`).
   - The District banner must span across all 5 table columns (`colspan="5"`) with a distinct background highlight (soft beige / pastel brown `#E3D3C4`).

4. **Formatting Rules for Output Cells:**
   - **Lokasi & Kehadiran Cell:** Format as `[LOCATION NAME]` in bold, followed by two line breaks, then `KEHADIRAN : [ATTENDANCE COUNT]`.
   - **VIP Cell:** Render as an ordered bulleted list using letters (A), B), C), D)...) with the VIP Name on top and Title underneath.

---

## 3. Functionalities

- **Form Reset & Clear:** Option to add new entries, edit existing entries, or clear all entries.
- **Export / Print View:** Include a print stylesheet (`@media print`) or PDF download option to render a clean, high-resolution official document matching police report standards.
