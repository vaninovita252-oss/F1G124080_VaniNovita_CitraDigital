# Tugas 4: Enhancement Nomor Ijazah untuk OCR

## Deskripsi

Tugas ini bertujuan meningkatkan kualitas citra pada area nomor ijazah agar karakter angka lebih mudah dikenali oleh sistem Optical Character Recognition (OCR).

Citra nomor ijazah yang telah dipotong (*crop*) disimpan dalam folder `CitraIjazah`. Selanjutnya, citra diubah dari RGB/BGR menjadi grayscale dan diproses menggunakan tiga metode enhancement, yaitu **Brightness Adjustment, Contrast Stretching, dan Histogram Equalization**.

Hasil dari ketiga metode dibandingkan berdasarkan tampilan citra dan distribusi intensitas piksel melalui histogram untuk menentukan metode yang paling sesuai dalam membantu proses OCR.

## Tujuan

* Menerapkan tiga metode enhancement pada citra nomor ijazah.
* Membandingkan citra sebelum dan sesudah enhancement.
* Menampilkan histogram citra asli dan hasil enhancement.
* Menganalisis perubahan distribusi intensitas piksel.
* Menentukan metode enhancement yang paling sesuai untuk proses OCR.

## Metode yang Digunakan

### 1. Brightness Adjustment

Metode ini digunakan untuk mengatur tingkat kecerahan citra dengan menambahkan nilai intensitas piksel. Pada program ini, nilai brightness yang digunakan adalah `20`, sehingga citra menjadi lebih terang.

### 2. Contrast Stretching

Metode ini memperluas rentang intensitas piksel berdasarkan nilai minimum dan maksimum pada citra. Tujuannya untuk meningkatkan perbedaan intensitas sehingga karakter nomor ijazah lebih mudah dibedakan dari latar belakang.

### 3. Histogram Equalization

Metode ini digunakan untuk memperbaiki distribusi intensitas piksel agar kontras citra dapat meningkat. Hasilnya bergantung pada karakteristik citra yang diproses.

## Teknologi yang Digunakan

* **Bahasa pemrograman:** Python
* **OpenCV:** Membaca citra, mengubah citra menjadi grayscale, dan melakukan enhancement.
* **NumPy:** Menghitung nilai intensitas serta statistik citra.
* **Matplotlib:** Menampilkan dan menyimpan perbandingan citra serta histogram.

## Struktur Folder

```text
PCD-Enhancement/
├── CitraIjazah/
│   └── citra nomor ijazah yang sudah di-crop
├── hasil/
│   ├── brightness/
│   ├── contrast_stretching/
│   ├── histogram_equalization/
│   ├── perbandingan/
│   └── histogram/
├── enhancement.py
├── histogram.py
└── README.md
```

## Cara Menjalankan Program

### 1. Instal library yang diperlukan

Buka terminal pada folder proyek, kemudian jalankan:

```bash
pip install opencv-python numpy matplotlib
```

### 2. Siapkan citra

Masukkan citra nomor ijazah yang sudah di-crop ke folder `CitraIjazah`. Program tidak melakukan proses crop otomatis.

Format citra yang didukung oleh kode adalah JPG, JPEG, PNG, dan BMP.

### 3. Jalankan enhancement

```bash
python enhancement.py
```

Program akan mengubah citra menjadi grayscale, menerapkan ketiga metode enhancement, menyimpan hasilnya, serta membuat gambar perbandingan sebelum dan sesudah enhancement.

### 4. Buat histogram

Setelah proses enhancement selesai, jalankan:

```bash
python histogram.py
```

Program akan membuat histogram citra asli, Brightness Adjustment, Contrast Stretching, dan Histogram Equalization dalam satu gambar perbandingan untuk setiap citra.

## Hasil Program

Hasil pemrosesan disimpan pada folder berikut:

* `hasil/brightness/` — hasil Brightness Adjustment.
* `hasil/contrast_stretching/` — hasil Contrast Stretching.
* `hasil/histogram_equalization/` — hasil Histogram Equalization.
* `hasil/perbandingan/` — perbandingan tampilan citra sebelum dan sesudah enhancement.
* `hasil/histogram/` — perbandingan histogram sebelum dan sesudah enhancement.

## Analisis dan Pembahasan

### Mengapa peningkatan kontras dapat membantu OCR?

Peningkatan kontras dapat memperjelas perbedaan intensitas antara karakter nomor ijazah dan latar belakang. Dengan perbedaan yang lebih jelas, bentuk angka berpotensi lebih mudah dikenali oleh sistem OCR.

### Apakah Histogram Equalization selalu menjadi metode terbaik?

Tidak. Setiap metode memiliki karakteristik yang berbeda. Brightness Adjustment lebih sesuai ketika citra terlalu gelap, Contrast Stretching dapat membantu ketika rentang intensitas citra sempit, sedangkan Histogram Equalization dapat membantu memperbaiki distribusi intensitas.

Histogram Equalization tidak selalu menghasilkan karakter yang paling jelas karena peningkatan kontras yang berlebihan dapat memperkuat noise atau membuat detail tertentu kurang terbaca. Oleh karena itu, metode terbaik perlu ditentukan berdasarkan hasil visual dan, jika dilakukan pengujian OCR, ketepatan pengenalan karakter.

### Penentuan metode terbaik untuk OCR

Metode terbaik ditentukan dengan membandingkan keterbacaan angka pada setiap hasil enhancement. Jika tersedia hasil OCR, perbandingan juga dapat dilakukan menggunakan jumlah karakter yang benar atau nilai akurasi terhadap teks acuan (*ground truth*).

## Kesimpulan

Brightness Adjustment, Contrast Stretching, dan Histogram Equalization merupakan tiga metode yang dapat digunakan untuk meningkatkan kualitas citra nomor ijazah. Perbandingan citra dan histogram membantu memahami perubahan kecerahan serta distribusi intensitas setelah enhancement. Metode yang paling sesuai adalah metode yang menghasilkan karakter nomor ijazah paling jelas dan memberikan hasil pengenalan OCR terbaik berdasarkan pengujian.
