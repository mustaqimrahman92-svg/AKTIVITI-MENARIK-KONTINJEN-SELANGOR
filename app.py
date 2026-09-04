import streamlit as st
import pandas as pd
import sqlite3

# ------------------------------------
# 1. TETAPAN HALAMAN & TEMA
# ------------------------------------
st.set_page_config(
    page_title="Sistem Rekod Aktiviti Kontinjen Selangor",
    page_icon="🛡️",
    layout="wide"
)

# Inisialisasi Pangkalan Data SQLite (Simpanan Tempatan)
conn = sqlite3.connect("rekod_aktiviti_selangor.db", check_same_thread=False)
cursor = conn.cursor()

# Cipta jadual pangkalan data jika belum wujud
cursor.execute("""
    CREATE TABLE IF NOT EXISTS aktiviti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        minggu_tarikh TEXT,
        daerah TEXT,
        tarikh_masa TEXT,
        program TEXT,
        lokasi TEXT,
        kehadiran TEXT,
        vips TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

# ------------------------------------
# 2. GAYA CSS TEMA SELANGOR & PDRM
# ------------------------------------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Header Utama Laporan Selangor */
    .selangor-header-box {
        background: linear-gradient(135deg, #0b192c 0%, #1e3a8a 100%);
        border-top: 5px solid #d10000;
        border-bottom: 5px solid #ffc700;
        padding: 20px;
        border-radius: 8px;
        color: #ffffff;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    .selangor-header-title {
        font-size: 20px;
        font-weight: 800;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .selangor-header-subtitle {
        font-size: 14px;
        font-weight: 600;
        color: #ffc700;
        margin-top: 5px;
        text-transform: uppercase;
    }

    /* Jadual Laporan Rasmi */
    .custom-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .custom-table th {
        background-color: #1e3a8a;
        color: #ffffff;
        text-align: center;
        font-weight: 700;
        font-size: 12px;
        padding: 10px;
        border: 1px solid #1e3a8a;
        text-transform: uppercase;
    }
    
    .custom-table td {
        border: 1px solid #cbd5e1;
        padding: 10px;
        vertical-align: top;
        font-size: 12px;
        color: #1e293b;
    }

    /* Pengepala Daerah / IPD */
    .district-header {
        background: linear-gradient(90deg, #8b0000 0%, #d10000 100%);
        color: #ffffff !important;
        text-align: left;
        font-weight: 800;
        font-size: 13px;
        padding: 8px 14px !important;
        text-transform: uppercase;
        border-left: 6px solid #ffc700 !important;
    }

    .badge-attendance {
        display: inline-block;
        background-color: #f1f5f9;
        border-left: 3px solid #1e3a8a;
        padding: 4px 8px;
        font-weight: 700;
        font-size: 11px;
        margin-top: 6px;
        color: #0f172a;
    }

    /* Tetapan Cetakan (Print Friendly) */
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
# 3. SIDEBAR: BORANG INPUT & TETAPAN
# ------------------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/9/99/Flag_of_Selangor.svg", width=100)
st.sidebar.title("KONTINJEN SELANGOR")

# Pilihan Label Minggu
st.sidebar.subheader("📌 Tetapan Minggu Laporan")
minggu_laporan = st.sidebar.text_input(
    "Label Minggu / Tarikh", 
    value="04 HINGGA 06 SEPTEMBER 2026",
    help="Ubah label ini untuk mengumpul atau melihat rekod mengikut minggu tertentu"
)

st.sidebar.markdown("---")
st.sidebar.subheader("📝 Borang Input Aktiviti")

with st.sidebar.form("event_form", clear_on_submit=True):
    district = st.selectbox("Daerah / IPD", [
        "IPD SHAH ALAM", "IPD SEPANG", "IPD SUBANG JAYA", "IPD SERDANG", 
        "IPD AMPANG JAYA", "IPD PETALING JAYA", "IPD KLANG UTARA", 
        "IPD KLANG SELATAN", "IPD KUALA SELANGOR", "IPD HULU SELANGOR", 
        "IPD SABAK BERNAM", "IPD KUALA LANGAT", "IPD KAJANG"
    ])
    
    date_time = st.text_input("Tarikh & Masa", placeholder="Contoh: 04 SEP 2026 @ 1900 HRS")
    program = st.text_area("Program / Anjuran", placeholder="Nama program dan penganjur...")
    location = st.text_input("Lokasi Tempat", placeholder="Lokasi program...")
    attendance = st.text_input("Anggaran Kehadiran", placeholder="Contoh: 2,000 ORANG")
    
    st.markdown("**VIP / Individu Dikenali:**")
    vip_a = st.text_input("VIP A", placeholder="Nama & Jawatan VIP A")
    vip_b = st.text_input("VIP B", placeholder="Nama & Jawatan VIP B")
    vip_c = st.text_input("VIP C", placeholder="Nama & Jawatan VIP C")
    vip_d = st.text_input("VIP D", placeholder="Nama & Jawatan VIP D")
    
    submitted = st.form_submit_button("💾 Simpan Ke Rekod Database")
    
    if submitted:
        if not date_time or not program:
            st.sidebar.error("⚠️ Sila isi sekurang-kurangnya Tarikh/Masa dan Program!")
        else:
            vips_list = [v for v in [vip_a, vip_b, vip_c, vip_d] if v.strip()]
            vips_str = "||".join(vips_list)
            
            # Simpan rekod ke dalam SQLite Database
            cursor.execute("""
                INSERT INTO aktiviti (minggu_tarikh, daerah, tarikh_masa, program, lokasi, kehadiran, vips)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (minggu_laporan, district, date_time, program, location, attendance, vips_str))
            conn.commit()
            
            st.sidebar.success("✅ Aktiviti berjaya disimpan ke rekod database!")

# ------------------------------------
# 4. PAPARAN UTAMA & JADUAL LAPORAN
# ------------------------------------
st.markdown(f"""
    <div class="selangor-header-box">
        <div class="selangor-header-title">POLIS DIRAJA MALAYSIA • KONTINJEN SELANGOR</div>
        <div style="font-size: 16px; font-weight: 700; margin-top: 5px;">LAPORAN AKTIVITI MENARIK PERHATIAN</div>
        <div class="selangor-header-subtitle">REKOD MINGGU: {minggu_laporan}</div>
    </div>
""", unsafe_allow_html=True)

# Ambil data daripada database berdasarkan minggu_tarikh
query = "SELECT * FROM aktiviti WHERE minggu_tarikh = ?"
df_db = pd.read_sql_query(query, conn, params=(minggu_laporan,))

# Baris Kawalan Data & Eksport
col_a, col_b, col_c = st.columns([2, 1, 1])

with col_a:
    st.write(f"📊 **Jumlah Rekod Minggu Ini:** {len(df_db)} aktiviti")

with col_b:
    if not df_db.empty:
        csv = df_db.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Muat Turun CSV (Excel)",
            data=csv,
            file_name=f"Rekod_Aktiviti_{minggu_laporan}.csv",
            mime="text/csv"
        )

with col_c:
    if not df_db.empty:
        if st.button("🗑️ Padam Rekod Minggu Ini"):
            cursor.execute("DELETE FROM aktiviti WHERE minggu_tarikh = ?", (minggu_laporan,))
            conn.commit()
            st.rerun()

st.markdown("---")

# Paparan Jadual
if df_db.empty:
    st.info(f"📌 **Tiada rekod disimpan untuk '{minggu_laporan}'.** Masukkan maklumat melalui borang di sebelah kiri dan tekan 'Simpan Ke Rekod Database'.")
else:
    grouped = df_db.groupby("daerah", sort=False)
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
            vips = row['vips'].split("||") if row['vips'] else []
            vip_formatted = "<br>".join([f"<b>{chr(65+i)})</b> {v}" for i, v in enumerate(vips)]) if vips else "-"
            
            table_html += f"""
            <tr>
                <td style="text-align: center; font-weight: bold;">{global_bil}</td>
                <td><b>{row['tarikh_masa']}</b></td>
                <td>{row['program']}</td>
                <td>
                    <b>{row['lokasi']}</b><br>
                    <div class="badge-attendance">KEHADIRAN : {row['kehadiran']}</div>
                </td>
                <td>{vip_formatted}</td>
            </tr>
            """
            global_bil += 1
            
    table_html += "</tbody></table>"
    
    # Render jadual HTML dengan kebenaran unsafe_allow_html=True
    st.markdown(table_html, unsafe_allow_html=True)

    # Ruangan Pengesahan Pegawai
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.caption("Disediakan Oleh: Pusat Kawalan Kontinjen (CCC) Selangor")
    with col2:
        st.caption("Disahkan Oleh: Pegawai Bertugas Kontinjen Selangor")
