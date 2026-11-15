"""
Tugas 7 (opsional) - Simulasi Replikasi Dua Server (Jakarta & Bandung)

Mensimulasikan delay replikasi dan masalah inconsistent read,
lalu memperbaikinya dengan mekanisme Read-Your-Writes sederhana
(version per user yang dibawa oleh sisi client / session).
"""

import time
import threading

REPLICATION_DELAY = 2.0
POLL_INTERVAL = 0.2
POLL_TIMEOUT = 5.0


class Replica:
    def __init__(self, name: str):
        self.name = name
        self.saldo: dict[str, float] = {}
        self.last_write_version: dict[str, int] = {}
        self._lock = threading.Lock()

    def write(self, user_id: str, saldo_baru: float, version: int) -> bool:
        with self._lock:
            current_version = self.last_write_version.get(user_id, 0)

            if version < current_version:
                print(
                    f"[{self.name}] WRITE DITOLAK: "
                    f"versi {version} lebih lama dari {current_version}"
                )
                return False

            self.saldo[user_id] = saldo_baru
            self.last_write_version[user_id] = version

        print(
            f"[{self.name}] WRITE: {user_id} = "
            f"Rp{saldo_baru:,.0f} (versi {version})"
        )
        return True

    def read_state(self, user_id: str) -> tuple[float, int]:
        with self._lock:
            saldo = self.saldo.get(user_id, 0.0)
            version = self.last_write_version.get(user_id, 0)

            return saldo, version


class ClientSession:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.versi_terakhir = 0
        self._lock = threading.Lock()

    def catat_versi(self, version: int):
        with self._lock:
            self.versi_terakhir = max(
                self.versi_terakhir, version
            )

    def get_versi(self) -> int:
        with self._lock:
            return self.versi_terakhir


class ReplicationSystem:
    def __init__(self):
        self.jakarta = Replica("Jakarta")
        self.bandung = Replica("Bandung")

        self.version_counter: dict[str, int] = {}

        self._write_lock = threading.Lock()

        self._timers = []
        self._timer_lock = threading.Lock()

    def pilih_server(self, server: str) -> Replica:
        if server == "Jakarta":
            return self.jakarta
        elif server == "Bandung":
            return self.bandung
        else:
            raise ValueError("Server tidak dikenal")

    def top_up(self, user_id: str, jumlah: float) -> int:
        if jumlah <= 0:
            raise ValueError("Jumlah top-up harus lebih dari 0")

        with self._write_lock:
            version = self.version_counter.get(user_id, 0) + 1
            self.version_counter[user_id] = version

            saldo_lama, _ = self.jakarta.read_state(user_id)
            saldo_baru = saldo_lama + jumlah

            berhasil = self.jakarta.write(
                user_id, saldo_baru, version
            )

            if not berhasil:
                raise RuntimeError("Top-up ke Jakarta gagal")

            timer = threading.Timer(
                REPLICATION_DELAY,
                self.bandung.write,
                args=(user_id, saldo_baru, version)
            )

            with self._timer_lock:
                self._timers.append(timer)

            timer.start()

            print(
                f"[REPLIKASI] Jakarta -> Bandung "
                f"dijadwalkan dalam {REPLICATION_DELAY} detik"
            )

            return version

    def baca_saldo_naif(
        self, user_id: str, server: str
    ) -> float:
        replica = self.pilih_server(server)
        saldo, _ = replica.read_state(user_id)

        return saldo

    def baca_saldo_read_your_writes(
        self,
        user_id: str,
        server: str,
        versi_minimal: int,
        strategi: str = "redirect"
    ) -> float:
        if strategi not in ("redirect", "polling"):
            raise ValueError(
                "Strategi harus redirect atau polling"
            )

        replica = self.pilih_server(server)

        saldo, versi = replica.read_state(user_id)

        if versi >= versi_minimal:
            print(
                f"[RYW] {server} sudah memenuhi versi "
                f"{versi_minimal}. Baca lokal."
            )
            return saldo

        print(
            f"[RYW] {server} masih versi {versi}. "
            f"Client membutuhkan versi {versi_minimal}."
        )

        if strategi == "polling":
            batas_waktu = time.monotonic() + POLL_TIMEOUT

            while time.monotonic() < batas_waktu:
                saldo, versi = replica.read_state(user_id)

                if versi >= versi_minimal:
                    print(
                        f"[RYW] {server} sudah sinkron "
                        f"pada versi {versi}."
                    )
                    return saldo

                time.sleep(POLL_INTERVAL)

            print(
                "[RYW] Polling timeout. "
                "Mengalihkan pembacaan ke Jakarta."
            )

        saldo, versi = self.jakarta.read_state(user_id)

        if versi < versi_minimal:
            raise RuntimeError(
                "Jakarta belum memenuhi versi yang diminta"
            )

        print(
            f"[RYW] Redirect berhasil. "
            f"Membaca saldo dari Jakarta versi {versi}."
        )

        return saldo

    def pesan_makanan(
        self,
        server: str,
        harga: float,
        saldo_dibaca: float
    ) -> bool:
        if saldo_dibaca >= harga:
            print(
                f"[{server}] PESANAN DITERIMA "
                f"(Rp{saldo_dibaca:,.0f} >= Rp{harga:,.0f})"
            )
            return True

        print(
            f"[{server}] PESANAN DITOLAK "
            f"(Rp{saldo_dibaca:,.0f} < Rp{harga:,.0f})"
        )
        return False

    def tunggu_replikasi_selesai(self):
        with self._timer_lock:
            timers = list(self._timers)
            self._timers.clear()

        for timer in timers:
            timer.join()


def main():
    system = ReplicationSystem()

    user_id = "user1"
    harga_makanan = 40000

    print("\n========================================")
    print(" SKENARIO 1: NAIVE READ")
    print("========================================")

    system.top_up(user_id, 50000)

    time.sleep(0.5)

    saldo = system.baca_saldo_naif(
        user_id, "Bandung"
    )

    print(f"Saldo Bandung : Rp{saldo:,.0f}")
    print(
        f"Saldo Jakarta : "
        f"Rp{system.jakarta.read_state(user_id)[0]:,.0f}"
    )

    system.pesan_makanan(
        "Bandung", harga_makanan, saldo
    )

    print("\n[BUG] Bandung masih membaca saldo lama.")

    system.tunggu_replikasi_selesai()

    print(
        "\n[EVENTUAL CONSISTENCY] "
        "Saldo Bandung setelah replikasi: "
        f"Rp{system.bandung.read_state(user_id)[0]:,.0f}"
    )

    print("\n========================================")
    print(" SKENARIO 2: READ-YOUR-WRITES REDIRECT")
    print("========================================")

    sesi = ClientSession(user_id)

    versi = system.top_up(user_id, 20000)
    sesi.catat_versi(versi)

    time.sleep(0.5)

    saldo_naif = system.baca_saldo_naif(
        user_id, "Bandung"
    )

    print(f"Saldo naif Bandung : Rp{saldo_naif:,.0f}")

    saldo = system.baca_saldo_read_your_writes(
        user_id,
        "Bandung",
        sesi.get_versi(),
        strategi="redirect"
    )

    print(f"Saldo RYW           : Rp{saldo:,.0f}")

    assert saldo == 70000

    system.pesan_makanan(
        "Bandung", 65000, saldo
    )

    print("[BENAR] Read-Your-Writes berhasil.")

    system.tunggu_replikasi_selesai()

    print("\n========================================")
    print(" SKENARIO 3: READ-YOUR-WRITES POLLING")
    print("========================================")

    versi = system.top_up(user_id, 10000)
    sesi.catat_versi(versi)

    saldo = system.baca_saldo_read_your_writes(
        user_id,
        "Bandung",
        sesi.get_versi(),
        strategi="polling"
    )

    print(f"Saldo RYW Polling  : Rp{saldo:,.0f}")

    assert saldo == 80000

    print("[BENAR] Polling berhasil.")

    system.tunggu_replikasi_selesai()

    print("\n========================================")
    print(" HASIL AKHIR REPLIKASI")
    print("========================================")

    saldo_jakarta, versi_jakarta = (
        system.jakarta.read_state(user_id)
    )

    saldo_bandung, versi_bandung = (
        system.bandung.read_state(user_id)
    )

    print(
        f"Jakarta : Rp{saldo_jakarta:,.0f} "
        f"(versi {versi_jakarta})"
    )

    print(
        f"Bandung : Rp{saldo_bandung:,.0f} "
        f"(versi {versi_bandung})"
    )

    assert saldo_jakarta == saldo_bandung
    assert versi_jakarta == versi_bandung

    print("\n[SELESAI] Kedua replika sudah konsisten.")


if __name__ == "__main__":
    main()