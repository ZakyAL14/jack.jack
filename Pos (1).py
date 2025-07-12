import csv
import os
from datetime import datetime

# ================= LINKED LIST =================
class ProdukNode:
    def __init__(self, kode, nama, harga, stok):
        self.kode = kode
        self.nama = nama
        self.harga = harga
        self.stok = stok
        self.next = None

class ProdukLinkedList:
    def __init__(self):
        self.head = None

    def tambah_produk(self, kode, nama, harga, stok):
        node_baru = ProdukNode(kode, nama, harga, stok)
        if not self.head:
            self.head = node_baru
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = node_baru

    def cari_produk(self, kode):
        cur = self.head
        while cur:
            if cur.kode == kode:
                return cur
            cur = cur.next
        return None

    def tampilkan(self):
        cur = self.head
        print("\n=== DAFTAR PRODUK ===")
        if not cur:
            print("Tidak ada produk.")
        while cur:
            print(f"{cur.kode} | {cur.nama} | Rp{cur.harga} | Stok: {cur.stok}")
            cur = cur.next

# ================ STACK ========================
class StackTransaksi:
    def __init__(self):
        self.stack = []

    def push(self, data):
        self.stack.append(data)

    def tampilkan(self):
        print("\n=== HISTORI TRANSAKSI TERBARU ===")
        if not self.stack:
            print("Belum ada transaksi.")
        for item in reversed(self.stack[-5:]):
            print(item)

# ============= INISIALISASI CSV ================
def buat_produk_awal():
    if not os.path.exists("produk.csv"):
        with open("produk.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["P001", "BearBrand", 10000, 100])
            writer.writerow(["P002", "Sari Roti", 14500, 20])
            writer.writerow(["P003", "Silverqueen", 15000, 15])
        print("File produk.csv berhasil dibuat otomatis.")

# ============= FUNGSI CSV ======================
def load_produk_csv():
    produk_list = ProdukLinkedList()
    try:
        with open("produk.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # Hindari baris kosong
                    produk_list.tambah_produk(row[0], row[1], int(row[2]), int(row[3]))
    except FileNotFoundError:
        print("produk.csv tidak ditemukan.")
    return produk_list

def simpan_produk_csv(produk_list):
    with open("produk.csv", "w", newline="") as file:
        writer = csv.writer(file)
        cur = produk_list.head
        while cur:
            writer.writerow([cur.kode, cur.nama, cur.harga, cur.stok])
            cur = cur.next

def simpan_transaksi_csv(kode, nama, jumlah, total):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("riwayat_transaksi.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([waktu, kode, nama, jumlah, total])

# ============ FITUR APLIKASI ===================
def tampilkan_produk(produk_list):
    produk_list.tampilkan()

def transaksi_penjualan(produk_list, histori):
    kode = input("Masukkan kode produk: ").strip()
    produk = produk_list.cari_produk(kode)
    if produk:
        print(f"{produk.nama} - Harga: Rp{produk.harga} - Stok: {produk.stok}")
        try:
            jumlah = int(input("Jumlah beli: "))
            if jumlah <= produk.stok:
                total = jumlah * produk.harga
                produk.stok -= jumlah
                simpan_produk_csv(produk_list)
                simpan_transaksi_csv(produk.kode, produk.nama, jumlah, total)
                histori.push(f"{produk.nama} | Jumlah: {jumlah} | Total: Rp{total}")
                print(f"Transaksi berhasil. Total bayar: Rp{total}")
            else:
                print("Stok tidak cukup.")
        except ValueError:
            print("Input jumlah tidak valid.")
    else:
        print("Produk tidak ditemukan.")

# ============ MENU UTAMA =======================
def main():
    buat_produk_awal()  # Membuat file CSV jika belum ada
    produk_list = load_produk_csv()
    histori_stack = StackTransaksi()

    while True:
        print("""
=== APLIKASI POS DENGAN LINKED LIST & STACK ===
1. Tampilkan Produk
2. Transaksi Penjualan
3. Tampilkan Histori Transaksi
4. Keluar
""")
        pilih = input("Pilih menu: ")

        if pilih == "1":
            tampilkan_produk(produk_list)
        elif pilih == "2":
            transaksi_penjualan(produk_list, histori_stack)
        elif pilih == "3":
            histori_stack.tampilkan()
        elif pilih == "4":
            print("Terima kasih telah menggunakan aplikasi POS.")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
