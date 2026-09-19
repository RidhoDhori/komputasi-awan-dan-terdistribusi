# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [nama kelompok]

| Nama | NIM | Kontribusi |
|---|---|---|
| [RIDHO BINTANG ADWITYA] | [103072400015] | [bandwidth is infinite] |
| [RANGGA DANI PRASETYA] | [103072400057] | [the network is reliable] |
| [RESTU FADILAH AL FATAH] | [103072400081] | [latency is zero] |
| [ALBERTRIO SURANTA GINTING] | [103072400081] | [single point of failure] |

## Pitfall 1: [nama pitfall] — ditulis oleh [nama]

**Bukti di skenario:** [kutip/paraphrase bagian skenario]

**Kenapa ini keliru:** [penjelasan]

**Dampak ke FoodGo:** [mekanisme kegagalan konkret]

**Solusi desain awal:** [usulan solusi]

**Trade-off:** [apa yang dikorbankan/risiko dari solusi ini]

---

## Pitfall 2: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Pitfall 3: (latency is zero) — ditulis oleh Restu Fadilah Al Fatah
**Bukti di skenario:** kode FoodGo melakukan komunikasi antar-service tanpa menerapkan mekanisme timeout. Modul pesanan memanggil modul pembayaran dan terus menunggu tanpa batas waktu yang ditentukan. Akibatnya, aplikasi mengalami perlambatan yang signifikan dan beberapa permintaan akhirnya mengalami timeout

**Kenapa ini keliru:** Asumsi latency is zero menganggap komunikasi antar-komponen berlangsung tanpa jeda. Padahal, dalam sistem terdistribusi, setiap komunikasi antar-service membutuhkan waktu untuk mengirim, memproses, dan menerima respons. Pada FoodGo, keterlambatan modul pembayaran dapat membuat modul pesanan ikut menunggu. Kondisi ini semakin terasa ketika jumlah pesanan meningkat sehingga banyak permintaan menunggu respons pembayaran.

**Dampak ke FoodGo:** Dampaknya, permintaan pada modul pesanan dapat menumpuk karena menunggu respons pembayaran. Tanpa timeout, proses dapat berlangsung terlalu lama dan menghabiskan resource seperti thread dan koneksi. Saat trafik meningkat, kondisi ini membuat aplikasi semakin lambat, beberapa request mengalami timeout, bahkan dapat menyebabkan server overload hingga crash.

**Solusi desain awal:** Solusi yang dapat diterapkan adalah menggunakan *timeout* agar waktu tunggu respons memiliki batas. Jika terjadi kegagalan sementara, sistem dapat melakukan *retry* dengan jeda yang semakin panjang. Selain itu, *circuit breaker* dapat digunakan untuk menghentikan sementara pemanggilan ketika modul pembayaran terus mengalami masalah. Untuk proses yang tidak membutuhkan respons langsung, komunikasi dapat dilakukan secara *asynchronous* agar modul pesanan tidak perlu menunggu.


**Trade-off:** Penggunaan retry memiliki risiko karena dapat membantu saat gangguan bersifat sementara, tetapi jika modul pembayaran sedang overload, percobaan ulang justru menambah beban sistem. Karena itu, retry perlu dibatasi dan menggunakan backoff agar request tidak terus bertambah saat terjadi gangguan.

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