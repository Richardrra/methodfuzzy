import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ==================================================
# KONFIGURASI HALAMAN
# ==================================================
st.set_page_config(
    page_title="Penilaian Mahasiswa Fuzzy",
    page_icon="🎓",
    layout="wide"
)
st.markdown("""
<style>

/* Background Utama */
.stApp{
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b,
        #334155
    );
}

/* Judul */
.main-title{
    text-align:center;
    color:white;
    font-size:48px;
    font-weight:800;
    margin-bottom:10px;
}

.subtitle{
    text-align:center;
    color:#cbd5e1;
    font-size:18px;
    margin-bottom:40px;
}

/* Card */
.custom-card{
    background:rgba(255,255,255,0.08);
    backdrop-filter:blur(10px);
    padding:25px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.1);
    margin-bottom:20px;
    box-shadow:0 8px 32px rgba(0,0,0,0.3);
}

/* Metric Card */
.metric-card{
    background:linear-gradient(
    135deg,
    #2563eb,
    #1d4ed8
    );
    padding:20px;
    border-radius:15px;
    text-align:center;
    color:white;
    box-shadow:0 5px 20px rgba(37,99,235,0.4);
}

/* Sidebar */
[data-testid="stSidebar"]{
    background:#0f172a;
}

/* Header */
.hero{
    background:linear-gradient(
    135deg,
    #2563eb,
    #7c3aed
    );
    padding:35px;
    border-radius:25px;
    text-align:center;
    color:white;
    margin-bottom:30px;
    box-shadow:0 10px 30px rgba(0,0,0,0.3);
}

/* Tabel */
[data-testid="stDataFrame"]{
    background:white;
    border-radius:15px;
}

/* Tombol */
.stButton button{
    background:linear-gradient(
    135deg,
    #2563eb,
    #7c3aed
    );
    color:white;
    border:none;
    border-radius:12px;
}

/* Footer */
.footer{
    text-align:center;
    color:#cbd5e1;
    margin-top:40px;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)
# ==================================================
# HEADER
# ==================================================
st.title("🎓 Sistem Penilaian Mahasiswa Menggunakan Logika Fuzzy")

st.markdown("""
Aplikasi ini digunakan untuk menentukan kategori nilai mahasiswa
menggunakan metode **Logika Fuzzy**.

### Kategori Penilaian
- Rendah
- Sedang
- Tinggi

### Domain Nilai
0 - 100
""")

# ==================================================
# SIDEBAR
# ==================================================
st.sidebar.header("Input Data")

nilai = st.sidebar.slider(
    "Masukkan Nilai Ujian",
    min_value=0,
    max_value=100,
    value=50
)

# ==================================================
# FUNGSI KEANGGOTAAN
# ==================================================
def rendah(x):
    if x <= 40:
        return 1
    elif 40 < x < 60:
        return (60 - x) / 20
    else:
        return 0


def sedang(x):
    if x <= 40 or x >= 70:
        return 0
    elif 40 < x <= 55:
        return (x - 40) / 15
    elif 55 < x < 70:
        return (70 - x) / 15
    else:
        return 0


def tinggi(x):
    if x <= 60:
        return 0
    elif 60 < x < 80:
        return (x - 60) / 20
    else:
        return 1


# ==================================================
# PERHITUNGAN FUZZY
# ==================================================
mu_rendah = rendah(nilai)
mu_sedang = sedang(nilai)
mu_tinggi = tinggi(nilai)

# ==================================================
# TAMPILKAN RUMUS
# ==================================================
st.header("📘 Fungsi Keanggotaan")

st.subheader("1. Rendah")

st.latex(r'''
\mu_{rendah}(x)=
\begin{cases}
1,&x\le40\\
\frac{60-x}{20},&40<x<60\\
0,&x\ge60
\end{cases}
''')

st.subheader("2. Sedang")

st.latex(r'''
\mu_{sedang}(x)=
\begin{cases}
0,&x\le40\\
\frac{x-40}{15},&40<x\le55\\
\frac{70-x}{15},&55<x<70\\
0,&x\ge70
\end{cases}
''')

st.subheader("3. Tinggi")

st.latex(r'''
\mu_{tinggi}(x)=
\begin{cases}
0,&x\le60\\
\frac{x-60}{20},&60<x<80\\
1,&x\ge80
\end{cases}
''')

# ==================================================
# HASIL PERHITUNGAN
# ==================================================
st.header("🧮 Perhitungan Derajat Keanggotaan")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Rendah", f"{mu_rendah:.2f}")

with col2:
    st.metric("Sedang", f"{mu_sedang:.2f}")

with col3:
    st.metric("Tinggi", f"{mu_tinggi:.2f}")

# ==================================================
# TABEL HASIL
# ==================================================
df = pd.DataFrame({
    "Kategori": ["Rendah", "Sedang", "Tinggi"],
    "Derajat Keanggotaan": [
        mu_rendah,
        mu_sedang,
        mu_tinggi
    ]
})

st.subheader("Tabel Derajat Keanggotaan")

st.dataframe(
    df,
    use_container_width=True
)

# ==================================================
# GRAFIK BAR
# ==================================================
st.subheader("Grafik Derajat Keanggotaan")

st.bar_chart(
    df.set_index("Kategori")
)

# ==================================================
# GRAFIK HIMPUNAN FUZZY
# ==================================================
st.header("📈 Grafik Himpunan Fuzzy")

x = np.linspace(0, 100, 1000)

y_rendah = [rendah(i) for i in x]
y_sedang = [sedang(i) for i in x]
y_tinggi = [tinggi(i) for i in x]

fig, ax = plt.subplots(figsize=(10,5))

ax.plot(
    x,
    y_rendah,
    linewidth=3,
    label="Rendah"
)

ax.plot(
    x,
    y_sedang,
    linewidth=3,
    label="Sedang"
)

ax.plot(
    x,
    y_tinggi,
    linewidth=3,
    label="Tinggi"
)

ax.axvline(
    nilai,
    linestyle="--",
    linewidth=2,
    label=f"Nilai = {nilai}"
)

ax.scatter(
    nilai,
    mu_rendah,
    s=100
)

ax.scatter(
    nilai,
    mu_sedang,
    s=100
)

ax.scatter(
    nilai,
    mu_tinggi,
    s=100
)

ax.set_xlabel("Nilai Ujian")
ax.set_ylabel("Derajat Keanggotaan")
ax.set_title("Grafik Himpunan Fuzzy Penilaian Mahasiswa")
ax.grid(True)
ax.legend()

st.pyplot(fig)

# ==================================================
# PENENTUAN HASIL
# ==================================================
maksimum = max(
    mu_rendah,
    mu_sedang,
    mu_tinggi
)

if maksimum == mu_rendah:
    hasil = "RENDAH"
elif maksimum == mu_sedang:
    hasil = "SEDANG"
else:
    hasil = "TINGGI"

# ==================================================
# IMPLEMENTASI HASIL
# ==================================================
st.header("🎯 Implementasi Hasil")

if hasil == "RENDAH":
    st.error("""
Mahasiswa memiliki performa akademik rendah.

Rekomendasi:
- Mengikuti remedial
- Menambah jam belajar
- Konsultasi dengan dosen
""")

elif hasil == "SEDANG":
    st.warning("""
Mahasiswa memiliki performa cukup baik.

Rekomendasi:
- Tingkatkan latihan soal
- Pertahankan konsistensi belajar
- Tingkatkan pemahaman materi
""")

else:
    st.success("""
Mahasiswa memiliki performa akademik tinggi.

Rekomendasi:
- Pertahankan prestasi
- Ikut kompetisi akademik
- Menjadi mentor belajar
""")

# ==================================================
# KESIMPULAN
# ==================================================
st.header("📋 Kesimpulan")

st.info(f"""
Nilai ujian mahasiswa adalah **{nilai}**

Derajat keanggotaan:

- Rendah = {mu_rendah:.2f}
- Sedang = {mu_sedang:.2f}
- Tinggi = {mu_tinggi:.2f}

Kategori akhir mahasiswa adalah:

### {hasil}
""")

# ==================================================
# FOOTER
# ==================================================
st.markdown("---")
st.caption(
    "Praktikum Logika Fuzzy - Penilaian Mahasiswa Menggunakan Streamlit"
)
