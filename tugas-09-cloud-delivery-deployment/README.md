# Tugas 9 (Pekan 9) — Cloud Delivery & Deployment Model

**Materi terkait:** Karakteristik esensial cloud computing (NIST SP 800-145), Deployment Model (Public/Private/Hybrid/Community), Service Model (IaaS/PaaS/SaaS).

> Bagian 2 mata kuliah ini murni **analisis & desain di atas kertas** — tidak ada biaya cloud sama sekali, karena tugas berhenti di tahap rekomendasi, bukan implementasi nyata (implementasi baru mulai Tugas 11).

## Studi Kasus

Pemerintah ingin membangun **Sistem Data Kependudukan** (nama, NIK, alamat, data biometrik) yang:
- Sangat **rahasia** (data pribadi warga negara, diatur UU Perlindungan Data Pribadi).
- Diakses oleh **ribuan instansi** (dukcapil daerah, kepolisian, bank untuk verifikasi KYC) dengan pola akses yang **tidak rata** (lonjakan saat musim pemilu/pendaftaran sekolah).
- Butuh **skalabilitas** agar tidak downtime saat lonjakan akses, tapi **tidak boleh** datanya berada di infrastruktur yang tidak terkendali penuh oleh negara.

## Tugas Kelompok

1. **Rekomendasikan Deployment Model** (Public / Private / Hybrid / Community Cloud) yang paling tepat untuk sistem ini. Jelaskan alasannya berdasarkan **karakteristik NIST** (on-demand self-service, broad network access, resource pooling, rapid elasticity, measured service) dikaitkan dengan kebutuhan kerahasiaan vs skalabilitas.
2. **Rekomendasikan Service Model** (IaaS / PaaS / SaaS) yang tepat untuk komponen-komponen berbeda dari sistem ini (boleh berbeda service model untuk komponen berbeda, mis. database inti vs portal publik untuk pengecekan status).
3. Jelaskan **minimal 2 risiko spesifik** dari pilihan kalian dan mitigasinya (mis. jika Hybrid Cloud dipilih: risiko sinkronisasi data antara private & public segment).
4. Bandingkan singkat dengan **satu alternatif yang kalian tolak** — kenapa alternatif itu kurang tepat (mis. kenapa Public Cloud murni ditolak, atau kenapa Private Cloud murni dianggap kurang skalabel).

## Struktur Submission

```
tugas-09-cloud-delivery-deployment/
├── README.md      # Analisis lengkap (isi dengan poin 1-4 di atas)
├── JURNAL.md
└── bukti/          # (opsional) diagram pendukung
```

## Rubrik Penilaian (Tugas 9)

| Komponen | Bobot | Kriteria |
|---|---|---|
| Ketepatan rekomendasi deployment model | 30% | Argumen berbasis karakteristik NIST, bukan sekadar "private cloud lebih aman" tanpa detail |
| Ketepatan rekomendasi service model | 25% | Pemetaan komponen sistem ke IaaS/PaaS/SaaS masuk akal |
| Analisis risiko & mitigasi | 25% | Risiko spesifik ke konteks data kependudukan (bukan risiko generik) |
| Perbandingan dengan alternatif yang ditolak | 20% | Argumen penolakan jelas dan berdasar |

## Batasan Penggunaan AI (Level 2)

Kebijakan **Level 2 (AI Assisted Idea Generation & Structuring)** berlaku — lihat [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Boleh bertanya ke AI gambaran umum karakteristik NIST/deployment model untuk brainstorming; **tidak boleh** meminta AI menuliskan rekomendasi/analisis akhir yang tinggal ditempel ke `README.md`. Catat pemakaian AI di "Log Penggunaan AI" pada `JURNAL.md`.

- Jawaban yang terasa seperti "template" (bisa dipakai untuk sistem cloud apa saja tanpa menyebut spesifik kependudukan/data pribadi/regulasi) akan dinilai rendah pada komponen ketepatan rekomendasi.
- `README.md` wajib membahas minimal satu skenario tandingan yang kalian buat sendiri (mis. "bagaimana jika instansi daerah tidak punya infrastruktur private cloud sendiri?") beserta jawabannya.

## Hasil Analisis
### 1. Rekomendasi Deployment Model: Hybrid Cloud
Deployment Model yang paling sesuai untuk Sistem Data Kependudukan adalah Hybrid Cloud, dengan Private Cloud sebagai infrastruktur utama dan Public Cloud sebagai pendukung layanan non-sensitif.

Hybrid Cloud merupakan kombinasi dua atau lebih infrastruktur cloud yang berbeda, seperti Private Cloud dan Public Cloud, yang tetap menjadi lingkungan terpisah tetapi dapat saling terhubung untuk mendukung kebutuhan sistem.

Hybrid Cloud dipilih karena mampu menyeimbangkan dua kebutuhan utama sistem, yaitu keamanan dan skalabilitas. Private Cloud memberikan pemerintah kendali terhadap penyimpanan serta pemrosesan data sensitif. Sementara itu, Public Cloud dapat dimanfaatkan untuk layanan non-sensitif yang membutuhkan fleksibilitas kapasitas. Dengan demikian, pemerintah tetap dapat mengendalikan data kependudukan tanpa harus mengorbankan kemampuan sistem dalam menghadapi peningkatan jumlah permintaan.

Pembagian infrastruktur yang direkomendasikan adalah:
- Private Cloud: Digunakan untuk menyimpan database utama kependudukan, NIK, alamat, data biometrik, serta menjalankan layanan autentikasi, otorisasi, dan verifikasi identitas. Infrastruktur ini sepenuhnya dikelola dan dikendalikan oleh pemerintah.
- Public Cloud: Digunakan untuk layanan yang tidak memerlukan akses terhadap data pribadi, seperti portal informasi umum dan analisis data yang telah dianonimkan.
- Integrasi antarinfrastruktur: Menggunakan API dengan enkripsi, autentikasi, dan pembatasan akses. Data pribadi tidak boleh direplikasi atau disimpan pada Public Cloud.

### Justifikasi Berdasarkan 5 Karakteristik Esensial NIST SP 800-145

| Karakteristik NIST | Implementasi pada Sistem Kependudukan (Kerahasiaan vs. Skalabilitas) |
| :--- | :--- |
| **On-Demand Self-Service** | Tim teknis pemerintah dan instansi mitra yang telah terotorisasi (*pre-approved tenant*, seperti bank peserta KYC atau Dukcapil provinsi) dapat melakukan provisi otomatis lingkungan *sandbox* API, peningkatan kuota *worker* verifikasi, atau penambahan *node* antrean melalui portal internal tanpa interaksi manual administrator. Kepatuhan kerahasiaan dijaga dengan **Policy-as-Code**, sehingga provisi otomatis hanya berjalan di dalam koridor hak akses dan batas keamanan yang telah disetujui sebelumnya. |
| **Broad Network Access** | Sistem diakses dari ribuan titik heterogen secara simultan (kantor Dukcapil kabupaten/kota, sistem kepolisian, *core banking*, hingga perangkat gawai masyarakat). Hybrid Cloud memisahkan jalur aksesnya: instansi resmi mengakses Zona Private melalui jaringan tertutup (*Dedicated Private Link* / VPN terenkripsi), sedangkan jutaan pengguna publik mengakses portal layanan melalui HTTPS standar di Zona Public agar perimeter jaringan privat negara tidak terpapar langsung ke internet publik. |
| **Resource Pooling** | Pada Zona Private, *resource pooling* dilakukan secara terisolasi khusus di lingkungan infrastruktur negara (*private multi-tenancy* antar-instansi pemerintah) sehingga komputasi dan penyimpanan tidak pernah bercampur dengan *tenant* komersial pihak luar. Sementara itu, *resource pooling* berskala masif di Zona Public dimanfaatkan khusus untuk menyerap beban komputasi *stateless* pada antarmuka publik. |
| **Rapid Elasticity** | Trafik sistem sangat timpang antara hari normal dan masa puncak (hari-H Pemilu, pembukaan serentak PPDB, atau periode registrasi KYC massal). Melalui mekanisme elastisitas di Zona Public, lapisan *edge*, *load balancer*, portal publik, dan antrean permintaan otomatis melakukan *scale-out* dalam hitungan menit saat trafik melonjak puluhan kali lipat, lalu melakukan *scale-in* kembali setelah puncak berakhir sehingga sistem terhindar dari *downtime* tanpa pemborosan perangkat keras fisik. |
| **Measured Service** | Setiap pemanggilan API verifikasi NIK/KYC oleh bank, kepolisian, atau instansi daerah dicatat secara presisi (volume *request*, latensi, sumber pemanggil, dan *bandwidth*). Selain digunakan untuk transparansi pembiayaan layanan verifikasi KYC (skema PNBP bagi sektor perbankan), metrik *measured service* berfungsi sebagai kontrol keamanan untuk mendeteksi anomali penarikan data massal (*mass scraping*) oleh kredensial instansi tertentu. |

---

### 2. Rekomendasi Service Model per Komponen Sistem
Karena setiap subsistem memiliki tingkat sensitivitas data dan kebutuhan kontrol berbeda, sistem memadukan **IaaS, PaaS, dan SaaS** secara proporsional:

| Komponen Sistem | Service Model | Zona Deployment | Alasan Pemilihan |
| :--- | :--- | :--- | :--- |
| **Core Database Kependudukan (NIK, Nama, Alamat, Biometrik) & HSM Enkripsi** | **IaaS** | Private Cloud | Memerlukan kendali penuh atas sistem operasi, segmentasi jaringan, *kernel hardening*, enkripsi level blok/disk, dan integrasi langsung dengan HSM fisik milik negara untuk memenuhi standar pengamanan Data Pribadi Spesifik (UU PDP). |
| **Core Biometric Matching Engine (Sidik Jari, Wajah, Iris)** | **IaaS** | Private Cloud | Pencocokan biometrik membutuhkan alokasi perangkat keras terdedikasi (CPU/GPU khusus) dan isolasi memori ketat agar templat biometrik mentah tidak pernah diproses di lapisan *managed* pihak ketiga. |
| **Core API Gateway (KYC Bank, Kepolisian, Dukcapil) & Sistem Tiket Pengaduan Warga (PII)** | **PaaS** | Private Cloud | Tim pengembang pemerintah dapat fokus membangun logika validasi, *RBAC*, enkripsi, dan penanganan laporan perbaikan data warga (yang memuat NIK/KTP) tanpa terbebani pemeliharaan *runtime* dan *patching* server dasar, sambil tetap memastikan seluruh data berada di dalam infrastruktur negara. |
| **Portal Publik (Cek Status DPT Pemilu/PPDB), Edge API Proxy & Antrean Permintaan** | **PaaS** | Public Cloud (Stateless, Region RI) | Memanfaatkan *managed container/serverless* dan *managed message queue* untuk *auto-scaling* instan menghadapi jutaan akses masyarakat serentak. Lapisan ini hanya meneruskan permintaan terenkripsi/ter-*hash* ke Zona Private tanpa menyimpan database warga. |
| **LMS Pelatihan Operator Dukcapil, Portal SOP Internal & Dashboard Statistik Demografi Agregat (Non-PII)** | **SaaS** | Public / Gov-SaaS Terisolasi | Komponen ini murni beroperasi pada data non-pribadi (materi pelatihan, panduan operasional, dan angka agregat demografi yang telah teranonimisasi penuh). Pemanfaatan SaaS mempercepat adopsi bagi ribuan kantor Dukcapil dengan biaya pemeliharaan minimal. |

---

### 3. Risiko dan Mitigasi
| Risiko | Mitigasi |
|---|---|
| Kebocoran data saat integrasi Private Cloud dan Public Cloud karena API dapat menjadi celah keamanan. | Data pribadi tidak disimpan di Public Cloud. Gunakan API terenkripsi, autentikasi, dan pembatasan akses. |
| Serangan dari Public Cloud menuju Private Cloud, misalnya melalui portal publik atau API. | Terapkan network segmentation, firewall/WAF, rate limiting, dan Zero Trust. Public Cloud tidak boleh memiliki akses langsung ke database utama. |
| Gangguan layanan Public Cloud saat terjadi lonjakan akses. | Gunakan redundancy dan failover, serta siapkan kapasitas cadangan untuk layanan yang bersifat kritis. |

---

### 4. Perbandingan dengan Alternatif: Public Cloud Murni
Public Cloud murni ditolak karena meskipun memiliki rapid elasticity, resource pooling, dan skalabilitas yang baik, pemerintah memiliki kontrol yang lebih terbatas terhadap infrastruktur tempat data sensitif diproses.

Hybrid Cloud lebih tepat karena data inti seperti NIK, alamat, dan biometrik tetap berada di Private Cloud, sedangkan Public Cloud digunakan untuk layanan non-sensitif yang membutuhkan skalabilitas tinggi. Dengan demikian, kebutuhan keamanan dan kontrol tetap terpenuhi tanpa mengorbankan skalabilitas.

---