🧠 Decision Support System (DSS) - Multi Criteria Decision Making (MCDM)
🪄 Deskripsi Singkat

Aplikasi Sistem Pendukung Keputusan (Decision Support System / DSS) ini membantu pengguna dalam melakukan Multi Criteria Decision Making (MCDM) menggunakan beberapa metode populer, yaitu:

Simple Additive Weighting (SAW)

Weighted Product (WP)

Analytical Hierarchy Process (AHP)

Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS)

Aplikasi dibangun menggunakan Streamlit, sehingga dapat dijalankan secara interaktif melalui browser.

🧭 Panduan Penggunaan Aplikasi
1️⃣ Pilih Metode

Di panel sidebar kiri, pengguna akan menemukan pilihan “Pilih Metode”.
Tersedia empat metode MCDM:

Simple Additive Weighting (SAW)

Weighted Product (WP)

Analytical Hierarchy Process (AHP)

2️⃣ Pilih Metode Input Data

Masih di sidebar, pilih cara input data:

Upload File (CSV/XLSX) → jika data sudah disiapkan dalam file spreadsheet.

Input Manual → jika ingin mengetikkan nilai langsung di dalam aplikasi.

3️⃣ Struktur Data Input

Tiap metode membutuhkan file berbeda:

🟢 Untuk SAW, WP, dan TOPSIS

Dibutuhkan dua file:

1. Kriteria
Contoh format:
| Kode | Nama Kriteria | Bobot | Arah    |
| ---- | ------------- | ----- | ------- |
| C1   | Harga         | 0.4   | cost    |
| C2   | Kualitas      | 0.3   | benefit |
| C3   | Pelayanan     | 0.3   | benefit |

2. Alternatif
Contoh format:
| Kode Alternatif | C1   | C2 | C3 |
| --------------- | ---- | -- | -- |
| A1              | 2000 | 7  | 8  |
| A2              | 1800 | 6  | 7  |
| A3              | 2200 | 8  | 9  |

🔵 Untuk AHP

Metode ini memerlukan tiga file:

Kriteria → daftar kriteria beserta kode.

Perbandingan Antar Kriteria (Pairwise Comparison)
Format:

| Kriteria | K1 | K2 | Nilai |
| -------- | -- | -- | ----- |
| C1       | C1 | C1 | 1     |
| C1       | C1 | C2 | 3     |
| C2       | C2 | C1 | 1/3   |


Perbandingan Antar Alternatif (per kriteria)
Format:
| Kriteria | A1 | A2 | Nilai |
| -------- | -- | -- | ----- |
| C1       | A1 | A2 | 2     |
| C1       | A2 | A1 | 0.5   |

4️⃣ Proses Perhitungan

Setelah file diunggah:

Aplikasi akan otomatis membaca data dan menampilkan matriks normalisasi serta hasil bobot akhir.

Setiap metode memiliki langkah tersendiri:

SAW → normalisasi nilai + penjumlahan bobot.

WP → perkalian dengan pangkat bobot.

AHP → hitung rasio eigenvector, konsistensi, dan bobot akhir.

TOPSIS → hitung jarak positif/negatif dan nilai preferensi.

5️⃣ Hasil dan Visualisasi

Hasil perhitungan akan ditampilkan dalam bentuk tabel ranking akhir.

Dilengkapi dengan visualisasi grafik batang yang menampilkan peringkat alternatif.

Alternatif dengan nilai tertinggi merupakan pilihan terbaik berdasarkan metode yang digunakan.

TOPSIS

Pilih salah satu metode untuk digunakan.
