# Tugas 1: Perkalian Matriks Array 3 Dimensi Menggunakan Python CLI

## Deskripsi

Program ini dibuat untuk menjalankan operasi perkalian matriks pada array 3 dimensi menggunakan bahasa pemrograman Python dengan antarmuka Command Line Interface (CLI).

Program menerima input berupa jumlah matriks atau lapisan (*depth*), jumlah baris, jumlah kolom, serta elemen-elemen dari Array A dan Array B. Selanjutnya, program melakukan perkalian matriks pada setiap lapisan dan menampilkan hasilnya melalui terminal.

## Tujuan

* Memahami representasi array 3 dimensi menggunakan Python.
* Mengimplementasikan perkalian matriks pada setiap lapisan array 3 dimensi.
* Memahami syarat perkalian matriks.
* Melatih penggunaan input, perulangan, fungsi, dan penanganan kesalahan dalam Python.
* Menjalankan program melalui terminal menggunakan CLI.

## Teknologi yang Digunakan

* **Bahasa pemrograman:** Python
* **Antarmuka:** Command Line Interface (CLI)
* **Library tambahan:** Tidak memerlukan library tambahan.

## Struktur Folder

```text
Tugas-Perkalian-Matriks-3D/
├── matrix-array3dimensi.py
└── README.md
```

## Fitur Program

1. Memasukkan jumlah matriks atau lapisan array 3 dimensi.
2. Menentukan ukuran baris dan kolom Array A dan Array B.
3. Memasukkan elemen matriks melalui terminal.
4. Memeriksa kesesuaian ukuran matriks sebelum perkalian.
5. Melakukan perkalian matriks pada setiap lapisan array.
6. Menampilkan Array A, Array B, dan hasil perkalian.
7. Menangani input yang bukan berupa angka dan jumlah elemen baris yang tidak sesuai.

## Syarat Perkalian Matriks

Perkalian matriks dapat dilakukan apabila jumlah kolom Array A sama dengan jumlah baris Array B.

$$
A_{m \times n} \times B_{n \times p}
= C_{m \times p}
$$

Artinya, jika Array A memiliki ukuran 2 × 3, maka Array B harus memiliki 3 baris. Hasil perkaliannya akan memiliki ukuran 2 × jumlah kolom Array B.

Pada program ini, perkalian dilakukan untuk setiap lapisan dengan indeks yang sama pada Array A dan Array B.

## Cara Menjalankan Program

**1. Pastikan Python sudah terinstal.**

Periksa versi Python melalui terminal:

```bash
python --version
```

**2. Buka terminal pada folder proyek.**

Pastikan file `matrix-array3dimensi.py` berada di folder tersebut.

**3. Jalankan program menggunakan perintah:**

```bash
python matrix-array3dimensi.py
```

**4. Masukkan data sesuai instruksi terminal.**

Masukkan jumlah lapisan, ukuran Array A dan Array B, kemudian elemen setiap baris matriks. Elemen dalam satu baris dipisahkan menggunakan spasi.

## Contoh Penggunaan

Misalnya, program menggunakan 1 lapisan dengan Array A berukuran 2 × 2 dan Array B berukuran 2 × 2.

Array A:

```text
1 2
3 4
```

Array B:

```text
5 6
7 8
```

Hasil perkalian:

```text
Array A x B:
19 22
43 50
```

Hasil tersebut diperoleh dari perkalian matriks:

$$
\begin{bmatrix}
1 & 2\\
3 & 4
\end{bmatrix}
\times
\begin{bmatrix}
5 & 6\\
7 & 8
\end{bmatrix}
=
\begin{bmatrix}
19 & 22\\
43 & 50
\end{bmatrix}
$$

## Kesimpulan

Program ini menerapkan perkalian matriks pada array 3 dimensi menggunakan Python berbasis CLI. Setiap lapisan Array A dikalikan dengan lapisan Array B yang bersesuaian. Program juga memeriksa kesesuaian ukuran matriks agar operasi perkalian dapat dilakukan sesuai aturan matematika.
