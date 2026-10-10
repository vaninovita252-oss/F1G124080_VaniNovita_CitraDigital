# Tugas 5 — Enhancement untuk OCR

## Deskripsi

Tugas ini bertujuan meningkatkan kualitas citra nomor ijazah yang memiliki noise atau kualitas rendah agar karakter lebih mudah dikenali oleh sistem Optical Character Recognition (OCR).

Proses dilakukan menggunakan empat metode, yaitu Mean Filter, Median Filter, Gaussian Filter, dan Sharpening. Hasil setiap metode kemudian digunakan sebagai input OCR dan dibandingkan dengan citra original.

Evaluasi dilakukan dengan membandingkan hasil OCR terhadap teks acuan (*ground truth*) untuk menghitung jumlah karakter benar dan akurasi pengenalan.

## Tujuan

* Menerapkan Mean Filter, Median Filter, dan Gaussian Filter untuk mengurangi noise.
* Menerapkan Sharpening untuk memperjelas detail karakter.
* Membandingkan hasil citra original dan citra hasil filtering.
* Menggunakan hasil enhancement sebagai input OCR.
* Menghitung jumlah karakter benar dan akurasi OCR.
* Menganalisis pengaruh metode filtering terhadap hasil pengenalan karakter.

## Metode yang Digunakan

### 1. Mean Filter

Mean Filter menghaluskan citra dengan menghitung rata-rata intensitas piksel di sekitar setiap piksel. Metode ini dapat mengurangi noise, tetapi berpotensi membuat tepi karakter menjadi kabur.

### 2. Median Filter

Median Filter mengganti nilai piksel dengan nilai median dari lingkungan sekitarnya. Metode ini efektif untuk mengurangi *salt-and-pepper noise* dengan mempertahankan tepi karakter relatif lebih baik dibandingkan filter perataan biasa.

### 3. Gaussian Filter

Gaussian Filter menghaluskan citra menggunakan pembobotan berdasarkan distribusi Gaussian. Metode ini dapat mengurangi noise, tetapi juga dapat mengurangi ketajaman detail karakter.

### 4. Sharpening

Sharpening digunakan untuk mempertegas tepi dan detail karakter agar bentuk angka lebih jelas. Namun, penerapan yang berlebihan dapat memperkuat noise pada citra.

## Teknologi yang Digunakan

* **Python:** Bahasa pemrograman utama.
* **OpenCV:** Membaca, mengubah, memfilter, dan menyimpan citra.
* **NumPy:** Membentuk kernel sharpening dan menyusun gambar perbandingan.
* **Tesseract OCR:** Mengenali teks pada citra original dan hasil enhancement.
* **pytesseract:** Menghubungkan Python dengan Tesseract OCR.

## Struktur Folder

```text
PCD-Enhancement-OCR/
├── citra/
│   └── gambar nomor ijazah
├── hasil/
│   ├── grayscale/
│   ├── mean/
│   ├── median/
│   ├── gaussian/
│   ├── sharpening/
│   ├── perbandingan/
│   ├── hasil_ocr.txt
│   └── evaluasi_ocr.txt
├── enhancement.py
├── ocr.py
├── evaluasi_ocr.py
└── README.md
```

## Instalasi

Pastikan Python sudah terinstal. Kemudian, instal library yang diperlukan melalui terminal:

```bash
pip install opencv-python numpy pytesseract
```

Program juga memerlukan **Tesseract OCR** yang terinstal pada komputer. Pastikan lokasi `tesseract.exe` sesuai dengan konfigurasi pada file `ocr.py`.

## Cara Menjalankan Program

Jalankan perintah berikut secara berurutan dari folder utama proyek.

### 1. Menjalankan enhancement

```bash
python enhancement.py
```

Program mengubah citra menjadi grayscale, menerapkan empat metode pemrosesan, menyimpan hasilnya ke folder masing-masing, dan membuat gambar perbandingan.

### 2. Menjalankan OCR

```bash
python ocr.py
```

Program menjalankan OCR pada citra original dan hasil setiap metode. Hasil pengenalan disimpan dalam file `hasil/hasil_ocr.txt`.

### 3. Menjalankan evaluasi OCR

```bash
python evaluasi_ocr.py
```

Program membandingkan teks hasil OCR dengan *ground truth*, menghitung karakter benar dan akurasi, kemudian menyimpan laporan pada `hasil/evaluasi_ocr.txt`.

## Ground Truth

Teks acuan yang digunakan dalam program adalah:

```text
Nomor ijazah: 571012022000056
```

Spasi tidak dihitung sebagai karakter dalam evaluasi. Jumlah karakter benar dihitung berdasarkan karakter yang cocok dengan teks acuan menggunakan `SequenceMatcher`.

## Hasil Evaluasi

Evaluasi membandingkan lima kondisi citra:

| Metode        | Keterangan                       |
| ------------- | -------------------------------- |
| Original      | Citra sebelum filtering          |
| Mean Filter   | Citra setelah perataan rata-rata |
| Median Filter | Citra setelah filter median      |
| Gaussian      | Citra setelah Gaussian Filter    |
| Sharpening    | Citra setelah penajaman          |

Hasil OCR, karakter benar, dan akurasi ditampilkan dalam laporan evaluasi untuk setiap citra. Program juga menghasilkan rekap akurasi berdasarkan metode.

## Pertanyaan Analisis

### Mengapa Median Filter dapat memberikan hasil OCR lebih baik pada citra dengan salt-and-pepper noise?

Median Filter menggunakan nilai median dari piksel di sekitarnya sehingga piksel yang sangat terang atau sangat gelap akibat noise dapat dikurangi. Metode ini cenderung mempertahankan tepi karakter, sehingga bentuk angka tetap lebih jelas dan berpotensi meningkatkan akurasi OCR.

### Apakah citra yang paling bagus secara visual selalu menghasilkan OCR dengan akurasi tertinggi?

Tidak selalu. Citra yang terlihat lebih halus atau tajam belum tentu memiliki bentuk karakter yang paling mudah dikenali oleh OCR. Filtering dapat menghilangkan detail penting, membuat garis karakter menipis, atau memperkuat noise. Oleh karena itu, hasil OCR dan nilai akurasinya perlu digunakan untuk menentukan metode yang paling sesuai.

## Kesimpulan

Tugas ini membandingkan Mean Filter, Median Filter, Gaussian Filter, dan Sharpening untuk meningkatkan kualitas citra nomor ijazah. Hasil pemrosesan digunakan sebagai input OCR, kemudian dievaluasi berdasarkan jumlah karakter benar dan akurasi terhadap *ground truth*. Metode terbaik ditentukan berdasarkan hasil eksperimen, bukan hanya berdasarkan tampilan visual citra.
