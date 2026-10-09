"""
Tugas 4 - Jalur A: RPC Server (simulasi modul Pembayaran)
Memakai xmlrpc.server dari Python standard library - tidak perlu install apa pun.
"""

from xmlrpc.server import SimpleXMLRPCServer

# Simulasi "database" saldo user
saldo_user = {
    "user1": 50000,
    "user2": 120000,
}


def cek_saldo(user_id: str) -> float:
    """Kembalikan saldo user_id saat ini."""
    # TODO 1: Mengambil saldo user
    # Jika user tidak ditemukan, kembalikan 0
    return saldo_user.get(user_id, 0)


def proses_pembayaran(user_id: str, jumlah: float) -> dict:
    """Kurangi saldo user sejumlah jumlah. Kembalikan status hasil."""

    # Memeriksa apakah user terdaftar
    if user_id not in saldo_user:
        return {
            "status": "gagal",
            "pesan": "User tidak ditemukan",
            "saldo_akhir": 0
        }

    # Memvalidasi jumlah pembayaran
    if jumlah <= 0:
        return {
            "status": "gagal",
            "pesan": "Jumlah pembayaran harus lebih dari 0",
            "saldo_akhir": saldo_user[user_id]
        }

    # Memvalidasi apakah saldo mencukupi
    if saldo_user[user_id] < jumlah:
        return {
            "status": "gagal",
            "pesan": "Saldo tidak mencukupi",
            "saldo_akhir": saldo_user[user_id]
        }

    # Mengurangi saldo jika pembayaran berhasil
    saldo_user[user_id] -= jumlah

    return {
        "status": "sukses",
        "pesan": "Pembayaran berhasil",
        "saldo_akhir": saldo_user[user_id]
    }


def main():
    # TODO 3: Membuat server RPC pada localhost port 8000
    server = SimpleXMLRPCServer(
        ("localhost", 8000),
        allow_none=True
    )

    # Mendaftarkan fungsi agar dapat dipanggil oleh client
    server.register_function(cek_saldo, "cek_saldo")
    server.register_function(proses_pembayaran, "proses_pembayaran")

    print("RPC server modul Pembayaran berjalan di port 8000...")

    # Menjalankan server dan menunggu permintaan dari client
    server.serve_forever()


if __name__ == "__main__":
    main()
