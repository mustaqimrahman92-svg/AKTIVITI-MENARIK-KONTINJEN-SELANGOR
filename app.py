import streamlit as st
import pandas as pd

# Tetapan Halaman
st.set_page_config(page_title="Aktiviti Menarik Kontinjen Selangor", layout="wide")

# Inisialisasi Data Simpanan (Session State)
if "events" not in st.session_state:
    st.session_state.events = []

# CSS Khas untuk Reka Bentuk Jadual Rasmi & Cetakan
st.markdown("""
    <style>
    .report-title {
        text-align: center;
        font-weight: bold;
        font-size: 20px;
        margin-bottom: 20px;
        text-transform: uppercase;
    }
    .district-header {
        background-color: #E3D3C4;
        color: #000;
        text-align: center;
        font-weight: bold;
        font-size: 14px;
        padding: 6px;
        text-transform: uppercase;
        border: 1px solid #000;
    }
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 15px;
    }
    .custom-table th, .custom-table td {
        border: 1px solid #000;
        padding: 8px;
        vertical-align: top;
        font-size: 12px;
    }
    .custom-table th {
        background-color: #B4C6E7;
        text-align: center;
        font-weight: bold;
    }
    
    /* Format Cetakan (Print Friendly) */
    @media print {
        [data-testid="stSidebar"] { display: none; }
        .stButton { display: none; }
        header { display: none; }
        footer { display: none; }
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------
# SIDEBAR: BORANG INPUT DATA
# ------------------------------------
st.sidebar.header("Borang Input Aktiviti")

with st.sidebar.form("event_form", clear_on_submit=True):
    district = st.selectbox("Daerah / IPD", [
        "SHAH ALAM", "SEPANG", "SUBANG JAYA", "SERDANG", 
        "AMPANG JAYA", "PETALING JAYA", "KLANG UTARA", 
        "KLANG SELATAN", "KUALA SELANGOR", "HULU SELANGOR", 
        "SABAK BERNAM", "KUALA LANGAT", "KAJANG"
    ])
    
    date_time = st.text_input("Tarikh & Jam", value="04 SEP 2026 @ 1900 HRS HINGGA SELESAI")
    program = st.text_area("Program / Anjuran", value="KONSERT AKHIR KITA ASLI BATTLE OF THE BAND - PEMADIAM NEGERI SELANGOR")
    location = st.text_input("Lokasi", value="AUDITORIUM DEWAN JUBLI PERAK SUK")
    attendance = st.text_input("Kehadiran", value="2000 ORANG")
    
    st.markdown("**Maklumat VIP / Individu Dikenali:**")
    vip_a = st.text_input("VIP A", value="DATO' SERI ANWAR BIN IBRAHIM - PERDANA MENTERI MALAYSIA")
    vip_b = st.text_input("VIP B", value="DATO' SERI AMIRUDIN BIN SHARI - MENTERI BESAR SELANGOR")
    vip_c = st.text_input("VIP C", value="")
    vip_d = st.text_input("VIP D", value="")
    
    submitted = st.form_submit_button("Tambah Aktiviti")
    
    if submitted:
        vips = [v for v in [vip_a, vip_b, vip_c, vip_d] if v.strip()]
        st.session_state.events.append({
            "district": district,
            "date_time": date_time,
            "program": program,
            "location": location,
            "attendance": attendance,
            "vips": vips
        })
        st.sidebar.success("Aktiviti berjaya ditambah!")

if st.sidebar.button("Kosongkan Semua Data"):
    st.session_state.events = []
    st.rerun()

# ------------------------------------
# PAPARAN UTAMA (JADUAL LAPORAN)
# ------------------------------------
title_date = st.text_input("Tajuk Laporan / Tarikh", value="4 HINGGA 6 SEPT 2026 (JUMAAT HINGGA AHAD)")

st.markdown(f'<div class="report-title">AKTIVITI MENARIK PERHATIAN<br>{title_date}</div>', unsafe_allow_html=True)

if not st.session_state.events:
    st.info("Tiada aktiviti dimasukkan lagi. Sila guna borang di sebelah kiri untuk menambah data.")
else:
    # Susun data mengikut daerah
    df_events = pd.DataFrame(st.session_state.events)
    grouped = df_events.groupby("district", sort=False)
    
    global_bil = 1
    
    # HTML Header Jadual
    table_html = """
    <table class="custom-table">
        <thead>
            <tr>
                <th style="width: 5%;">BIL.</th>
                <th style="width: 20%;">TARIKH @ JAM</th>
                <th style="width: 25%;">PROGRAM / ANJURAN</th>
                <th style="width: 25%;">LOKASI / KEHADIRAN</th>
                <th style="width: 25%;">VIP / INDIVIDU DIKENALI</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for district, group in grouped:
        # Header Daerah
        table_html += f"""
        <tr>
            <td colspan="5" class="district-header">{district}</td>
        </tr>
        """
        for _, row in group.iterrows():
            vip_formatted = "<br>".join([f"{chr(65+i)}) {v}" for i, v in enumerate(row['vips'])])
            
            table_html += f"""
            <tr>
                <td style="text-align: center;">{global_bil}</td>
                <td>{row['date_time']}</td>
                <td>{row['program']}</td>
                <td><b>{row['location']}</b><br><br>KEHADIRAN : {row['attendance']}</td>
                <td>{vip_formatted}</td>
            </tr>
            """
            global_bil += 1
            
    table_html += "</tbody></table>"
    
    # Paparkan Jadual
    st.markdown(table_html, unsafe_allow_html=True)

    st.caption("Petua: Gunakan fungsi **Ctrl + P** (atau Cmd + P pada Mac) di pelayar web anda untuk cetak/simpan sebagai PDF.")
