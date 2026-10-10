import cv2
import numpy as np
import matplotlib.pyplot as plt

from pathlib import Path


# ==========================================================
# KONFIGURASI FOLDER
# ==========================================================

# Folder citra asli hasil crop
folder_asli = Path("CitraIjazah")

# Folder hasil enhancement
folder_brightness = Path("hasil/brightness")
folder_contrast = Path("hasil/contrast_stretching")
folder_equalization = Path("hasil/histogram_equalization")

# Folder untuk menyimpan hasil histogram
folder_histogram = Path("hasil/histogram")


# ==========================================================
# MEMBUAT FOLDER HISTOGRAM
# ==========================================================

folder_histogram.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================================
# FUNGSI MEMBACA GAMBAR
# ==========================================================

def baca_gambar(path):

    gambar = cv2.imread(str(path))

    if gambar is None:
        return None

    # Jika gambar masih RGB/BGR
    # ubah menjadi grayscale
    if len(gambar.shape) == 3:
        gambar = cv2.cvtColor(
            gambar,
            cv2.COLOR_BGR2GRAY
        )

    return gambar


# ==========================================================
# FUNGSI MEMBUAT HISTOGRAM
# ==========================================================

def tampilkan_histogram(
    gambar,
    judul,
    posisi
):

    plt.subplot(2, 2, posisi)

    plt.hist(
        gambar.ravel(),
        bins=256,
        range=(0, 256)
    )

    plt.title(judul)

    plt.xlabel(
        "Intensitas Piksel"
    )

    plt.ylabel(
        "Jumlah Piksel"
    )

    plt.xlim(
        0,
        255
    )

    plt.grid(
        alpha=0.3
    )


# ==========================================================
# MENCARI GAMBAR ASLI
# ==========================================================

daftar_gambar = []

daftar_gambar.extend(
    folder_asli.glob("*.jpg")
)

daftar_gambar.extend(
    folder_asli.glob("*.jpeg")
)

daftar_gambar.extend(
    folder_asli.glob("*.png")
)

daftar_gambar.extend(
    folder_asli.glob("*.bmp")
)


daftar_gambar = sorted(
    daftar_gambar
)


# ==========================================================
# CEK GAMBAR
# ==========================================================

if not daftar_gambar:

    print("=" * 70)
    print("ERROR")
    print("=" * 70)

    print(
        "Tidak ditemukan gambar di:"
    )

    print(
        folder_asli
    )

    print()

    print(
        "Pastikan gambar crop berada di folder:"
    )

    print(
        "CitraIjazah"
    )

    exit()


# ==========================================================
# INFORMASI PROGRAM
# ==========================================================

print("=" * 70)
print("PROGRAM HISTOGRAM ENHANCEMENT NOMOR IJAZAH")
print("=" * 70)

print()

print(
    f"Jumlah gambar : {len(daftar_gambar)}"
)

print()


# ==========================================================
# PROSES SETIAP GAMBAR
# ==========================================================

for nomor, file_asli in enumerate(
    daftar_gambar,
    start=1
):

    print(
        f"[{nomor}/{len(daftar_gambar)}] "
        f"{file_asli.name}"
    )


    # ======================================================
    # NAMA FILE
    # ======================================================

    nama = file_asli.stem


    # ======================================================
    # BACA CITRA ASLI
    # ======================================================

    gambar_asli = baca_gambar(
        file_asli
    )


    if gambar_asli is None:

        print(
            "  Gagal membaca gambar asli."
        )

        continue


    # ======================================================
    # CARI HASIL BRIGHTNESS
    # ======================================================

    file_brightness = (
        folder_brightness /
        f"{nama}_brightness.jpg"
    )


    # ======================================================
    # CARI HASIL CONTRAST STRETCHING
    # ======================================================

    file_contrast = (
        folder_contrast /
        f"{nama}_contrast.jpg"
    )


    # ======================================================
    # CARI HASIL HISTOGRAM EQUALIZATION
    # ======================================================

    file_equalization = (
        folder_equalization /
        f"{nama}_equalization.jpg"
    )


    # ======================================================
    # BACA HASIL ENHANCEMENT
    # ======================================================

    gambar_brightness = baca_gambar(
        file_brightness
    )

    gambar_contrast = baca_gambar(
        file_contrast
    )

    gambar_equalization = baca_gambar(
        file_equalization
    )


    # ======================================================
    # CEK HASIL ENHANCEMENT
    # ======================================================

    if gambar_brightness is None:

        print(
            "  Hasil brightness tidak ditemukan."
        )

        continue


    if gambar_contrast is None:

        print(
            "  Hasil contrast stretching tidak ditemukan."
        )

        continue


    if gambar_equalization is None:

        print(
            "  Hasil histogram equalization tidak ditemukan."
        )

        continue


    # ======================================================
    # MEMBUAT FIGURE
    # ======================================================

    plt.figure(
        figsize=(14, 8)
    )


    # ======================================================
    # 1. HISTOGRAM SEBELUM ENHANCEMENT
    # ======================================================

    tampilkan_histogram(
        gambar_asli,
        "Sebelum Enhancement",
        1
    )


    # ======================================================
    # 2. HISTOGRAM BRIGHTNESS
    # ======================================================

    tampilkan_histogram(
        gambar_brightness,
        "Brightness Adjustment",
        2
    )


    # ======================================================
    # 3. HISTOGRAM CONTRAST STRETCHING
    # ======================================================

    tampilkan_histogram(
        gambar_contrast,
        "Contrast Stretching",
        3
    )


    # ======================================================
    # 4. HISTOGRAM EQUALIZATION
    # ======================================================

    tampilkan_histogram(
        gambar_equalization,
        "Histogram Equalization",
        4
    )


    # ======================================================
    # JUDUL UTAMA
    # ======================================================

    plt.suptitle(
        f"Perbandingan Histogram - {nama}",
        fontsize=15
    )


    # ======================================================
    # TATA LETAK
    # ======================================================

    plt.tight_layout(
        rect=[0, 0, 1, 0.95]
    )


    # ======================================================
    # PATH OUTPUT
    # ======================================================

    file_output = (
        folder_histogram /
        f"{nama}_histogram.png"
    )


    # ======================================================
    # SIMPAN GAMBAR
    # ======================================================

    plt.savefig(
        str(file_output),
        dpi=150,
        bbox_inches="tight"
    )


    # ======================================================
    # TUTUP FIGURE
    # ======================================================

    plt.close()


    print(
        f"  Histogram disimpan:"
    )

    print(
        f"  {file_output}"
    )

    print()


# ==========================================================
# SELESAI
# ==========================================================

print("=" * 70)
print("PROSES HISTOGRAM SELESAI")
print("=" * 70)

print()

print(
    "Semua histogram tersimpan di:"
)

print(
    folder_histogram
)