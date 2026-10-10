from pathlib import Path
import cv2
import matplotlib.pyplot as plt
import numpy as np

# ============================================================
# 1. FOLDER
# ============================================================

# Folder citra asli
folder_citra = Path("citra")

# Folder hasil utama
folder_hasil = Path("hasil")

# Folder hasil grayscale
folder_grayscale = folder_hasil / "grayscale"

# Folder histogram citra asli
folder_histogram_asli = folder_hasil / "histogram_asli"

# Folder histogram grayscale
folder_histogram_grayscale = folder_hasil / "histogram_grayscale"


# Membuat folder jika belum ada
folder_grayscale.mkdir(parents=True, exist_ok=True)
folder_histogram_asli.mkdir(parents=True, exist_ok=True)
folder_histogram_grayscale.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. MENCARI CITRA
# ============================================================

ekstensi = ["*.jpg", "*.jpeg", "*.png", "*.bmp"]

daftar_citra = []

for ext in ekstensi:
    daftar_citra.extend(folder_citra.glob(ext))

# Mengurutkan nama file
daftar_citra = sorted(daftar_citra)


# ============================================================
# 3. INFORMASI PROGRAM
# ============================================================

print("=" * 70)
print("                 PROGRAM ANALISIS HISTOGRAM")
print("=" * 70)

print(f"Jumlah citra ditemukan : {len(daftar_citra)}")
print(f"Folder citra asli      : {folder_citra}")
print(f"Folder grayscale       : {folder_grayscale}")
print(f"Histogram citra asli   : {folder_histogram_asli}")
print(f"Histogram grayscale    : {folder_histogram_grayscale}")


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
    print("=" * 70)
    print(f"CITRA {nomor:02d} : {file_citra.name}")
    print("=" * 70)

    # ========================================================
    # A. MEMBACA CITRA ASLI
    # ========================================================

    img = cv2.imread(str(file_citra))

    if img is None:

        print("❌ Citra gagal dibaca!")

        continue

    # ========================================================
    # B. MENGUBAH BGR KE RGB
    # ========================================================

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # ========================================================
    # C. MEMBACA CITRA GRAYSCALE
    # ========================================================

    nama_grayscale = f"{file_citra.stem}_grayscale.jpg"

    file_grayscale = folder_grayscale / nama_grayscale

    gray = cv2.imread(str(file_grayscale), cv2.IMREAD_GRAYSCALE)

    # Jika file grayscale belum ditemukan, buat dari citra asli
    if gray is None:

        print("⚠ Citra grayscale belum ditemukan.")
        print("Membuat grayscale dari citra asli...")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        cv2.imwrite(str(file_grayscale), gray)

        print(f"✓ Grayscale dibuat: {file_grayscale}")

    # ========================================================
    # D. HISTOGRAM CITRA ASLI RGB
    # ========================================================

    histogram_r = cv2.calcHist([rgb], [0], None, [256], [0, 256])

    histogram_g = cv2.calcHist([rgb], [1], None, [256], [0, 256])

    histogram_b = cv2.calcHist([rgb], [2], None, [256], [0, 256])

    # ========================================================
    # E. MEMBUAT HISTOGRAM RGB (BENTUK BATANG/SOLID)
    # ========================================================

    plt.figure(figsize=(10, 6))

    x = np.arange(256)

    # Menggunakan plt.bar agar grafik terisi solid seperti contoh gambar
    plt.bar(
        x,
        histogram_r.ravel(),
        color="red",
        alpha=0.4,
        label="Red",
        width=1.0,
    )
    plt.bar(
        x,
        histogram_g.ravel(),
        color="green",
        alpha=0.4,
        label="Green",
        width=1.0,
    )
    plt.bar(
        x,
        histogram_b.ravel(),
        color="blue",
        alpha=0.4,
        label="Blue",
        width=1.0,
    )

    plt.title(f"Histogram Citra Asli RGB - {file_citra.stem}")

    plt.xlabel("Intensitas Piksel (0-255)")

    plt.ylabel("Jumlah Piksel")

    plt.xlim(0, 255)

    plt.legend()

    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()

    # ========================================================
    # F. MENYIMPAN HISTOGRAM RGB
    # ========================================================

    nama_histogram_asli = f"{file_citra.stem}_rgb_histogram.png"

    path_histogram_asli = folder_histogram_asli / nama_histogram_asli

    plt.savefig(path_histogram_asli, dpi=300, bbox_inches="tight")

    plt.close()

    print("✓ Histogram RGB disimpan:")
    print(f"  {path_histogram_asli}")

    # ========================================================
    # G. HISTOGRAM GRAYSCALE
    # ========================================================

    histogram_gray = cv2.calcHist([gray], [0], None, [256], [0, 256])

    # ========================================================
    # H. MEMBUAT HISTOGRAM GRAYSCALE (BENTUK BATANG/SOLID)
    # ========================================================

    plt.figure(figsize=(10, 6))

    x = np.arange(256)

    # Menggunakan plt.bar dengan warna biru khas histogram
    plt.bar(
        x, histogram_gray.ravel(), color="#1f77b4", width=1.0, label="Grayscale"
    )

    plt.title(f"Histogram Grayscale - {file_citra.stem}")

    plt.xlabel("Intensitas Piksel (0-255)")

    plt.ylabel("Jumlah Piksel")

    plt.xlim(0, 255)

    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()

    # ========================================================
    # I. MENYIMPAN HISTOGRAM GRAYSCALE
    # ========================================================

    nama_histogram_grayscale = f"{file_citra.stem}_grayscale_histogram.png"

    path_histogram_grayscale = (
        folder_histogram_grayscale / nama_histogram_grayscale
    )

    plt.savefig(path_histogram_grayscale, dpi=300, bbox_inches="tight")

    plt.close()

    print("✓ Histogram grayscale disimpan:")
    print(f"  {path_histogram_grayscale}")

    # ========================================================
    # J. ANALISIS INTENSITAS GRAYSCALE
    # ========================================================

    mean = np.mean(gray)

    median = np.median(gray)

    minimum = np.min(gray)

    maksimum = np.max(gray)

    rentang = maksimum - minimum

    variance = np.var(gray)

    standard_deviation = np.std(gray)

    # ========================================================
    # K. MENAMPILKAN HASIL ANALISIS
    # ========================================================

    print("\nAnalisis Intensitas Grayscale:")

    print(f"Mean               : {mean:.2f}")

    print(f"Median             : {median:.2f}")

    print(f"Minimum            : {minimum}")

    print(f"Maksimum           : {maksimum}")

    print(f"Rentang Intensitas : {rentang}")

    print(f"Variansi           : {variance:.2f}")

    print(f"Standar Deviasi    : {standard_deviation:.2f}")

    print("\n✓ Citra selesai diproses.")


# ============================================================
# 6. SELESAI
# ============================================================

print("\n")
print("=" * 70)
print("                 ANALISIS HISTOGRAM SELESAI")
print("=" * 70)

print(f"\nTotal citra diproses : {len(daftar_citra)}")

print("\nHistogram citra asli RGB:")
print(folder_histogram_asli)

print("\nHistogram citra grayscale:")
print(folder_histogram_grayscale)

print("\nSemua histogram telah disimpan.")
print("=" * 70)