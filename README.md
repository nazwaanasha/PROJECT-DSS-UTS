# 🧠 Decision Support System (DSS) - Multi Criteria Decision Making (MCDM)
---
Nazwa Nashatasya   -   140810230019
Senia Nur Hasanah   -   140810230021

---
## 🪄 Deskripsi Singkat
Aplikasi **Sistem Pendukung Keputusan (Decision Support System / DSS)** ini membantu pengguna dalam melakukan **Multi Criteria Decision Making (MCDM)** menggunakan beberapa metode populer, yaitu:

- **Simple Additive Weighting (SAW)**
- **Weighted Product (WP)**
- **Analytical Hierarchy Process (AHP)**
- **Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS)**

Aplikasi ini dibangun menggunakan **Streamlit**, sehingga dapat dijalankan secara interaktif melalui browser dan memudahkan pengguna dalam menganalisis alternatif berdasarkan kriteria yang ditentukan.

---

## 🧭 Panduan Penggunaan Aplikasi

### 1️⃣ Pilih Metode
Di panel **sidebar kiri**, pengguna akan menemukan pilihan **“Pilih Metode”**.  
Tersedia empat metode **MCDM**, yaitu:

- `Simple Additive Weighting (SAW)`
- `Weighted Product (WP)`
- `Analytical Hierarchy Process (AHP)`
- `TOPSIS`

> Pilih salah satu metode untuk digunakan dalam proses perhitungan.

---

### 2️⃣ Pilih Metode Input Data
Masih di **sidebar**, pilih cara input data:

- **Upload File (CSV/XLSX)** → jika data sudah disiapkan dalam file spreadsheet.  
- **Input Manual** → jika ingin mengetikkan nilai langsung di dalam aplikasi.

---

### 3️⃣ Struktur Data Input
Setiap metode membutuhkan format file yang berbeda agar sistem dapat membaca data dengan benar.

---

#### 🟢 Untuk SAW, WP, dan TOPSIS
Metode ini membutuhkan **dua file**, yaitu:
Format File SAW/WP/TOPSIS:

-File Kriteria: Kode Kriteria, Bobot, Nama Kriteria, Atribut (cost/benefit)

-File Alternatif: Kode Alternatif, C1, C2, ..., dst.


#### 1. File Kriteria
Format contoh:

| Kode Kriteria | Bobot | Nama Kriteria | Atribut |
| -------------- | ------ | -------------- | -------- |
| C1             | 0.4    | Harga          | cost     |
| C2             | 0.3    | Kualitas       | benefit  |
| C3             | 0.3    | Pelayanan      | benefit  |

#### 2. File Alternatif
Format contoh:

| Kode Alternatif | C1   | C2 | C3 |
| ---------------- | ---- | -- | -- |
| A1               | 2000 | 7  | 8  |
| A2               | 1800 | 6  | 7  |
| A3               | 2200 | 8  | 9  |

---

#### 🔵 Untuk AHP
Metode AHP memerlukan **dua file**, yaitu:

1. **File Perbandingan Antar Kriteria**  
   Digunakan untuk menentukan seberapa penting satu kriteria dibandingkan yang lain.  
   Format contoh:
   
| Kode Kriteria | C01   | C02 | C03 | C04   | C05 | Nama Kriteria          | Atribut |
| ------------- | ----- | --- | --- | ----- | --- | ---------------------- | ------- |
| C01           | 1     | 1   | 3   | 1     | 3   | Jarak ke kos mahasiswa | Benefit |
| C02           | 1     | 1   | 2   | 1     | 1   | Jarak ke kampus        | Benefit |
| C03           | 0.333 | 0.5 | 1   | 1     | 2   | Jarak ke pujasera      | Benefit |
| C04           | 1     | 1   | 1   | 1     | 1   | Biaya                  | Cost    |
| C05           | 0.333 | 1   | 0.5 | 0.333 | 1   | Luas bangunan          | Benefit |


3. **File Perbandingan Antar Alternatif (per Kriteria)**  
   Menentukan nilai perbandingan antar alternatif terhadap setiap kriteria.  
   Format contoh:
   
| Kode Alternatif | A01   | A02   | A03 | Nama Alternatif | Kriteria |
| --------------- | ----- | ----- | --- | --------------- | -------- |
| A01             | 1     | 3     | 3   | Lokasi 1        | C01      |
| A02             | 0.333 | 1     | 2   | Lokasi 2        | C01      |
| A03             | 0.333 | 0.5   | 1   | Lokasi 3        | C01      |
| A01             | 1     | 2     | 4   | Lokasi 1        | C02      |
| A02             | 0.5   | 1     | 3   | Lokasi 2        | C02      |
| A03             | 0.25  | 0.333 | 1   | Lokasi 3        | C02      |

---

### 4️⃣ Proses Perhitungan
Setelah file diunggah atau data diinput secara manual:

- Aplikasi akan **membaca data otomatis** dan menampilkan **matriks normalisasi**.
- Setelah data terbaca, klik tombol **Hitung Ranking** untuk memproses pertihungannya.
- Hasil Akhir dan langkah perhitungannya dapat dilihat ketika muncul **Perhitungan Selesai**.
- Setiap metode memiliki langkah perhitungan berbeda:

| Metode | Langkah Utama |
| ------- | -------------- |
| **SAW** | Normalisasi nilai dan penjumlahan bobot untuk tiap alternatif. |
| **WP** | Perkalian nilai kriteria yang dipangkatkan dengan bobot. |
| **AHP** | Menghitung eigenvector, konsistensi rasio (CR), dan bobot kriteria. |
| **TOPSIS** | Menghitung jarak positif/negatif dan nilai preferensi (V). |

---

### 5️⃣ Hasil dan Visualisasi
- Setelah proses selesai, hasil akan muncul dalam bentuk **Hasil Akhir**.
- Dilengkapi dengan proses setiap **Langkah Perhitungan** hingga hasil akhir metodenya masing-masing.
---

## 🧩 Contoh Alur Penggunaan
1. Di sidebar, pilih salah satu metode yang ingin digunakan, misalnya metode **SAW**.
3. Upload dua file: `kriteria.csv` dan `alternatif.csv`.
4. Klik tombol **Hitung Ranking**.
5. Lihat hasil ranking dan langkah perhitungannya di halaman utama.

---

## 🎨 Tampilan Aplikasi
Aplikasi menggunakan tampilan modern dengan **CSS eksternal** (`style.css`).
