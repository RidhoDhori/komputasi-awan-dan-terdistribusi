# Tugas 7 (Pekan 7) — Konsistensi Data

**Materi terkait:** Data-Centric Consistency (Sequential, Eventual), Client-Centric Consistency.

## Studi Kasus

Data saldo *e-wallet* pelanggan FoodGo berbeda antara server wilayah **Jakarta** dan **Bandung** karena replikasi antar server berjalan lambat. Contoh kasus nyata: pelanggan top-up saldo lewat server Jakarta, lalu dalam hitungan detik memesan makanan lewat aplikasi yang tersambung ke server Bandung — saldo belum ter-update, transaksi ditolak padahal saldo sebenarnya cukup.

## Tugas Kelompok

### Bagian 1 — Analisis (wajib)

1. Tentukan: apakah kasus ini **membutuhkan Sequential Consistency** (semua replika melihat urutan operasi yang sama) atau **cukup Eventual Consistency** (replika akan konsisten "pada akhirnya", boleh sementara berbeda)? Berikan argumen berbasis dampak bisnis (mis. kasus saldo *e-wallet* jauh lebih sensitif dibanding kasus "jumlah like" di media sosial).
2. Jika kalian menyimpulkan Eventual Consistency saja **tidak cukup** untuk skenario ini, usulkan pendekatan **Client-Centric Consistency** yang relevan (mis. *Read-Your-Writes*: pelanggan yang baru top-up harus selalu melihat saldo terbarunya sendiri, walau replika lain belum sinkron).
3. Gambarkan **diagram alir urutan (sequence diagram)** yang menunjukkan operasi read/write antara pelanggan, server Jakarta, server Bandung, dan proses replikasi — untuk skenario **tanpa** jaminan konsistensi (bug terjadi) DAN skenario **dengan** solusi yang kalian usulkan (bug teratasi). Pakai Mermaid (`sequenceDiagram`) di `README.md` — lihat contoh cara pakai di Tugas 2.

### Bagian 2 — Simulasi (opsional, nilai tambah)

Skeleton `src/replica_simulation.py` mensimulasikan dua replika (Jakarta & Bandung) dengan delay replikasi buatan. Lengkapi TODO untuk:
1. Menunjukkan kondisi **inconsistent read** (replika Bandung masih menunjukkan saldo lama walau Jakarta sudah update).
2. Mengimplementasikan mekanisme **Read-Your-Writes** sederhana (mis. dengan version/timestamp per client) yang memperbaiki masalah tersebut.

```bash
python3 src/replica_simulation.py
```

## Struktur Submission

```
tugas-07-konsistensi-data/
├── README.md      # Analisis konsistensi + sequence diagram Mermaid
├── JURNAL.md
├── src/            # (opsional) simulasi replikasi
└── bukti/          # (jika mengerjakan simulasi) output program
```

## Rubrik Penilaian (Tugas 7)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Ketepatan pemilihan model konsistensi | 30% | Argumen berbasis dampak bisnis nyata, bukan hafalan definisi |
| Kualitas sequence diagram | 30% | Menunjukkan jelas titik kegagalan & titik perbaikan |
| Usulan solusi client-centric | 25% | Solusi konkret dan dapat diimplementasikan (bukan wacana abstrak) |
| Proses & kontribusi kelompok | 15% | `JURNAL.md`, commit history (+ bonus jika simulasi dikerjakan) |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya konsep umum consistency model ke AI untuk brainstorming; **tidak boleh** meminta AI menuliskan analisis akhir/sequence diagram atau isi `# TODO` di `src/replica_simulation.py` yang tinggal ditempel. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Sebagai bukti pemahaman konsep (bukan hafalan jawaban skenario FoodGo saja), `README.md` wajib menyertakan **satu skenario tambahan** yang kalian buat sendiri (mis. kasus lain di aplikasi ojek online) dan menentukan model konsistensi yang tepat untuk skenario tambahan tersebut.

## Analisis
#### 1. Model Konsistensi
FoodGo sebaiknya memakai **Eventual Consistency yang dilengkapi Client-Centric Consistency (Read-Your-Writes)**.

**Dampak bisnis.** Saldo e-wallet adalah data uang milik pelanggan. Jika saldo yang terbaca basi, pelanggan yang sebenarnya punya saldo cukup ditolak pesanannya tepat setelah top-up. Akibatnya pesanan batal, pelanggan komplain ke layanan pelanggan, dan kepercayaan terhadap dompet digital menurun. Bandingkan dengan "jumlah like" di media sosial: angka yang salah beberapa detik tidak merugikan siapa pun dan tidak membatalkan transaksi, sehingga Eventual Consistency murni sudah cukup di sana. Karena dampak salah-baca pada saldo jauh lebih mahal, Eventual saja tidak cukup untuk kasus ini.

**Kenapa tidak Sequential penuh.** Sequential Consistency membuat semua replika melihat urutan operasi yang sama, tetapi setiap operasi harus menunggu koordinasi antar-kota. Itu menambah latensi di setiap transaksi dan menurunkan ketersediaan: jika jaringan Jakarta–Bandung terganggu, replika tidak boleh menjawab sampai sinkron kembali, padahal mayoritas pembacaan saldo tidak bermasalah. Biaya itu terlalu besar untuk masalah yang sebenarnya sempit, yaitu pelanggan harus melihat hasil tulisannya sendiri.

**Kesimpulan.** Replika dibiarkan sinkron secara longgar (Eventual), tetapi pelanggan dijamin membaca saldo yang setidaknya sama barunya dengan operasi terakhirnya sendiri (Read-Your-Writes). Latensi tambahan hanya terjadi pada pelanggan yang replikanya tertinggal.

#### 2. Solusi Client-Centric Consistency menggunakan Read-Your-Writes

Read-Your-Writes merupakan mekanisme konsistensi yang memastikan pengguna dapat membaca kembali perubahan data yang sebelumnya telah dilakukan oleh pengguna tersebut.

Pada sistem FoodGo, mekanisme ini diterapkan dengan menggunakan version number pada setiap perubahan saldo.

Alur penerapannya adalah:
1. Pelanggan melakukan top-up melalui server Jakarta.
2. Server Jakarta memperbarui saldo dan menaikkan nomor versi data.
3. Server Jakarta mengirimkan informasi replikasi ke Bandung dengan jeda waktu tertentu.
4. Ketika pelanggan membaca saldo melalui Bandung, sistem memeriksa versi data yang tersedia.
5. Jika versi Bandung lebih lama daripada versi yang dibutuhkan pelanggan, sistem mengarahkan permintaan pembacaan ke Jakarta yang sudah memiliki data terbaru.
6. Jika versi Bandung sudah sesuai, pelanggan dapat membaca saldo langsung dari Bandung.
Dengan mekanisme tersebut, pelanggan tetap dapat melihat saldo terbaru tanpa harus menunggu seluruh replika selesai melakukan sinkronisasi.

**Alternatif: polling.** Bandung (atau aplikasi) menunggu sampai versi lokal Bandung mencapai versi yang dibutuhkan, lalu membaca. Ini tidak menambah beban ke Jakarta, tetapi latensinya tidak pasti dan perlu batas waktu (timeout). Jika timeout terlewati, sistem jatuh kembali ke redirect ke Jakarta.

**Batasan.** Read-Your-Writes hanya menjamin pelanggan melihat tulisannya sendiri, bukan mencegah konflik penulisan. Jika pesanan memotong saldo dari dua perangkat hampir bersamaan, kedua replika bisa sama-sama menerima dan saldo menjadi negatif (double-spend). Karena itu **pemotongan saldo ditulis ke satu server otoritatif (Jakarta) dengan compare-and-set**: tulisan hanya berhasil jika versi yang dibaca masih sama dengan versi terbaru. Jika gagal, aplikasi membaca ulang saldo dan mencoba lagi. Dengan begitu pembacaan boleh dilayani replika mana pun, tetapi penulisan saldo tetap terurut.

#### 3. Diagram alir urutan (sequence diagram)

### 3.1 Skenario TANPA jaminan konsistensi (bug terjadi)

```mermaid
sequenceDiagram
    autonumber
    actor P as Pelanggan
    participant J as Server Jakarta
    participant R as Proses Replikasi
    participant B as Server Bandung

    Note over J,B: Kondisi awal: saldo = 20.000 (versi 1) di kedua replika

    P->>J: WRITE: top-up Rp100.000
    J->>J: saldo = 120.000 (versi 2)
    J-->>P: OK, saldo 120.000
    J-)R: kirim update ke Bandung (asinkron, delay beberapa detik)

    Note over P,B: Beberapa detik kemudian, aplikasi pelanggan tersambung ke Bandung

    P->>B: pesan makanan Rp80.000
    B->>B: baca saldo lokal = 20.000 (versi 1, STALE)
    Note right of B: TITIK KEGAGALAN: Bandung belum menerima update top-up
    B-->>P: DITOLAK, saldo tidak cukup

    R-)B: update tiba: saldo 120.000 (versi 2)
    Note over J,B: Replika akhirnya konsisten, tetapi pesanan sudah gagal
```

### 3.2 Skenario DENGAN Read-Your-Writes (bug teratasi)

```mermaid
sequenceDiagram
    autonumber
    actor P as Pelanggan (App)
    participant J as Server Jakarta
    participant R as Proses Replikasi
    participant B as Server Bandung

    Note over J,B: Kondisi awal: saldo = 20.000 (versi 1) di kedua replika

    P->>J: WRITE: top-up Rp100.000
    J->>J: saldo = 120.000 (versi 2)
    J-->>P: OK, saldo 120.000 + token versi = 2
    Note left of P: TITIK PERBAIKAN 1: aplikasi menyimpan versi terakhir = 2
    J-)R: kirim update ke Bandung (asinkron, delay)

    P->>B: pesan makanan Rp80.000 + versi dibutuhkan = 2
    B->>B: periksa versi data Bandung
    Note right of B: TITIK PERBAIKAN 2: Bandung membandingkan versinya dengan versi yang dibutuhkan pelanggan

    alt Versi Bandung (1) lebih lama dari versi dibutuhkan (2)
        B->>J: arahkan pembacaan saldo ke Jakarta
        J-->>B: saldo 120.000 (versi 2)
    else Versi Bandung sudah sesuai
        B->>B: baca saldo langsung dari Bandung
    end

    B->>B: saldo 120.000 ≥ 80.000, pesanan diterima
    B-->>P: Pesanan BERHASIL
    R-)B: update replikasi tiba, Bandung ikut tersinkronisasi
```

### 3.3 Penjelasan

| Aspek | Tanpa Jaminan Konsistensi | Dengan Read-Your-Writes |
|---|---|---|
| **Titik kegagalan** | Langkah 6 Bandung membaca saldo basi lalu menolak pesanan | Tidak ada, karena Bandung memeriksa versi sebelum menjawab |
| **Titik perbaikan** | - | Langkah 3 (aplikasi menyimpan token versi) dan langkah 6 (Bandung memeriksa versi) |
| **Saat Bandung tertinggal** | Menjawab dengan data lama | Pembacaan diarahkan ke Jakarta yang sudah memiliki data terbaru |
| **Saat Bandung sudah sesuai** | Menjawab dari data lokal | Menjawab dari data lokal, tanpa tambahan latensi |
| **Trade-off** | Cepat tetapi salah | Latensi tambahan hanya pada permintaan pelanggan yang replikanya tertinggal |

#### 4. Skenario Tambahan: Aplikasi Ojek Online

Dalam satu aplikasi ojek online terdapat dua data dengan kebutuhan konsistensi yang berbeda:

| Data | Kebutuhan | Model yang dipilih | Alasan |
|---|---|---|---|
| Posisi driver di peta | Boleh terlambat 1–3 detik | **Eventual Consistency** | Posisi terus berubah dan akan segera tertimpa data baru. Titik driver yang meleset sedikit di peta tidak merugikan siapa pun, dan sinkronisasi ketat justru memperlambat pembaruan posisi ribuan driver. |
| Status "order diambil driver" | Tidak boleh ada dua driver mengambil order yang sama | **Konsistensi kuat (satu pemilik data, penulisan terurut)** | Jika dua replika sama-sama melihat order masih "menunggu", dua driver bisa sama-sama berhasil mengambilnya. Akibatnya satu pelanggan dijemput dua driver, satu driver rugi waktu, dan satu order bermasalah. |

Selain itu, **Read-Your-Writes** dipakai agar driver yang baru menekan "ambil order" langsung melihat statusnya sendiri sebagai "order diambil", walau replika di dekatnya belum sinkron.

```mermaid
sequenceDiagram
    autonumber
    actor A as Driver A
    actor B as Driver B
    participant J as Server Pemilik Order (Jakarta)
    participant S as Server Replika (Bandung)

    Note over J,S: Order #7 berstatus MENUNGGU di kedua server

    A->>J: ambil order #7
    B->>S: ambil order #7
    S->>J: teruskan klaim order #7 ke server pemilik (bukan memutuskan sendiri)

    J->>J: klaim A masuk lebih dulu, status = DIAMBIL oleh A (versi 2)
    J-->>A: BERHASIL + token versi = 2
    J->>J: klaim B tiba, order sudah DIAMBIL (cek versi gagal)
    J-->>S: DITOLAK, order sudah diambil
    S-->>B: Order sudah diambil driver lain

    J-)S: replikasi status DIAMBIL (versi 2)
```

Dari kedua data ini terlihat bahwa satu aplikasi bisa memakai beberapa model konsistensi sekaligus, tergantung dampak bisnis tiap data. Konsistensi kuat dipakai hanya pada data yang berisiko merugikan jika salah, supaya sistem tetap cepat untuk data lain.
