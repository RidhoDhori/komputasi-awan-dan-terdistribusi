# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- [RPC] Alasan: Dalam studi kasus aplikasi FoodGo, arsitektur sistem membutuhkan dua jenis pola komunikasi: sinkron (untuk cek saldo) dan asinkron (untuk notifikasi kurir). Operasi seperti "cek status saldo" bersifat blocking dan time-sensitive. Modul Pembayaran tidak dapat melanjutkan proses transaksi jika belum mendapatkan kepastian jumlah saldo pengguna. RPC dirancang khusus untuk pola komunikasi request-response yang instan, di mana klien memanggil fungsi di server jarak jauh dan menunggu hasilnya saat itu juga seolah-olah memanggil fungsi lokal.

- Error saat setup (mis. koneksi RabbitMQ ditolak, port bentrok): -

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
- Hasil yang diamati: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 9 Oktober 2026 | Gemini | Dari dua metode RPC dan MQ mana yang cocok dengan studi kasus Modul Pembayaran dan modul Pesanan FoodGo| AI menyarankan pendekatan Arsitektur Hibrida. Menggunakan RPC (gRPC) untuk operasi sinkron (cek saldo) karena butuh respons instan, latensi rendah, dan tipe data ketat | - |
