"""
Tugas 4 - Jalur A: RPC Client (simulasi modul Pesanan)
Jalankan server.py di terminal lain terlebih dahulu.
"""

import xmlrpc.client
import time


def main():
    # TODO 1: Membuat koneksi ke server RPC
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000")

    print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")

    # Mencatat waktu sebelum request dikirim
    start = time.time()

    # TODO 2: Memanggil cek_saldo dan menunggu respons server
    hasil_saldo = proxy.cek_saldo("user1")

    # Menghitung waktu tempuh setelah respons diterima
    end = time.time()
    waktu_tempuh = end - start

    print("Hasil cek saldo:", hasil_saldo)
    print(f"Waktu tempuh: {waktu_tempuh:.2f} detik")

    print("Memanggil proses_pembayaran('user1', 20000) ...")

    # TODO 3: Memanggil proses_pembayaran
    hasil_pembayaran = proxy.proses_pembayaran("user1", 20000)

    print("Hasil proses pembayaran:", hasil_pembayaran)


if __name__ == "__main__":
    main()