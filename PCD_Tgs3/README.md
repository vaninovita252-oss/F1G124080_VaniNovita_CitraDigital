# Tugas 3 — Grayscale, Histogram, dan Analisis Intensitas Citra

## Deskripsi

Tugas ini bertujuan untuk menganalisis kualitas citra dokumen ijazah dengan kondisi pencahayaan dan kualitas yang berbeda melalui konversi grayscale, visualisasi histogram, dan analisis distribusi intensitas piksel.

Proses dilakukan menggunakan Python, OpenCV, NumPy, dan Matplotlib untuk mengamati karakteristik intensitas piksel serta mengidentifikasi indikasi permasalahan pada citra, seperti terlalu gelap, terlalu terang, dan kontras rendah.

## Tujuan

* Mengubah citra berwarna (RGB) menjadi grayscale.
* Menampilkan histogram citra asli RGB dan citra grayscale.
* Menganalisis distribusi intensitas piksel menggunakan statistik deskriptif.
* Mengidentifikasi indikasi kondisi citra berdasarkan histogram, statistik, dan pengamatan visual.
* Menentukan metode enhancement yang sesuai berdasarkan kondisi setiap citra.
* Memahami apakah histogram dengan distribusi intensitas yang lebih tersebar selalu menunjukkan kualitas citra yang lebih baik.

## Teknologi yang Digunakan

* **Python** — bahasa pemrograman.
* **OpenCV** — membaca citra, konversi grayscale, dan perhitungan histogram.
* **NumPy** — perhitungan statistik intensitas piksel.
* **Matplotlib** — visualisasi histogram.

## Struktur Folder

```text
Tugas-3/
├── citra/
│   └── (citra dokumen ijazah asli)
├── hasil/
│   ├── grayscale/
│   │   └── (hasil konversi grayscale)
│   ├── histogram_asli/
│   │   └── (histogram citra RGB)
│   ├── histogram_grayscale/
│   │   └── (histogram citra grayscale)
│   └── analisis/
│       └── (hasil analisis dalam format TXT)
├── gbr-ke-grascale.py
├── histogram.py
├── analisis.py
└── README.md
```

## Penjelasan Program

### 1. Konversi Grayscale — `gbr-ke-grascale.py`

Program membaca seluruh citra dalam folder `citra/`, mengubah citra berwarna menjadi grayscale menggunakan `cv2.cvtColor()` dengan `cv2.COLOR_BGR2GRAY`, kemudian menyimpan hasilnya ke folder `hasil/grayscale/`.

Program juga menampilkan informasi ukuran citra, jumlah citra yang ditemukan, serta status keberhasilan pemrosesan.

### 2. Pembuatan Histogram — `histogram.py`

Program membuat histogram untuk citra asli RGB dan citra grayscale.

Histogram citra asli menampilkan distribusi intensitas kanal merah, hijau, dan biru. Histogram grayscale menampilkan distribusi intensitas keabuan dari 0 hingga 255.

Program juga menghitung statistik intensitas grayscale, meliputi:

* Mean (rata-rata intensitas).
* Median (nilai tengah intensitas).
* Minimum dan maksimum.
* Rentang intensitas.
* Variansi.
* Standar deviasi.

Hasil histogram disimpan dalam folder `hasil/histogram_asli/` dan `hasil/histogram_grayscale/`.

### 3. Analisis Distribusi Intensitas — `analisis.py`

Program menghitung statistik intensitas grayscale dan persentase piksel gelap, sedang, serta terang.

Pembagian intensitas yang digunakan:

* Piksel gelap: intensitas di bawah 85.
* Piksel sedang: intensitas 85 hingga kurang dari 170.
* Piksel terang: intensitas 170 hingga 255.

Program memberikan indikasi awal kondisi citra berdasarkan nilai mean dan standar deviasi, kemudian menyimpan hasil analisis setiap citra dalam format TXT ke folder `hasil/analisis/`.

Indikasi tersebut merupakan analisis statistik sederhana sehingga perlu dikombinasikan dengan pengamatan visual dan histogram untuk menentukan kondisi citra secara lebih tepat.

## Cara Menjalankan Program

### 1. Instalasi pustaka

Pastikan Python telah terinstal. Buka terminal pada folder proyek, kemudian jalankan:

```bash
pip install opencv-python numpy matplotlib
```

### 2. Siapkan citra

Masukkan citra dokumen ijazah ke folder `citra/`. Format yang didukung adalah JPG, JPEG, PNG, dan BMP.

### 3. Jalankan konversi grayscale

```bash
python gbr-ke-grascale.py
```

### 4. Buat histogram citra asli dan grayscale

```bash
python histogram.py
```

### 5. Jalankan analisis distribusi intensitas

```bash
python analisis.py
```

Jalankan perintah dari direktori utama proyek agar jalur folder input dan output sesuai.

## Hasil yang Diharapkan

Setelah program dijalankan, folder `hasil/` berisi:

* Citra grayscale dari setiap citra input.
* Histogram citra asli RGB.
* Histogram citra grayscale.
* Statistik dan analisis distribusi intensitas dalam format TXT.

Hasil tersebut digunakan sebagai dasar untuk membandingkan kondisi citra dan menentukan metode enhancement yang sesuai.

## Kesimpulan

Histogram dan statistik intensitas dapat membantu memahami karakteristik pencahayaan dan kontras citra dokumen ijazah. Namun, histogram yang lebih tersebar tidak selalu menunjukkan kualitas citra yang lebih baik. Kualitas juga dipengaruhi oleh noise, ketajaman karakter, pencahayaan yang tidak merata, dan keterbacaan informasi pada citra.

Pemilihan metode enhancement perlu mempertimbangkan karakteristik setiap citra agar detail karakter tetap terjaga dan kualitas citra menjadi lebih sesuai untuk kebutuhan pengolahan selanjutnya.
