# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## [Tanggal diskusi 1]
- 19 September 2026
- Peserta: [RIDHO BINTANG ADWITYA, RANGGA DANI PRASETYA, RESTU FADILAH AL FATAH, ALBERTRIO SURANTA GINTING]
- Poin diskusi: Mengidentifikasi masalah utama pada FoodGo dan menentukan pitfall yang sesuai.
- Perbedaan pendapat (jika ada): tidak ada

## Review Silang
- [Nama] mengomentari analisis [Nama lain]: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
| 19 Sept 2026 | Gemini | Meminta contoh cara menghubungkan masalah desain SPOF dengan gejala yang terjadi pada FoodGo. | AI memberikan ide untuk memfokuskan analisis pada perebutan sumber daya (*resource contention*). AI mencontohkan bagaimana lonjakan trafik pada modul pesanan bisa ikut mematikan modul notifikasi dan pembayaran karena ketiganya berbagi *resource* CPU dan RAM yang sama di satu *server*, sehingga memicu *crash* total. | Menggunakan konsep "perebutan sumber daya" tersebut untuk menyusun penjelasan pada bagian dampak konkret, lalu merangkai kalimat analisis dan menjelaskan mengapa *crash* tersebut melumpuhkan seluruh operasi dengan bahasa sendiri.|
| 19 Sept 2026 | Claude | Meminta brainstorming pitfall yang bisa menjadi penyebab aplikasi lambat, timeout, dan server crash pada FoodGo. | AI memberikan beberapa ide pitfall dari Fallacies of Distributed Computing yang relevan dengan skenario FoodGo. | Kelompok menggunakan ide tersebut sebagai bahan awal, kemudian memilih pitfall yang paling sesuai dengan skenario, yaitu The network is reliable. |
