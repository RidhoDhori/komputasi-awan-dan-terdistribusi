# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat: 64
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): Hal ini terjadi karena adanya *race condition*, di mana beberapa *thread* membaca variabel `processed_count` secara bersamaan. Saat program dijeda sementara oleh fungsi `time.sleep`, *thread-thread* tersebut akhirnya mengolah nilai lama yang sama. Akibatnya, saat hasil penjumlahannya disimpan ulang, mereka saling menimpa perhitungan satu sama lain sehingga banyak pesanan yang tidak terhitung.

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: 100

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
