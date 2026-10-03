# Nalarin Quiz

Satu file `index.html` untuk semuanya: menu pilihan kuis **dan** halaman mengerjakan kuis. Semua kuis cukup berupa folder berisi `soal.json` (dan folder `gambar/` jika perlu). Tidak perlu lagi menyalin file HTML ke tiap folder.

## Struktur folder

```
Kuis/
├── index.html          ← satu-satunya file HTML (menu + kuis)
├── daftar.json         ← daftar kuis (dibuat otomatis)
├── buat-daftar.py      ← pembuat daftar.json
├── README.md
├── .github/workflows/daftar.yml   ← (opsional) pembaruan otomatis di GitHub
│
├── Biologi/
│   └── Kelas9/DiagnosticTest/
│       └── soal.json
├── Matematika/
│   ├── Kelas7/Perbandingan/
│   │   ├── soal.json
│   │   └── gambar/          ← gambar kuis ini (jika ada)
│   └── Kelas9/DiagnosticTest/soal.json
├── tkaEkonomi/
│   └── kuis1/soal.json
│
└── _template/          ← contoh soal teks, bergambar, dan bahasa (tidak tampil di menu)
```

Pola yang dikenali: `Mapel / Kelas / Topik / soal.json`. Kedalaman boleh berbeda (contoh: `tkaEkonomi/kuis1/` tidak punya kelas, akan masuk ke filter **Umum**).

## Cara kerja

1. `buat-daftar.py` memindai semua file `.json` yang punya kunci `"questions"` lalu menulis `daftar.json`.
2. Tanpa parameter, `index.html` menampilkan menu dari `daftar.json`: filter **Mata pelajaran** → filter **Kelas** → daftar topik, plus kolom pencarian. Daftar yang panjang ditampilkan 40 per halaman dengan tombol "Tampilkan lebih banyak". Filter terakhir diingat saat siswa kembali dari kuis.
3. Saat topik dipilih, `index.html` membuka kuis dengan alamat seperti:

```
index.html?kuis=Matematika/Kelas7/Perbandingan/soal.json
```

Alamat ini bisa dibagikan langsung ke siswa. Gambar kuis otomatis dicari di folder `gambar/` di samping `soal.json` itu.

Browser tidak bisa membaca isi folder sendiri, jadi `daftar.json` perlu dibuat ulang setiap kali ada kuis yang ditambah, dihapus, atau diganti namanya (lihat bagian berikut).

## Menambah kuis baru

1. Buat folder sesuai pola, misalnya `Kimia/Kelas10/Stoikiometri/`.
2. Letakkan `soal.json` di dalamnya. Mulai dari contoh di `_template/`:
   - `SoalTeks/`: soal teks biasa
   - `SoalBergambar/`: soal dengan gambar
   - `SoalBahasa/`: teks bacaan bersama, gambar opsional
3. Jika ada gambar, taruh di `gambar/` di sebelah `soal.json`.
4. Perbarui daftar:

```bash
python3 buat-daftar.py
```

Skrip menampilkan ringkasan kuis yang ditemukan dan **memeriksa isi soal**: jumlah pilihan kurang dari dua, kunci `answer` yang tidak ada di `options`, teks soal kosong, atau `total_questions` yang tidak cocok. Bagian *Perhatian* di akhir hasil menunjukkan file dan nomor soal yang bermasalah.

Satu folder boleh berisi lebih dari satu file soal (misalnya `soal-a.json` dan `soal-b.json`). Masing-masing menjadi satu kuis, dan nama filenya ditambahkan ke label topik.

### Pembaruan otomatis di GitHub (opsional)

File `.github/workflows/daftar.yml` menjalankan `buat-daftar.py` setiap kali ada `push` ke cabang `main` atau `master`, lalu menyimpan `daftar.json` yang baru. Dengan ini cukup tambah folder kuis dan `push`. Skrip hanya menulis ulang `daftar.json` jika isinya benar-benar berubah.

## Pengaturan menu

Dari nama folder:

| Tampilan | Sumber |
|---|---|
| Mata pelajaran | Folder tingkat pertama |
| Kelas | Folder bernama seperti `Kelas7`, `Kelas 9`, `Fase D`, `X`, `XI`. Jika tidak ada, folder tingkat kedua dipakai bila masih ada folder di bawahnya |
| Topik | Folder sisanya |
| Judul | `title` di JSON (jika kosong: `topic`, lalu nama folder) |

Nama folder dirapikan otomatis (`Kelas9` → Kelas 9, `DiagnosticTest` → Diagnostic Test).

Untuk menimpa dari dalam `soal.json`, tambahkan kolom opsional `"mapel"`, `"kelas"`, atau `"topik"`.

Pengaturan di bagian atas `buat-daftar.py`:

| Pengaturan | Fungsi |
|---|---|
| `LABELS` | Nama tampilan khusus per folder, misalnya `"tkaEkonomi": "TKA Ekonomi"` |
| `EXCLUDE` | Folder yang dilewati. Bawaan: `htmlTemplate`, `gambar`, `node_modules` |

Folder berawalan `_` atau `.` selalu dilewati. Untuk menyembunyikan kuis yang belum siap, ganti nama foldernya menjadi `_Kimia`.

## Format `soal.json`

```json
{
  "title": "Diagnostic Test Biologi",
  "topic": "Sel dan Jaringan",
  "difficulty_summary": "3 soal mudah, 4 sedang, 3 sulit.",
  "total_questions": 10,
  "questions": [
    {
      "number": 1,
      "difficulty": "Mudah",
      "question": "Organ yang menghasilkan empedu adalah ...",
      "options": { "A": "Lambung", "B": "Hati", "C": "Pankreas", "D": "Usus halus" },
      "answer": "B",
      "explanation": "Empedu dihasilkan oleh hati."
    }
  ]
}
```

| Kolom | Wajib | Keterangan |
|---|---|---|
| `title` | disarankan | Judul kuis |
| `topic` | tidak | Judul besar di halaman awal dan data topik yang dikirim ke spreadsheet |
| `difficulty_summary` | tidak | Keterangan singkat di halaman awal |
| `total_questions` | tidak | Jika kosong, dihitung dari jumlah soal |
| `questions[].number` | disarankan | Nomor soal. Juga dipakai sebagai nama file gambar |
| `questions[].difficulty` | tidak | `Mudah`, `Sedang`, atau `Sulit` |
| `questions[].question` | ya | Teks soal |
| `questions[].options` | ya | Pilihan jawaban. Kuncinya bebas (A–D, boleh lebih) |
| `questions[].answer` | ya | Harus sama persis dengan salah satu kunci di `options` |
| `questions[].explanation` | tidak | Pembahasan di mode review |

**Format teks.** Semua teks (soal, pilihan, pembahasan, teks bacaan) menerima tag dasar `<b> <i> <u> <em> <strong> <sub> <sup> <br> <code> <mark> <small>`. Tag lain ditampilkan apa adanya sebagai teks, sehingga simbol seperti `a < b` aman ditulis langsung. Entitas HTML seperti `&lt;` dan `&amp;` tetap berfungsi. Baris baru (`\n`) dihormati.

## Gambar

Gambar dicari otomatis dari nomor soal di folder `gambar/` di samping `soal.json`:

- Soal nomor 1 mencari `1.jpg`, `1.png`, `1.jpeg`, `1.webp`, `1.gif`, `1.svg`, `1.avif` (campur format diperbolehkan).
- Gunakan ekstensi huruf kecil, karena GitHub Pages membedakan huruf besar dan kecil.
- Jika tidak ada file, soal tampil tanpa gambar dan tanpa pesan error.
- Gambar bisa diketuk atau diklik untuk diperbesar (tutup dengan ketuk lagi atau `Esc`).

Pengaturan per soal:

| Di JSON | Hasil |
|---|---|
| (tidak ditulis) | Mencari gambar sesuai nomor soal |
| `"image": "segitiga.png"` | Memakai file bernama khusus (subfolder boleh: `"bangun/segitiga.png"`). Jika tidak ditemukan, muncul kotak merah berisi nama file yang dicari |
| `"image": false` | Soal ini tanpa gambar |

Pengaturan tingkat kuis:

| Di JSON | Hasil |
|---|---|
| `"image_folder": "img"` | Folder gambar selain `gambar/` (relatif terhadap `soal.json`) |
| `"warn_missing_image": true` | Tampilkan kotak merah untuk semua gambar yang tidak ditemukan (berguna untuk kuis yang semua soalnya bergambar, saat menyusun soal) |

## Teks bacaan (soal bahasa)

Tulis teks sekali di `passages`, lalu panggil dari soal dengan `passage`:

```json
{
  "passages": [
    {
      "id": "teks1",
      "title": "Bank Sampah di Sekolah Kami",
      "text": ["Paragraf pertama ...", "Paragraf kedua ..."],
      "image": "poster-lomba"
    }
  ],
  "questions": [
    { "number": 1, "passage": "teks1", "question": "...", "options": {}, "answer": "B" },
    { "number": 2, "passage": "teks1", "question": "...", "options": {}, "answer": "C" },
    { "number": 3, "question": "Soal tanpa teks bacaan ...", "options": {}, "answer": "A" }
  ]
}
```

| Kolom `passages` | Wajib | Keterangan |
|---|---|---|
| `id` | ya | Nama pengenal, dipanggil lewat `"passage"` |
| `title` | tidak | Judul di atas teks |
| `text` | ya | Array paragraf, atau satu string dengan paragraf dipisah baris kosong |
| `image` | tidak | Gambar milik teks (ekstensi boleh dihilangkan). Disimpan di folder `gambar/` dengan nama bebas, hindari nama berupa angka agar tidak tertukar dengan gambar soal |

Di PC, teks bacaan tampil di kolom kiri dan tetap terlihat saat halaman digulir. Di HP, teks tampil di atas soal dengan tombol **Sembunyikan teks**. Keterangan "Teks ini dipakai untuk soal 1–4" muncul otomatis.

## Menyimpan nilai ke Google Sheets

Nilai dikirim ke Google Apps Script lewat konstanta `SCRIPT_URL` di dalam `index.html`. Ganti nilainya dengan alamat web app milikmu. Data yang dikirim (`POST`, isi JSON):

```json
{
  "nama": "Nama siswa",
  "topik": "Sel dan Jaringan",
  "durasi": "12 menit 30 detik",
  "skor": 80,
  "benar": 8,
  "salah": 2,
  "detailJawaban": [ { "jawaban": "B", "benar": true }, { "jawaban": "-", "benar": false } ]
}
```

Skor = jumlah benar ÷ total soal × 100. Soal kosong dicatat `"-"` dan dihitung salah. Jika pengiriman gagal, layar hasil menampilkan tombol **coba kirim lagi**.

## Fitur siswa

- Timer, tanda **Ragu-ragu**, navigasi nomor soal, mode gelap, dan mode review (kunci, jawaban sendiri, pembahasan).
- Progres tersimpan otomatis di browser per kuis. Jika halaman dimuat ulang, siswa bisa melanjutkan dengan nama yang sama. Progres dihapus setelah nilai berhasil terkirim.
- Nama siswa diingat untuk kuis berikutnya.
- Pintasan PC: `A`–`E` atau `1`–`9` memilih jawaban, `←` `→` pindah soal, `F` tandai ragu-ragu, `Esc` tutup gambar.

## Menjalankan

**Lokal.** Browser memblokir pembacaan JSON jika halaman dibuka langsung dari file, jadi jalankan server sederhana di folder `Kuis/`:

```bash
python3 buat-daftar.py
python3 -m http.server 8000
```

Lalu buka `http://localhost:8000`.

**Online.** Unggah folder ke GitHub Pages. Folder `_template` boleh ikut diunggah tetapi tidak tampil di menu.

## Pindah dari struktur lama

- File `Kuis.html` dan `EkonomiKuis1.html` di tiap folder tidak diperlukan lagi dan boleh dihapus. Cukup simpan `soal.json`.
- Tautan lama ke `.../Kuis.html` tidak berlaku lagi. Gunakan `index.html?kuis=.../soal.json` atau pilih dari menu.
- Jika `SCRIPT_URL` di kuis lama berbeda dengan yang ada di `index.html`, samakan dulu.
- Folder `htmlTemplate` lama aman dibiarkan, karena otomatis dilewati.

## Pemecahan masalah

| Masalah | Penyebab dan solusi |
|---|---|
| "Daftar kuis belum bisa dimuat" | `daftar.json` belum ada, atau halaman dibuka langsung dari file. Jalankan `buat-daftar.py` dan buka lewat server |
| Kuis baru tidak muncul di menu | Daftar belum diperbarui. Jalankan `python3 buat-daftar.py` dan lihat bagian *Perhatian* |
| Kuis yang sudah dihapus masih muncul | Jalankan ulang `buat-daftar.py`, lalu segarkan browser (Ctrl+F5) |
| Kuis berada di kelompok yang salah | Periksa nama folder, atau isi `"mapel"`, `"kelas"`, `"topik"` di JSON |
| "Kuis tidak bisa dimuat" setelah memilih | JSON rusak (koma atau kurung salah). Skrip menampilkan file yang rusak |
| Gambar tidak muncul | Cek nama file sesuai nomor soal, ekstensi huruf kecil, dan lokasinya di `gambar/` di samping `soal.json` |
| Jawaban benar dianggap salah | `answer` harus sama persis dengan kunci di `options` (huruf besar/kecil berpengaruh) |
| Nilai tidak masuk spreadsheet | Periksa `SCRIPT_URL` dan akses web app Apps Script, lalu gunakan **coba kirim lagi** |

## Kredit

Dibuat oleh Johan Herdi Putra, 2026.
