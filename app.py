# Nama Program    : app.py
# Nama            : Nazwa Nashatasya | Senia Nur Hasanah
# NPM             : 140810230019 | 140810230021
# Tanggal Buat    : Jumat, 3 Oktober 2025
# Deskripsi       : Aplikasi Sistem Pendukung Keputusan (DSS) untuk MCDM menggunakan metode Simple Additive Weighting (SAW), Weighted Product (WP), Analytical Hierarchy Process (AHP), dan Technique for Order Preference by Similarity to Ideal Solution (TOPSIS)

import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

def apply_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Poppins', sans-serif;
    }
    /* ======== WRAPPER UTAMA BIAR NENGAH ======== */
 
    /* Reset posisi layout utama agar selalu di tengah, sidebar aktif/tidak */
    div[data-testid="stAppViewContainer"] > div.main {
        padding-left: 0 !important;
        padding-right: 0 !important;
        margin: 0 auto !important;
        display: flex;
        justify-content: center;
    }

    .block-container {
        padding-top: 1rem !important;
    }
  
        /* ====== HOVER EFFECT DENGAN HINT UNGU-VIOLET-BIRU-PINK ====== */
    div[data-testid="stVerticalBlock"] > div {
        transition: all 0.35s ease;
    }

    div[data-testid="stVerticalBlock"] > div:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow:
            0 0 15px rgba(168, 85, 247, 0.5),   /* violet */
            0 0 25px rgba(99, 102, 241, 0.4),   /* biru neon */
            0 0 40px rgba(236, 72, 153, 0.3);   /* pink neon */
        border: 1px solid rgba(168, 85, 247, 0.4); /* ungu lembut */
        background: linear-gradient(135deg,
            rgba(168, 85, 247, 0.08),   /* violet */
            rgba(99, 102, 241, 0.08),   /* biru */
            rgba(236, 72, 153, 0.1)     /* pink */
        );
        transition: all 0.3s ease;
    }

    h1 {
        background: linear-gradient(90deg, #6C63FF 0%, #C77DFF 40%, #FF6F91 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        color: #fff;
        text-align: center;
        font-weight: 700;
        font-size: 3rem;
        letter-spacing: 1px;
        text-shadow:
            0 0 10px rgba(108, 99, 255, 0.6),
            0 0 20px rgba(199, 125, 255, 0.4),
            0 0 40px rgba(255, 111, 145, 0.3);              /* ini padding keseluruhan */
        padding-bottom: 2rem;          /* ⬅️ tambah ini untuk jarak bawah ekstra */
        border-radius: 20px;
        background-color: rgba(20, 15, 40, 0.8);
        box-shadow: 0 0 30px rgba(199, 125, 255, 0.3);
        animation: glowPulse 3s ease-in-out infinite alternate;
    }


    /* Subtitle */
    .main > div:first-child > div > div > p {
        color: #bdbdbd !important;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    /* Kotak utama (blok konten) */
    .stTabs, .stElementContainer, .stExpander, div[data-testid="stVerticalBlock"] > div {
        width: 99% !important;
        background: linear-gradient(135deg, #202534 0%, #181C27 100%);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 0.5rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
        margin-bottom: 1.2rem;
        color: #E0E0E0;
        transition: transform 0.3s ease, box-shadow 0.3s ease;    
    }

 
    /* Subjudul */
    h2, h3 {
        color: #9D84FF !important;
        font-weight: 600 !important;
        margin-left: 1.1rem !important;
        margin-top: 1rem !important;
        margin-bottom: 1.5rem !important;
    }
    p {
        text-align: center;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2B1055 0%, #5E17EB 50%, #1597BB 100%);
        padding-top: 1.5rem;
    }

    section[data-testid="stSidebar"] > div {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(8px);
        padding: 1.rem;
    }

    section[data-testid="stSidebar"] h2 {
        color: #FFFFFF !important;
        text-align: center;
        font-weight: 600;
        padding-bottom: 1.5rem;
        padding-right: 1.7rem;
    }

    section[data-testid="stSidebar"] label {
        color: #FFFFFF !important;
        font-weight: 500;
        padding-left: 1rem;
    }

    /* Tombol utama */
    .stButton > button {
        background: linear-gradient(135deg, #6C63FF 0%, #FF6F91 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.05rem;
        box-shadow: 0 4px 12px rgba(255, 111, 145, 0.3);
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;   
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(108, 99, 255, 0.5);
        background: linear-gradient(135deg, #8A63FF 0%, #FF85B3 100%);
    }

    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #333;
        background-color: rgba(255, 255, 255, 0.08);
        color: #FFFFFF;
        padding: 0.6rem;
        transition: all 0.3s ease;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #FF85B3;
        box-shadow: 0 0 0 2px rgba(255, 133, 179, 0.3);
    }

    /* Radio Buttons */
    .stRadio > label {
        color: #E0E0E0 !important;
        font-weight: 500;
        padding-left: 0.5rem
    }

    /* Dataframe */
    .dataframe {
        border-radius: 10px !important;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
    }

    .dataframe th {
        background: linear-gradient(135deg, #6C63FF 0%, #FF85B3 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        text-align: center !important;
        padding: 1rem !important;
    }

    .dataframe td {
        background: rgba(255, 255, 255, 0.03);
        color: #E0E0E0;
        text-align: center !important;
        padding: 0.75rem !important;
    }

    /* Expander Header */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #6C63FF 0%, #FF6F91 100%);
        color: white !important;
        width: 100% !important;   /* lebar relatif terhadap sidebar */
        margin: auto;            /* biar di tengah */
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(108, 99, 255, 0.3);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #2B1055 0%, #6C63FF 100%);
        color: white;
        border-radius: 10px 10px 0 0;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: 0.3s;   
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #FF6F91 0%, #6C63FF 100%);
        text-align: center !important;
        color: #FFF;
        font-weight: 600;
    }

    /* File Uploader */
    .stFileUploader {
        background: rgba(255, 255, 255, 0.05);
        border: 2px dashed #6C63FF;
        border-radius: 15px;
        padding: 2rem;
        transition: all 0.3s ease;
        color: #FFFFFF;
    }

    .stFileUploader:hover {
        background: rgba(108, 99, 255, 0.1);
        border-color: #FF85B3;
    }

    /* Animasi */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* HR */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #6C63FF, #FF85B3, transparent);
    }
    
    
    /* ===== Footer di Bawah ===== */
    .sidebar-footer {
    position: absolute;
    bottom: opx;           /* jarak dari bawah */
    left: 0;
    text-align: left;
    font-size: 13px;
    top: 24rem
}
    </style>
    """, unsafe_allow_html=True)

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
    
    # 1️⃣ Validasi Data
    if not criteria or not alternatives:
        raise ValueError("Kriteria atau alternatif kosong. Pastikan data sudah lengkap.")

    # 2️⃣ Matriks Keputusan Awal (X)
    matrix = np.array([[alt.values.get(crit.id, 0.0) for crit in criteria] for alt in alternatives], dtype=float)
    df_initial = pd.DataFrame(matrix, index=[alt.name or alt.id for alt in alternatives], columns=[f"{c.name} ({c.id})" for c in criteria])
    steps.append(("Matriks Keputusan Awal", df_initial))

    # 3️⃣ Normalisasi Matriks
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
            # Hindari pembagian dengan nol jika ada nilai 0 di kriteria cost
            safe_col = np.where(col == 0, 1e-9, col)
            norm_matrix[:, j] = min_val / safe_col
            norm_matrix[:, j][col == 0] = 0

    df_norm = pd.DataFrame(norm_matrix, index=[alt.name or alt.id for alt in alternatives], columns=[f"{c.name} ({c.attribute})" for c in criteria])
    steps.append(("Normalisasi Matriks (Benefit/Cost)", df_norm))

    # 4️⃣ Normalisasi Bobot
    # Setiap bobot dinormalisasi agar totalnya = 1
    total_weight = sum(c.weight for c in criteria)
    normalized_weights = [(c.weight / total_weight) if total_weight != 0 else (1.0/len(criteria)) for c in criteria]
    df_norm_weights = pd.DataFrame([normalized_weights], index=['Bobot Ternormalisasi (wj)'], columns=[c.id for c in criteria])
    steps.append(("Normalisasi Bobot", df_norm_weights))
    
    # 5️⃣ Hitung Nilai Preferensi (V)
    # Rumus: V_i = Σ(w_j * r_ij)
    # Hasil penjumlahan terbobot antara nilai normalisasi dan bobot
    v_values = np.dot(norm_matrix, normalized_weights)
    df_v = pd.DataFrame({"Nilai V (Skor)": v_values}, index=[alt.name or alt.id for alt in alternatives])
    steps.append(("Perhitungan Skor V (V = Σ(wj * rij))", df_v))

    # 8️⃣ Perangkingan Akhir
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
    
    # 1️⃣ Validasi data
    if not criteria or not alternatives:
        raise ValueError("Kriteria atau alternatif kosong.")

    # 2️⃣ Matriks Keputusan Awal (X)
    matrix = np.array([[alt.values.get(crit.id, 0.0) for crit in criteria] for alt in alternatives])
    df_initial = pd.DataFrame(matrix, index=[alt.name or alt.id for alt in alternatives], columns=[f"{c.name} ({c.id})" for c in criteria])
    steps.append(("Matriks Keputusan Awal", df_initial))

    # 3️⃣ Normalisasi Bobot
    # Setiap bobot dinormalisasi agar totalnya = 1
    total_weight = sum(c.weight for c in criteria)
    normalized_weights = [(c.weight / total_weight) if total_weight != 0 else (1.0/len(criteria)) for c in criteria]
    df_norm_weights = pd.DataFrame([normalized_weights], index=['Bobot Ternormalisasi (wj)'], columns=[c.id for c in criteria])
    steps.append(("Normalisasi Bobot", df_norm_weights))

    # 4️⃣ Penyesuaian Bobot
    # Jika kriteria bertipe "cost", bobot dijadikan negatif karena dalam WP nilai cost berbanding terbalik (semakin kecil semakin baik)
    adjusted_weights = [-w if crit.attribute.lower() == 'cost' else w for w, crit in zip(normalized_weights, criteria)]
    df_adj_weights = pd.DataFrame([adjusted_weights], index=['Bobot Disesuaikan (w)'], columns=[f"{c.name} ({c.attribute})" for c in criteria])
    steps.append(("Penyesuaian Bobot (Atribut Cost bernilai negatif)", df_adj_weights))

    # 5️⃣ Perhitungan Nilai S
    # Rumus: S_i = ∏(x_ij ^ w_j)
    # Pastikan tidak ada nilai nol agar tidak error saat dipangkatkan
    matrix[matrix <= 0] = 1e-9
    s_values = np.prod(matrix ** adjusted_weights, axis=1)
    df_s = pd.DataFrame({"Nilai S": s_values}, index=[alt.name or alt.id for alt in alternatives])
    steps.append(("Perhitungan Nilai S (S = ∏(xij^w))", df_s))

    # 6️⃣ Perhitungan Nilai V (Preferensi)
    # Rumus: V_i = S_i / ΣS_i
    total_s = np.sum(s_values)
    v_values = s_values / total_s if total_s != 0 else np.zeros_like(s_values)
    df_v = pd.DataFrame({"Nilai S": s_values, "Nilai V (Skor)": v_values}, index=[alt.name or alt.id for alt in alternatives])
    steps.append(("Perhitungan Nilai V (V = S / ΣS)", df_v))

    # 7️⃣ Perangkingan Akhir
    # Urutkan dari skor tertinggi ke terendah (semakin besar semakin baik)
    ranking_data = sorted(zip([alt.name or alt.id for alt in alternatives], v_values), key=lambda x: x[1], reverse=True)
    df_ranking = pd.DataFrame([[name, score, rank + 1] for rank, (name, score) in enumerate(ranking_data)], columns=['Alternatif', 'Skor Akhir (V)', 'Ranking'])
    steps.append(("Hasil Perankingan", df_ranking))

    return steps, df_ranking

# ============================
# AHP CALCULATION
# ============================
def calculate_ahp(df_kriteria, df_alternatif):
    steps = []
    
    # 1️⃣ Validasi Data
    df_kriteria.columns = [str(c).strip() for c in df_kriteria.columns]
    df_alternatif.columns = [str(c).strip() for c in df_alternatif.columns]

    if 'Kriteria' not in df_alternatif.columns:
        raise ValueError("Kolom 'Kriteria' tidak ditemukan di file AHP-alternatif.csv. Pastikan nama kolomnya persis 'Kriteria'.")

    # 2️⃣ Matriks Perbandingan Kriteria
    try:
        crit_cols = [c for c in df_kriteria.columns if c.lower().startswith("c")]
        crit_index = df_kriteria["Kode Kriteria"].values
        mat_kriteria = df_kriteria[crit_cols].to_numpy(dtype=float)
        kriteria_matrix = pd.DataFrame(mat_kriteria, index=crit_index, columns=crit_cols)
        steps.append(("Matriks Perbandingan Kriteria", kriteria_matrix))
    except Exception as e:
        raise ValueError(f"Format file AHP-Kriteria tidak valid: {e}")

    # Normalisasi Matriks Kriteria dan Hitung Bobot
    col_sums = kriteria_matrix.sum(axis=0)
    norm_matrix = kriteria_matrix / col_sums
    weights = norm_matrix.mean(axis=1)
    steps.append(("Normalisasi Matriks Kriteria", norm_matrix))
    steps.append(("Bobot Kriteria", pd.DataFrame(weights, columns=['Bobot'])))

    # Uji Konsistensi
    n = len(kriteria_matrix)
    if n > 0 :
        lambda_max = (col_sums * weights).sum()
        CI = (lambda_max - n) / (n - 1) if (n - 1) > 0 else 0
        RI_table = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
        RI = RI_table.get(n, 1.49)
        CR = CI / RI if RI != 0 else 0
        steps.append(("Uji Konsistensi Kriteria", pd.DataFrame({
            'λ maks': [lambda_max], 'CI': [CI], 'CR': [CR],
            'Konsisten': ['Ya' if CR < 0.1 else 'Tidak']
        })))

    # 3️⃣ Matriks Perbandingan Alternatif per Kriteria
    alt_scores = {}
    unique_kriteria = df_alternatif['Kriteria'].unique()
    for crit in unique_kriteria:
        df_block = df_alternatif[df_alternatif['Kriteria'] == crit]

        # Validasi blok kriteria
        alt_cols = [c for c in df_block.columns if c.lower().startswith("a")]
        alt_ids = df_block['Kode Alternatif'].values

        # Pastikan matriks persegi
        if len(alt_ids) != len(alt_cols):
            raise ValueError(f"Jumlah baris dan kolom alternatif pada kriteria '{crit}' tidak seimbang. Matriks harus persegi.")

        mat_alt = df_block[alt_cols].to_numpy(dtype=float)
        alt_matrix = pd.DataFrame(mat_alt, index=alt_ids, columns=alt_cols)
        steps.append((f"Matriks Perbandingan Alternatif ({crit})", alt_matrix))

        # Normalisasi kolom & hitung bobot rata-rata
        col_sum = alt_matrix.sum(axis=0)
        norm = alt_matrix / col_sum
        w_alt = norm.mean(axis=1)

        steps.append((f"Normalisasi & Bobot Alternatif ({crit})", pd.DataFrame({
            "Normalisasi": norm.mean(axis=1),
            "Bobot": w_alt
        })))

        alt_scores[crit] = w_alt

    # 4️⃣ Hitung Skor Akhir & Perangkingan
    all_alts = sorted(list(df_alternatif['Kode Alternatif'].unique()))
    result = pd.DataFrame(index=all_alts)

    # Gabungkan semua skor alternatif ke dalam satu DataFrame
    for crit in alt_scores:
        result[crit] = alt_scores[crit].reindex(result.index, fill_value=0)

    # Menyamakan format kode kriteria (misal, C01 -> C1) untuk pencocokan
    weights.index = [i.replace("C0", "C") for i in weights.index]
    result.columns = [c.replace("C0", "C") for c in result.columns]

    # Pastikan hanya kriteria yang ada di bobot yang dihitung
    common_cols = [c for c in result.columns if c in weights.index]
    if not common_cols:
        raise ValueError("Tidak ada kriteria yang cocok antara bobot kriteria dan hasil alternatif.")
    
    # Ambil Nama Alternatif dari data input
    alt_names_map = df_alternatif.drop_duplicates(subset=['Kode Alternatif'])
    alt_names_map = dict(zip(alt_names_map['Kode Alternatif'], alt_names_map['Nama Alternatif']))

    # Hasil Skor Akhir berdasarkan bobot kriteria (hasil dari tahap kriteria)
    result["Skor Akhir"] = 0.0
    for c in common_cols:
        result["Skor Akhir"] += result[c] * weights[c]

    # Perhitungan bobot kriteria (rata-rata dari tahap kriteria)
    steps.append(("Rata-rata Bobot Kriteria (dari langkah 1)", pd.DataFrame(weights, columns=["Rata-rata Kriteria"])))

    # Urutkan hasil akhir berdasarkan skor
    result = result.sort_values("Skor Akhir", ascending=False)
    result["Ranking"] = np.arange(1, len(result) + 1)

    steps.append(("Hasil Akhir AHP", result))
    return steps, result.reset_index().rename(columns={'index': 'Alternatif'})

# ============================
# TOPSIS CALCULATION
# ============================
def calculate_topsis(criteria, alternatives):
    """Hitung metode TOPSIS"""
    steps = []
    
    # 1️⃣ Validasi Data
    if not criteria or not alternatives:
        raise ValueError("Kriteria atau alternatif kosong.")

    # 2️⃣ Matriks Keputusan Awal (X)
    matrix = np.array([[alt.values.get(crit.id, 0.0) for crit in criteria] for alt in alternatives], dtype=float)
    df_initial = pd.DataFrame(matrix, index=[alt.name or alt.id for alt in alternatives], columns=[f"{c.name} ({c.id})" for c in criteria])
    steps.append(("Matriks Keputusan Awal", df_initial))

    # 3️⃣ Normalisasi Matriks
    # Rumus: rij = xij / √(Σxij²)
    # Setiap kolom dinormalisasi agar tidak dipengaruhi skala nilai
    norm_denominators = np.sqrt(np.sum(matrix**2, axis=0))
    norm_denominators[norm_denominators == 0] = 1.0
    normalized_matrix = matrix / norm_denominators
    df_normalized = pd.DataFrame(normalized_matrix, index=[alt.name or alt.id for alt in alternatives], columns=[c.name for c in criteria])
    steps.append(("Matriks Ternormalisasi (rij = xij / √(Σxij²))", df_normalized))

    # 4️⃣ Matriks Ternormalisasi Terbobot
    # Rumus: y_ij = w_j * r_ij
    # Gunakan bobot yang sudah ternormalisasi
    total_weight = sum(c.weight for c in criteria)
    normalized_weights = [(c.weight / total_weight) if total_weight != 0 else (1.0/len(criteria)) for c in criteria]
    weighted_matrix = normalized_matrix * normalized_weights
    df_weighted = pd.DataFrame(weighted_matrix, index=[alt.name or alt.id for alt in alternatives], columns=[f"{c.name} (w={w:.3f})" for c, w in zip(criteria, normalized_weights)])
    steps.append(("Matriks Ternormalisasi Terbobot (yij = wj × rij)", df_weighted))

    # 5️⃣ Menentukan Solusi Ideal Positif (A+) dan Negatif (A-)
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

    # 6️⃣ Hitung Jarak Separasi
    # Rumus:
    # D+ = √Σ(y_ij - y_j+)²
    # D- = √Σ(y_ij - y_j-)²
    separation_positive = np.sqrt(np.sum((weighted_matrix - ideal_positive)**2, axis=1))
    separation_negative = np.sqrt(np.sum((weighted_matrix - ideal_negative)**2, axis=1))
    df_separation = pd.DataFrame({'D+ (Jarak ke A+)': separation_positive, 'D- (Jarak ke A-)': separation_negative}, index=[alt.name or alt.id for alt in alternatives])
    steps.append(("Jarak Separasi", df_separation))

    # 7️⃣ Hitung Nilai Kedekatan Relatif (V)
    # Rumus:
    # V_i = D- / (D+ + D-)
    closeness_denominator = separation_positive + separation_negative
    closeness = np.divide(separation_negative, closeness_denominator, out=np.zeros_like(separation_negative), where=closeness_denominator!=0)
    df_closeness = pd.DataFrame({'D+': separation_positive, 'D-': separation_negative, 'Skor V': closeness}, index=[alt.name or alt.id for alt in alternatives])
    steps.append(("Kedekatan Relatif (V = D- / (D+ + D-))", df_closeness))
    
    # 8️⃣ Perangkingan Akhir
    # Semakin tinggi nilai V → semakin dekat dengan solusi ideal → semakin baik
    ranking_data = sorted(zip([alt.name or alt.id for alt in alternatives], closeness), key=lambda x: x[1], reverse=True)
    df_ranking = pd.DataFrame([[name, score, rank+1] for rank, (name, score) in enumerate(ranking_data)], columns=['Alternatif', 'Skor Akhir', 'Ranking'])
    steps.append(("Hasil Perankingan", df_ranking))

    return steps, df_ranking

# ============================
# AHP MANUAL INPUT HELPERS
# ============================
def update_reciprocal(matrix_key, i, j):
    """Callback untuk memperbarui nilai timbal balik dalam matriks AHP."""
    try:
        val = st.session_state[f"{matrix_key}_{i}_{j}"]
        if val != 0:
            st.session_state[f"{matrix_key}_{j}_{i}_val"] = 1/val
    except (ValueError, ZeroDivisionError):
        pass # Biarkan jika input tidak valid

def prepare_ahp_dfs_from_manual():
    """Mempersiapkan DataFrame untuk AHP dari input manual di session_state."""
    # 1. Buat df_kriteria
    crit_ids = list(st.session_state.ahp_manual_crit_names.keys())
    crit_matrix_data = []
    for r_idx, r_id in enumerate(crit_ids):
        row_data = {'Kode Kriteria': r_id, 'Nama Kriteria': st.session_state.ahp_manual_crit_names[r_id], 'Atribut': 'benefit'}
        for c_idx, c_id in enumerate(crit_ids):
            key = f"ahp_crit_matrix_{r_idx}_{c_idx}"
            row_data[c_id] = st.session_state.get(key, 1.0)
        crit_matrix_data.append(row_data)
    df_kriteria = pd.DataFrame(crit_matrix_data)

    # 2. Buat df_alternatif
    alt_ids = list(st.session_state.ahp_manual_alt_names.keys())
    alt_dfs = []
    for crit_id in crit_ids:
        alt_matrix_data = []
        for r_idx, r_id in enumerate(alt_ids):
            row_data = {'Kode Alternatif': r_id, 'Nama Alternatif': st.session_state.ahp_manual_alt_names[r_id], 'Kriteria': crit_id}
            for c_idx, c_id in enumerate(alt_ids):
                key = f"ahp_alt_matrix_{crit_id}_{r_idx}_{c_idx}"
                row_data[c_id] = st.session_state.get(key, 1.0)
            alt_matrix_data.append(row_data)
        alt_dfs.append(pd.DataFrame(alt_matrix_data))
    df_alternatif = pd.concat(alt_dfs, ignore_index=True)
    
    return df_kriteria, df_alternatif

# ============================
# STREAMLIT UI
# ============================
def main():
    st.set_page_config(page_title="MCDM Calculator", layout="wide", page_icon="🎯")
    
    # Apply Custom CSS
    apply_custom_css()
    
    st.title("🎯 MCDM Calculator")
    
    st.markdown("**Multi-Criteria Decision Making** menggunakan metode Simple Additive Weighting (SAW), Weighted Product (WP), Analytical Hierarchy Process (AHP), dan Technique for Order Preference by Similarity to Ideal Solution (TOPSIS).")

    # Inisialisasi session state
    if 'criteria' not in st.session_state: st.session_state.criteria = []
    if 'alternatives' not in st.session_state: st.session_state.alternatives = []
    if 'ahp_manual_crit_names' not in st.session_state: st.session_state.ahp_manual_crit_names = {}
    if 'ahp_manual_alt_names' not in st.session_state: st.session_state.ahp_manual_alt_names = {}

    # Sidebar untuk pengaturan
    st.sidebar.header("⚙️ Pengaturan")
    method = st.sidebar.selectbox("Pilih Metode", ["Simple Additive Weighting (SAW)", "Weighted Product (WP)", "Analytical Hierarchy Process (AHP)", "Technique for Order Preference by Similarity to Ideal Solution (TOPSIS)"])
    st.sidebar.markdown("""
    <div class="sidebar-footer">
        © 2025 DSS 💜
        \nNazwa-140810230019 & Senia-140810230021
    </div>
    """, unsafe_allow_html=True)
    input_method = st.radio("Metode Input Data", ["Upload File (CSV/XLSX)", "Input Manual"], horizontal=True)

    is_ahp = "Analytical Hierarchy Process (AHP)" in method

    # ===========================
    # INPUT DATA - UPLOAD
    # ===========================
    if input_method == "Upload File (CSV/XLSX)":
        st.subheader("📁 Upload File")
        if is_ahp:
            st.info("""**Format File AHP:**
                    \n -**File Kriteria:** `Kode Kriteria`, `C01`,`C02`, ..., `Nama Kriteria`, `Atribut`
                    \n -**File Alternatif:** `Kode Alternatif`, `A01`, `A02`, ..., `Nama Alternatif`, `Kriteria`
                    \n Anda dapat mengunggah satu file Excel (dengan sheet terpisah) atau beberapa file CSV sekaligus.""")
        else:
            st.info("""**Format File SAW/WP/TOPSIS:**
                    \n -**File Kriteria:** `Kode Kriteria`, `Bobot`, `Nama Kriteria`, `Atribut (cost/benefit)`
                    \n -**File Alternatif:** `Kode Alternatif`, `C1`, `C2`, ..., `Nama Alternatif`
                    \n Anda dapat mengunggah satu file Excel (dengan sheet terpisah) atau beberapa file CSV sekaligus.""")
                

        uploaded_files = st.file_uploader("Pilih file CSV atau XLSX", type=['csv', 'xlsx', 'xls'], accept_multiple_files=True)

        if uploaded_files:
            df_criteria, df_alternatives = None, None
            for f in uploaded_files:
                try:
                    df_temp = pd.read_excel(f) if f.name.lower().endswith(('.xls', '.xlsx')) else pd.read_csv(f)
                    if is_ahp:
                        if "kriteria" in f.name.lower():
                            df_criteria = df_temp
                            st.success(f"✔️ File AHP kriteria terdeteksi: `{f.name}`")
                        elif "alternatif" in f.name.lower():
                            df_alternatives = df_temp
                            st.success(f"✔️ File AHP alternatif terdeteksi: `{f.name}`")
                        else: st.warning(f"⚠️ File `{f.name}` tidak dikenali sebagai file AHP valid!")
                    else:
                        if is_criteria_df(df_temp):
                            df_criteria = df_temp
                            st.success(f"✔️ File kriteria terdeteksi: `{f.name}`")
                        elif is_alternatives_df(df_temp):
                            df_alternatives = df_temp
                            st.success(f"✔️ File alternatif terdeteksi: `{f.name}`")
                        else: st.warning(f"⚠️ Tidak dapat mendeteksi jenis file `{f.name}`!")
                except Exception as e:
                    st.error(f"Gagal memuat file {f.name}: {e}")

            try:
                if is_ahp:
                    if df_criteria is not None and df_alternatives is not None:
                        st.session_state.df_ahp_criteria = df_criteria
                        st.session_state.df_ahp_alternatives = df_alternatives
                        st.success("✅ File AHP berhasil dimuat & disinkronkan ke Input Manual!")

                        # Sinkronisasi Kriteria ke state manual
                        crit_ids = df_criteria['Kode Kriteria'].tolist()
                        st.session_state.ahp_manual_crit_names = dict(zip(crit_ids, df_criteria['Nama Kriteria']))
                        for i, r_id in enumerate(crit_ids):
                            for j, c_id in enumerate(crit_ids):
                                value = df_criteria.loc[df_criteria['Kode Kriteria'] == r_id, c_id].iloc[0]
                                st.session_state[f"ahp_crit_matrix_{i}_{j}"] = float(value)

                        # Sinkronisasi Alternatif ke state manual
                        alt_ids = sorted(list(df_alternatives['Kode Alternatif'].unique()))
                        alt_names_map = df_alternatives.drop_duplicates(subset=['Kode Alternatif'])
                        alt_names_map = dict(zip(alt_names_map['Kode Alternatif'], alt_names_map['Nama Alternatif']))
                        st.session_state.ahp_manual_alt_names = {aid: alt_names_map.get(aid, f"Alt-{i+1}") for i, aid in enumerate(alt_ids)}
                        
                        for crit_id in df_alternatives['Kriteria'].unique():
                            df_block = df_alternatives[df_alternatives['Kriteria'] == crit_id].set_index('Kode Alternatif')
                            for i, r_id in enumerate(alt_ids):
                                for j, c_id in enumerate(alt_ids):
                                    st.session_state[f"ahp_alt_matrix_{crit_id}_{i}_{j}"] = float(df_block.loc[r_id, c_id])

                    else: st.warning("⚠️ Harap unggah kedua file: kriteria dan alternatif untuk AHP.")
                else:
                    criteria, alternatives = parse_data(df_alternatives, df_criteria)
                    st.session_state.criteria = criteria
                    st.session_state.alternatives = alternatives
                    if criteria and alternatives: st.success(f"✅ Data berhasil dimuat! Ditemukan {len(alternatives)} alternatif dan {len(criteria)} kriteria.")
                    elif criteria: st.info(f"✅ Kriteria dimuat ({len(criteria)}). Unggah file alternatif.")
                    elif alternatives: st.info(f"✅ Alternatif dimuat ({len(alternatives)}). Kriteria dibuat otomatis.")
            except Exception as e:
                st.error(f"❌ Terjadi kesalahan saat memproses data: {e}")
    # ===========================
    # INPUT DATA - MANUAL
    # ===========================       
    else:  
        st.subheader("✏️ Input Manual") 
        # --- UI MANUAL AHP ---
        if is_ahp:
            c1, c2 = st.columns(2)
            num_criteria = c1.number_input("Jumlah Kriteria", 1, 10, len(st.session_state.ahp_manual_crit_names) or 3)
            num_alternatives = c2.number_input("Jumlah Alternatif", 1, 20, len(st.session_state.ahp_manual_alt_names) or 3)

            crit_ids = [f"C{i+1}" for i in range(num_criteria)]
            alt_ids = [f"A{i+1}" for i in range(num_alternatives)]

            # Sinkronisasi nama kriteria & alternatif jika jumlah berubah
            if set(crit_ids) != set(st.session_state.ahp_manual_crit_names.keys()):
                st.session_state.ahp_manual_crit_names = {cid: f"Kriteria {i+1}" for i, cid in enumerate(crit_ids)}
            if set(alt_ids) != set(st.session_state.ahp_manual_alt_names.keys()):
                st.session_state.ahp_manual_alt_names = {aid: f"Alternatif {i+1}" for i, aid in enumerate(alt_ids)}

            # Bagian Input Nama Kriteria & Alternatif
            with st.expander("**1. Nama Kriteria & Alternatif**", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.write("**Nama Kriteria**")
                    for i, cid in enumerate(crit_ids):
                        st.session_state.ahp_manual_crit_names[cid] = st.text_input(f"Nama {cid}", st.session_state.ahp_manual_crit_names[cid], key=f"crit_name_{cid}")
                with c2:
                    st.write("**Nama Alternatif**")
                    for i, aid in enumerate(alt_ids):
                        st.session_state.ahp_manual_alt_names[aid] = st.text_input(f"Nama {aid}", st.session_state.ahp_manual_alt_names[aid], key=f"alt_name_{aid}")
            
            # Bagian Input Matriks Perbandingan Kriteria
            st.markdown("---")
            st.write("**2. Matriks Perbandingan Kriteria**")
            cols_h = st.columns([1.5] + [1] * num_criteria)
            for j, cid in enumerate(crit_ids):
                cols_h[j+1].markdown(f"**{st.session_state.ahp_manual_crit_names[cid]}**")
            for i, r_cid in enumerate(crit_ids):
                cols_r = st.columns([1.5] + [1] * num_criteria)
                cols_r[0].markdown(f"**{st.session_state.ahp_manual_crit_names[r_cid]}**")
                for j, c_cid in enumerate(crit_ids):
                    key = f"ahp_crit_matrix_{i}_{j}"
                    if i == j:
                        cols_r[j+1].number_input(key, value=1.0, disabled=True, label_visibility="collapsed")
                        st.session_state[key] = 1.0
                    else:
                        is_reciprocal = st.session_state.get(f"{key}_val") is not None and key not in st.session_state
                        value = st.session_state.get(f"{key}_val", st.session_state.get(key, 1.0))
                        cols_r[j+1].number_input(key, min_value=0.0, value=float(value), key=key, on_change=update_reciprocal, args=('ahp_crit_matrix', i, j), label_visibility="collapsed", disabled=is_reciprocal)

            # Bagian Input Matriks Perbandingan Alternatif per Kriteria
            st.markdown("---")
            st.write("**3. Matriks Perbandingan Alternatif (berdasarkan setiap Kriteria)**")
            tabs = st.tabs([name for name in st.session_state.ahp_manual_crit_names.values()])
            for i_crit, crit_id in enumerate(crit_ids):
                with tabs[i_crit]:
                    cols_h = st.columns([1.5] + [1] * num_alternatives)
                    for j, aid in enumerate(alt_ids):
                        cols_h[j+1].markdown(f"**{st.session_state.ahp_manual_alt_names[aid]}**")

                    for i, r_aid in enumerate(alt_ids):
                        cols_r = st.columns([1.5] + [1] * num_alternatives)
                        cols_r[0].markdown(f"**{st.session_state.ahp_manual_alt_names[r_aid]}**")
                        for j, c_aid in enumerate(alt_ids):
                            key = f"ahp_alt_matrix_{crit_id}_{i}_{j}"
                            if i == j:
                                cols_r[j+1].number_input(key, value=1.0, disabled=True, label_visibility="collapsed")
                                st.session_state[key] = 1.0
                            else:
                                matrix_key = f"ahp_alt_matrix_{crit_id}"
                                is_reciprocal = st.session_state.get(f"{key}_val") is not None and key not in st.session_state
                                value = st.session_state.get(f"{key}_val", st.session_state.get(key, 1.0))
                                cols_r[j+1].number_input(key, min_value=0.0, value=float(value), key=key, on_change=update_reciprocal, args=(matrix_key, i, j), label_visibility="collapsed", disabled=is_reciprocal)

        # --- UI MANUAL SAW/WP/TOPSIS ---
        else:
            # Bagian Input Kriteria & Alternatif
            num_criteria = st.number_input("Jumlah Kriteria", 1, 50, len(st.session_state.criteria) or 3)
            if len(st.session_state.criteria) != num_criteria:
                st.session_state.criteria = [Criterion(f"C{i+1}", f"Kriteria {i+1}", 1.0, 'benefit') for i in range(num_criteria)]

            # Bagian Input Kriteria
            cols_crit = st.columns(num_criteria)
            for i, crit in enumerate(st.session_state.criteria):
                with cols_crit[i]:
                    st.markdown(f"**Kriteria {i+1}**")
                    crit.id = f"C{i+1}"
                    crit.name = st.text_input("Nama", crit.name, key=f"crit_name_{i}")
                    crit.weight = st.number_input("Bobot", 0.0, value=float(crit.weight), key=f"crit_weight_{i}")
                    crit.attribute = st.selectbox("Atribut", ['benefit', 'cost'], index=0 if crit.attribute == 'benefit' else 1, key=f"crit_attr_{i}")
            
            # Bagian Input Alternatif
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
    # ===========================
    # PERIKSA APAKAH DATA SIAP & TAMPILKAN
    # ===========================
    data_is_ready = False
    if is_ahp:
        if (input_method == "Upload File (CSV/XLSX)" and "df_ahp_criteria" in st.session_state) or \
           (input_method == "Input Manual" and st.session_state.ahp_manual_crit_names):
            data_is_ready = True
    elif st.session_state.criteria and st.session_state.alternatives:
        data_is_ready = True

    if data_is_ready:
        st.markdown("---")
        st.subheader("📊 Data Saat Ini")
        # --- AHP ---
        if is_ahp: 
            df_crit_display, df_alt_display = None, None
            if input_method == "Input Manual":
                df_crit_display, df_alt_display = prepare_ahp_dfs_from_manual()
            elif "df_ahp_criteria" in st.session_state:
                df_crit_display = st.session_state.df_ahp_criteria
                df_alt_display = st.session_state.df_ahp_alternatives
            
            if df_crit_display is not None and df_alt_display is not None:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Matriks Perbandingan Kriteria:**")
                    st.dataframe(df_crit_display, use_container_width=True, hide_index=True)
                with col2:
                    st.markdown("**Matriks Perbandingan Alternatif:**")
                    st.dataframe(df_alt_display, use_container_width=True, hide_index=True)
        # --- SAW/WP/TOPSIS ---
        else: 
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Kriteria:**")
                df_crit_display = pd.DataFrame([{'ID': c.id, 'Nama': c.name, 'Bobot': c.weight, 'Atribut': c.attribute} for c in st.session_state.criteria])
                st.dataframe(df_crit_display, use_container_width=True, hide_index=True)
            with col2:
                st.markdown("**Alternatif:**")
                df_alt_display_data = [{'Nama': alt.name or alt.id, **{c.name: alt.values.get(c.id, 0.0) for c in st.session_state.criteria}} for alt in st.session_state.alternatives]
                st.dataframe(pd.DataFrame(df_alt_display_data), use_container_width=True, hide_index=True)
        
        # ===========================
        # TOMBOL HITUNG & TAMPILKAN HASIL
        # ===========================
        st.markdown("---")
        if st.button("🚀 Hitung Ranking", type="primary", use_container_width=True):
            with st.spinner("Menghitung..."):
                try:
                    steps, ranking = [], pd.DataFrame()
                    if method == "Simple Additive Weighting (SAW)":
                        steps, ranking = calculate_saw(st.session_state.criteria, st.session_state.alternatives)
                    elif method == "Weighted Product (WP)":
                        steps, ranking = calculate_wp(st.session_state.criteria, st.session_state.alternatives)
                    elif method == "Technique for Order Preference by Similarity to Ideal Solution (TOPSIS)":
                        steps, ranking = calculate_topsis(st.session_state.criteria, st.session_state.alternatives)
                    elif method == "Analytical Hierarchy Process (AHP)":
                        df_crit, df_alt = None, None
                        if input_method == "Input Manual":
                            df_crit, df_alt = prepare_ahp_dfs_from_manual()
                        elif "df_ahp_criteria" in st.session_state and "df_ahp_alternatives" in st.session_state:
                             df_crit, df_alt = st.session_state.df_ahp_criteria, st.session_state.df_ahp_alternatives
                        
                        if df_crit is not None and df_alt is not None:
                            steps, ranking = calculate_ahp(df_crit, df_alt)
                        else:
                            st.warning("⚠️ Data AHP belum lengkap. Harap isi atau unggah data.")
                            st.stop()
                    
                    st.success("✅ Perhitungan selesai!")
                    st.markdown("---")
                    st.header("🏆 Hasil Akhir")

                    def highlight_top3(row):
                        color = ''
                        if row.Ranking == 1: color = 'background-color: #35166E'
                        elif row.Ranking == 2: color = 'background-color: #6834D4'
                        elif row.Ranking == 3: color = 'background-color: #AF93D7'
                        return [color] * len(row)

                    st.dataframe(
                        ranking.style.apply(highlight_top3, axis=1).format({ranking.columns[1]: "{:.4f}"}),
                        use_container_width=True, hide_index=True
                    )

                    st.markdown("---")
                    st.header("📝 Langkah Perhitungan")
                    for title, df in steps:
                        with st.expander(title): st.dataframe(df, use_container_width=True)

                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan saat menghitung: {e}")

# ============================
# MAIN ENTRY POINT
# ============================
if __name__ == "__main__":
    main()
