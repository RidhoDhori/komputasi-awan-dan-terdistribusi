# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [7 - mafia dodol gresik]

| Nama | NIM | Kontribusi |
|---|---|---|
| [RIDHO BINTANG ADWITYA] | [103072400015] | [bandwidth is infinite] |
| [RANGGA DANI PRASETYA] | [103072400057] | [the network is reliable] |
| [RESTU FADILAH AL FATAH] | [103072400081] | [latency is zero] |
| [ALBERTRIO SURANTA GINTING] | [103072400128] | [single point of failure] |

## Pitfall 1: (Bandwidth is Infinite) — ditulis oleh Ridho Bintang Adwitya

**Bukti di skenario:** Aplikasi jadi sangat lambat, beberapa permintaan timeout... Saat trafik naik, satu server... kewalahan.

**Kenapa ini keliru:** Kapasitas jaringan dan I/O server memiliki batas fisik. Menganggap bandwidth tak terbatas saat mengirim data besar (gambar makanan, detail pesanan, notifikasi) akan menciptakan kemacetan data.

**Dampak ke FoodGo:** Saat jam makan siang, antrean request menumpuk bukan karena logika error, tapi karena "jalan raya" data (bandwidth/network I/O) penuh. Server menghabiskan waktu hanya untuk mengirim/menerima data, bukan memprosesnya.

**Solusi desain awal:** Kompresi data (seperti Gzip), pagination pada daftar menu, dan memisahkan aset statis (gambar) ke CDN (Content Delivery Network).

**Trade-off:** Kompresi data menghemat bandwidth, tetapi membebani CPU server untuk melakukan kompresi/dekompresi. Ini adalah pertukaran antara penggunaan CPU dan penggunaan jaringan.

---

## Pitfall 2: (the network is reliable) — ditulis oleh RANGGA DANI PRASETYA

**Bukti di skenario:** Menemukan komentar kode network is always reliable, no need for retry. Pemanggilan dari modul pesanan ke modul pembayaran juga tidak memakai timeout sama sekali, sehingga modul pesanan menunggu tanpa batas waktu.

**Kenapa ini keliru:** Jaringan bisa mengalami packet loss, latensi yang tidak stabil, koneksi terputus, atau service tujuan yang lambat bahkan mati. Saat pemanggilan antarservice, kegagalan bisa terjadi secara parsial, yaitu ketika sebagian komponen masih berjalan, sedangkan komponen lainnya mengalami kegagalan. Pemanggil juga sulit membedakan apakah service sedang lambat atau sudah mati.

**Dampak ke FoodGo:** Saat trafik meningkat, pembayaran melambat dan tanpa timeout membuat thread serta koneksi tertahan hingga sumber daya habis, sehingga request lain ikut mengantre, beban semakin tinggi akibat pengguna menekan tombol berulang kali, dan server bisa crash hingga menjatuhkan seluruh modul.

**Solusi desain awal:** Menerapkan timeout pada setiap pemanggilan antarservice, retry terbatas dengan exponential backoff dan jitter serta idempotency key pada pembayaran, circuit breaker dan bulkhead untuk membatasi dampak kegagalan, serta message queue untuk pekerjaan asinkron seperti notifikasi kurir.

**Trade-off:** Jika timeout terlalu singkat, request bisa dianggap gagal padahal masih bisa berhasil, sedangkan timeout terlalu lama membuat sumber daya terus terpakai. Retry juga bisa menambah beban server, circuit breaker dan bulkhead bisa menolak request yang sebenarnya masih bisa diproses, sedangkan message queue membuat data tidak selalu langsung diperbarui dan sistem menjadi lebih rumit untuk dikelola.

---

## Pitfall 3: (latency is zero) — ditulis oleh Restu Fadilah Al Fatah
**Bukti di skenario:** Modul pesanan FoodGo harus berkomunikasi dengan modul pembayaran sebelum pesanan dapat diproses lebih lanjut. Komunikasi tersebut membutuhkan waktu sehingga tidak terjadi secara instan

**Kenapa ini keliru:** Asumsi latency is zero menganggap komunikasi antar-service tidak membutuhkan waktu. Padahal, request harus dikirim melalui jaringan, diproses oleh service tujuan, lalu respons dikirim kembali.

**Dampak ke FoodGo:** Ketika jumlah pesanan meningkat, waktu komunikasi dapat bertambah sehingga modul pesanan harus menunggu lebih lama. Akibatnya, request menumpuk dan aplikasi menjadi lambat.

**Solusi desain awal:** Mengurangi komunikasi yang tidak diperlukan, menggunakan caching, dan menerapkan komunikasi asynchronous untuk proses yang tidak membutuhkan respons langsung.


**Trade-off:** Caching dapat menyebabkan data tidak selalu terbaru, sedangkan komunikasi asynchronous membuat hasil proses tidak langsung tersedia dan sistem menjadi lebih kompleks.

---

## Pitfall 4 (Masalah Desain): Single Point of Failure — ditulis oleh Albertrio Ginting

**Bukti di skenario:** Satu server menangani semua modul (pesanan, pembayaran, notifikasi kurir) dalam satu proses monolitik yang sama.

**Kenapa ini keliru:** Sistem terdistribusi didesain agar tahan terhadap partial failure, di mana satu bagian boleh mati tanpa membuat layanan lain ikut mati. Tetapi di arsitektur monolitik, semua modul memperebutkan resource komputasi (CPU, RAM, Disk I/O) yang sama. Akibatnya, jika ada satu modul yang bermasalah atau mengalami kebocoran memori (memory leak), seluruh aplikasi di dalam server akan ikut crash. Hal inilah yang menciptakan Single Point of Failure (titik kegagalan tunggal).

**Dampak ke FoodGo:** Saat ada lonjakan pesanan, ketiga modul (pesanan, pembayaran, dan notifikasi) saling berebut sumber daya di server yang sama. Akibatnya, server jadi kewalahan sampai akhirnya mati total. Karena bertumpu pada satu server ini saja, operasional FoodGo langsung mati total sehingga Pelanggan tidak bisa order atau melakukan pembayaran, dan kurir tidak mendapatkan notifikasi.

**Solusi desain awal:** Migrasikan arsitektur dari Monolitik menuju Microservices. Pecah aplikasi menjadi layanan-layanan yang berdiri sendiri (layanan pesanan, layanan pembayaran, dan layanan notifikasi). Dengan begini, jika trafik pesanan melonjak, hanya perlu melakukan scale-out (menambah jumlah server atau container) khusus untuk layanan pesanan saja, tanpa harus menanggung beban tambahan di modul lain.

**Trade-off:** Beralih ke microservices meningkatkan kompleksitas infrastruktur dan operasional secara drastis. Tim harus mengelola banyak deployment secara terpisah, mengamankan komunikasi jaringan antar-servis, serta membutuhkan alat pemantauan yang lebih canggih (distributed tracing) karena log eror tidak lagi berada di satu tempat yang sama.

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]