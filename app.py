import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 Dashboard Analisis Kuesioner")

uploaded_file = st.file_uploader("Upload file Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("📋 Data Preview")
    st.dataframe(df)

    # ==========================
    # Mapping Skor
    # ==========================
    skor_map = {
        "SS": 6,
        "S": 5,
        "CS": 4,
        "CTS": 3,
        "TS": 2,
        "STS": 1
    }

    kategori_map = {
        "SS": "Positif",
        "S": "Positif",
        "CS": "Netral",
        "CTS": "Negatif",
        "TS": "Negatif",
        "STS": "Negatif"
    }

    # Ubah ke skor numerik
    df_skor = df.replace(skor_map)

    # ==========================
    # 1️⃣ Bar Chart Distribusi Keseluruhan
    # ==========================
    st.subheader("📊 Distribusi Jawaban Keseluruhan")

    semua_jawaban = pd.Series(df.values.ravel())
    distribusi = semua_jawaban.value_counts().reindex(
        ["SS", "S", "CS", "CTS", "TS", "STS"]
    )

    fig1, ax1 = plt.subplots()
    distribusi.plot(kind="bar", ax=ax1)
    ax1.set_title("Distribusi Jawaban Keseluruhan")
    st.pyplot(fig1)

    # ==========================
    # 2️⃣ Pie Chart Proporsi
    # ==========================
    st.subheader("🥧 Proporsi Jawaban Keseluruhan")

    fig2, ax2 = plt.subplots()
    distribusi.plot(kind="pie", autopct="%1.1f%%", ax=ax2)
    ax2.set_ylabel("")
    st.pyplot(fig2)

    # ==========================
    # 3️⃣ Stacked Bar per Pertanyaan
    # ==========================
    st.subheader("📊 Distribusi Jawaban per Pertanyaan (Stacked)")

    distribusi_per_pertanyaan = pd.DataFrame()

    for kolom in df.columns:
        distribusi_per_pertanyaan[kolom] = df[kolom].value_counts()

    distribusi_per_pertanyaan = distribusi_per_pertanyaan.fillna(0)
    distribusi_per_pertanyaan = distribusi_per_pertanyaan.reindex(
        ["SS", "S", "CS", "CTS", "TS", "STS"]
    )

    fig3, ax3 = plt.subplots(figsize=(10,6))
    distribusi_per_pertanyaan.T.plot(kind="bar", stacked=True, ax=ax3)
    ax3.set_title("Distribusi Jawaban per Pertanyaan")
    st.pyplot(fig3)

    # ==========================
    # 4️⃣ Rata-rata Skor per Pertanyaan
    # ==========================
    st.subheader("📈 Rata-rata Skor per Pertanyaan")

    rata_rata = df_skor.mean()

    fig4, ax4 = plt.subplots()
    rata_rata.plot(kind="bar", ax=ax4)
    ax4.set_title("Rata-rata Skor")
    st.pyplot(fig4)

    # ==========================
    # 5️⃣ Distribusi Kategori (Positif/Netral/Negatif)
    # ==========================
    st.subheader("📊 Distribusi Kategori Jawaban")

    semua_kategori = semua_jawaban.map(kategori_map)
    distribusi_kategori = semua_kategori.value_counts().reindex(
        ["Positif", "Netral", "Negatif"]
    )

    fig5, ax5 = plt.subplots()
    distribusi_kategori.plot(kind="bar", ax=ax5)
    ax5.set_title("Distribusi Positif, Netral, Negatif")
    st.pyplot(fig5)

    # ==========================
    # 🎁 BONUS: Radar Chart Rata-rata Skor
    # ==========================
    st.subheader("🎯 Bonus: Radar Chart Rata-rata Skor")

    import numpy as np

    labels = rata_rata.index
    stats = rata_rata.values

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
    stats = np.concatenate((stats, [stats[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    fig6 = plt.figure()
    ax6 = fig6.add_subplot(111, polar=True)
    ax6.plot(angles, stats)
    ax6.fill(angles, stats, alpha=0.25)
    ax6.set_xticks(angles[:-1])
    ax6.set_xticklabels(labels)
    st.pyplot(fig6)

else:
    st.info("Silakan upload file Excel terlebih dahulu.")
