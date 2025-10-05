# Nama Program    : app.py
# Nama            : Nazwa Nashatasya | Senia Nur Hasanah
# NPM             : 140810230019 | 140810230021
# Tanggal Buat    : Jumat, 3 Oktober 2025
# Deskripsi       : Aplikasi Sistem Pendukung Keputusan (DSS) untuk MCDM menggunakan metode Simple Additive Weighting (SAW), Weighted Product (WP), Analytical Hierarchy Process (AHP), dan Technique for Order Preference by Similarity to Ideal Solution (TOPSIS)

import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# ============================
# DATA TYPES
# ============================
class Criterion:
    def __init__(self, id, name, weight, attribute):
        self.id = id.strip() if id else ""
        self.name = name.strip() if name else ""
        self.weight = float(weight) if weight is not None else 1.0
        self.attribute = attribute.lower().strip() if attribute else "benefit"  # 'benefit' or 'cost'

class Alternative:
    def __init__(self, id, name, values):
        self.id = id.strip() if id else ""
        self.name = name.strip() if name else ""
        self.values = values  # dict: {criterion_id: value}

# ============================
# AUTO DETECTION HELPERS
# ============================
def is_criteria_df(df: pd.DataFrame):
    """
    Deteksi apakah dataframe berisi data kriteria. Dibuat lebih spesifik
    untuk menghindari kesalahan deteksi dengan file alternatif.
    """
    cols = [c.lower().strip() for c in df.columns]
    # Kata kunci "bobot" dan "atribut" adalah indikator yang jauh lebih kuat.
    if any(col in cols for col in ['bobot', 'atribut', 'attribute', 'nama kriteria']):
        return True
    return False

def is_alternatives_df(df: pd.DataFrame):
    """
    Deteksi apakah dataframe berisi data alternatif.
    Akan mengembalikan True jika kolom memiliki 'Kode Alternatif' atau 'Nama Alternatif'.
    """
    cols = [c.lower().strip() for c in df.columns]
    # Diperbarui untuk mengenali 'Kode Alternatif'
    if any(col in cols for col in ['kode alternatif', 'nama alternatif', 'alternatif', 'kode']):
        # Cek tambahan: pastikan bukan file kriteria yang menyamar
        if not any(col in cols for col in ['bobot', 'atribut', 'attribute']):
            return True

    # fallback check: jika lebih dari separuh kolom (selain kolom pertama) berisi angka
    if df.shape[1] >= 2:
        numeric_counts = 0
        total_vals = 0
        for c in df.columns[1:]:
            if pd.api.types.is_numeric_dtype(df[c].dropna()):
                 numeric_counts += df[c].notna().sum()
            total_vals += len(df)
        
        if total_vals > 0 and (numeric_counts / (total_vals * (df.shape[1]-1))) > 0.6:
            return True

    return False

# ============================
# FILE PARSER
# ============================
def parse_data(df_alt, df_crit=None):
    """Mengubah DataFrame menjadi list Criterion dan Alternative secara terurut."""
    criteria = []
    alternatives = []

    # -------------------------------------
    # STEP 1: PARSE ATAU BUAT KRITERIA
    # -------------------------------------
    if df_crit is not None:
        df_crit.columns = [str(c).strip() for c in df_crit.columns]
        for i, row in df_crit.iterrows():
            # Diperbarui untuk membaca 'Kode Kriteria' dan 'Kode' sebagai fallback
            crit_id = str(row.get("Kode Kriteria", row.get("Kode", f"C{i+1}"))).strip()
            name = str(row.get("Nama Kriteria", row.get("Kriteria", f"Kriteria {i+1}"))).strip()
            weight = row.get("Bobot", 1.0)
            try:
                weight = float(weight)
            except (ValueError, TypeError):
                weight = 1.0
            attr = str(row.get("Atribut", "benefit")).lower().strip()
            attr = "cost" if attr == "cost" else "benefit"
            criteria.append(Criterion(crit_id, name, weight, attr))

    elif df_alt is not None:
        crit_cols = [
            c for c in df_alt.columns if str(c).strip().lower().startswith("c") and str(c).strip()[1:].isdigit()
        ]
        for i, col in enumerate(crit_cols):
            col_id = str(col).strip()
            criteria.append(Criterion(col_id, f"Kriteria {i+1}", 1.0, "benefit"))

    if not criteria:
        return [], []

    # -------------------------------------
    # STEP 2: PARSE ALTERNATIF
    # -------------------------------------
    if df_alt is not None:
        df_alt.columns = [str(c).strip() for c in df_alt.columns]
        
        for col in ["Nama Alternatif", "Nama"]:
            if col in df_alt.columns:
                df_alt[col] = df_alt[col].fillna('')

        for i, row in df_alt.iterrows():
            # Diperbarui untuk membaca 'Kode Alternatif' dan 'Kode' sebagai fallback
            alt_id = str(row.get("Kode Alternatif", row.get("Kode", f"A{i+1}"))).strip()
            alt_name = str(row.get("Nama Alternatif", row.get("Nama", f"Alternatif {i+1}"))).strip()

            values = {}
            for crit in criteria:
                raw_val = row.get(crit.id, row.get(crit.id.upper(), row.get(crit.id.lower(), 0.0)))
                try:
                    val = float(raw_val)
                except (ValueError, TypeError):
                    val = 0.0
                values[crit.id] = val

            alternatives.append(Alternative(alt_id, alt_name, values))

    return criteria, alternatives

# ============================
# SAW CALCULATION
# ============================
def calculate_saw(criteria, alternatives):
    """Hitung metode Simple Additive Weighting (SAW)"""
    steps = []
    
    # =======================
    # 1️⃣ Validasi Data
    # =======================
    if not criteria or not alternatives:
        raise ValueError("Kriteria atau alternatif kosong. Pastikan data sudah lengkap.")

    # =======================
    # 2️⃣ Matriks Keputusan Awal (X)
    # =======================
    matrix = np.array([[alt.values.get(crit.id, 0.0) for crit in criteria] for alt in alternatives], dtype=float)
    df_initial = pd.DataFrame(matrix, index=[alt.name or alt.id for alt in alternatives], columns=[f"{c.name} ({c.id})" for c in criteria])
    steps.append(("Matriks Keputusan Awal", df_initial))

    # =======================
    # 3️⃣ Normalisasi Matriks
    # =======================
    # Rumus:
    # Untuk kriteria benefit  → r_ij = x_ij / max(x_j)
    # Untuk kriteria cost     → r_ij = min(x_j) / x_ij
    norm_matrix = np.zeros_like(matrix, dtype=float)
    for j, crit in enumerate(criteria):
        col = matrix[:, j]
        if crit.attribute.lower() == 'benefit':
            max_val = np.max(col)
            norm_matrix[:, j] = col / max_val if max_val != 0 else 0
        else:  # cost
            min_val = np.min(col)
            norm_matrix[:, j] = min_val / col
            norm_matrix[:, j][col == 0] = 0
    df_norm = pd.DataFrame(norm_matrix, index=[alt.name or alt.id for alt in alternatives], columns=[f"{c.name} ({c.attribute})" for c in criteria])
    steps.append(("Normalisasi Matriks (Benefit/Cost)", df_norm))

    # =======================
    # 3️⃣ Normalisasi Bobot
    # =======================
    # Setiap bobot dinormalisasi agar totalnya = 1
    total_weight = sum(c.weight for c in criteria)
    normalized_weights = [(c.weight / total_weight) if total_weight != 0 else (1.0/len(criteria)) for c in criteria]
    df_norm_weights = pd.DataFrame([normalized_weights], index=['Bobot Ternormalisasi (wj)'], columns=[c.id for c in criteria])
    steps.append(("Normalisasi Bobot", df_norm_weights))
    
    # =======================
    # 5️⃣ Hitung Nilai Preferensi (V)
    # =======================
    # Rumus: V_i = Σ(w_j * r_ij)
    # → hasil penjumlahan terbobot antara nilai normalisasi dan bobot
    v_values = np.dot(norm_matrix, normalized_weights)
    df_v = pd.DataFrame({"Nilai V (Skor)": v_values}, index=[alt.name or alt.id for alt in alternatives])
    steps.append(("Perhitungan Skor V (V = Σ(wj * rij))", df_v))

    # =======================
    # 8️⃣ Perangkingan Akhir
    # =======================
    # Urutkan dari skor tertinggi ke terendah (semakin besar semakin baik)
    ranking_data = sorted(zip([alt.name or alt.id for alt in alternatives], v_values), key=lambda x: x[1], reverse=True)
    df_ranking = pd.DataFrame([[name, score, rank + 1] for rank, (name, score) in enumerate(ranking_data)], columns=['Alternatif', 'Skor Akhir (V)', 'Ranking'])
    steps.append(("Hasil Perankingan", df_ranking))

    return steps, df_ranking

# ============================
# WP CALCULATION
# ============================
def calculate_wp(criteria, alternatives):
    """Hitung metode Weighted Product (WP)"""
    steps = []
    
    # =======================
    # 1️⃣ Validasi data
    # =======================
    if not criteria or not alternatives:
        raise ValueError("Kriteria atau alternatif kosong.")

    # =======================
    # 2️⃣ Matriks Keputusan Awal
    # =======================
    matrix = np.array([[alt.values.get(crit.id, 0.0) for crit in criteria] for alt in alternatives])
    df_initial = pd.DataFrame(matrix, index=[alt.name or alt.id for alt in alternatives], columns=[f"{c.name} ({c.id})" for c in criteria])
    steps.append(("Matriks Keputusan Awal", df_initial))

    # =======================
    # 3️⃣ Normalisasi Bobot
    # =======================
    # Setiap bobot dinormalisasi agar totalnya = 1
    total_weight = sum(c.weight for c in criteria)
    normalized_weights = [(c.weight / total_weight) if total_weight != 0 else (1.0/len(criteria)) for c in criteria]
    df_norm_weights = pd.DataFrame([normalized_weights], index=['Bobot Ternormalisasi (wj)'], columns=[c.id for c in criteria])
    steps.append(("Normalisasi Bobot", df_norm_weights))

    # =======================
    # 4️⃣ Penyesuaian Bobot
    # =======================
    # Jika kriteria bertipe "cost", bobot dijadikan negatif karena dalam WP nilai cost berbanding terbalik (semakin kecil semakin baik)
    adjusted_weights = [-w if crit.attribute.lower() == 'cost' else w for w, crit in zip(normalized_weights, criteria)]
    df_adj_weights = pd.DataFrame([adjusted_weights], index=['Bobot Disesuaikan (w)'], columns=[f"{c.name} ({c.attribute})" for c in criteria])
    steps.append(("Penyesuaian Bobot (Atribut Cost bernilai negatif)", df_adj_weights))

    # =======================
    # 5️⃣ Perhitungan Nilai S
    # =======================
    # Rumus: S_i = ∏(x_ij ^ w_j)
    # Pastikan tidak ada nilai nol agar tidak error saat dipangkatkan
    matrix[matrix <= 0] = 1e-9
    s_values = np.prod(matrix ** adjusted_weights, axis=1)
    df_s = pd.DataFrame({"Nilai S": s_values}, index=[alt.name or alt.id for alt in alternatives])
    steps.append(("Perhitungan Nilai S (S = ∏(xij^w))", df_s))

     # =======================
    # 6️⃣ Perhitungan Nilai V (Preferensi)
    # =======================
    total_s = np.sum(s_values)
    v_values = s_values / total_s if total_s != 0 else np.zeros_like(s_values)
    df_v = pd.DataFrame({"Nilai S": s_values, "Nilai V (Skor)": v_values}, index=[alt.name or alt.id for alt in alternatives])
    steps.append(("Perhitungan Nilai V (V = S / ΣS)", df_v))

    # =======================
    # 6️⃣ Perangkingan Akhir
    # =======================
    # Urutkan dari skor tertinggi ke terendah (semakin besar semakin baik)
    ranking_data = sorted(zip([alt.name or alt.id for alt in alternatives], v_values), key=lambda x: x[1], reverse=True)
    df_ranking = pd.DataFrame([[name, score, rank + 1] for rank, (name, score) in enumerate(ranking_data)], columns=['Alternatif', 'Skor Akhir (V)', 'Ranking'])
    steps.append(("Hasil Perankingan", df_ranking))

    return steps, df_ranking

# ============================
# AHP CALCULATION
# ============================

# ============================
# TOPSIS CALCULATION
# ============================
def calculate_topsis(criteria, alternatives):
    """Hitung metode TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)"""
    steps = []
    
    # =======================
    # 1️⃣ Validasi data
    # =======================
    if not criteria or not alternatives:
        raise ValueError("Kriteria atau alternatif kosong.")

    # =======================
    # 2️⃣ Matriks Keputusan Awal (X)
    # =======================
    matrix = np.array([[alt.values.get(crit.id, 0.0) for crit in criteria] for alt in alternatives], dtype=float)
    df_initial = pd.DataFrame(matrix, index=[alt.name or alt.id for alt in alternatives], columns=[f"{c.name} ({c.id})" for c in criteria])
    steps.append(("Matriks Keputusan Awal", df_initial))

    # =======================
    # 3️⃣ Normalisasi Matriks
    # =======================
    # Rumus: r_ij = x_ij / sqrt(Σx_ij²)
    # Setiap kolom dinormalisasi agar tidak dipengaruhi skala nilai
    norm_denominators = np.sqrt(np.sum(matrix**2, axis=0))
    norm_denominators[norm_denominators == 0] = 1.0
    normalized_matrix = matrix / norm_denominators
    df_normalized = pd.DataFrame(normalized_matrix, index=[alt.name or alt.id for alt in alternatives], columns=[c.name for c in criteria])
    steps.append(("Matriks Ternormalisasi (rij = xij / √(Σxij²))", df_normalized))

    # =======================
    # 4️⃣ Matriks Ternormalisasi Terbobot
    # =======================
    # Rumus: y_ij = w_j * r_ij
    # Gunakan bobot yang sudah ternormalisasi
    total_weight = sum(c.weight for c in criteria)
    normalized_weights = [(c.weight / total_weight) if total_weight != 0 else (1.0/len(criteria)) for c in criteria]
    weighted_matrix = normalized_matrix * normalized_weights
    df_weighted = pd.DataFrame(weighted_matrix, index=[alt.name or alt.id for alt in alternatives], columns=[f"{c.name} (w={w:.3f})" for c, w in zip(criteria, normalized_weights)])
    steps.append(("Matriks Ternormalisasi Terbobot (yij = wj × rij)", df_weighted))

    # =======================
    # 5️⃣ Menentukan Solusi Ideal Positif (A+) dan Negatif (A-)
    # =======================
    # Benefit → nilai maksimum (semakin besar semakin baik)
    # Cost → nilai minimum (semakin kecil semakin baik)
    ideal_positive = np.zeros(len(criteria))
    ideal_negative = np.zeros(len(criteria))
    for j, crit in enumerate(criteria):
        col = weighted_matrix[:, j]
        if crit.attribute == 'benefit':
            ideal_positive[j] = np.max(col)
            ideal_negative[j] = np.min(col)
        else: # cost
            ideal_positive[j] = np.min(col)
            ideal_negative[j] = np.max(col)
            
    df_ideal = pd.DataFrame([ideal_positive, ideal_negative], index=['A+ (Ideal Positif)', 'A- (Ideal Negatif)'], columns=[f"{c.name} ({c.attribute})" for c in criteria])
    steps.append(("Solusi Ideal", df_ideal))

    # =======================
    # 6️⃣ Hitung Jarak Separasi
    # =======================
    # Rumus:
    # D+ = √Σ(y_ij - y_j+)²
    # D- = √Σ(y_ij - y_j-)²
    separation_positive = np.sqrt(np.sum((weighted_matrix - ideal_positive)**2, axis=1))
    separation_negative = np.sqrt(np.sum((weighted_matrix - ideal_negative)**2, axis=1))
    df_separation = pd.DataFrame({'D+ (Jarak ke A+)': separation_positive, 'D- (Jarak ke A-)': separation_negative}, index=[alt.name or alt.id for alt in alternatives])
    steps.append(("Jarak Separasi", df_separation))

    # =======================
    # 7️⃣ Hitung Nilai Kedekatan Relatif (V)
    # =======================
    # Rumus:
    # V_i = D- / (D+ + D-)
    closeness_denominator = separation_positive + separation_negative
    closeness = np.divide(separation_negative, closeness_denominator, out=np.zeros_like(separation_negative), where=closeness_denominator!=0)
    df_closeness = pd.DataFrame({'D+': separation_positive, 'D-': separation_negative, 'Skor V': closeness}, index=[alt.name or alt.id for alt in alternatives])
    steps.append(("Kedekatan Relatif (V = D- / (D+ + D-))", df_closeness))
    
    # =======================
    # 8️⃣ Perangkingan Akhir
    # =======================
    # Semakin tinggi nilai V → semakin dekat dengan solusi ideal → semakin baik
    ranking_data = sorted(zip([alt.name or alt.id for alt in alternatives], closeness), key=lambda x: x[1], reverse=True)
    df_ranking = pd.DataFrame([[name, score, rank+1] for rank, (name, score) in enumerate(ranking_data)], columns=['Alternatif', 'Skor Akhir', 'Ranking'])
    steps.append(("Hasil Perankingan", df_ranking))

    return steps, df_ranking

# ============================
# STREAMLIT UI
# ============================
def main():
    st.set_page_config(page_title="MCDM Calculator", layout="wide")
    st.title("🎯 MCDM Calculator (SAW, WP, AHP, TOPSIS)")
    st.markdown("**Multi-Criteria Decision Making** menggunakan metode Simple Additive Weighting (SAW), Weighted Product (WP), Analytical Hierarchy Process (AHP), dan Technique for Order Preference by Similarity to Ideal Solution (TOPSIS).")

    if 'criteria' not in st.session_state:
        st.session_state.criteria = []
    if 'alternatives' not in st.session_state:
        st.session_state.alternatives = []

    st.sidebar.header("Pengaturan")
    method = st.sidebar.selectbox("Pilih Metode", ["Simple Additive Weighting (SAW)", "Weighted Product (WP)", "Analytical Hierarchy Process (AHP)", "Technique for Order Preference by Similarity to Ideal Solution (TOPSIS)"])

    input_method = st.radio("Metode Input Data", ["Upload File (CSV/XLSX)", "Input Manual"], horizontal=True)

    if input_method == "Upload File (CSV/XLSX)":
        st.subheader("📁 Upload File")
        st.info("""
        **Format File yang Direkomendasikan:**
        - **File Alternatif:** `Kode Alternatif`, `C1`, `C2`, ..., `Nama Alternatif`
        - **File Kriteria:** `Kode Kriteria`, `Bobot`, `Nama Kriteria`, `Atribut` (cost/benefit)
        
        Anda dapat mengunggah satu file Excel (dengan sheet terpisah) atau beberapa file CSV sekaligus.
        """)
        uploaded_files = st.file_uploader("Pilih file CSV atau XLSX", type=['csv', 'xlsx', 'xls'], accept_multiple_files=True)

        if uploaded_files:
            df_criteria, df_alternatives = None, None
            for f in uploaded_files:
                try:
                    df_temp = pd.read_excel(f) if f.name.lower().endswith(('.xls', '.xlsx')) else pd.read_csv(f)
                    if is_criteria_df(df_temp):
                        df_criteria = df_temp
                        st.write(f"✔️ File kriteria terdeteksi: `{f.name}`")
                    elif is_alternatives_df(df_temp):
                        df_alternatives = df_temp
                        st.write(f"✔️ File alternatif terdeteksi: `{f.name}`")
                    else:
                        st.warning(f"⚠️ Tidak dapat mendeteksi jenis file `{f.name}` secara otomatis.")
                except Exception as e:
                    st.error(f"Gagal memuat file {f.name}: {e}")

            try:
                criteria, alternatives = parse_data(df_alternatives, df_criteria)
                st.session_state.criteria = criteria
                st.session_state.alternatives = alternatives
                if criteria and alternatives:
                    st.success(f"✅ Data berhasil dimuat! Ditemukan {len(alternatives)} alternatif dan {len(criteria)} kriteria.")
                elif criteria:
                    st.info(f"✅ Kriteria berhasil dimuat ({len(criteria)}). Silakan unggah file alternatif.")
                elif alternatives:
                    st.info(f"✅ Alternatif berhasil dimuat ({len(alternatives)}). Kriteria dibuat otomatis.")
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan saat memproses data: {e}")
    
    else:  # Manual Input
        st.subheader("✏️ Input Manual")
        num_criteria = st.number_input("Jumlah Kriteria", 1, 50, len(st.session_state.criteria) or 3)
        if len(st.session_state.criteria) != num_criteria:
            st.session_state.criteria = [Criterion(f"C{i+1}", f"Kriteria {i+1}", 1.0, 'benefit') for i in range(num_criteria)]

        cols_crit = st.columns(num_criteria)
        for i, crit in enumerate(st.session_state.criteria):
            with cols_crit[i]:
                st.markdown(f"**Kriteria {i+1}**")
                crit.id = f"C{i+1}"
                crit.name = st.text_input("Nama", crit.name, key=f"crit_name_{i}")
                crit.weight = st.number_input("Bobot", 0.0, value=float(crit.weight), key=f"crit_weight_{i}")
                crit.attribute = st.selectbox("Atribut", ['benefit', 'cost'], index=0 if crit.attribute == 'benefit' else 1, key=f"crit_attr_{i}")
        
        st.markdown("---")
        num_alternatives = st.number_input("Jumlah Alternatif", 1, 200, len(st.session_state.alternatives) or 3)
        if len(st.session_state.alternatives) != num_alternatives:
            st.session_state.alternatives = [Alternative(f"A{i+1}", f"Alternatif {i+1}", {c.id: 1.0 for c in st.session_state.criteria}) for i in range(num_alternatives)]

        header_cols = st.columns([2] + [1] * num_criteria)
        header_cols[0].markdown("**Nama Alternatif**")
        for i, crit in enumerate(st.session_state.criteria):
            header_cols[i+1].markdown(f"**{crit.name}**")
        
        for i, alt in enumerate(st.session_state.alternatives):
            alt.id = f"A{i+1}"
            row_cols = st.columns([2] + [1] * num_criteria)
            alt.name = row_cols[0].text_input(f"Nama Alt {i+1}", alt.name, key=f"alt_name_{i}", label_visibility="collapsed")
            for j, crit in enumerate(st.session_state.criteria):
                alt.values[crit.id] = row_cols[j+1].number_input(crit.id, value=float(alt.values.get(crit.id, 1.0)), key=f"alt_val_{i}_{j}", label_visibility="collapsed")

    if st.session_state.criteria and st.session_state.alternatives:
        st.markdown("---")
        st.subheader("📊 Data Saat Ini")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Kriteria:**")
            df_crit_display = pd.DataFrame([
                {'ID': c.id, 'Nama': c.name, 'Bobot': c.weight, 'Atribut': c.attribute}
                for c in st.session_state.criteria
            ])
            st.dataframe(df_crit_display, use_container_width=True, hide_index=True)
        with col2:
            st.markdown("**Alternatif:**")
            df_alt_display_data = [{'Nama': alt.name or alt.id, **{c.name: alt.values.get(c.id, 0.0) for c in st.session_state.criteria}} for alt in st.session_state.alternatives]
            st.dataframe(pd.DataFrame(df_alt_display_data), use_container_width=True, hide_index=True)

        st.markdown("---")
        if st.button("🚀 Hitung Ranking", type="primary", use_container_width=True):
            with st.spinner("Menghitung..."):
                try:
                    # Pilih fungsi perhitungan sesuai metode yang dipilih
                    if method == "Simple Additive Weighting (SAW)":
                        calculate_func = calculate_saw
                    elif method == "Weighted Product (WP)":
                        calculate_func = calculate_wp
                    elif method == "Technique for Order Preference by Similarity to Ideal Solution (TOPSIS)":
                        calculate_func = calculate_topsis
                    else:
                        st.error("Metode belum didukung.")
                        st.stop()

                    # Jalankan perhitungan
                    steps, ranking = calculate_func(st.session_state.criteria, st.session_state.alternatives)

                    st.success("✅ Perhitungan selesai!")
                    st.markdown("---")
                    st.header("🏆 Hasil Akhir")

                    # Highlight warna emas, perak, perunggu
                    def highlight_top3(row):
                        color = ''
                        if row.Ranking == 1:
                            color = 'background-color: #FFD700'  # Gold
                        elif row.Ranking == 2:
                            color = 'background-color: #C0C0C0'  # Silver
                        elif row.Ranking == 3:
                            color = 'background-color: #CD7F32'  # Bronze
                        return [color] * len(row)

                    st.dataframe(
                        ranking.style.apply(highlight_top3, axis=1).format({ranking.columns[1]: "{:.4f}"}),
                        use_container_width=True,
                        hide_index=True
                    )

                    st.markdown("---")
                    st.header("📝 Langkah Perhitungan")
                    for title, df in steps:
                        with st.expander(title):
                            st.dataframe(df, use_container_width=True)

                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan saat menghitung: {e}")

    elif input_method == "Upload File (CSV/XLSX)" and "uploaded_files" in locals() and not uploaded_files:
        st.info("Silakan unggah file kriteria dan alternatif Anda.")

if __name__ == "__main__":
    main()