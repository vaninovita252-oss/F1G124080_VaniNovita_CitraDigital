import os
import re
import csv
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

# Ganti dengan nomor ijazah yang benar jika semua gambar sama.
GROUND_TRUTH = "DN-123456789"

# Koordinat crop: x1, y1, x2, y2 dalam rasio 0 sampai 1.
# Koordinat ini hanya titik awal; sesuaikan dengan layout ijazah.
CROP_NOMOR = (0.05, 0.65, 0.95, 0.98)
CROP_TTD = (0.15, 0.15, 0.95, 0.65)

GAMMA_VALUE = 1.5

# Parameter awal deteksi tinta; mungkin perlu disesuaikan.
MIN_INK_RATIO = 0.003
MAX_INK_RATIO = 0.35
MIN_COMPONENT_AREA = 8

EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}


# ============================================================
# 2. TESSERACT OCR
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


# ============================================================
# 3. FOLDER DAN UTILITAS
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
        "ttd/6_kontur",
        "ttd/7_perbandingan_proses",
    ]

    os.makedirs(FOLDER_OUTPUT, exist_ok=True)

    for nama in folder:
        os.makedirs(
            os.path.join(FOLDER_OUTPUT, nama),
            exist_ok=True
        )


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
    folder = os.path.join(FOLDER_OUTPUT, folder_rel)
    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, nama_file)

    sukses = cv2.imwrite(path, gambar)

    if not sukses:
        print(f"[PERINGATAN] Gagal menyimpan: {path}")


def grayscale(gambar):
    if len(gambar.shape) == 2:
        return gambar.copy()

    return cv2.cvtColor(gambar, cv2.COLOR_BGR2GRAY)


def crop_rasio(gambar, koordinat):
    tinggi, lebar = gambar.shape[:2]
    x1, y1, x2, y2 = koordinat

    x1 = max(0, min(lebar - 1, int(x1 * lebar)))
    x2 = max(x1 + 1, min(lebar, int(x2 * lebar)))
    y1 = max(0, min(tinggi - 1, int(y1 * tinggi)))
    y2 = max(y1 + 1, min(tinggi, int(y2 * tinggi)))

    return gambar[y1:y2, x1:x2].copy()


def bersihkan_teks(teks):
    teks = str(teks).upper().strip()
    teks = re.sub(r"\s+", "", teks)
    return re.sub(r"[^A-Z0-9-]", "", teks)


# ============================================================
# 4. ENHANCEMENT NOMOR IJAZAH
# ============================================================

def contrast_stretching(gambar):
    gray = grayscale(gambar)
    nilai_min = int(np.min(gray))
    nilai_maks = int(np.max(gray))

    if nilai_maks == nilai_min:
        return gray.copy()

    hasil = (
        (gray.astype(np.float32) - nilai_min)
        * (255.0 / (nilai_maks - nilai_min))
    )

    return np.clip(hasil, 0, 255).astype(np.uint8)


def clahe_enhancement(gambar):
    gray = grayscale(gambar)

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    return clahe.apply(gray)


def gamma_correction(gambar, gamma=GAMMA_VALUE):
    gray = grayscale(gambar)
    gamma = max(0.01, float(gamma))

    tabel = np.array([
        ((i / 255.0) ** (1.0 / gamma)) * 255
        for i in range(256)
    ]).astype(np.uint8)

    return cv2.LUT(gray, tabel)


def semua_enhancement(crop):
    gray = grayscale(crop)

    hasil = {
        "Contrast Stretching": contrast_stretching(gray),
        "CLAHE": clahe_enhancement(gray),
        "Gamma Correction": gamma_correction(gray),
    }

    return gray, hasil


def simpan_perbandingan_enhancement(
    nama_file,
    crop_asli,
    hasil_enhancement
):
    daftar_panel = [
        ("Crop Asli", grayscale(crop_asli)),
        ("Contrast Stretching", hasil_enhancement["Contrast Stretching"]),
        ("CLAHE", hasil_enhancement["CLAHE"]),
        ("Gamma Correction", hasil_enhancement["Gamma Correction"]),
    ]

    tinggi_target = 250
    panel_list = []

    for judul, img in daftar_panel:
        rasio = tinggi_target / img.shape[0]
        lebar_target = max(1, int(img.shape[1] * rasio))

        img = cv2.resize(img, (lebar_target, tinggi_target))
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        panel = np.full(
            (tinggi_target + 45, lebar_target, 3),
            255,
            dtype=np.uint8
        )

        panel[45:, :] = img

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

    tinggi = max(panel.shape[0] for panel in panel_list)
    panel_seragam = []

    for panel in panel_list:
        if panel.shape[0] < tinggi:
            tambahan = np.full(
                (tinggi - panel.shape[0], panel.shape[1], 3),
                255,
                dtype=np.uint8
            )
            panel = np.vstack([panel, tambahan])

        panel_seragam.append(panel)

    hasil = cv2.hconcat(panel_seragam)

    simpan_gambar(
        "nomor_ijazah/7_perbandingan",
        f"{Path(nama_file).stem}_perbandingan.png",
        hasil
    )


# ============================================================
# 5. OCR DAN CER
# ============================================================

def jalankan_ocr(gambar):
    konfigurasi = (
        "--oem 3 --psm 6 "
        "-c tessedit_char_whitelist="
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-"
    )

    teks = pytesseract.image_to_string(
        gambar,
        config=konfigurasi
    )

    return bersihkan_teks(teks)


def jarak_levenshtein(a, b):
    if len(a) < len(b):
        a, b = b, a

    baris_lama = list(range(len(b) + 1))

    for i, char_a in enumerate(a, start=1):
        baris_baru = [i]

        for j, char_b in enumerate(b, start=1):
            biaya = 0 if char_a == char_b else 1

            baris_baru.append(min(
                baris_lama[j] + 1,
                baris_baru[j - 1] + 1,
                baris_lama[j - 1] + biaya
            ))

        baris_lama = baris_baru

    return baris_lama[-1]


def hitung_cer(referensi, prediksi):
    referensi = bersihkan_teks(referensi)
    prediksi = bersihkan_teks(prediksi)

    if not referensi:
        return None

    return jarak_levenshtein(referensi, prediksi) / len(referensi)


def baca_ground_truth(nama_file):
    path_csv = Path("ground_truth.csv")

    if not path_csv.exists():
        return GROUND_TRUTH

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
# 6. DETEKSI TANDA TANGAN DENGAN BOUNDING BOX
# ============================================================

def deteksi_tanda_tangan(crop_ttd, nama_file):
    """
    Pipeline:
    crop -> grayscale -> threshold -> morfologi -> kontur
    -> bounding box -> prediksi keberadaan tinta.
    """

    # Tahap 1: grayscale
    gray = grayscale(crop_ttd)

    # Tingkatkan kontras lokal agar tinta lebih terlihat.
    gray = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    ).apply(gray)

    # Tahap 2: thresholding adaptif.
    threshold = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        31,
        15
    )

    # Tahap 3: buang noise kecil.
    kernel_open = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (2, 2)
    )

    hasil_open = cv2.morphologyEx(
        threshold,
        cv2.MORPH_OPEN,
        kernel_open
    )

    # Tahap 4: sambungkan goresan tinta yang terputus.
    kernel_close = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (3, 3)
    )

    morfologi = cv2.morphologyEx(
        hasil_open,
        cv2.MORPH_CLOSE,
        kernel_close
    )

    # Tahap 5: cari kontur.
    kontur, _ = cv2.findContours(
        morfologi.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    luas_minimum = max(
        MIN_COMPONENT_AREA,
        int(gray.shape[0] * gray.shape[1] * 0.00001)
    )

    kontur_valid = []

    for c in kontur:
        luas = cv2.contourArea(c)

        if luas >= luas_minimum:
            kontur_valid.append(c)

    # Gabungkan bounding box kontur yang cukup besar.
    kotak = []

    for c in kontur_valid:
        x, y, w, h = cv2.boundingRect(c)
        kotak.append((x, y, w, h))

    # Ukuran dan jumlah piksel tinta.
    jumlah_piksel = gray.shape[0] * gray.shape[1]
    jumlah_ink = cv2.countNonZero(morfologi)
    rasio_ink = jumlah_ink / max(1, jumlah_piksel)

    # Prediksi sederhana berdasarkan tinta dan komponen.
    ada_ttd = (
        MIN_INK_RATIO <= rasio_ink <= MAX_INK_RATIO
        and len(kotak) >= 1
    )

    status = "PRESENT" if ada_ttd else "ABSENT"

    # --------------------------------------------------------
    # Simpan setiap tahap
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Visualisasi bounding box
    # --------------------------------------------------------

    visual = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    for x, y, w, h in kotak:
        cv2.rectangle(
            visual,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    warna = (0, 180, 0) if ada_ttd else (0, 0, 255)

    cv2.rectangle(
        visual,
        (0, 0),
        (visual.shape[1] - 1, visual.shape[0] - 1),
        warna,
        3
    )

    teks_status = f"{status} | Ink ratio: {rasio_ink:.4f}"

    cv2.putText(
        visual,
        teks_status,
        (8, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        warna,
        2,
        cv2.LINE_AA
    )

    simpan_gambar(
        "ttd/5_deteksi",
        nama_file,
        visual
    )

    # --------------------------------------------------------
    # Gambar semua kontur
    # --------------------------------------------------------

    visual_kontur = cv2.cvtColor(
        morfologi,
        cv2.COLOR_GRAY2BGR
    )

    if kontur_valid:
        cv2.drawContours(
            visual_kontur,
            kontur_valid,
            -1,
            (0, 255, 0),
            2
        )

    simpan_gambar(
        "ttd/6_kontur",
        nama_file,
        visual_kontur
    )

    # --------------------------------------------------------
    # Perbandingan seluruh tahap dalam satu gambar
    # --------------------------------------------------------

    tahapan = [
        ("Crop Asli", grayscale(crop_ttd)),
        ("Grayscale", gray),
        ("Threshold", threshold),
        ("Morfologi", morfologi),
        ("Bounding Box", cv2.cvtColor(
            visual,
            cv2.COLOR_BGR2GRAY
        )),
    ]

    panel_list = []
    tinggi_target = 220

    for judul, img in tahapan:
        rasio = tinggi_target / img.shape[0]
        lebar_target = max(1, int(img.shape[1] * rasio))

        img = cv2.resize(img, (lebar_target, tinggi_target))
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        panel = np.full(
            (tinggi_target + 42, lebar_target, 3),
            255,
            dtype=np.uint8
        )

        panel[42:, :] = img

        cv2.putText(
            panel,
            judul,
            (8, 26),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 0, 0),
            1,
            cv2.LINE_AA
        )

        panel_list.append(panel)

    tinggi_maks = max(p.shape[0] for p in panel_list)
    panel_seragam = []

    for panel in panel_list:
        if panel.shape[0] < tinggi_maks:
            tambahan = np.full(
                (tinggi_maks - panel.shape[0], panel.shape[1], 3),
                255,
                dtype=np.uint8
            )
            panel = np.vstack([panel, tambahan])

        panel_seragam.append(panel)

    gambar_proses = cv2.hconcat(panel_seragam)

    simpan_gambar(
        "ttd/7_perbandingan_proses",
        f"{Path(nama_file).stem}_proses_ttd.png",
        gambar_proses
    )

    return status, rasio_ink, len(kotak)


# ============================================================
# 7. MENYIMPAN TABEL TXT
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
# 8. PEMROSESAN GAMBAR
# ============================================================

def proses_gambar(
    path_gambar,
    label_asli,
    data_evaluasi,
    data_verifikasi
):
    nama_file = path_gambar.name

    print(f"\nMemproses: {nama_file}")

    gambar = cv2.imread(str(path_gambar))

    if gambar is None:
        print(f"[GAGAL] Gambar tidak dapat dibaca: {path_gambar}")
        return

    # Crop dua area secara otomatis.
    crop_nomor = crop_rasio(gambar, CROP_NOMOR)
    crop_ttd = crop_rasio(gambar, CROP_TTD)

    # ========================================================
    # OCR NOMOR IJAZAH
    # ========================================================

    gray_nomor, hasil_enhancement = semua_enhancement(crop_nomor)

    simpan_gambar(
        "nomor_ijazah/1_crop_asli",
        nama_file,
        crop_nomor
    )

    simpan_gambar(
        "nomor_ijazah/2_grayscale",
        nama_file,
        gray_nomor
    )

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

    simpan_perbandingan_enhancement(
        nama_file,
        crop_nomor,
        hasil_enhancement
    )

    referensi = baca_ground_truth(nama_file)
    hasil_cer = []

    for metode, gambar_enhanced in hasil_enhancement.items():
        teks_ocr = jalankan_ocr(gambar_enhanced)
        cer = hitung_cer(referensi, teks_ocr)

        hasil_cer.append({
            "metode": metode,
            "teks": teks_ocr,
            "cer": cer
        })

        data_evaluasi.append([
            nama_file,
            metode,
            teks_ocr if teks_ocr else "(kosong)",
            f"{cer:.4f}" if cer is not None else "N/A",
            f"{cer * 100:.2f}%" if cer is not None else "N/A"
        ])

        print(
            f"  OCR {metode}: {teks_ocr} "
            f"| CER: {cer:.4f}" if cer is not None
            else f"  OCR {metode}: {teks_ocr} | CER: N/A"
        )

    hasil_valid = [
        h for h in hasil_cer
        if h["cer"] is not None
    ]

    if hasil_valid:
        terbaik = min(hasil_valid, key=lambda h: h["cer"])

        data_evaluasi.append([
            nama_file,
            "METODE TERBAIK",
            terbaik["metode"],
            f"{terbaik['cer']:.4f}",
            f"{terbaik['cer'] * 100:.2f}%"
        ])

    # ========================================================
    # DETEKSI TANDA TANGAN
    # ========================================================

    status, rasio_ink, jumlah_kotak = deteksi_tanda_tangan(
        crop_ttd,
        nama_file
    )

    evaluasi = (
        "SESUAI"
        if status == label_asli
        else "TIDAK SESUAI"
    )

    data_verifikasi.append([
        nama_file,
        label_asli,
        status,
        f"{rasio_ink:.4f}",
        str(jumlah_kotak),
        evaluasi
    ])

    print(
        f"  Tanda tangan: {status}; "
        f"rasio tinta={rasio_ink:.4f}; "
        f"evaluasi={evaluasi}"
    )


# ============================================================
# 9. MAIN
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
        print("Periksa nama folder input.")
        return

    for path_gambar in daftar_present:
        proses_gambar(
            path_gambar,
            "PRESENT",
            data_evaluasi,
            data_verifikasi
        )

    for path_gambar in daftar_absent:
        proses_gambar(
            path_gambar,
            "ABSENT",
            data_evaluasi,
            data_verifikasi
        )

    simpan_tabel_txt(
        "HASIL EVALUASI OCR NOMOR IJAZAH",
        [
            "Nama File",
            "Metode",
            "Hasil OCR / Metode Terbaik",
            "CER",
            "CER (%)"
        ],
        data_evaluasi,
        os.path.join(FOLDER_OUTPUT, "hasil_evaluasi.txt")
    )

    simpan_tabel_txt(
        "HASIL VERIFIKASI TANDA TANGAN",
        [
            "Nama File",
            "Label Asli",
            "Hasil Deteksi",
            "Rasio Tinta",
            "Jumlah Kotak",
            "Evaluasi"
        ],
        data_verifikasi,
        os.path.join(FOLDER_OUTPUT, "hasil_verifikasi.txt")
    )

    print("\n" + "=" * 55)
    print("PEMROSESAN SELESAI")
    print("=" * 55)
    print(f"Jumlah gambar PRESENT: {len(daftar_present)}")
    print(f"Jumlah gambar ABSENT : {len(daftar_absent)}")
    print(f"Folder hasil: {os.path.abspath(FOLDER_OUTPUT)}")
    print("Laporan OCR: outputs/hasil_evaluasi.txt")
    print("Laporan tanda tangan: outputs/hasil_verifikasi.txt")
    print("Visualisasi tanda tangan: outputs/ttd/7_perbandingan_proses/")


if __name__ == "__main__":
    main()