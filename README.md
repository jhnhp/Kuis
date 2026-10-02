# Kuis Nalarin: Kumpulan Kuis

Folder ini berisi semua kuis (Biologi, Fisika, Matematika, TKA Ekonomi, dan seterusnya) beserta halaman depan `index.html` yang menampilkan daftar kuis dengan pencarian dan filter mata pelajaran.

## Struktur folder

```
Kuis/
├── index.html            ← halaman depan (daftar semua kuis)
├── daftar.json           ← data daftar kuis (dibuat otomatis, jangan diedit manual)
├── buat-daftar.py        ← skrip pembuat daftar.json
├── README.md
│
├── Biologi/
│   └── Kelas9/DiagnosticTest/
│       ├── Kuis.html
│       └── soal.json
├── Fisika/…
├── Matematika/
│   ├── Kelas7/Perbandingan/
│   └── Kelas9/DiagnosticTest/
├── tkaEkonomi/
│   └── kuis1/
│       ├── EkonomiKuis1.html
│       └── soal.json
│
└── htmlTemplate/         ← bahan membuat kuis baru (tidak tampil di index)
    ├── SoalBergambar/
    ├── SoalTeks/
    └── TemplateAwal/
```

Pola yang dipakai: `Mata pelajaran / Kelas / Nama kuis /`. Kedalamannya bebas, tidak harus tiga tingkat (contoh: `tkaEkonomi/kuis1/` hanya dua tingkat).

## Cara kerja halaman depan

GitHub Pages dan browser tidak bisa membaca isi folder secara langsung. Karena itu:

1. `buat-daftar.py` memindai semua folder dan menulis `daftar.json`.
2. `index.html` membaca `daftar.json` lalu menampilkan kartu kuis yang dikelompokkan per mata pelajaran.

Sebuah folder dianggap **kuis** jika berisi:
- minimal satu file `.html`, dan
- minimal satu file `.json` yang punya kunci `"questions"`.

Informasi di kartu diambil otomatis:

| Tampilan | Sumber |
|---|---|
| Kelompok (mata pelajaran) | Nama folder tingkat pertama |
| Label kecil (Kelas 9, Diagnostic Test) | Nama folder tingkat berikutnya, dirapikan otomatis |
| Judul kartu | `title` di `soal.json` (jika kosong: `topic`, lalu nama folder) |
| Keterangan | `topic` di `soal.json` |
| Jumlah soal | `total_questions`, atau jumlah item di `questions` |

## Menambah kuis baru

1. Buat folder baru mengikuti pola, misalnya `Kimia/Kelas10/Stoikiometri/`.
2. Salin template yang sesuai dari `htmlTemplate/` ke folder itu:
   - soal teks biasa: `TemplateAwal/` (pilih salah satu HTML-nya)
   - soal bergambar: `SoalBergambar/`
   - soal bahasa dengan teks bacaan: `SoalTeks/`
3. Ganti nama file menjadi `Kuis.html` dan `soal.json`. Jika file soal tidak bernama `soal.json`, kuis harus dibuka dengan `?data=nama-file.json`. Skrip akan menambahkan parameter itu otomatis di daftar.
4. Isi `soal.json`. Jika kuis memakai gambar, taruh di folder `gambar/` di sebelah `Kuis.html`.
5. Jika perlu mengirim nilai ke spreadsheet, periksa `SCRIPT_URL` di dalam `Kuis.html`.
6. Perbarui daftar (lihat di bawah).

## Memperbarui daftar

Setiap kali menambah, menghapus, atau mengganti nama kuis, jalankan dari folder `Kuis/`:

```bash
python3 buat-daftar.py
```

Skrip menampilkan ringkasan kuis yang ditemukan, misalnya:

```
5 kuis ditemukan -> daftar.json

  [Biologi] Kelas 9 / Diagnostic Test  |  Diagnostic Test Biologi  (20 soal)
  ...
Perhatian:
  - Fisika/Kelas9/Latihan: ada file .html tetapi tidak ada JSON soal yang valid
```

Bagian **Perhatian** muncul jika ada folder yang tidak lengkap (misalnya HTML tanpa JSON, atau JSON yang formatnya rusak), sehingga kesalahan mudah ketahuan.

Agar tidak lupa, jalankan skrip ini sebelum `git push`.

## Pengaturan di `buat-daftar.py`

Bagian atas skrip bisa diubah:

| Pengaturan | Fungsi |
|---|---|
| `EXCLUDE` | Folder yang tidak didaftarkan. Bawaan: `htmlTemplate`, `gambar`, `node_modules`. Folder berawalan `.` atau `_` juga selalu diabaikan |
| `LABELS` | Nama tampilan khusus. Contoh: `"tkaEkonomi": "TKA Ekonomi"`. Tanpa ini, nama dirapikan otomatis (`Kelas9` → `Kelas 9`, `DiagnosticTest` → `Diagnostic Test`) |
| `DEFAULT_JSON` | Nama file soal bawaan (`soal.json`) |
| `PREFERRED_HTML` | Urutan pilihan file HTML jika satu folder punya beberapa (`Kuis.html`, lalu `index.html`) |

Kiat:
- **Menyembunyikan kuis** (misalnya belum siap): ganti nama foldernya dengan awalan `_` (`_Kimia`), atau tambahkan namanya ke `EXCLUDE`, lalu jalankan ulang skrip.
- **Satu folder, beberapa file soal** (misalnya `soal-a.json` dan `soal-b.json`): masing-masing muncul sebagai kartu sendiri. Pastikan `title` di tiap JSON berbeda agar mudah dibedakan.
- **Folder `gambar/`** otomatis diabaikan, jadi aman diletakkan di dalam folder kuis.

## Menjalankan

**Lokal.** Browser memblokir pembacaan JSON jika halaman dibuka langsung dari file, jadi jalankan server sederhana di folder `Kuis/`:

```bash
python3 -m http.server 8000
```

Lalu buka `http://localhost:8000`.

**Online.** Unggah seluruh folder ke GitHub Pages. Jika repositori hanya berisi folder `Kuis/`, alamatnya akan seperti `https://username.github.io/nama-repo/`. Folder `htmlTemplate` boleh ikut diunggah, tetapi tidak muncul di daftar. Jika tidak ingin template terbuka untuk umum, jangan sertakan di repositori publik.

## Pemecahan masalah

| Masalah | Penyebab dan solusi |
|---|---|
| Muncul pesan "Daftar kuis belum bisa dimuat" | `daftar.json` belum ada, atau halaman dibuka langsung dari file. Jalankan `buat-daftar.py` dan buka lewat server |
| Kuis baru tidak muncul | Daftar belum diperbarui. Jalankan `python3 buat-daftar.py`. Periksa juga bagian Perhatian di hasil skrip |
| Kuis lama masih muncul padahal sudah dihapus | Jalankan ulang `buat-daftar.py`, lalu segarkan browser (Ctrl+F5) |
| Judul kartu hanya nama folder | `title` dan `topic` di `soal.json` kosong. Isi salah satunya |
| Kartu terbuka tetapi kuis "tidak bisa dimuat" | Nama file soal tidak cocok dengan yang dibaca `Kuis.html`. Ganti nama menjadi `soal.json` atau buka dengan `?data=` |
| Gambar tidak muncul di kuis | Periksa folder `gambar/`, nama file sesuai nomor soal, dan `image_folder` di JSON (template `SoalBergambar` lama memakai `gambar/soal-gambar`) |

## Dokumentasi format soal

Format `soal.json`, aturan penamaan gambar, teks bacaan, dan pengiriman nilai ke Google Sheets dijelaskan di README template. Jika kamu menyimpannya, letakkan di `htmlTemplate/README.md`.

## Kredit

Dibuat oleh Johan Herdi Putra, 2026.
