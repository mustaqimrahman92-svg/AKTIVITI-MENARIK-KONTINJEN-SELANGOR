import streamlit as st
import pandas as pd

# ------------------------------------
# TETAPAN HALAMAN & TEMA
# ------------------------------------
st.set_page_config(
    page_title="Sistem Aktiviti Menarik Kontinjen Selangor",
    page_icon="🛡️",
    layout="wide"
)

# Inisialisasi Data Simpanan (Session State)
if "events" not in st.session_state:
    st.session_state.events = []

# ------------------------------------
# CSS KHAS: TEMA SELANGOR & PDRM
# ------------------------------------
st.markdown("""
    <style>
    /* Latar Belakang & Tipografi */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Header Laporan Selangor */
    .selangor-header-box {
        background: linear-gradient(135deg, #0b192c 0%, #1e3a8a 100%);
        border-top: 5px solid #d10000;
        border-bottom: 5px solid #ffc700;
        padding: 20px;
        border-radius: 8px;
        color: #ffffff;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 25px;
    }
    
    .selangor-header-title {
        font-size: 22px;
        font-weight: 800;
        letter-spacing: 1px;
        color: #ffffff;
        margin: 0;
        text-transform: uppercase;
    }
    
    .selangor-header-subtitle {
        font-size: 15px;
        font-weight: 600;
        color: #ffc700;
        margin-top: 5px;
        text-transform: uppercase;
    }

    /* Jadual Rasmi */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        background-color: #ffffff;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .custom-table th {
        background-color: #1e3a8a;
        color: #ffffff;
        text-align: center;
        font-weight: 700;
        font-size: 13px;
        padding: 10px;
        border: 1px solid #1e3a8a;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .custom-table td {
        border: 1px solid #cbd5e1;
        padding: 10px;
        vertical-align: top;
        font-size: 12px;
        color: #1e293b;
    }

    /* Header IPD / Daerah (Inspirasi Bendera Selangor) */
    .district-header {
        background: linear-gradient(90deg, #8b0000 0%, #d10000 100%);
        color: #ffffff !important;
        text-align: left;
        font-weight: 800;
        font-size: 13px;
        padding: 8px 15px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-left: 6px solid #ffc700 !important;
    }

    .badge-attendance {
        display: inline-block;
        background-color: #f1f5f9;
        border-left: 3px solid #1e3a8a;
        padding: 4px 8px;
        font-weight: 700;
        font-size: 11px;
        margin-top: 8px;
        color: #0f172a;
    }

    /* Format Cetakan (Print Friendly) */
    @media print {
        [data-testid="stSidebar"] { display: none; }
        .stButton { display: none; }
        header { display: none; }
        footer { display: none; }
        .selangor-header-box {
            background: #1e3a8a !important;
            color: #ffffff !important;
            -webkit-print-color-adjust: exact;
        }
        .district-header {
            background: #8b0000 !important;
            color: #ffffff !important;
            -webkit-print-color-adjust: exact;
        }
        .custom-table th {
            background-color: #1e3a8a !important;
            color: #ffffff !important;
            -webkit-print-color-adjust: exact;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------
# SIDEBAR: BORANG INPUT DATA
# ------------------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/9/99/Flag_of_Selangor.svg", width=120)
st.sidebar.title("KONTINJEN SELANGOR")
st.sidebar.subheader("Borang Input Aktiviti")

with st.sidebar.form("event_form", clear_on_submit=True):
    district = st.selectbox("Daerah / IPD", [
        "IPD SHAH ALAM", "IPD SEPANG", "IPD SUBANG JAYA", "IPD SERDANG", 
        "IPD AMPANG JAYA", "IPD PETALING JAYA", "IPD KLANG UTARA", 
        "IPD KLANG SELATAN", "IPD KUALA SELANGOR", "IPD HULU SELANGOR", 
        "IPD SABAK BERNAM", "IPD KUALA LANGAT", "IPD KAJANG"
    ])
    
    date_time = st.text_input("Tarikh & Masa", placeholder="Contoh: 04 SEP 2026 @ 1900 HRS HINGGA SELESAI")
    program = st.text_area("Program / Anjuran", placeholder="Nama program dan penganjur...")
    location = st.text_input("Lokasi Tempat", placeholder="Lokasi berlangsung...")
    attendance = st.text_input("Anggaran Kehadiran", placeholder="Contoh: 2,000 ORANG")
    
    st.markdown("---")
    st.markdown("**Maklumat VIP / Individu Dikenali:**")
    vip_a = st.text_input("VIP A", placeholder="Nama & Jawatan VIP A")
    vip_b = st.text_input("VIP B", placeholder="Nama & Jawatan VIP B")
    vip_c = st.text_input("VIP C", placeholder="Nama & Jawatan VIP C")
    vip_d = st.text_input("VIP D", placeholder="Nama & Jawatan VIP D")
    
    submitted = st.form_submit_button("➕ Tambah Rekod Aktiviti")
    
    if submitted:
        if not date_time or not program:
            st.sidebar.error("⚠️ Sila isi sekurang-kurangnya Tarikh & Masa dan Program!")
        else:
            vips = [v for v in [vip_a, vip_b, vip_c, vip_d] if v.strip()]
            st.session_state.events.append({
                "district": district,
                "date_time": date_time,
                "program": program,
                "location": location,
                "attendance": attendance,
                "vips": vips
            })
            st.sidebar.success("✅ Aktiviti berjaya ditambah!")

if st.sidebar.button("🗑️ Kosongkan Senarai Data"):
    st.session_state.events = []
    st.rerun()

# ------------------------------------
# PAPARAN UTAMA (LAPORAN RASMI)
# ------------------------------------
title_date = st.text_input("Tarikh / Tempoh Laporan", value="04 HINGGA 06 SEPTEMBER 2026")

# Banner Header Laporan
st.markdown(f"""
    <div class="selangor-header-box">
        <div class="selangor-header-title">POLIS DIRAJA MALAYSIA • KONTINJEN SELANGOR</div>
        <div style="font-size: 18px; font-weight: 700; margin-top: 8px;">LAPORAN AKTIVITI MENARIK PERHATIAN</div>
        <div class="selangor-header-subtitle">TARIKH: {title_date}</div>
    </div>
""", unsafe_allow_html=True)

if not st.session_state.events:
    st.info("📌 **Tiada Aktiviti Dimasukkan.** Sila gunakan borang di sebelah kiri (Sidebar) untuk mula memasukkan maklumat aktiviti harian/mingguan.")
else:
    df_events = pd.DataFrame(st.session_state.events)
    grouped = df_events.groupby("district", sort=False)
    
    global_bil = 1
    
    table_html = """
    <table class="custom-table">
        <thead>
            <tr>
                <th style="width: 5%;">BIL.</th>
                <th style="width: 18%;">TARIKH @ JAM</th>
                <th style="width: 27%;">PROGRAM / ANJURAN</th>
                <th style="width: 25%;">LOKASI / KEHADIRAN</th>
                <th style="width: 25%;">VIP / INDIVIDU DIKENALI</th>
            </tr>
        </thead>
        <tbody>
    """
    
    for district_name, group in grouped:
        table_html += f"""
        <tr>
            <td colspan="5" class="district-header">📍 {district_name}</td>
        </tr>
        """
        for _, row in group.iterrows():
            vip_formatted = "<br>".join([f"<b>{chr(65+i)})</b> {v}" for i, v in enumerate(row['vips'])]) if row['vips'] else "-"
            
            table_html += f"""
            <tr>
                <td style="text-align: center; font-weight: bold;">{global_bil}</td>
                <td><b>{row['date_time']}</b></td>
                <td>{row['program']}</td>
                <td>
                    <b>{row['location']}</b><br>
                    <div class="badge-attendance">KEHADIRAN : {row['attendance']}</div>
                </td>
                <td>{vip_formatted}</td>
            </tr>
            """
            global_bil += 1
            
    table_html += "</tbody></table>"
    
    st.markdown(table_html, unsafe_allow_html=True)

    # Ruangan Tandatangan / Pengesahan
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.caption("Disediakan Oleh: Pusat Kawalan Kontinjen (CCC) Selangor")
    with col2:
        st.caption("Disahkan Oleh: Pegawai Bertugas Kontinjen Selangor")

    st.caption("💡 *Gunakan Ctrl + P (pada komputer) atau fungsi Print pada iPhone untuk menyimpan laporan ini sebagai PDF.*")
