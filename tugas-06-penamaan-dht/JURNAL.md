# Jurnal Proses — Tugas 6

## Implementasi find_successor

- Kesalahan pertama yang ditemui: urutan node di `self.nodes` mengikuti urutan `join`, bukan urutan ID. Pada simulasi, node masuk dengan ID 177, 102, 40, 136. Jika daftar ini dipakai langsung, pencarian "node pertama dengan ID ≥ hash" bisa salah. Contohnya `kurir-001` (hash 50) akan berhenti di node 177, padahal seharusnya node 102. Kasus lain yang rawan adalah wrap-around: hash yang lebih besar dari semua ID node (misalnya 200) tidak punya node dengan ID ≥ hash, sehingga pencarian harus kembali ke node terkecil. **[KONFIRMASI: ganti dengan kesalahan yang benar-benar dialami kelompok jika berbeda]**
- Cara memperbaikinya: ID node diurutkan dulu dengan `sorted(node_ids)` di `successor_in`, lalu dicari node pertama dengan ID ≥ `key_hash` menggunakan `next(...)`. Nilai default `ids[0]` menangani wrap-around, karena key yang melewati node terbesar kembali ke node terkecil (contoh: hash 200 → node 40). Fungsi ini dipakai bersama oleh `find_successor`, `join`, dan `leave`, sehingga aturan successor hanya ada di satu tempat.

## Skenario join/leave

- Hasil sebelum & sesudah node baru bergabung: sebelum `node-medan-1` bergabung, ring berisi node 40, 102, 136, 177. Setelah bergabung dengan ID 123, node ini berada di antara node 102 dan 136, dan successor-nya adalah node 136. Program mengecek mapping milik node 136, yaitu `kurir-003` (hash 132). Karena 132 > 123, successor `kurir-003` tetap node 136, sehingga tidak ada mapping yang berpindah (`[INFO] Tidak ada mapping yang berpindah tanggung jawab`). Node 123 tetap kosong, tetapi rentang node 136 menyempit menjadi 124–136.
- Hasil sebelum & sesudah node keluar: sebelum `node-bandung-1` (ID 40) keluar, node ini menyimpan `kurir-002` (hash 28). Setelah node 40 keluar, `find_successor(28)` menghasilkan node 102, sehingga program memigrasikan `kurir-002` ke node 102 (`[MIGRASI] kurir-002: node 40 -> node 102`). Node 102 kini menyimpan `kurir-001` dan `kurir-002`, dan rentangnya melebar menjadi 178–255 dan 0–102. Lookup setelah perubahan tetap berhasil untuk ketiga kurir (`kurir-001` → 192.168.7.99, `kurir-002` → 192.168.1.11, `kurir-003` → 192.168.1.12), jadi tidak ada mapping yang hilang dan IP terbaru `kurir-001` tetap terjaga.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | NO AI | ... | ... | ... |
