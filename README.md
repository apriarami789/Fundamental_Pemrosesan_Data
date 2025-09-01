### Proyek ETL Data Produk Fashion

**1. Penjelasan Singkat Proyek**

Proyek ini adalah sebuah pipeline ETL (Extract, Transform, Load) sederhana yang dibangun dengan Python. Tujuannya adalah untuk mengumpulkan data produk fashion dari situs web, membersihkan dan mentransformasikannya, lalu menyimpannya dalam format yang siap untuk dianalisis.

- **Extract**: Skrip akan melakukan scraping data dari situs web fashion, menangani paginasi untuk mengambil semua produk. Data mentah yang diekstrak (nama produk, harga, rating, dll.) disimpan dalam file `fashion_data.csv`.
- **Transform**: Data mentah kemudian dibersihkan. Proses ini mencakup ekstraksi nilai numerik dari teks (misalnya, mengambil `100.00` dari `$100.00`), konversi harga dari USD ke IDR, penyesuaian tipe data (float, integer, category), dan penghapusan data yang tidak valid atau duplikat.
- **Load**: Data yang sudah bersih dan terstruktur disimpan ke dalam file baru bernama `clean_fashion_data.csv`.

**2. Cara Menjalankan Skrip ETL Pipeline**

Pastikan Anda berada di direktori utama proyek (`d:\Tugas_Dicoding\Fundamental_Pemrosesan_Data`). Jalankan file `main.py` melalui terminal.

```sh
python main.py
```

Skrip akan secara otomatis mencoba mengakses URL default. Jika gagal, Anda akan diminta untuk memasukkan URL yang valid secara manual di terminal.

**3. Cara Menjalankan Unit Test**

Semua skrip pengujian berada di dalam folder `tests/`. Untuk menjalankan semua unit test secara otomatis, gunakan perintah berikut dari direktori utama:

```sh
python -m unittest discover tests
```

Perintah ini akan mencari dan menjalankan semua file test (yang berawalan `test_`) di dalam folder `tests`.

**4. Cara Menjalankan Test Coverage**

Untuk memeriksa seberapa banyak kode sumber yang dicakup oleh unit test, Anda dapat menggunakan library `coverage`.

a. **Instalasi (jika belum ada):**
```sh
pip install coverage
```

b. **Jalankan Test Melalui Coverage:**
Perintah ini akan menjalankan semua test sambil memantau kode di dalam folder `utils`.
```sh
coverage run --source=utils -m unittest discover tests
```

c. **Lihat Laporan Coverage:**
- **Laporan di Terminal:** Untuk ringkasan cepat.
  ```sh
  coverage report -m
  ```
- **Laporan HTML (Direkomendasikan):** Untuk laporan interaktif yang lebih detail.
  ```sh
  coverage html
  ```
  Setelah itu, buka file `htmlcov/index.html` di browser Anda untuk melihat laporan lengkap dengan visualisasi baris kode yang ter-cover dan