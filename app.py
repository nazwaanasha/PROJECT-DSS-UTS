import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

# ==================== DATA TYPES ====================
class Criterion:
    def __init__(self, id, name, weight, attribute):
        self.id = id
        self.name = name
        self.weight = weight
        self.attribute = attribute  # 'benefit' or 'cost'

class Alternative:
    def __init__(self, id, name, values):
        self.id = id
        self.name = name
        self.values = values  # dict: {criterion_id: value}

# ==================== AUTO DETECTION HELPERS ====================
def is_criteria_df(df: pd.DataFrame):
    """Return True if dataframe looks like a criteria sheet (has 'Bobot' or 'Weight' column or 'Atribut')."""
    cols = [c.lower() for c in df.columns]
    if 'bobot' in cols or 'weight' in cols or 'atribut' in cols or 'attribute' in cols:
        return True
    # if first column is 'kriteria' or 'criteria' or 'criterion'
    first = cols[0]
    if first in ('kriteria', 'kriteria ', 'criteria', 'criterion', 'kriteria_name', 'nama kriteria', 'nama'):
        return True
    return False

def is_alternatives_df(df: pd.DataFrame):
    """Return True if dataframe looks like an alternatives sheet (first col is name and other cols numeric)."""
    if df.shape[1] < 2:
        return False
    # If first column name suggests alternative
    first_col = str(df.columns[0]).lower()
    if first_col in ('alternatif', 'alternative', 'nama', 'nama alternatif', 'alt', 'nama_alt'):
        return True
    # Heuristic: check if at least half of remaining columns are numeric-like
    numeric_counts = 0
    for c in df.columns[1:]:
        # try convert sample values
        vals = pd.to_numeric(df[c].dropna(), errors='coerce')
        numeric_counts += vals.notna().sum()
    total_vals = sum(len(df[c].dropna()) for c in df.columns[1:])
    if total_vals == 0:
        return False
    # if a majority of non-null values are numeric -> alternative matrix likely
    return (numeric_counts / total_vals) > 0.6

# Normalize column name helper
def norm_col(s):
    return str(s).strip()

# ==================== FILE PARSER ====================
def parse_excel(file):
    xls = pd.ExcelFile(file)
    df = pd.read_excel(xls, sheet_name=xls.sheet_names[0])  # ambil 1 sheet

    # cek apakah ada baris "Bobot" atau "Atribut"
    lower_df = df.applymap(lambda x: str(x).lower() if isinstance(x, str) else x)
    weight_row = lower_df[lower_df.iloc[:, 0].str.contains("bobot", na=False)]
    attr_row = lower_df[lower_df.iloc[:, 0].str.contains("atribut", na=False)]

    if not weight_row.empty or not attr_row.empty:
        # misahin alternatif dan kriteria
        alt_df = df.iloc[:weight_row.index[0], :]
        crit_names = list(df.columns[1:])
        bobot = list(weight_row.iloc[0, 1:])
        attr = list(attr_row.iloc[0, 1:]) if not attr_row.empty else ['benefit'] * len(bobot)

        crit_df = pd.DataFrame({
            'Kriteria': crit_names,
            'Bobot': bobot,
            'Atribut': attr
        })
        return parse_data(alt_df, crit_df)
    else:
        # fallback ke mode lama
        return parse_data(df, None)

def parse_csv(file):
    """Parse CSV file or multiple CSVs: streamlit may pass a single file object."""
    df = pd.read_csv(file)
    if is_criteria_df(df):
        return parse_data(None, df)
    elif is_alternatives_df(df):
        return parse_data(df, None)
    else:
        # fallback try to treat as alternatives
        return parse_data(df, None)

def parse_data(df_alt, df_crit=None):
    """Parse dataframes into Criterion and Alternative objects.
    Accepts df_alt or df_crit possibly being None.
    """
    criteria = []
    alternatives = []

    # ----- Parse criteria DF if provided -----
    if df_crit is not None:
        # Normalize columns to find likely columns: name, weight, attribute
        cols = [c.lower() for c in df_crit.columns]
        # heuristics for which column is which
        def find_col(possible):
            for p in possible:
                for i, c in enumerate(cols):
                    if p == c:
                        return df_crit.columns[i]
            return None

        name_col = find_col(['kriteria', 'criteria', 'criterion', 'nama', 'nama kriteria'])
        weight_col = find_col(['bobot', 'weight'])
        attribute_col = find_col(['atribut', 'attribute', 'attr', 'tipe'])
        # if weight missing, try second column by position
        if weight_col is None and df_crit.shape[1] >= 2:
            weight_col = df_crit.columns[1]
        if name_col is None:
            # if no clear name col, use first column
            name_col = df_crit.columns[0]
        # Build criteria list
        for idx, row in df_crit.iterrows():
            raw_name = row.get(name_col, None)
            if pd.isna(raw_name):
                continue
            crit_name = str(raw_name).strip()
            # weight parsing
            raw_w = None
            if weight_col is not None:
                raw_w = row.get(weight_col, None)
            try:
                weight = float(raw_w)
            except Exception:
                weight = 1.0
            # attribute parsing
            raw_attr = None
            if attribute_col is not None:
                raw_attr = row.get(attribute_col, '')
            attr = 'cost' if str(raw_attr).strip().lower() == 'cost' else 'benefit'
            crit_id = f"c{len(criteria)+1}"
            criteria.append(Criterion(crit_id, crit_name, weight, attr))

    # ----- Parse alternatives DF if provided -----
    if df_alt is not None:
        # assume first column is alternative name
        df_alt = df_alt.copy()
        df_alt.columns = [norm_col(c) for c in df_alt.columns]
        alt_name_col = df_alt.columns[0]
        # If no criteria from df_crit, take header names as criteria
        if not criteria:
            crit_names = [norm_col(c) for c in df_alt.columns[1:]]
            for i, name in enumerate(crit_names):
                criteria.append(Criterion(f"c{i+1}", str(name), 1.0, 'benefit'))
        # Build mapping from column name -> criterion id
        # We'll match by name if possible (case-insensitive); otherwise by order
        col_to_critid = {}
        critname_to_id = {c.name.strip().lower(): c.id for c in criteria}
        # attempt match for each data column (from df_alt)
        for i, col in enumerate(df_alt.columns[1:]):
            col_norm = str(col).strip().lower()
            if col_norm in critname_to_id:
                col_to_critid[col] = critname_to_id[col_norm]
            else:
                # fallback assign by order if available
                if i < len(criteria):
                    col_to_critid[col] = criteria[i].id
                else:
                    # create a new criterion if extra column present
                    new_id = f"c{len(criteria)+1}"
                    new_name = str(col)
                    criteria.append(Criterion(new_id, new_name, 1.0, 'benefit'))
                    col_to_critid[col] = new_id

        # Now parse alternative rows
        for idx, row in df_alt.iterrows():
            alt_name = row.get(alt_name_col, f"Alternatif {idx+1}")
            alt_name = str(alt_name)
            values = {}
            for col in df_alt.columns[1:]:
                crit_id = col_to_critid.get(col)
                raw = row.get(col, np.nan)
                try:
                    val = float(raw)
                except Exception:
                    # try convert comma decimal
                    if isinstance(raw, str):
                        raw2 = raw.replace(',', '.')
                        try:
                            val = float(raw2)
                        except Exception:
                            val = 0.0
                    else:
                        val = 0.0
                values[crit_id] = val
            alternatives.append(Alternative(f"alt-{len(alternatives)+1}", alt_name, values))

    # ----- If only criteria provided, no alternatives - return criteria and empty alternatives -----
    # ----- If only alternatives provided, criteria already built above -----
    return criteria, alternatives

# ==================== WP CALCULATION ====================
def calculate_wp(criteria, alternatives):
    """Calculate Weighted Product method"""
    steps = []

    if not criteria or not alternatives:
        raise ValueError("Kriteria atau alternatif kosong. Pastikan data sudah lengkap.")

    # Step 1: Initial Decision Matrix
    matrix = []
    for alt in alternatives:
        row = [alt.values.get(crit.id, 0.0) for crit in criteria]
        matrix.append(row)

    df_initial = pd.DataFrame(
        matrix,
        index=[alt.name for alt in alternatives],
        columns=[f"{c.name} ({c.weight})" for c in criteria]
    )
    steps.append(("Matriks Keputusan Awal", df_initial))

    # Step 2: Normalize weights
    total_weight = sum(c.weight for c in criteria)
    if total_weight == 0:
        normalized_weights = [1.0 / len(criteria) for _ in criteria]
    else:
        normalized_weights = [c.weight / total_weight for c in criteria]

    df_norm_weights = pd.DataFrame(
        [normalized_weights],
        index=['Bobot Ternormalisasi'],
        columns=[c.name for c in criteria]
    )
    steps.append(("Normalisasi Bobot", df_norm_weights))

    # Step 3: Adjust weights for cost criteria
    adjusted_weights = [
        -w if criteria[i].attribute == 'cost' else w
        for i, w in enumerate(normalized_weights)
    ]

    df_adj_weights = pd.DataFrame(
        [adjusted_weights],
        index=['Bobot Disesuaikan'],
        columns=[f"{c.name} ({c.attribute})" for c in criteria]
    )
    steps.append(("Penyesuaian Bobot (Cost = Negatif)", df_adj_weights))

    # Step 4: Calculate S values
    s_values = []
    for alt in alternatives:
        product = 1.0
        for i, crit in enumerate(criteria):
            value = alt.values.get(crit.id, 0.0)
            # avoid negative/zero issues: if value <= 0 and power not 0, set small positive
            if value <= 0:
                value = 1e-9
            power = adjusted_weights[i]
            product *= (value ** power)
        s_values.append(product)

    matrix_s = []
    for i, alt in enumerate(alternatives):
        row = [alt.values.get(crit.id, 0.0) for crit in criteria] + [s_values[i]]
        matrix_s.append(row)

    df_s = pd.DataFrame(
        matrix_s,
        index=[alt.name for alt in alternatives],
        columns=[c.name for c in criteria] + ['Nilai S']
    )
    steps.append(("Perhitungan Nilai S (S = ∏(xij^wj))", df_s))

    # Step 5: Calculate V values (preference)
    total_s = sum(s_values)
    if total_s == 0:
        v_values = [1.0/len(s_values) for _ in s_values]
    else:
        v_values = [s / total_s for s in s_values]

    df_v = pd.DataFrame(
        [[s_values[i], v_values[i]] for i in range(len(alternatives))],
        index=[alt.name for alt in alternatives],
        columns=['Nilai S', 'Nilai V (Skor)']
    )
    steps.append(("Perhitungan Nilai V (V = S / ΣS)", df_v))

    # Step 6: Ranking
    ranking = [(alternatives[i].name, v_values[i]) for i in range(len(alternatives))]
    ranking.sort(key=lambda x: x[1], reverse=True)

    df_ranking = pd.DataFrame(
        [[name, score, rank+1] for rank, (name, score) in enumerate(ranking)],
        columns=['Alternatif', 'Skor Akhir', 'Ranking']
    )
    steps.append(("Hasil Perankingan", df_ranking))

    return steps, df_ranking

# ==================== TOPSIS CALCULATION ====================
def calculate_topsis(criteria, alternatives):
    """Calculate TOPSIS method"""
    steps = []

    if not criteria or not alternatives:
        raise ValueError("Kriteria atau alternatif kosong. Pastikan data sudah lengkap.")

    # Step 1: Initial Decision Matrix
    matrix = []
    for alt in alternatives:
        row = [alt.values.get(crit.id, 0.0) for crit in criteria]
        matrix.append(row)

    df_initial = pd.DataFrame(
        matrix,
        index=[alt.name for alt in alternatives],
        columns=[f"{c.name} ({c.weight})" for c in criteria]
    )
    steps.append(("Matriks Keputusan Awal", df_initial))

    # Step 2: Normalize matrix (vector normalization)
    matrix_np = np.array(matrix, dtype=float)
    column_sums = np.sqrt(np.sum(matrix_np**2, axis=0))
    # avoid division by zero
    column_sums[column_sums == 0] = 1.0
    normalized_matrix = matrix_np / column_sums

    df_normalized = pd.DataFrame(
        normalized_matrix,
        index=[alt.name for alt in alternatives],
        columns=[c.name for c in criteria]
    )
    steps.append(("Matriks Ternormalisasi (rij = xij / √(Σxij²))", df_normalized))

    # Step 3: Weighted normalized matrix
    total_weight = sum(c.weight for c in criteria)
    if total_weight == 0:
        normalized_weights = [1.0/len(criteria) for _ in criteria]
    else:
        normalized_weights = [c.weight / total_weight for c in criteria]

    weighted_matrix = normalized_matrix * normalized_weights

    df_weighted = pd.DataFrame(
        weighted_matrix,
        index=[alt.name for alt in alternatives],
        columns=[f"{c.name} (w={normalized_weights[i]:.3f})" for i, c in enumerate(criteria)]
    )
    steps.append(("Matriks Ternormalisasi Terbobot (yij = wj × rij)", df_weighted))

    # Step 4: Determine ideal solutions
    ideal_positive = []
    ideal_negative = []

    for j, crit in enumerate(criteria):
        col = weighted_matrix[:, j]
        if crit.attribute == 'benefit':
            ideal_positive.append(np.max(col))
            ideal_negative.append(np.min(col))
        else:  # cost
            ideal_positive.append(np.min(col))
            ideal_negative.append(np.max(col))

    df_ideal = pd.DataFrame(
        [ideal_positive, ideal_negative],
        index=['A+ (Ideal Positif)', 'A- (Ideal Negatif)'],
        columns=[f"{c.name} ({c.attribute})" for c in criteria]
    )
    steps.append(("Solusi Ideal", df_ideal))

    # Step 5: Calculate separation measures
    separation_positive = []
    separation_negative = []

    for i in range(len(alternatives)):
        d_plus = np.sqrt(np.sum((weighted_matrix[i] - ideal_positive)**2))
        d_minus = np.sqrt(np.sum((weighted_matrix[i] - ideal_negative)**2))
        separation_positive.append(d_plus)
        separation_negative.append(d_minus)

    df_separation = pd.DataFrame(
        [[separation_positive[i], separation_negative[i]] for i in range(len(alternatives))],
        index=[alt.name for alt in alternatives],
        columns=['D+ (Jarak ke A+)', 'D- (Jarak ke A-)']
    )
    steps.append(("Jarak Separasi", df_separation))

    # Step 6: Calculate relative closeness
    closeness = [
        separation_negative[i] / (separation_positive[i] + separation_negative[i])
        for i in range(len(alternatives))
    ]

    df_closeness = pd.DataFrame(
        [[separation_positive[i], separation_negative[i], closeness[i]] for i in range(len(alternatives))],
        index=[alt.name for alt in alternatives],
        columns=['D+', 'D-', 'Skor C']
    )
    steps.append(("Kedekatan Relatif (C = D- / (D+ + D-))", df_closeness))

    # Step 7: Ranking
    ranking = [(alternatives[i].name, closeness[i]) for i in range(len(alternatives))]
    ranking.sort(key=lambda x: x[1], reverse=True)

    df_ranking = pd.DataFrame(
        [[name, score, rank+1] for rank, (name, score) in enumerate(ranking)],
        columns=['Alternatif', 'Skor Akhir', 'Ranking']
    )
    steps.append(("Hasil Perankingan", df_ranking))

    return steps, df_ranking

# ==================== STREAMLIT UI ====================
def main():
    st.set_page_config(page_title="MCDM Calculator", layout="wide")
    st.title("🎯 MCDM Calculator (WP & TOPSIS)")
    st.markdown("**Multi-Criteria Decision Making** menggunakan metode Weighted Product dan TOPSIS")

    # Initialize session state
    if 'criteria' not in st.session_state:
        st.session_state.criteria = []
    if 'alternatives' not in st.session_state:
        st.session_state.alternatives = []

    # Sidebar for method selection
    st.sidebar.header("Pengaturan")
    method = st.sidebar.selectbox("Pilih Metode", ["Weighted Product (WP)", "TOPSIS"])

    # Input method selection
    input_method = st.radio("Metode Input Data", ["Upload File (CSV/XLSX)", "Input Manual"], horizontal=True)

    if input_method == "Upload File (CSV/XLSX)":
        st.subheader("📁 Upload File")
        st.info("""
        **Format File:**
        - **Sheet Alternatif (atau CSV):** Alternatif | C1 | C2 | C3 | ...
        - **Sheet Kriteria (opsional):** Kriteria | Bobot | Keterangan | Atribut (cost/benefit)
        
        Kamu bisa unggah:
        - 1 file Excel (sheet1=alternatif, sheet2=kriteria), atau
        - 1 file CSV (alternatif atau kriteria), atau
        - beberapa file sekaligus (mis. alternatif.csv + kriteria.csv).
        """)
        uploaded_files = st.file_uploader("Pilih file CSV atau XLSX (boleh multiple)", type=['csv', 'xlsx', 'xls'], accept_multiple_files=True)

        if uploaded_files:
            # reset
            combined_criteria = None
            combined_alts = None
            # try parse each file and merge
            for f in uploaded_files:
                try:
                    name = f.name.lower()
                    if name.endswith(('.xls', '.xlsx')):
                        crits, alts = parse_excel(f)
                    else:
                        # csv
                        crits, alts = parse_csv(f)
                    # merge criteria
                    if crits:
                        if combined_criteria is None:
                            combined_criteria = crits
                        else:
                            # append any new criteria names that don't exist yet
                            existing_names = [c.name.strip().lower() for c in combined_criteria]
                            for c in crits:
                                if c.name.strip().lower() not in existing_names:
                                    new_id = f"c{len(combined_criteria)+1}"
                                    combined_criteria.append(Criterion(new_id, c.name, c.weight, c.attribute))
                    # merge alternatives
                    if alts:
                        if combined_alts is None:
                            combined_alts = alts
                        else:
                            # append alternatives
                            for a in alts:
                                combined_alts.append(a)
                except Exception as e:
                    st.error(f"Error parsing {f.name}: {e}")

            # if only criteria present
            if combined_criteria is not None and combined_alts is None:
                st.session_state.criteria = combined_criteria
                st.session_state.alternatives = []
                st.success(f"✅ Kriteria terdeteksi: {len(combined_criteria)}. Silakan input alternatif manual atau upload file alternatif.")
            elif combined_alts is not None and combined_criteria is None:
                # criteria not provided, parse from alt headers
                crits_from_alt, _ = parse_data(pd.DataFrame([a.values for a in combined_alts]), None) if False else None
                # safer: rebuild criteria from alt columns (we already build in parse_data when given alt_df)
                # But since parse_csv returned criteria when alt only, let's reconstruct from first alt
                # We'll extract criteria ids from first alt
                if len(combined_alts) > 0:
                    # build criteria from keys of first alt
                    keys = list(combined_alts[0].values.keys())
                    new_criteria = []
                    for i, k in enumerate(keys):
                        new_criteria.append(Criterion(f"c{i+1}", f"Kriteria {i+1}", 1.0, 'benefit'))
                    # Map values of alternatives to these criteria ids if needed
                    # (they already use c1.. format from parse_data)
                    st.session_state.criteria = new_criteria
                st.session_state.alternatives = combined_alts
                st.success(f"✅ Alternatif terdeteksi: {len(combined_alts)} alternatif. Kriteria dibuat otomatis dari header.")
            else:
                # both present
                st.session_state.criteria = combined_criteria or []
                st.session_state.alternatives = combined_alts or []
                st.success(f"✅ File berhasil dimuat! {len(st.session_state.alternatives)} alternatif, {len(st.session_state.criteria)} kriteria")
    else:  # Manual Input
        st.subheader("✏️ Input Manual")

        # Criteria input
        st.markdown("#### Kriteria")
        num_criteria = st.number_input("Jumlah Kriteria", min_value=1, max_value=50, value=len(st.session_state.criteria) or 3)

        if len(st.session_state.criteria) != num_criteria:
            st.session_state.criteria = [
                Criterion(f"c{i+1}", f"Kriteria {i+1}", 1.0, 'benefit')
                for i in range(num_criteria)
            ]

        for i, crit in enumerate(st.session_state.criteria):
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                crit.name = st.text_input(f"Nama C{i+1}", value=crit.name, key=f"crit_name_{i}")
            with col2:
                crit.weight = st.number_input(f"Bobot C{i+1}", min_value=0.0, value=float(crit.weight), key=f"crit_weight_{i}")
            with col3:
                crit.attribute = st.selectbox(f"Atribut C{i+1}", ['benefit', 'cost'], index=0 if crit.attribute == 'benefit' else 1, key=f"crit_attr_{i}")

        # Alternatives input
        st.markdown("#### Alternatif")
        num_alternatives = st.number_input("Jumlah Alternatif", min_value=1, max_value=200, value=len(st.session_state.alternatives) or 3)

        if len(st.session_state.alternatives) != num_alternatives:
            st.session_state.alternatives = [
                Alternative(f"alt-{i+1}", f"Alternatif {i+1}", {c.id: 0.0 for c in st.session_state.criteria})
                for i in range(num_alternatives)
            ]

        # Create table for alternatives
        for i, alt in enumerate(st.session_state.alternatives):
            cols = st.columns([2] + [1] * len(st.session_state.criteria))
            with cols[0]:
                alt.name = st.text_input(f"Nama Alt {i+1}", value=alt.name, key=f"alt_name_{i}")

            for j, crit in enumerate(st.session_state.criteria):
                with cols[j+1]:
                    alt.values[crit.id] = st.number_input(
                        crit.name,
                        value=float(alt.values.get(crit.id, 0.0)),
                        key=f"alt_val_{i}_{j}",
                        label_visibility="collapsed"
                    )

    # Display current data
    if st.session_state.criteria and st.session_state.alternatives:
        st.markdown("---")
        st.subheader("📊 Data Saat Ini")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Kriteria:**")
            df_crit = pd.DataFrame([
                {
                    'ID': c.id,
                    'Nama': c.name,
                    'Bobot': c.weight,
                    'Atribut': c.attribute
                }
                for c in st.session_state.criteria
            ])
            st.dataframe(df_crit, use_container_width=True)

        with col2:
            st.markdown("**Alternatif:**")
            df_alt = pd.DataFrame([
                {'Nama': alt.name, **{c.name: alt.values.get(c.id, 0.0) for c in st.session_state.criteria}}
                for alt in st.session_state.alternatives
            ])
            st.dataframe(df_alt, use_container_width=True)

        # Calculate button
        st.markdown("---")
        if st.button("🚀 Hitung Ranking", type="primary", use_container_width=True):
            with st.spinner("Menghitung..."):
                try:
                    if method == "Weighted Product (WP)":
                        steps, ranking = calculate_wp(st.session_state.criteria, st.session_state.alternatives)
                    else:
                        steps, ranking = calculate_topsis(st.session_state.criteria, st.session_state.alternatives)

                    st.success("✅ Perhitungan selesai!")

                    # Display calculation steps
                    st.markdown("---")
                    st.header("📝 Langkah Perhitungan")

                    for title, df in steps:
                        with st.expander(title, expanded=(title == "Hasil Perankingan")):
                            st.dataframe(df, use_container_width=True)

                    # Display final ranking with styling
                    st.markdown("---")
                    st.header("🏆 Hasil Akhir")

                    # Highlight top 3
                    def highlight_top3(row):
                        if row['Ranking'] == 1:
                            return ['background-color: #FFD700'] * len(row)
                        elif row['Ranking'] == 2:
                            return ['background-color: #C0C0C0'] * len(row)
                        elif row['Ranking'] == 3:
                            return ['background-color: #CD7F32'] * len(row)
                        return [''] * len(row)

                    st.dataframe(
                        ranking.style.apply(highlight_top3, axis=1),
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan saat menghitung: {e}")

    else:
        st.info("Silakan upload file atau input manual kriteria dan alternatif terlebih dahulu.")

if __name__ == "__main__":
    main()
