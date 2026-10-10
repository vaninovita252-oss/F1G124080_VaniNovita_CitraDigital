import cv2
from pathlib import Path


# ============================================================
# KONFIGURASI FOLDER
# ============================================================

# Folder tempat citra asli
folder_citra = Path("citra")

# Folder utama hasil
folder_hasil = Path("hasil")

# Folder khusus hasil grayscale
folder_grayscale = folder_hasil / "grayscale"

# Membuat folder jika belum ada
folder_grayscale.mkdir(parents=True, exist_ok=True)


# ============================================================
# MENCARI SEMUA CITRA
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

# Mengurutkan nama file
daftar_citra = sorted(daftar_citra)


# ============================================================
# INFORMASI PROGRAM
# ============================================================

print("=" * 60)
print("        PROGRAM KONVERSI RGB KE GRAYSCALE")
print("=" * 60)

print(f"Folder citra asli : {folder_citra}")
print(f"Folder hasil      : {folder_grayscale}")
print(f"Jumlah citra      : {len(daftar_citra)}")


# ============================================================
# CEK CITRA
# ============================================================

if len(daftar_citra) == 0:

    print("\nTidak ada citra yang ditemukan!")
    print("Pastikan gambar berada di folder 'citra'.")

    exit()


# ============================================================
# PROSES KONVERSI
# ============================================================

berhasil = 0
gagal = 0


for nomor, file_citra in enumerate(daftar_citra, start=1):

    print("\n" + "-" * 60)
    print(f"Citra ke-{nomor}")
    print(f"Nama file : {file_citra.name}")
    print("-" * 60)


    # --------------------------------------------------------
    # Membaca citra
    # --------------------------------------------------------

    img = cv2.imread(str(file_citra))


    # --------------------------------------------------------
    # Mengecek apakah citra berhasil dibaca
    # --------------------------------------------------------

    if img is None:

        print("Status : GAGAL membaca citra")

        gagal += 1

        continue


    # --------------------------------------------------------
    # Menampilkan ukuran citra
    # --------------------------------------------------------

    tinggi, lebar, channel = img.shape

    print(f"Ukuran   : {lebar} x {tinggi} piksel")
    print(f"Channel  : {channel}")


    # --------------------------------------------------------
    # Mengubah BGR menjadi Grayscale
    # --------------------------------------------------------

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )


    # --------------------------------------------------------
    # Nama file hasil
    # --------------------------------------------------------

    nama_hasil = (
        f"citra{nomor:02d}_grayscale.jpg"
    )


    # --------------------------------------------------------
    # Lokasi penyimpanan
    # --------------------------------------------------------

    path_hasil = (
        folder_grayscale / nama_hasil
    )


    # --------------------------------------------------------
    # Menyimpan citra grayscale
    # --------------------------------------------------------

    sukses = cv2.imwrite(
        str(path_hasil),
        gray
    )


    # --------------------------------------------------------
    # Mengecek hasil penyimpanan
    # --------------------------------------------------------

    if sukses:

        print("Status   : BERHASIL")
        print(f"Disimpan : {path_hasil}")

        berhasil += 1

    else:

        print("Status   : GAGAL menyimpan")

        gagal += 1


# ============================================================
# RINGKASAN
# ============================================================

print("\n")
print("=" * 60)
print("                 PROSES SELESAI")
print("=" * 60)

print(f"Total citra ditemukan : {len(daftar_citra)}")
print(f"Berhasil              : {berhasil}")
print(f"Gagal                 : {gagal}")

print("\nHasil grayscale disimpan di:")
print(folder_grayscale)

print("=" * 60)