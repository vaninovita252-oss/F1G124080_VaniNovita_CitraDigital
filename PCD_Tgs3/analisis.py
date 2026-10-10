import cv2
import numpy as np
from pathlib import Path


# ============================================================
# 1. FOLDER
# ============================================================

folder_citra = Path("citra")

folder_hasil = Path("hasil")

folder_grayscale = folder_hasil / "grayscale"

folder_analisis = folder_hasil / "analisis"

# Membuat folder analisis jika belum ada
folder_analisis.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. MENCARI CITRA
# ============================================================

ekstensi = [
    "*.jpg",
    "*.jpeg",
    "*.png",
    "*.bmp"
]

daftar_citra = []

for ext in ekstensi:
    daftar_citra.extend(folder_citra.glob(ext))

daftar_citra = sorted(daftar_citra)


# ============================================================
# 3. INFORMASI PROGRAM
# ============================================================

print("=" * 75)
print("              PROGRAM ANALISIS DISTRIBUSI INTENSITAS")
print("=" * 75)

print(f"Jumlah citra ditemukan : {len(daftar_citra)}")
print(f"Folder citra           : {folder_citra}")
print(f"Folder grayscale       : {folder_grayscale}")
print(f"Folder hasil analisis  : {folder_analisis}")


# ============================================================
# 4. CEK CITRA
# ============================================================

if len(daftar_citra) == 0:

    print("\nTidak ada citra ditemukan!")
    print("Pastikan gambar berada di folder 'citra'.")

    exit()


# ============================================================
# 5. PROSES SEMUA CITRA
# ============================================================

for nomor, file_citra in enumerate(daftar_citra, start=1):

    print("\n")
    print("=" * 75)
    print(f"CITRA {nomor:02d} : {file_citra.name}")
    print("=" * 75)


    # ========================================================
    # A. MEMBACA CITRA ASLI
    # ========================================================

    img = cv2.imread(str(file_citra))

    if img is None:

        print("Citra gagal dibaca!")

        continue


    # ========================================================
    # B. MEMBACA CITRA GRAYSCALE
    # ========================================================

    nama_grayscale = (
        f"{file_citra.stem}_grayscale.jpg"
    )

    file_grayscale = (
        folder_grayscale / nama_grayscale
    )

    gray = cv2.imread(
        str(file_grayscale),
        cv2.IMREAD_GRAYSCALE
    )


    # Jika grayscale belum ada,
    # buat dari citra asli

    if gray is None:

        print("Grayscale belum ditemukan.")
        print("Membuat grayscale dari citra asli...")

        gray = cv2.cvtColor(
            img,
            cv2.COLOR_BGR2GRAY
        )

        cv2.imwrite(
            str(file_grayscale),
            gray
        )

        print(
            f"Grayscale dibuat: {file_grayscale}"
        )


    # ========================================================
    # C. MENGHITUNG STATISTIK INTENSITAS
    # ========================================================

    mean = np.mean(gray)

    median = np.median(gray)

    minimum = np.min(gray)

    maksimum = np.max(gray)

    rentang = maksimum - minimum

    standar_deviasi = np.std(gray)


    # ========================================================
    # D. MENGHITUNG PERSENTASE PIXEL
    # ========================================================

    total_pixel = gray.size


    # Pixel gelap
    pixel_gelap = np.sum(gray < 85)

    persentase_gelap = (
        pixel_gelap /
        total_pixel *
        100
    )


    # Pixel sedang
    pixel_sedang = np.sum(
        (gray >= 85) &
        (gray < 170)
    )

    persentase_sedang = (
        pixel_sedang /
        total_pixel *
        100
    )


    # Pixel terang
    pixel_terang = np.sum(gray >= 170)

    persentase_terang = (
        pixel_terang /
        total_pixel *
        100
    )


    # ========================================================
    # E. INTENSITAS DOMINAN
    # ========================================================

    histogram = cv2.calcHist(
        [gray],
        [0],
        None,
        [256],
        [0, 256]
    )

    intensitas_dominan = int(
        np.argmax(histogram)
    )


    # ========================================================
    # F. MENENTUKAN INDIKASI KONDISI
    # ========================================================

    kondisi = []


    # --------------------------------------------------------
    # TERLALU GELAP
    # --------------------------------------------------------

    if mean < 85:

        kondisi.append(
            "Terlalu gelap"
        )


    # --------------------------------------------------------
    # TERLALU TERANG
    # --------------------------------------------------------

    elif mean > 200:

        kondisi.append(
            "Terlalu terang"
        )


    # --------------------------------------------------------
    # CONTRAST RENDAH
    # --------------------------------------------------------

    if standar_deviasi < 30:

        kondisi.append(
            "Contrast rendah"
        )


    # --------------------------------------------------------
    # CONTRAST TINGGI
    # --------------------------------------------------------

    elif standar_deviasi > 70:

        kondisi.append(
            "Contrast tinggi"
        )


    # --------------------------------------------------------
    # DISTRIBUSI SEIMBANG
    # --------------------------------------------------------

    if (
        mean >= 85 and
        mean <= 200 and
        standar_deviasi >= 30 and
        standar_deviasi <= 70
    ):

        kondisi.append(
            "Distribusi intensitas relatif seimbang"
        )


    # Jika tidak ada kondisi khusus
    if len(kondisi) == 0:

        kondisi.append(
            "Tidak terdapat indikasi kuat dari statistik sederhana"
        )


    # ========================================================
    # G. HASIL ANALISIS DI TERMINAL
    # ========================================================

    print("\nANALISIS DISTRIBUSI INTENSITAS")

    print(
        f"Mean                 : {mean:.2f}"
    )

    print(
        f"Median               : {median:.2f}"
    )

    print(
        f"Minimum              : {minimum}"
    )

    print(
        f"Maksimum             : {maksimum}"
    )

    print(
        f"Rentang intensitas   : {rentang}"
    )

    print(
        f"Standar deviasi      : {standar_deviasi:.2f}"
    )

    print(
        f"Piksel gelap         : {persentase_gelap:.2f}%"
    )

    print(
        f"Piksel sedang        : {persentase_sedang:.2f}%"
    )

    print(
        f"Piksel terang        : {persentase_terang:.2f}%"
    )

    print(
        f"Intensitas dominan   : {intensitas_dominan}"
    )


    # ========================================================
    # H. MENAMPILKAN KONDISI
    # ========================================================

    print("\nINDIKASI KONDISI CITRA:")

    for item in kondisi:

        print(
            f"- {item}"
        )


    # ========================================================
    # I. CATATAN ANALISIS
    # ========================================================

    print("\nCATATAN:")

    print(
        "- Hasil di atas merupakan analisis statistik "
        "dari citra grayscale."
    )

    print(
        "- Histogram RGB dan histogram grayscale "
        "tetap digunakan sebagai bahan analisis."
    )

    print(
        "- Kondisi akhir sebaiknya ditentukan dengan "
        "menggabungkan statistik, histogram, dan "
        "pengamatan visual citra."
    )


    # ========================================================
    # J. MENYIMPAN HASIL KE TXT
    # ========================================================

    nama_txt = (
        f"{file_citra.stem}_analisis.txt"
    )

    file_txt = (
        folder_analisis / nama_txt
    )


    with open(
        file_txt,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("=" * 75 + "\n")

        file.write(
            f"CITRA {nomor:02d} : "
            f"{file_citra.name}\n"
        )

        file.write("=" * 75 + "\n\n")


        file.write(
            "ANALISIS DISTRIBUSI INTENSITAS\n"
        )

        file.write(
            f"Mean                 : {mean:.2f}\n"
        )

        file.write(
            f"Median               : {median:.2f}\n"
        )

        file.write(
            f"Minimum              : {minimum}\n"
        )

        file.write(
            f"Maksimum             : {maksimum}\n"
        )

        file.write(
            f"Rentang intensitas   : {rentang}\n"
        )

        file.write(
            f"Standar deviasi      : "
            f"{standar_deviasi:.2f}\n"
        )

        file.write(
            f"Piksel gelap         : "
            f"{persentase_gelap:.2f}%\n"
        )

        file.write(
            f"Piksel sedang        : "
            f"{persentase_sedang:.2f}%\n"
        )

        file.write(
            f"Piksel terang        : "
            f"{persentase_terang:.2f}%\n"
        )

        file.write(
            f"Intensitas dominan   : "
            f"{intensitas_dominan}\n"
        )


        file.write(
            "\nINDIKASI KONDISI CITRA:\n"
        )

        for item in kondisi:

            file.write(
                f"- {item}\n"
            )


        file.write(
            "\nCATATAN ANALISIS:\n"
        )

        file.write(
            "- Statistik dihitung dari citra grayscale.\n"
        )

        file.write(
            "- Histogram RGB dan grayscale digunakan "
            "sebagai bahan pendukung analisis.\n"
        )

        file.write(
            "- Kesimpulan akhir harus mempertimbangkan "
            "statistik, histogram, dan pengamatan visual.\n"
        )


    print(
        f"\n✓ Hasil analisis disimpan:"
    )

    print(
        f"  {file_txt}"
    )


# ============================================================
# 6. SELESAI
# ============================================================

print("\n")
print("=" * 75)
print("              ANALISIS SELESAI")
print("=" * 75)

print(
    f"Total citra diproses : {len(daftar_citra)}"
)

print(
    f"Hasil analisis       : {folder_analisis}"
)

print("=" * 75)