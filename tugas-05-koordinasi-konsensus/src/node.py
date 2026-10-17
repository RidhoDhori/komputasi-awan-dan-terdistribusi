"""
Tugas 5 - Simulasi Node untuk Bully Algorithm

Infrastruktur jaringan (socket server/client) sudah disediakan.
Logika Bully Algorithm dilengkapi pada bagian TODO.

Contoh menjalankan (5 terminal terpisah):
    python node.py --id 1 --port 5001 --peers 5002,5003,5004,5005
    python node.py --id 2 --port 5002 --peers 5001,5003,5004,5005
    ... dst untuk id 3, 4, 5
"""

import argparse
import socket
import threading
import time

ELECTION_TIMEOUT = 2.0     # detik menunggu balasan OK sebelum menyatakan diri leader
COORDINATOR_TIMEOUT = 8.0  # detik menunggu COORDINATOR setelah menerima OK


class Node:
    def __init__(self, node_id: int, port: int, peers: dict):
        self.node_id = node_id
        self.port = port

        # peers: dict {peer_id: peer_port} untuk semua node LAIN
        self.peers = peers
        self.leader_id = None
        self.lock = threading.Lock()

        # Event untuk menandai penerimaan pesan OK
        self.ok_received = threading.Event()

        # Event untuk menandai penerimaan pesan COORDINATOR yang sah
        self.coordinator_received = threading.Event()

        # Mencegah beberapa election berjalan bersamaan pada node yang sama
        self.election_lock = threading.Lock()

        self.election_in_progress = False
        self.last_coordinator_time = time.time()

    # ---------- Infrastruktur jaringan (SUDAH LENGKAP, jangan diubah) ----------

    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("localhost", self.port))
        server.listen()

        print(f"[Node {self.node_id}] Listening di port {self.port}")

        while True:
            conn, _ = server.accept()
            threading.Thread(
                target=self.handle_connection,
                args=(conn,),
                daemon=True
            ).start()

    def handle_connection(self, conn: socket.socket):
        with conn:
            data = conn.recv(1024).decode()

            if not data:
                return

            sender_id, msg_type = data.split(":")
            self.on_message(int(sender_id), msg_type)

    def send_message(self, target_port: int, msg_type: str) -> bool:
        """Kirim pesan ke node lain. Return False jika target tidak merespons."""
        try:
            with socket.create_connection(
                ("localhost", target_port),
                timeout=1.0
            ) as s:
                s.sendall(f"{self.node_id}:{msg_type}".encode())

            return True

        except (ConnectionRefusedError, socket.timeout, OSError):
            return False

    # ---------- Logika Bully Algorithm ----------

    def on_message(self, sender_id: int, msg_type: str):
        """Memproses pesan yang diterima dari node lain."""

        if msg_type == "ELECTION":
            print(
                f"[Node {self.node_id}] Menerima ELECTION "
                f"dari node {sender_id}"
            )

            if self.node_id > sender_id:
                sender_port = self.peers.get(sender_id)

                if sender_port is not None:
                    self.send_message(sender_port, "OK")
                    print(
                        f"[Node {self.node_id}] Mengirim OK "
                        f"ke node {sender_id}"
                    )

                threading.Thread(
                    target=self.start_election,
                    daemon=True
                ).start()

        elif msg_type == "OK":
            print(
                f"[Node {self.node_id}] Menerima OK "
                f"dari node {sender_id}"
            )
            self.ok_received.set()

        elif msg_type == "COORDINATOR":
            # Prinsip Bully: hanya node ber-ID LEBIH TINGGI yang boleh
            # menjadi leader. COORDINATOR dari node ber-ID lebih rendah
            # (basi/stale) ditolak, lalu node ini mengambil alih lewat election.
            if sender_id < self.node_id:
                print(
                    f"[Node {self.node_id}] Mengabaikan COORDINATOR dari "
                    f"node {sender_id} (ID lebih rendah). Memulai election."
                )
                threading.Thread(
                    target=self.start_election,
                    daemon=True
                ).start()
                return

            with self.lock:
                old_leader = self.leader_id
                self.leader_id = sender_id
                self.last_coordinator_time = time.time()

            self.coordinator_received.set()

            if old_leader != sender_id:
                print(
                    f"[Node {self.node_id}] Leader berubah: "
                    f"{old_leader} -> {sender_id}"
                )
            else:
                print(
                    f"[Node {self.node_id}] Leader tetap: {sender_id}"
                )

        else:
            print(
                f"[Node {self.node_id}] Pesan tidak dikenal: "
                f"{msg_type} dari node {sender_id}"
            )

    def start_election(self):
        """Memulai election untuk menentukan leader."""

        if not self.election_lock.acquire(blocking=False):
            return

        try:
            # Diulang jika sudah menerima OK tetapi COORDINATOR tidak datang
            # (misalnya node yang membalas OK crash sebelum mengumumkan diri).
            while True:
                higher_peers = {
                    pid: port
                    for pid, port in self.peers.items()
                    if pid > self.node_id
                }

                print(
                    f"[Node {self.node_id}] Memulai election. "
                    f"Peer dengan ID lebih tinggi: "
                    f"{list(higher_peers.keys())}"
                )

                self.ok_received.clear()
                self.coordinator_received.clear()

                reachable = 0

                # Kirim ELECTION ke seluruh peer dengan ID lebih tinggi
                for peer_id, peer_port in higher_peers.items():
                    success = self.send_message(peer_port, "ELECTION")

                    if success:
                        reachable += 1
                        print(
                            f"[Node {self.node_id}] Mengirim ELECTION "
                            f"ke node {peer_id}"
                        )
                    else:
                        print(
                            f"[Node {self.node_id}] Node {peer_id} "
                            f"tidak merespons"
                        )

                # Tidak ada node lebih tinggi yang hidup -> menang langsung,
                # tidak perlu menunggu ELECTION_TIMEOUT.
                if reachable == 0:
                    self.declare_leader()
                    return

                # Tunggu OK selama batas waktu
                if not self.ok_received.wait(ELECTION_TIMEOUT):
                    self.declare_leader()
                    return

                print(
                    f"[Node {self.node_id}] Menerima OK. "
                    "Menunggu COORDINATOR."
                )

                # Tunggu pemenang mengumumkan diri
                if self.coordinator_received.wait(COORDINATOR_TIMEOUT):
                    return

                print(
                    f"[Node {self.node_id}] COORDINATOR tidak diterima "
                    "dalam batas waktu. Mengulang election."
                )

        finally:
            self.election_lock.release()

    def declare_leader(self):
        """Node ini menyatakan dirinya leader dan memberi tahu semua peer."""

        with self.lock:
            self.leader_id = self.node_id

        print(
            f"[Node {self.node_id}] Menjadi LEADER"
        )

        # Broadcast COORDINATOR ke semua peer, baik ID lebih rendah
        # maupun ID lebih tinggi
        for peer_id, peer_port in self.peers.items():
            success = self.send_message(peer_port, "COORDINATOR")

            if success:
                print(
                    f"[Node {self.node_id}] Mengirim COORDINATOR "
                    f"ke node {peer_id}"
                )
            else:
                print(
                    f"[Node {self.node_id}] Gagal mengirim "
                    f"COORDINATOR ke node {peer_id}"
                )

    def monitor_leader(self):
        """Memeriksa apakah leader masih hidup secara berkala."""

        while True:
            time.sleep(3)

            with self.lock:
                current_leader = self.leader_id

            # Belum ada leader (mis. election sebelumnya tidak menghasilkan
            # leader). Jika tidak ada election yang sedang berjalan, mulai
            # election agar node tidak macet tanpa leader.
            if current_leader is None:
                if not self.election_lock.locked():
                    threading.Thread(
                        target=self.start_election,
                        daemon=True
                    ).start()
                continue

            # Tidak perlu memeriksa koneksi ke diri sendiri
            if current_leader == self.node_id:
                continue

            leader_port = self.peers.get(current_leader)

            if leader_port is None:
                continue

            # Coba menghubungi port leader untuk memastikan node hidup
            try:
                with socket.create_connection(
                    ("localhost", leader_port),
                    timeout=1.0
                ):
                    pass

            except (ConnectionRefusedError, socket.timeout, OSError):
                print(
                    f"[Node {self.node_id}] Leader {current_leader} "
                    "tidak merespons. Memulai election ulang."
                )

                # Reset leader hanya jika belum berubah
                with self.lock:
                    if self.leader_id == current_leader:
                        self.leader_id = None
                        should_elect = True
                    else:
                        should_elect = False

                if should_elect:
                    threading.Thread(
                        target=self.start_election,
                        daemon=True
                    ).start()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--id", type=int, required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument(
        "--peers",
        type=str,
        required=True,
        help="Daftar port peer dipisah koma, mis. 5002,5003,5004,5005"
    )

    args = parser.parse_args()

    # Konvensi: ID N menggunakan port 5000 + N
    peer_ports = [int(p) for p in args.peers.split(",")]
    peers = {port - 5000: port for port in peer_ports}

    node = Node(args.id, args.port, peers)

    threading.Thread(
        target=node.start_server,
        daemon=True
    ).start()

    threading.Thread(
        target=node.monitor_leader,
        daemon=True
    ).start()

    # Beri waktu server node lain untuk aktif
    time.sleep(1)

    # Election awal
    node.start_election()

    while True:
        time.sleep(60)


if __name__ == "__main__":
        main()