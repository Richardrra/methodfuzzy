import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ==========================
# KONFIGURASI HALAMAN
# ==========================
st.set_page_config(
    page_title="Logika Fuzzy - Penilaian Mahasiswa",
    layout="wide"
)

st.title("🎓 Studi Kasus 1 - Penilaian Mahasiswa (Logika Fuzzy)")
st.write("Input nilai ujian mahasiswa dan lihat hasil himpunan fuzzy.")

# ==========================
# FUNGSI KEANGGOTAAN
# ==========================

def rendah(x):
    if x <= 40:
        return 1
    elif 40 < x < 60:
        return (60 - x) / (60 - 40)
    else:
        return 0


def sedang(x):
    if x <= 40 or x >= 70:
        return 0
    elif 40 < x <= 55:
        return (x - 40) / (55 - 40)
    elif 55 < x < 70:
        return (70 - x) / (70 - 55)
    else:
        return 0


def tinggi(x):
    if x <= 60:
        return 0
    elif 60 < x < 80:
        return (x - 60) / (80 - 60)
    else:
        return 1


# ==========================
# INPUT USER
# ==========================

nilai = st.slider(
    "Masukkan Nilai Ujian",
    min_value=0,
    max_value=100,
    value=50
)

# ==========================
# HITUNG FUZZY
# ==========================

mu_rendah = rendah(nilai)
mu_sedang = sedang(nilai)
mu_tinggi = tinggi(nilai)

# ==========================
# HASIL
# ==========================

st.subheader("Hasil Derajat Keanggotaan")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Rendah", f"{mu_rendah:.2f}")

with col2:
    st.metric("Sedang", f"{mu_sedang:.2f}")

with col3:
    st.metric("Tinggi", f"{mu_tinggi:.2f}")

# ==========================
# INTERPRETASI
# ==========================

nilai_tertinggi = max(mu_rendah, mu_sedang, mu_tinggi)

if nilai_tertinggi == mu_rendah:
    hasil = "RENDAH"
elif nilai_tertinggi == mu_sedang:
    hasil = "SEDANG"
else:
    hasil = "TINGGI"

st.success(f"Kategori Penilaian Mahasiswa: **{hasil}**")

# ==========================
# VISUALISASI GRAFIK
# ==========================

x = np.linspace(0, 100, 500)

y_rendah = [rendah(i) for i in x]
y_sedang = [sedang(i) for i in x]
y_tinggi = [tinggi(i) for i in x]

fig, ax = plt.subplots(figsize=(10, 5))

ax.plot(x, y_rendah, label='Rendah')
ax.plot(x, y_sedang, label='Sedang')
ax.plot(x, y_tinggi, label='Tinggi')

# garis nilai input user
ax.axvline(
    nilai,
    linestyle='--',
    label=f'Nilai Input = {nilai}'
)

ax.set_title("Grafik Himpunan Fuzzy Penilaian Mahasiswa")
ax.set_xlabel("Nilai Ujian")
ax.set_ylabel("Derajat Keanggotaan")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# ==========================
# PENJELASAN
# ==========================

st.subheader("Interpretasi")

st.write(f"""
Nilai ujian mahasiswa adalah **{nilai}**.

- Derajat Rendah = **{mu_rendah:.2f}**
- Derajat Sedang = **{mu_sedang:.2f}**
- Derajat Tinggi = **{mu_tinggi:.2f}**

Berdasarkan nilai keanggotaan terbesar, mahasiswa termasuk kategori **{hasil}**.
""")
