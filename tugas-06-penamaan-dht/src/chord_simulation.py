"""Tugas 6 - Simulasi Chord DHT (single-process). ID Kurir -> IP Kurir."""

import hashlib

M_BITS = 8
RING_SIZE = 2 ** M_BITS


def hash_id(key: str) -> int:
    """Hash ID node atau ID kurir ke ruang identifier 0-255."""
    return int.from_bytes(hashlib.sha1(key.encode()).digest(), "big") % RING_SIZE


def successor_in(node_ids, key_hash: int) -> int:
    """Node dengan ID terkecil >= key_hash; jika tidak ada, wrap ke terkecil."""
    ids = sorted(node_ids)
    return next((n for n in ids if n >= key_hash), ids[0])


class ChordRing:
    def __init__(self):
        self.nodes: dict[int, str] = {}              # node_id -> IP node
        self.names: dict[int, str] = {}              # node_id -> nama node
        self.store: dict[int, dict[str, str]] = {}   # node_id -> {kurir_id: IP}

    def find_successor(self, key_hash: int) -> int:
        if not self.nodes:
            raise ValueError("Ring belum memiliki node.")
        return successor_in(self.nodes, key_hash)

    def join(self, node_name: str, node_ip: str):
        node_id = hash_id(node_name)
        if node_id in self.nodes:
            print(f"[INFO] Node '{node_name}' (id={node_id}) sudah ada di ring.")
            return

        succ = successor_in(self.nodes, node_id) if self.nodes else None
        self.nodes[node_id], self.names[node_id], self.store[node_id] = node_ip, node_name, {}
        print(f"[JOIN] Node '{node_name}' (id={node_id}) bergabung, IP={node_ip}")

        if succ is None:
            print("  [INFO] Node pertama dalam ring.")
            return

        # Hanya successor lama yang bisa kehilangan key ke node baru.
        moved = False
        for kurir, ip in list(self.store[succ].items()):
            if self.find_successor(hash_id(kurir)) == node_id:
                self.store[node_id][kurir] = self.store[succ].pop(kurir)
                moved = True
                print(f"  [MIGRASI] {kurir}: node {succ} -> node {node_id}, IP kurir tetap {ip}")
        if not moved:
            print("  [INFO] Tidak ada mapping yang berpindah tanggung jawab.")

    def leave(self, node_name: str):
        node_id = hash_id(node_name)
        if node_id not in self.nodes:
            print(f"[INFO] Node '{node_name}' tidak ditemukan.")
            return

        data = self.store.pop(node_id)
        del self.nodes[node_id], self.names[node_id]
        print(f"[LEAVE] Node '{node_name}' (id={node_id}) keluar dari ring.")

        if not self.nodes:
            print("  [PERINGATAN] Ring kosong; mapping hilang.")
            return
        if not data:
            print("  [INFO] Node ini tidak memegang mapping kurir.")
            return

        for kurir, ip in data.items():
            owner = self.find_successor(hash_id(kurir))
            self.store[owner][kurir] = ip
            print(f"  [MIGRASI] {kurir}: node {node_id} -> node {owner} "
                  f"({self.nodes[owner]}), IP kurir tetap {ip}")

    def register_kurir(self, kurir_id: str, ip_kurir: str):
        """Daftarkan kurir, atau perbarui IP-nya jika sudah ada."""
        h = hash_id(kurir_id)
        owner = self.find_successor(h)
        aksi = "UPDATE" if kurir_id in self.store[owner] else "REGISTER"
        self.store[owner][kurir_id] = ip_kurir
        print(f"[{aksi}] {kurir_id} (hash={h}) -> node {owner} -> IP {ip_kurir}")

    def lookup(self, kurir_id: str) -> str | None:
        if not self.nodes:
            return None
        h = hash_id(kurir_id)
        owner = self.find_successor(h)
        print(f"[LOOKUP] {kurir_id} (hash={h}) bertanggung jawab pada node {owner}")
        return self.store[owner].get(kurir_id)

    def print_ring(self):
        print("[RING] Urutan node (searah jarum jam):")
        for nid in sorted(self.nodes):
            isi = ", ".join(f"{k}(hash={hash_id(k)})" for k in sorted(self.store[nid])) or "-"
            print(f"  id={nid:3d} {self.names[nid]:<16} {self.nodes[nid]:<9} menyimpan: {isi}")


def main():
    ring = ChordRing()

    for nama, ip in [("node-jakarta-1", "10.0.0.1"), ("node-jakarta-2", "10.0.0.2"),
                     ("node-bandung-1", "10.0.0.3"), ("node-surabaya-1", "10.0.0.4")]:
        ring.join(nama, ip)

    for kid, ip in [("kurir-001", "192.168.1.10"), ("kurir-002", "192.168.1.11"),
                    ("kurir-003", "192.168.1.12")]:
        ring.register_kurir(kid, ip)
    print()
    ring.print_ring()

    print("\n--- Lookup sebelum perubahan topologi ---")
    print("kurir-001 ->", ring.lookup("kurir-001"))
    print("kurir-002 ->", ring.lookup("kurir-002"))

    print("\n--- IP kurir berubah ---")
    ring.register_kurir("kurir-001", "192.168.7.99")
    print("kurir-001 ->", ring.lookup("kurir-001"))

    print("\n--- Node baru bergabung ---")
    ring.join("node-medan-1", "10.0.0.5")

    print("\n--- Node keluar dari ring ---")
    ring.leave("node-bandung-1")
    print()
    ring.print_ring()

    print("\n--- Lookup setelah perubahan topologi ---")
    for kid in ("kurir-001", "kurir-002", "kurir-003"):
        print(f"{kid} ->", ring.lookup(kid))


if __name__ == "__main__":
    main()