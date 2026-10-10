
import os
import re
import cv2
import numpy as np
import pytesseract

from pathlib import Path


# ============================================================
# 1. KONFIGURASI
# ============================================================

FOLDER_PRESENT = "data_foto_ijazah"
FOLDER_ABSENT = "data_tanpattd"
FOLDER_OUTPUT = "outputs"

# Ganti dengan nomor ijazah referensi yang sebenarnya jika
# semua gambar menggunakan nomor yang sama.
GROUND_TRUTH = "DN-123456789"

# Koordinat crop dalam rasio: x1, y1, x2, y2.
# Sesuaikan berdasarkan posisi nomor dan tanda tangan
# pada gambar ijazah milikmu.
CROP_NOMOR = (0.05, 0.65, 0.95, 0.98)
CROP_TTD = (0.15, 0.15, 0.95, 0.65)

# Parameter gamma.
GAMMA_VALUE = 1.5

# Ambang heuristik deteksi tanda tangan.
# Perlu diuji dan disesuaikan dengan data asli.
MIN_INK_RATIO = 0.003
MAX_INK_RATIO = 0.35

EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


# ============================================================
# 2. KONFIGURASI TESSERACT
# ============================================================

def konfigurasi_tesseract():
    kandidat = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    ]

    for path in kandidat:
        if os.path.isfile(path):
            pytesseract.pytesseract.tesseract_cmd = path
            return

    # Jika Tesseract tersedia di PATH, gunakan konfigurasi default.
    # Jika tidak, pytesseract akan menampilkan error saat OCR.


# ============================================================
# 3. FUNGSI UTILITAS
# ============================================================

def buat_folder_output():
    folder = [
        "nomor_ijazah/1_crop_asli",
        "nomor_ijazah/2_grayscale",
        "nomor_ijazah/3_contrast_stretching",
        "nomor_ijazah/4_clahe",
        "nomor_ijazah/5_gamma_correction",
        "nomor_ijazah/7_perbandingan",
        "ttd/1_crop_asli",
        "ttd/2_grayscale",
        "ttd/3_threshold",
        "ttd/4_morfologi",
        "ttd/5_deteksi",
    ]

    os.makedirs(FOLDER_OUTPUT, exist_ok=True)

    for nama in folder:
        os.makedirs(os.path.join(FOLDER_OUTPUT, nama), exist_ok=True)


def daftar_gambar(folder):
    path_folder = Path(folder)

    if not path_folder.exists():
        print(f"[PERINGATAN] Folder tidak ditemukan: {folder}")
        return []

    return sorted([
        p for p in path_folder.iterdir()
        if p.is_file() and p.suffix.lower() in EXTENSIONS
    ])


def simpan_gambar(folder_rel, nama_file, gambar):
    path = os.path.join(FOLDER_OUTPUT, folder_rel, nama_file)
    cv2.imwrite(path, gambar)


def crop_rasio(gambar, koordinat):
    tinggi, lebar = gambar.shape[:2]
    x1, y1, x2, y2 = koordinat

    x1 = max(0, min(lebar - 1, int(x1 * lebar)))
    x2 = max(x1 + 1, min(lebar, int(x2 * lebar)))
    y1 = max(0, min(tinggi - 1, int(y1 * tinggi)))
    y2 = max(y1 + 1, min(tinggi, int(y2 * tinggi)))

    return gambar[y1:y2, x1:x2].copy()


def bersihkan_teks(teks):
    teks = teks.upper().strip()
    teks = re.sub(r"\s+", "", teks)
    teks = re.sub(r"[^A-Z0-9-]", "", teks)
    return teks


# ============================================================
# 4. PREPROCESSING DAN ENHANCEMENT
# ============================================================

def grayscale(gambar):
    if len(gambar.shape) == 2:
        return gambar.copy()

    return cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)


def contrast_stretching(gambar):
    gambar = grayscale(gambar)

    nilai_min = np.min(gambar)
    nilai_maks = np.max(gambar)

    if nilai_maks == nilai_min:
        return gambar.copy()

    hasil = (
        (gambar.astype(np.float32) - nilai_min)
        * (255.0 / (nilai_maks - nilai_min))
    )

    return np.clip(hasil, 0, 255).astype(np.uint8)


def clahe_enhancement(gambar):
    gambar = grayscale(gambar)

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    return clahe.apply(gambar)


def gamma_correction(gambar, gamma=GAMMA_VALUE):
    gambar = grayscale(gambar)

    gamma = max(0.01, float(gamma))
    tabel = np.array([
        ((i / 255.0) ** (1.0 / gamma)) * 255
        for i in range(256)
    ]).astype(np.uint8)

    return cv2.LUT(gambar, tabel)


def semua_enhancement(crop):
    gray = grayscale(crop)

    hasil = {
        "Contrast Stretching": contrast_stretching(gray),
        "CLAHE": clahe_enhancement(gray),
        "Gamma Correction": gamma_correction(gray),
    }

    return gray, hasil


# ============================================================
# 5. PERBANDINGAN VISUAL ENHANCEMENT
# ============================================================

def simpan_perbandingan_enhancement(
    nama_file,
    crop_asli,
    hasil_enhancement
):
    gambar_list = [
        ("Crop Asli", grayscale(crop_asli)),
        (
            "Contrast Stretching",
            hasil_enhancement["Contrast Stretching"]
        ),
        ("CLAHE", hasil_enhancement["CLAHE"]),
        ("Gamma Correction", hasil_enhancement["Gamma Correction"]),
    ]

    tinggi_target = 250
    panel_list = []

    for judul, gambar in gambar_list:
        rasio = tinggi_target / gambar.shape[0]
        lebar_target = max(1, int(gambar.shape[1] * rasio))

        gambar_resize = cv2.resize(
            gambar,
            (lebar_target, tinggi_target)
        )

        gambar_warna = cv2.cvtColor(
            gambar_resize,
            cv2.COLOR_GRAY2BGR
        )

        panel = np.full(
            (tinggi_target + 45, lebar_target, 3),
            255,
            dtype=np.uint8
        )

        panel[45:, :] = gambar_warna

        cv2.putText(
            panel,
            judul,
            (8, 28),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 0, 0),
            1,
            cv2.LINE_AA
        )

        panel_list.append(panel)

    tinggi_maks = max(panel.shape[0] for panel in panel_list)
    panel_seragam = []

    for panel in panel_list:
        if panel.shape[0] < tinggi_maks:
            tambahan = np.full(
                (
                    tinggi_maks - panel.shape[0],
                    panel.shape[1],
                    3
                ),
                255,
                dtype=np.uint8
            )

            panel = np.vstack([panel, tambahan])

        panel_seragam.append(panel)

    perbandingan = cv2.hconcat(panel_seragam)

    nama_output = f"{Path(nama_file).stem}_perbandingan.png"

    simpan_gambar(
        "nomor_ijazah/7_perbandingan",
        nama_output,
        perbandingan
    )


# ============================================================
# 6. OCR DAN EVALUASI CER
# ============================================================

def jalankan_ocr(gambar):
    konfigurasi = (
        "--oem 3 --psm 6 "
        "-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "abcdefghijklmnopqrstuvwxyz0123456789-"
    )

    teks = pytesseract.image_to_string(
        gambar,
        config=konfigurasi
    )

    return bersihkan_teks(teks)


def jarak_levenshtein(teks_a, teks_b):
    a = str(teks_a)
    b = str(teks_b)

    if len(a) < len(b):
        a, b = b, a

    baris_sebelumnya = list(range(len(b) + 1))

    for i, karakter_a in enumerate(a, start=1):
        baris_sekarang = [i]

        for j, karakter_b in enumerate(b, start=1):
            biaya = 0 if karakter_a == karakter_b else 1

            baris_sekarang.append(min(
                baris_sebelumnya[j] + 1,
                baris_sekarang[j - 1] + 1,
                baris_sebelumnya[j - 1] + biaya
            ))

        baris_sebelumnya = baris_sekarang

    return baris_sebelumnya[-1]


def hitung_cer(teks_referensi, teks_prediksi):
    referensi = bersihkan_teks(teks_referensi)
    prediksi = bersihkan_teks(teks_prediksi)

    if not referensi:
        return None

    return jarak_levenshtein(referensi, prediksi) / len(referensi)


def baca_ground_truth(nama_file):
    """
    Jika tersedia ground_truth.csv, gunakan format:
    nama_file,nomor_ijazah

    Contoh:
    ijazah1.jpg,DN-123456789
    ijazah2.jpg,DN-987654321

    File ini hanya dibaca sebagai referensi input;
    hasil evaluasi tetap disimpan dalam TXT.
    """
    path_csv = os.path.join(
        os.path.dirname(__file__),
        "ground_truth.csv"
    )

    if not os.path.isfile(path_csv):
        return GROUND_TRUTH

    import csv

    with open(path_csv, "r", encoding="utf-8-sig", newline="") as file:
        pembaca = csv.DictReader(file)

        for row in pembaca:
            nama = (
                row.get("nama_file")
                or row.get("filename")
                or row.get("file")
                or ""
            ).strip()

            nomor = (
                row.get("nomor_ijazah")
                or row.get("ground_truth")
                or row.get("nomor")
                or ""
            ).strip()

            if nama.lower() == nama_file.lower() and nomor:
                return nomor

    return GROUND_TRUTH


# ============================================================
# 7. DETEKSI TANDA TANGAN
# ============================================================

def deteksi_tanda_tangan(crop_ttd, nama_file):
    gray = grayscale(crop_ttd)

    # Threshold adaptif untuk memisahkan tinta dari latar.
    threshold = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        31,
        15
    )

    # Hilangkan noise kecil.
    kernel_open = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (2, 2)
    )

    hasil_open = cv2.morphologyEx(
        threshold,
        cv2.MORPH_OPEN,
        kernel_open
    )

    # Sambungkan bagian tinta yang berdekatan.
    kernel_close = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (3, 3)
    )

    morfologi = cv2.morphologyEx(
        hasil_open,
        cv2.MORPH_CLOSE,
        kernel_close
    )

    jumlah_piksel = gray.shape[0] * gray.shape[1]
    jumlah_ink = cv2.countNonZero(morfologi)
    rasio_ink = jumlah_ink / max(1, jumlah_piksel)

    jumlah_label, label, statistik, pusat = (
        cv2.connectedComponentsWithStats(morfologi, 8)
    )

    komponen_besar = 0

    for i in range(1, jumlah_label):
        luas = statistik[i, cv2.CC_STAT_AREA]

        if luas >= 8:
            komponen_besar += 1

    # Heuristik sederhana, bukan verifikasi autentisitas tanda tangan.
    ada_ttd = (
        MIN_INK_RATIO <= rasio_ink <= MAX_INK_RATIO
        and komponen_besar >= 1
    )

    status = "PRESENT" if ada_ttd else "ABSENT"

    # Simpan seluruh tahap pemrosesan.
    simpan_gambar(
        "ttd/1_crop_asli",
        nama_file,
        crop_ttd
    )

    simpan_gambar(
        "ttd/2_grayscale",
        nama_file,
        gray
    )

    simpan_gambar(
        "ttd/3_threshold",
        nama_file,
        threshold
    )

    simpan_gambar(
        "ttd/4_morfologi",
        nama_file,
        morfologi
    )

    # Visualisasi hasil deteksi.
    visual = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    warna = (0, 160, 0) if ada_ttd else (0, 0, 220)

    teks_visual = f"{status} | Ink ratio: {rasio_ink:.4f}"

    cv2.putText(
        visual,
        teks_visual,
        (10, min(30, max(20, visual.shape[0] - 5))),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        warna,
        2,
        cv2.LINE_AA
    )

    simpan_gambar(
        "ttd/5_deteksi",
        nama_file,
        visual
    )

    return status, rasio_ink, komponen_besar


# ============================================================
# 8. MENYIMPAN LAPORAN TXT BERBENTUK TABEL
# ============================================================

def simpan_tabel_txt(judul, kolom, baris, path_file):
    data = [
        [str(nilai) for nilai in row]
        for row in baris
    ]

    lebar = []

    for i, nama_kolom in enumerate(kolom):
        panjang = [len(str(nama_kolom))]
        panjang.extend(len(row[i]) for row in data)
        lebar.append(max(panjang) + 2)

    garis = "+" + "+".join("-" * w for w in lebar) + "+"

    with open(path_file, "w", encoding="utf-8") as file:
        file.write(judul + "\n")
        file.write("=" * len(judul) + "\n\n")
        file.write(garis + "\n")

        file.write(
            "|"
            + "|".join(
                str(nama_kolom).center(lebar[i])
                for i, nama_kolom in enumerate(kolom)
            )
            + "|\n"
        )

        file.write(garis + "\n")

        for row in data:
            file.write(
                "|"
                + "|".join(
                    row[i].ljust(lebar[i])
                    for i in range(len(kolom))
                )
                + "|\n"
            )

        file.write(garis + "\n")


# ============================================================
# 9. PEMROSESAN SATU GAMBAR
# ============================================================

def proses_gambar(path_gambar, label_asli, data_evaluasi, data_verifikasi):
    nama_file = path_gambar.name

    print(f"\nMemproses: {nama_file}")
    print(f"Label folder: {label_asli}")

    gambar = cv2.imread(str(path_gambar))

    if gambar is None:
        print(f"[GAGAL] Gambar tidak bisa dibaca: {path_gambar}")
        return

    # --------------------------------------------------------
    # A. Crop otomatis berdasarkan rasio koordinat
    # --------------------------------------------------------
    crop_nomor = crop_rasio(gambar, CROP_NOMOR)
    crop_ttd = crop_rasio(gambar, CROP_TTD)

    simpan_gambar(
        "nomor_ijazah/1_crop_asli",
        nama_file,
        crop_nomor
    )

    gray_nomor, hasil_enhancement = semua_enhancement(crop_nomor)

    simpan_gambar(
        "nomor_ijazah/2_grayscale",
        nama_file,
        gray_nomor
    )

    # --------------------------------------------------------
    # B. Simpan hasil enhancement
    # --------------------------------------------------------
    nama_stem = Path(nama_file).stem

    folder_metode = {
        "Contrast Stretching": "nomor_ijazah/3_contrast_stretching",
        "CLAHE": "nomor_ijazah/4_clahe",
        "Gamma Correction": "nomor_ijazah/5_gamma_correction",
    }

    for metode, hasil in hasil_enhancement.items():
        simpan_gambar(
            folder_metode[metode],
            nama_file,
            hasil
        )

    # Buat perbandingan visual.
    simpan_perbandingan_enhancement(
        nama_file,
        crop_nomor,
        hasil_enhancement
    )

    # --------------------------------------------------------
    # C. OCR dan evaluasi CER
    # --------------------------------------------------------
    referensi = baca_ground_truth(nama_file)
    hasil_cer = []

    for metode, gambar_enhanced in hasil_enhancement.items():
        try:
            teks_ocr = jalankan_ocr(gambar_enhanced)
            cer = hitung_cer(referensi, teks_ocr)

            if cer is None:
                cer_tampilan = "N/A"
                cer_nilai = None
            else:
                cer_tampilan = f"{cer:.4f}"
                cer_nilai = cer

            hasil_cer.append({
                "metode": metode,
                "teks": teks_ocr,
                "cer": cer_nilai,
            })

            data_evaluasi.append([
                nama_file,
                metode,
                teks_ocr if teks_ocr else "(kosong)",
                cer_tampilan,
                f"{cer * 100:.2f}%" if cer is not None else "N/A"
            ])

            print(
                f"  {metode}: OCR='{teks_ocr}' | CER={cer_tampilan}"
            )

        except pytesseract.pytesseract.TesseractNotFoundError:
            raise RuntimeError(
                "Tesseract tidak ditemukan. Instal Tesseract OCR "
                "dan pastikan path executable sudah benar."
            )

    hasil_valid = [
        hasil for hasil in hasil_cer
        if hasil["cer"] is not None
    ]

    if hasil_valid:
        terbaik = min(hasil_valid, key=lambda x: x["cer"])

        data_evaluasi.append([
            nama_file,
            "METODE TERBAIK",
            terbaik["metode"],
            f"{terbaik['cer']:.4f}",
            f"{terbaik['cer'] * 100:.2f}%"
        ])

        print(
            f"  Metode terbaik: {terbaik['metode']} "
            f"(CER {terbaik['cer']:.4f})"
        )

    # --------------------------------------------------------
    # D. Deteksi tanda tangan
    # --------------------------------------------------------
    status, rasio_ink, komponen = deteksi_tanda_tangan(
        crop_ttd,
        nama_file
    )

    sesuai = "SESUAI" if status == label_asli else "TIDAK SESUAI"

    data_verifikasi.append([
        nama_file,
        label_asli,
        status,
        f"{rasio_ink:.4f}",
        str(komponen),
        sesuai
    ])

    print(
        f"  Tanda tangan: {status} | "
        f"Rasio tinta={rasio_ink:.4f} | Evaluasi={sesuai}"
    )


# ============================================================
# 10. PROGRAM UTAMA
# ============================================================

def main():
    konfigurasi_tesseract()
    buat_folder_output()

    data_evaluasi = []
    data_verifikasi = []

    daftar_present = daftar_gambar(FOLDER_PRESENT)
    daftar_absent = daftar_gambar(FOLDER_ABSENT)

    if not daftar_present and not daftar_absent:
        print("Tidak ada gambar yang ditemukan.")
        print(
            f"Periksa folder '{FOLDER_PRESENT}' dan "
            f"'{FOLDER_ABSENT}'."
        )
        return

    # Gambar dari folder pertama diasumsikan memiliki tanda tangan.
    for path_gambar in daftar_present:
        proses_gambar(
            path_gambar,
            "PRESENT",
            data_evaluasi,
            data_verifikasi
        )

    # Gambar dari folder kedua diasumsikan tanpa tanda tangan.
    for path_gambar in daftar_absent:
        proses_gambar(
            path_gambar,
            "ABSENT",
            data_evaluasi,
            data_verifikasi
        )

    # --------------------------------------------------------
    # Simpan laporan evaluasi OCR dalam TXT
    # --------------------------------------------------------
    simpan_tabel_txt(
        judul="HASIL EVALUASI OCR NOMOR IJAZAH",
        kolom=[
            "Nama File",
            "Metode",
            "Hasil OCR / Metode Terbaik",
            "CER",
            "CER (%)"
        ],
        baris=data_evaluasi,
        path_file=os.path.join(
            FOLDER_OUTPUT,
            "hasil_evaluasi.txt"
        )
    )

    # --------------------------------------------------------
    # Simpan laporan verifikasi tanda tangan dalam TXT
    # --------------------------------------------------------
    simpan_tabel_txt(
        judul="HASIL VERIFIKASI TANDA TANGAN",
        kolom=[
            "Nama File",
            "Label Asli",
            "Hasil Deteksi",
            "Rasio Tinta",
            "Komponen",
            "Evaluasi"
        ],
        baris=data_verifikasi,
        path_file=os.path.join(
            FOLDER_OUTPUT,
            "hasil_verifikasi.txt"
        )
    )

    print("\n" + "=" * 55)
    print("PEMROSESAN SELESAI")
    print("=" * 55)
    print(f"Total gambar bertanda tangan : {len(daftar_present)}")
    print(f"Total gambar tanpa tanda tangan: {len(daftar_absent)}")
    print(f"Folder hasil: {os.path.abspath(FOLDER_OUTPUT)}")
    print("Laporan OCR: outputs/hasil_evaluasi.txt")
    print("Laporan tanda tangan: outputs/hasil_verifikasi.txt")
    print(
        "Gambar perbandingan: "
        "outputs/nomor_ijazah/7_perbandingan/"
    )


if __name__ == "__main__":
    main()
    