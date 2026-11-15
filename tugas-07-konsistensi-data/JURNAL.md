# Jurnal Proses — Tugas 7

## Diskusi pemilihan model konsistensi
- Argumen yang dipertimbangkan:
  - Eventual Consistency saja: ringan dan cepat, tetapi saldo e-wallet yang basi membuat order ditolak padahal saldo cukup, berbeda dengan kasus "jumlah like" yang tidak merugikan siapa pun.
  - Sequential Consistency: urutan operasi sama di semua replika, tetapi sinkronisasi ketat antar kota menambah latensi dan menurunkan ketersediaan saat replikasi terganggu.
  - Eventual + Read-Your-Writes: replika tetap longgar, tetapi pelanggan dijamin melihat hasil top-up-nya sendiri.
- Kesimpulan akhir & alasan: Eventual Consistency dilengkapi Read-Your-Writes berbasis version number. Dampak bisnisnya paling kritis pada saldo pelanggan sendiri, sedangkan konsistensi ketat antar semua replika terlalu mahal untuk kebutuhan ini.
- Catatan batasan: RYW tidak menyelesaikan konflik penulisan bersamaan (mis. debit dari dua perangkat), sehingga debit sebaiknya ke satu sumber otoritatif. [sesuaikan dengan keputusan kelompok]

## Simulasi (jika dikerjakan)
- Hasil skenario naif vs Read-Your-Writes:
  - Skenario 1 (naive read): Jakarta menulis Rp50.000 (versi 1), Bandung masih Rp0, pesanan Rp40.000 ditolak. Bug terbukti; setelah replikasi 2 detik Bandung baru ikut Rp50.000.
  - Skenario 2 (RYW redirect): Jakarta Rp70.000 (versi 2), Bandung masih versi 1. Client membutuhkan versi 2, sehingga pembacaan dialihkan ke Jakarta; pesanan Rp65.000 diterima.
  - Skenario 3 (RYW polling): Bandung masih versi 2, client menunggu sampai Bandung versi 3, lalu membaca Rp80.000.
  - Hasil akhir: Jakarta dan Bandung sama-sama Rp80.000 (versi 3), jadi eventual consistency tercapai.
- Trade-off: redirect memberi jawaban segera tetapi menambah beban ke Jakarta; polling tidak membebani Jakarta tetapi latensinya tidak pasti.

## Log Penggunaan AI (Level 2)

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 15 Nov 2026 | Claude | saya punya kasus yang dimana ini membutuhkan Sequential Consistency (semua replika melihat urutan operasi yang sama) atau cukup Eventual Consistency, kasus foofgo data saldo e-wallet pelanggan foodgo berbeda antara server | Mengapa Eventual Consistency ditolak? Karena ada jeda waktu sinkronisasi. Pelanggan bisa melakukan kecurangan belanja dua kali di server berbeda (double spending), atau saldo berubah-ubah acak yang membuat pengguna panik. Mengapa harus Sequential Consistency? Semua server wajib melihat urutan transaksi yang sama persis (misal: Top-up dulu, baru Belanja). Ini memastikan validasi saldo selalu akurat sebelum transaksi diizinkan. | langsung di implementasikan ke kode |
