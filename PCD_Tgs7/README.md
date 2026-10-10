# Tugas Pertemuan 7 — Mini Project Integrasi

## Deskripsi Proyek

Mini Project Integrasi merupakan program pengolahan citra digital untuk membantu proses verifikasi ijazah. Sistem memproses citra ijazah melalui tahap grayscale, image enhancement, OCR untuk membaca nomor ijazah, serta thresholding dan morfologi untuk mendeteksi keberadaan tanda tangan kepala sekolah.

Program menghasilkan laporan evaluasi OCR menggunakan Character Error Rate (CER) dan laporan verifikasi tanda tangan dalam format TXT.

## Tujuan

1. Membaca nomor ijazah menggunakan Optical Character Recognition (OCR).
2. Membandingkan metode image enhancement berdasarkan nilai CER.
3. Mendeteksi keberadaan tanda tangan kepala sekolah.
4. Menghasilkan laporan evaluasi dan verifikasi secara otomatis.

## Metode yang Digunakan

### 1. Grayscale

Citra berwarna dikonversi menjadi citra grayscale untuk menyederhanakan informasi warna dan mempersiapkan citra untuk proses enhancement serta deteksi tanda tangan.

### 2. Image Enhancement

Program menggunakan tiga metode enhancement untuk meningkatkan kualitas area nomor ijazah.

* **Contrast Stretching:** Memperluas rentang intensitas piksel agar kontras citra meningkat.
* **CLAHE (Contrast Limited Adaptive Histogram Equalization):** Meningkatkan kontras secara lokal agar detail karakter lebih mudah terlihat.
* **Gamma Correction:** Menyesuaikan kecerahan citra melalui transformasi intensitas gamma.

Hasil ketiga metode dibandingkan menggunakan OCR dan nilai CER untuk menentukan metode yang memberikan hasil pembacaan terbaik.

### 3. Optical Character Recognition (OCR)

OCR menggunakan Tesseract melalui library `pytesseract`. Hasil pembacaan dibersihkan dengan mengubah huruf menjadi kapital, menghapus spasi, dan mempertahankan karakter huruf, angka, serta tanda hubung.

### 4. Character Error Rate (CER)

CER digunakan untuk mengukur kesalahan karakter hasil OCR dibandingkan dengan nomor ijazah referensi.

Rumus:

`CER = Jarak Levenshtein / Jumlah Karakter Referensi`

Semakin kecil nilai CER, semakin baik hasil pembacaan OCR. Nilai CER sebesar `0` menunjukkan bahwa hasil OCR sama dengan teks referensi setelah proses normalisasi.

Metode enhancement terbaik ditentukan dari nilai CER terendah pada setiap citra yang dievaluasi.

### 5. Thresholding

Adaptive Gaussian Thresholding digunakan untuk memisahkan tinta tanda tangan dari latar belakang. Metode ini menyesuaikan ambang berdasarkan lingkungan piksel sehingga dapat membantu menangani pencahayaan yang tidak merata.

### 6. Morfologi

Operasi morfologi yang digunakan adalah:

* **Opening:** Mengurangi noise kecil yang tidak diperlukan.
* **Closing:** Menghubungkan bagian tinta yang berdekatan.

Setelah itu, program menghitung rasio piksel tinta dan komponen terhubung untuk membantu menentukan status tanda tangan.

### 7. Deteksi Tanda Tangan

Program menentukan hasil deteksi berdasarkan rasio tinta dan jumlah komponen yang memenuhi kriteria.

* `PRESENT`: Terdeteksi pola tinta yang memenuhi kriteria.
* `ABSENT`: Pola tinta tidak memenuhi kriteria.

Metode ini menggunakan aturan heuristik sederhana, sehingga hasilnya merupakan indikasi keberadaan tanda tangan, bukan verifikasi keaslian tanda tangan.

## Alur Program

```text
Citra Ijazah
     |
  Grayscale
     |
Image Enhancement
     |
     +-----------------------+
     |                       |
 Area Nomor              Area Tanda Tangan
     |                       |
Contrast Stretching           |
CLAHE                    Thresholding
Gamma Correction              |
     |                    Morfologi
    OCR                       |
     |                Deteksi Tanda Tangan
Evaluasi CER                   |
     |                       |
     +-----------+-----------+
                 |
         Hasil Verifikasi
                 |
          Laporan TXT
```

## Struktur Folder

```text
Mini-Project-Integrasi/
├── main.py
├── data_foto_ijazah/
│   └── gambar ijazah dengan tanda tangan
├── data_tanpattd/
│   └── gambar ijazah tanpa tanda tangan
└── outputs/
    ├── hasil_evaluasi.txt
    ├── hasil_verifikasi.txt
    ├── nomor_ijazah/
    │   ├── 1_crop_asli/
    │   ├── 2_grayscale/
    │   ├── 3_contrast_stretching/
    │   ├── 4_clahe/
    │   ├── 5_gamma_correction/
    │   └── 7_perbandingan/
    └── ttd/
        ├── 1_crop_asli/
        ├── 2_grayscale/
        ├── 3_threshold/
        ├── 4_morfologi/
        └── 5_deteksi/
```

Folder `outputs/` beserta subfoldernya dibuat otomatis saat program dijalankan.

## Persiapan

### 1. Instalasi Library

Pastikan Python sudah terpasang, kemudian jalankan perintah berikut di terminal VS Code:

```bash
pip install opencv-python numpy pytesseract
```

### 2. Instalasi Tesseract OCR

Instal aplikasi Tesseract OCR dan pastikan lokasinya sesuai dengan konfigurasi di `main.py`, atau pastikan perintah Tesseract tersedia melalui `PATH` sistem.

### 3. Menyiapkan Dataset

Masukkan citra ijazah ke folder berikut:

* `data_foto_ijazah/` untuk citra yang memiliki tanda tangan.
* `data_tanpattd/` untuk citra yang tidak memiliki tanda tangan.

Program menggunakan label folder sebagai label aktual dalam evaluasi tanda tangan.

### 4. Menyesuaikan Konfigurasi

Periksa dan sesuaikan beberapa parameter pada `main.py`:

* `GROUND_TRUTH`: nomor ijazah referensi.
* `CROP_NOMOR`: koordinat area nomor ijazah.
* `CROP_TTD`: koordinat area tanda tangan.
* `GAMMA_VALUE`: nilai gamma correction.
* `MIN_INK_RATIO` dan `MAX_INK_RATIO`: batas rasio tinta untuk deteksi tanda tangan.

Koordinat crop dinyatakan dalam rasio terhadap ukuran citra. Parameter tersebut perlu disesuaikan dengan posisi nomor dan tanda tangan pada dataset yang digunakan.

Jika setiap citra memiliki nomor ijazah berbeda, sediakan file `ground_truth.csv` dengan format:

```csv
nama_file,nomor_ijazah
ijazah1.jpg,DN-123456789
ijazah2.jpg,DN-987654321
```

File tersebut digunakan sebagai referensi evaluasi CER.

## Cara Menjalankan Program

Buka terminal VS Code pada direktori proyek, kemudian jalankan:

```bash
python main.py
```

Program akan memproses seluruh citra dengan ekstensi yang didukung di kedua folder dataset. Hasil pemrosesan dan laporan disimpan secara otomatis ke folder `outputs/`.

## Hasil Program

### 1. Evaluasi OCR

File `outputs/hasil_evaluasi.txt` berisi tabel evaluasi OCR yang mencakup:

* Nama file citra.
* Metode enhancement.
* Hasil pembacaan OCR.
* Nilai CER.
* Persentase CER.
* Metode terbaik berdasarkan CER terendah untuk setiap citra.

### 2. Verifikasi Tanda Tangan

File `outputs/hasil_verifikasi.txt` berisi:

* Nama file citra.
* Label aktual dari folder.
* Hasil deteksi tanda tangan.
* Rasio tinta.
* Jumlah komponen terhubung yang memenuhi kriteria.
* Status kesesuaian antara hasil deteksi dan label aktual.

### 3. Hasil Visual

Program juga menyimpan citra hasil crop, grayscale, enhancement, thresholding, morfologi, dan visualisasi deteksi tanda tangan untuk membantu analisis setiap tahap pemrosesan.

## Analisis Efektivitas Enhancement

Efektivitas enhancement ditentukan dengan membandingkan nilai CER dari Contrast Stretching, CLAHE, dan Gamma Correction.

Metode dengan CER paling rendah merupakan metode yang paling efektif untuk citra yang diuji. Jika CER bernilai `0`, hasil OCR sesuai dengan teks referensi setelah normalisasi. Jika nilai CER lebih tinggi, berarti masih terdapat kesalahan karakter pada hasil pembacaan.

Metode terbaik dapat berbeda pada setiap citra karena kualitas, kontras, pencahayaan, dan ketajaman karakter pada ijazah tidak selalu sama. Oleh karena itu, penentuan metode terbaik harus berdasarkan hasil evaluasi aktual, bukan hanya tampilan visual citra.

## Kesimpulan

Mini Project Integrasi menggabungkan pengolahan citra digital, image enhancement, OCR, evaluasi CER, thresholding, dan morfologi dalam satu program. Sistem menghasilkan pembacaan nomor ijazah, indikasi keberadaan tanda tangan, serta laporan evaluasi otomatis dalam format TXT.

Keberhasilan program dievaluasi melalui nilai CER untuk OCR dan kesesuaian hasil deteksi tanda tangan terhadap label dataset. Hasil pengujian digunakan untuk mengetahui metode enhancement yang paling efektif serta mengevaluasi kemampuan deteksi tanda tangan pada citra yang digunakan.