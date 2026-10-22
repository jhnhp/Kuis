# Catatan untuk Claude

Repo ini (`jhnhp/Kuis`) adalah **Nalarin Kuis** yang berdiri sendiri. Format berkas soal dan cara menambah kuis: lihat `README.md`.

## Peran repo

- Repo ini akan terus ditambah kuis sebanyak-banyaknya, tidak terbatas pada pelajaran sekolah (misalnya Olimpiade Matematika dan kuis TKA).
- Kuis yang fokus ke pelajaran sekolah dan terhubung dengan materi Learn juga ada di repo `nalarin-learn-html` (`/home/jhn/projects/Nalarin/nalarin-learn-html`). Folder seperti `TKA SMA` ada di kedua repo; setelah salah satunya berubah, salin ke repo lain (`rsync -a`) agar tetap identik.

## Jumlah soal

- Aturan 20 soal per bab dan 40 soal per Simulasi/Evaluasi Akhir **tidak berlaku** di repo ini secara umum (kuis Olimpiade boleh 30 soal, mengikuti format lomba aslinya).
- Namun, kuis yang disalin dari `nalarin-learn-html` harus tetap memenuhi aturan di sana: 20 atau 40 soal, komposisi 30% Mudah / 50% Sedang / 20% Sulit, kunci jawaban merata A–D.

## Alur kerja

- Setelah menambah, menghapus, atau mengubah nama kuis: `python3 buat-daftar.py`, lalu commit `daftar.json` bersama kuisnya.
- Commit dan push ke `main`.
