
import streamlit as st
import pandas as pd
import sqlite3

# 1. Tetapan Halaman
st.set_page_config(
    page_title="Sistem Rekod Aktiviti Kontinjen Selangor",
    page_icon="🛡️",
    layout="wide"
)

# 2. Pangkalan Data SQLite
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

# 3. Sidebar Input
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/9/99/Flag_of_Selangor.svg", width=100)
st.sidebar.title("KONTINJEN SELANGOR")

st.sidebar.subheader("📌 Tetapan Minggu Laporan")
minggu_laporan = st.sidebar.text_input(
    "Label Minggu / Tarikh", 
    value="04 HINGGA 06 SEPTEMBER 2026"
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
    
    date_time = st.text_input("Tarikh & Masa", placeholder="04 SEP 2026 @ 1900 HRS")
    program = st.text_area("Program / Anjuran", placeholder="Nama program...")
    location = st.text_input("Lokasi Tempat", placeholder="Lokasi...")
    attendance = st.text_input("Anggaran Kehadiran", placeholder="2,000 ORANG")
    
    st.markdown("**VIP / Individu Dikenali:**")
    vip_a = st.text_input("VIP A", placeholder="VIP A")
    vip_b = st.text_input("VIP B", placeholder="VIP B")
    vip_c = st.text_input("VIP C", placeholder="VIP C")
    vip_d = st.text_input("VIP D", placeholder="VIP D")
    
    submitted = st.form_submit_button("💾 Simpan Ke Rekod Database")
    
    if submitted:
        if not date_time or not program:
            st.sidebar.error("⚠️ Sila isi Tarikh/Masa dan Program!")
        else:
            vips_list = [v for v in [vip_a, vip_b, vip_c, vip_d] if v.strip()]
            vips_str = "||".join(vips_list)
            
            cursor.execute("""
                INSERT INTO aktiviti (minggu_tarikh, daerah, tarikh_masa, program, lokasi, kehadiran, vips)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (minggu_laporan, district, date_time, program, location, attendance, vips_str))
            conn.commit()
            st.sidebar.success("✅ Berjaya disimpan!")

# 4. Paparan Utama Laporan
st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0b192c 0%, #1e3a8a 100%); border-top: 5px solid #d10000; border-bottom: 5px solid #ffc700; padding: 15px; border-radius: 8px; color: #ffffff; text-align: center; margin-bottom: 20px;">
        <div style="font-size: 18px; font-weight: 800; text-transform: uppercase;">POLIS DIRAJA MALAYSIA • KONTINJEN SELANGOR</div>
        <div style="font-size: 15px; font-weight: 700; margin-top: 5px;">LAPORAN AKTIVITI MENARIK PERHATIAN</div>
        <div style="font-size: 13px; font-weight: 600; color: #ffc700; margin-top: 5px; text-transform: uppercase;">REKOD MINGGU: {minggu_laporan}</div>
    </div>
""", unsafe_allow_html=True)

query = "SELECT * FROM aktiviti WHERE minggu_tarikh = ?"
df_db = pd.read_sql_query(query, conn, params=(minggu_laporan,))

col_a, col_b, col_c = st.columns([2, 1, 1])
with col_a:
    st.write(f"📊 **Jumlah Rekod:** {len(df_db)} aktiviti")
with col_b:
    if not df_db.empty:
        csv = df_db.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Muat Turun CSV", csv, f"Rekod_Aktiviti_{minggu_laporan}.csv", "text/csv")
with col_c:
    if not df_db.empty:
        if st.button("🗑️ Padam Rekod"):
            cursor.execute("DELETE FROM aktiviti WHERE minggu_tarikh = ?", (minggu_laporan,))
            conn.commit()
            st.rerun()

st.markdown("---")

if df_db.empty:
    st.info(f"📌 Tiada rekod disimpan untuk '{minggu_laporan}'. Sila masukkan data di sebelah kiri.")
else:
    grouped = df_db.groupby("daerah", sort=False)
    global_bil = 1
    
    # Bina HTML tanpa ruang kosong pembawa ralat
    rows_html = ""
    for district_name, group in grouped:
        rows_html += f'<tr><td colspan="5" style="background: linear-gradient(90deg, #8b0000 0%, #d10000 100%); color: #ffffff; text-align: left; font-weight: 800; font-size: 13px; padding: 8px 12px; text-transform: uppercase; border-left: 6px solid #ffc700;">📍 {district_name}</td></tr>'
        for _, row in group.iterrows():
            vips = row['vips'].split("||") if row['vips'] else []
            vip_formatted = "<br>".join([f"<b>{chr(65+i)})</b> {v}" for i, v in enumerate(vips)]) if vips else "-"
            
            rows_html += f'<tr><td style="text-align: center; font-weight: bold; border: 1px solid #cbd5e1; padding: 8px;">{global_bil}</td><td style="border: 1px solid #cbd5e1; padding: 8px;"><b>{row["tarikh_masa"]}</b></td><td style="border: 1px solid #cbd5e1; padding: 8px;">{row["program"]}</td><td style="border: 1px solid #cbd5e1; padding: 8px;"><b>{row["lokasi"]}</b><br><div style="display: inline-block; background: #f1f5f9; border-left: 3px solid #1e3a8a; padding: 2px 6px; font-weight: 700; font-size: 11px; margin-top: 5px;">KEHADIRAN : {row["kehadiran"]}</div></td><td style="border: 1px solid #cbd5e1; padding: 8px;">{vip_formatted}</td></tr>'
            global_bil += 1

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ font-family: sans-serif; margin: 0; padding: 0; }}
        table {{ width: 100%; border-collapse: collapse; background: #ffffff; font-size: 12px; }}
        th {{ background-color: #1e3a8a; color: #ffffff; text-align: center; font-weight: 700; padding: 10px; border: 1px solid #1e3a8a; text-transform: uppercase; }}
    </style>
    </head>
    <body>
        <table>
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
                {rows_html}
            </tbody>
        </table>
    </body>
    </html>
    """
    
    # Rendera HTML terus menggunakan komponen rasmi tanpa halangan parser Markdown
    st.components.v1.html(full_html, height=500, scrolling=True)

    st.caption("Disediakan Oleh: Bahagian E9 Cawangan Khas IPK Selangor")
