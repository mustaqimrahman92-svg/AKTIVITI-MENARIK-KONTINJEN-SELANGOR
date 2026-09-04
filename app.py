import streamlit as st
import pandas as pd
import sqlite3

# ------------------------------------
# 1. TETAPAN HALAMAN
# ------------------------------------
st.set_page_config(
    page_title="Aktiviti Menarik Perhatian - Kontinjen Selangor",
    page_icon="📋",
    layout="wide"
)

# Inisialisasi Pangkalan Data
conn = sqlite3.connect("rekod_aktiviti_selangor.db", check_same_thread=False)
cursor = conn.cursor()

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
# 2. SIDEBAR: BORANG INPUT & TETAPAN
# ------------------------------------
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/9/99/Flag_of_Selangor.svg", width=90)
st.sidebar.title("KONTINJEN SELANGOR")

st.sidebar.subheader("📌 Tajuk Laporan Mingguan")
minggu_laporan = st.sidebar.text_input(
    "Tarikh Laporan", 
    value="4 HINGGA 6 SEPT 2026 (JUMAAT HINGGA AHAD)"
)

st.sidebar.markdown("---")
st.sidebar.subheader("📝 Masukkan Data Aktiviti")

with st.sidebar.form("event_form", clear_on_submit=True):
    district = st.selectbox("Daerah / IPD", [
        "SHAH ALAM", "SEPANG", "SUBANG JAYA", "SERDANG", 
        "AMPANG JAYA", "PETALING JAYA", "KLANG UTARA", 
        "KLANG SELATAN", "KUALA SELANGOR", "HULU SELANGOR", 
        "SABAK BERNAM", "KUALA LANGAT", "KAJANG"
    ])
    
    date_time = st.text_input("Tarikh & Jam", placeholder="04 SEP 2026 @ 1900 HRS HINGGA SELESAI")
    program = st.text_area("Program / Anjuran", placeholder="NAMA PROGRAM\n\nPENGANJUR")
    location = st.text_input("Lokasi Tempat", placeholder="AUDITORIUM DEWAN JUBLI PERAK SUK")
    attendance = st.text_input("Kehadiran", placeholder="2000 ORANG")
    
    st.markdown("**VIP / Individu Dikenali (Format: Nama - Jawatan):**")
    vip_a = st.text_input("VIP A", placeholder="DATO' SERI ANWAR BIN IBRAHIM - PERDANA MENTERI MALAYSIA")
    vip_b = st.text_input("VIP B", placeholder="DATO' SERI AMIRUDIN BIN SHARI - MENTERI BESAR SELANGOR")
    vip_c = st.text_input("VIP C", placeholder="VIP C")
    vip_d = st.text_input("VIP D", placeholder="VIP D")
    
    submitted = st.form_submit_button("💾 Simpan Aktiviti")
    
    if submitted:
        if not date_time or not program:
            st.sidebar.error("⚠️ Sila isi Tarikh/Jam dan Program!")
        else:
            vips_list = [v for v in [vip_a, vip_b, vip_c, vip_d] if v.strip()]
            vips_str = "||".join(vips_list)
            
            cursor.execute("""
                INSERT INTO aktiviti (minggu_tarikh, daerah, tarikh_masa, program, lokasi, kehadiran, vips)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (minggu_laporan, district, date_time, program, location, attendance, vips_str))
            conn.commit()
            st.sidebar.success("✅ Berjaya disimpan!")

# ------------------------------------
# 3. KAWALAN DATA UTAMA
# ------------------------------------
query = "SELECT * FROM aktiviti WHERE minggu_tarikh = ?"
df_db = pd.read_sql_query(query, conn, params=(minggu_laporan,))

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.write(f"📊 **Jumlah Rekod:** {len(df_db)} aktiviti")
with col2:
    if not df_db.empty:
        csv = df_db.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Muat Turun CSV (Excel)", csv, f"Laporan_{minggu_laporan}.csv", "text/csv")
with col3:
    if not df_db.empty:
        if st.button("🗑️ Padam Rekod Minggu Ini"):
            cursor.execute("DELETE FROM aktiviti WHERE minggu_tarikh = ?", (minggu_laporan,))
            conn.commit()
            st.rerun()

st.markdown("---")

# ------------------------------------
# 4. PAPARAN LAPORAN (IKUT PDF)
# ------------------------------------
if df_db.empty:
    st.info(f"📌 Tiada rekod disimpan untuk '{minggu_laporan}'. Masukkan data melalui borang di sebelah kiri.")
else:
    grouped = df_db.groupby("daerah", sort=False)
    global_bil = 1
    
    rows_html = ""
    for district_name, group in grouped:
        # Header IPD / Daerah (Warna Peach/Oren Lembut seperti dalam dokumen)
        rows_html += f"""
        <tr>
            <td colspan="5" style="background-color: #fce4d6; color: #000000; font-weight: bold; text-align: center; font-size: 11px; padding: 4px; border: 1px solid #000000; text-transform: uppercase;">
                {district_name}
            </td>
        </tr>
        """
        for _, row in group.iterrows():
            # Format Senarai VIP
            vips = row['vips'].split("||") if row['vips'] else []
            vip_formatted_list = []
            for i, v in enumerate(vips):
                parts = v.split("-", 1)
                if len(parts) == 2:
                    name_part = parts[0].strip()
                    title_part = parts[1].strip()
                    vip_formatted_list.append(f"<b>{chr(65+i)}) {name_part}</b><br>&nbsp;&nbsp;&nbsp;&nbsp;- {title_part}")
                else:
                    vip_formatted_list.append(f"<b>{chr(65+i)}) {v.strip()}</b>")
            
            vip_final_str = "<br><br>".join(vip_formatted_list) if vip_formatted_list else "-"
            
            # Format Program & Lokasi
            program_str = row['program'].replace('\n', '<br>')
            lokasi_str = f"{row['lokasi']}<br><br><b>KEHADIRAN : {row['kehadiran']}</b>" if row['kehadiran'] else row['lokasi']
            
            rows_html += f"""
            <tr>
                <td style="text-align: center; vertical-align: top; border: 1px solid #000000; padding: 6px; font-size: 11px;">{global_bil}.</td>
                <td style="vertical-align: top; border: 1px solid #000000; padding: 6px; font-size: 11px;">{row['tarikh_masa']}</td>
                <td style="vertical-align: top; border: 1px solid #000000; padding: 6px; font-size: 11px;">{program_str}</td>
                <td style="vertical-align: top; border: 1px solid #000000; padding: 6px; font-size: 11px;">{lokasi_str}</td>
                <td style="vertical-align: top; border: 1px solid #000000; padding: 6px; font-size: 11px;">{vip_final_str}</td>
            </tr>
            """
            global_bil += 1

    # Kira dinamik tinggi container HTML supaya muat skrin
    dynamic_height = max(600, len(df_db) * 160 + len(grouped) * 40 + 100)

    pdf_style_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{
            font-family: Arial, Helvetica, sans-serif;
            margin: 0;
            padding: 10px;
            background-color: #ffffff;
        }}
        .header-title {{
            text-align: center;
            font-weight: bold;
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 2px;
        }}
        .header-subtitle {{
            text-align: center;
            font-weight: bold;
            font-size: 12px;
            text-transform: uppercase;
            margin-bottom: 12px;
            text-decoration: underline;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            background-color: #ffffff;
        }}
        th {{
            background-color: #8ea9db;
            color: #000000;
            font-weight: bold;
            font-size: 11px;
            padding: 6px;
            border: 1px solid #000000;
            text-align: center;
            text-transform: uppercase;
        }}
    </style>
    </head>
    <body>

        <div class="header-title">AKTIVITI MENARIK PERHATIAN</div>
        <div class="header-subtitle">{minggu_laporan}</div>

        <table>
            <thead>
                <tr>
                    <th style="width: 4%;">BIL.</th>
                    <th style="width: 18%;">TARIKH @ JAM</th>
                    <th style="width: 28%;">PROGRAM / ANJURAN</th>
                    <th style="width: 25%;">LOKASI / KEHADIRAN</th>
                    <th style="width: 25%;">VIP / INDIVIDU DIKENALI</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>

    </body>
    </html>
    """
    
    # Render Paparan HTML Rasmi
    st.components.v1.html(pdf_style_html, height=dynamic_height, scrolling=True)
