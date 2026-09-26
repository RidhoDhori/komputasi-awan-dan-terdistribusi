# Jurnal Proses — Tugas 2

## [16 September 2026]
- Opsi arsitektur yang dipertimbangkan: Kombinasi dari SOA dan Pub-Sub
- Kenapa akhirnya pilih [SOA/Pub-Sub]: Dalam Kombinasi ini dirancang untuk menjaga keseimbangan antara konsistensi data dan otonomi sistem. SOA menangani alur transaksi utama secara sinkron untuk menjamin kepastian data seketika. Adapun proses lanjutan, seperti pendelegasian tugas ke kurir dan pemberitahuan ke restoran, diproses secara asinkron melalui pola Publish-Subscribe.
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): -

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 26 September 2026 | Gemini | "Saya memiliki Perancangan Arsitektur untuk sistem FoodGo. Tolong ubah bahasanya menjadi gaya penulisan akademis yang sopan, baku,  namun tetap mempertahankan makna teknis aslinya." | AI menyarankan penggunaan istilah yang lebih presisi dan formal AI juga menyusun struktur poin agar lebih sistematis. | Kami membaca hasil suntingan AI, memastikan bahwa alur teknis (HTTP POST/GET, publish/subscribe) tetap akurat sesuai pemahaman kami. |