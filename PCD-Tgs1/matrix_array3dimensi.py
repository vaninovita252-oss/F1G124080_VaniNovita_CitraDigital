
import numpy as np


def input_array_3d(nama, depth, baris, kolom):
    print(f"\n=== INPUT ARRAY {nama} ===")

    array = []

    for d in range(depth):
        print(f"\nArray {nama} - Matriks ke-{d + 1}")

        matriks = []

        for i in range(baris):
            while True:
                try:
                    data = input(f"Baris {i + 1}: ").split()

                    if len(data) != kolom:
                        print(f"  Masukkan {kolom} angka.")
                        continue

                    matriks.append([int(x) for x in data])
                    break

                except ValueError:
                    print("  Input harus berupa angka.")

        array.append(matriks)

    # Mengubah list Python menjadi array NumPy 3D
    return np.array(array, dtype=int)


def perkalian_matriks(A, B):
    depth = A.shape[0]

    baris_A = A.shape[1]
    kolom_A = A.shape[2]

    baris_B = B.shape[1]
    kolom_B = B.shape[2]

    # Syarat perkalian matriks
    if kolom_A != baris_B:
        return None

    hasil = []

    # Perkalian setiap matriks pada lapisan yang sama
    for d in range(depth):
        matriks_hasil = np.matmul(A[d], B[d])
        hasil.append(matriks_hasil)

    # Mengubah hasil menjadi array NumPy 3D
    return np.array(hasil, dtype=int)


def tampilkan_array(array, nama):
    print(f"\nArray {nama}:")

    for d, matriks in enumerate(array):
        print(f"\nArray {nama} - Matriks ke-{d + 1}")

        for baris in matriks:
            print(" ".join(map(str, baris)))


# ========================================
# PROGRAM UTAMA
# ========================================

print("=" * 40)
print("   PERKALIAN MATRIKS ARRAY 3D")
print("=" * 40)

try:
    # Input ukuran array
    depth = int(input("\nJumlah matriks/lapisan: "))

    print("\nUkuran Array A")
    baris_A = int(input("Jumlah baris   : "))
    kolom_A = int(input("Jumlah kolom   : "))

    print("\nUkuran Array B")
    baris_B = int(input("Jumlah baris   : "))
    kolom_B = int(input("Jumlah kolom   : "))

    # Mengecek syarat perkalian
    if kolom_A != baris_B:
        print("\nERROR: Kolom Array A harus sama dengan baris Array B.")
        raise SystemExit

    # Input Array A
    A = input_array_3d(
        "A", depth, baris_A, kolom_A
    )

    # Input Array B
    B = input_array_3d(
        "B", depth, baris_B, kolom_B
    )

    # Perkalian
    hasil = perkalian_matriks(A, B)

    # Menampilkan hasil
    print("\n" + "=" * 40)
    print("        HASIL PERKALIAN")
    print("=" * 40)

    tampilkan_array(A, "A")
    tampilkan_array(B, "B")
    tampilkan_array(hasil, "A x B")

except ValueError:
    print("\nERROR: Input harus berupa angka.")
