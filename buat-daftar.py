#!/usr/bin/env python3
"""
Memindai semua soal.json di bawah folder ini lalu menulis daftar.json
(dipakai index.html untuk menu pilihan kuis).

Pakai:  python3 buat-daftar.py

Setiap file .json yang punya kunci "questions" dianggap sebuah kuis.
Pola folder yang dikenali:   Mapel / Kelas / Topik / soal.json
"""
import json, os, re, sys, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))

# Folder yang tidak dipindai (nama folder, di kedalaman mana pun).
# Folder berawalan "." atau "_" selalu diabaikan.
EXCLUDE = {"htmlTemplate", "gambar", "node_modules"}

# Nama tampilan khusus. Jika tidak ada di sini, nama folder dirapikan otomatis.
LABELS = {
    "tkaEkonomi": "TKA Ekonomi",
}

KELAS_RE = re.compile(r"^((kelas|kls|class|grade|fase|tingkat)[\s_-]*(\d+|[ivx]+)|\d{1,2}|[ivx]{1,4})$", re.I)


def pretty(name):
    if name in LABELS:
        return LABELS[name]
    s = re.sub(r"[_\-]+", " ", name)
    s = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", s)
    s = re.sub(r"(?<=[A-Za-z])(?=\d)", " ", s)
    s = re.sub(r"(?<=\d)(?=[A-Za-z])", " ", s)
    return " ".join(w[:1].upper() + w[1:] for w in s.split())


def natural(text):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", text)]


def split_path(parts):
    """['Matematika','Kelas7','Perbandingan'] -> (mapel, kelas, [topik...])"""
    if not parts:
        return "Umum", "", []
    mapel, rest = parts[0], list(parts[1:])
    idx = next((i for i, p in enumerate(rest) if KELAS_RE.match(p)), None)
    if idx is None and len(rest) >= 2:
        idx = 0
    kelas = ""
    if idx is not None:
        kelas = rest.pop(idx)
    return mapel, kelas, rest


def validate(d):
    """Pemeriksaan cepat isi soal. Mengembalikan daftar masalah."""
    problems = []
    qs = d["questions"]
    if d.get("total_questions") and d["total_questions"] != len(qs):
        problems.append(f"total_questions={d['total_questions']} tetapi ada {len(qs)} soal")
    for i, q in enumerate(qs, 1):
        no = q.get("number", i)
        opts = q.get("options")
        if not q.get("question"):
            problems.append(f"soal {no}: teks soal kosong")
        if not isinstance(opts, dict) or len(opts) < 2:
            problems.append(f"soal {no}: pilihan jawaban kurang dari 2")
        elif q.get("answer") not in opts:
            problems.append(f"soal {no}: answer '{q.get('answer')}' tidak ada di options")
    return problems


def main():
    entries, warnings = [], []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames
                             if d not in EXCLUDE and not d.startswith((".", "_")))
        rel = os.path.relpath(dirpath, ROOT)
        parts = [] if rel == "." else rel.replace(os.sep, "/").split("/")
        for fn in sorted(filenames):
            if not fn.lower().endswith(".json") or fn == "daftar.json":
                continue
            full = os.path.join(dirpath, fn)
            where = "/".join(parts + [fn])
            try:
                with open(full, encoding="utf-8") as f:
                    d = json.load(f)
            except Exception as e:
                if fn.lower().startswith("soal"):
                    warnings.append(f"{where}: JSON rusak ({e})")
                continue
            if not (isinstance(d, dict) and isinstance(d.get("questions"), list)):
                continue

            mapel, kelas, topik = split_path(parts)
            stem = os.path.splitext(fn)[0]
            mapel = d.get("mapel") or pretty(mapel)
            kelas = d.get("kelas") or (pretty(kelas) if kelas else "")
            topik_lbl = [pretty(t) for t in topik]
            if stem.lower() != "soal":
                topik_lbl.append(pretty(stem))
            if d.get("topik"):
                topik_lbl = [d["topik"]]

            entries.append({
                "title": d.get("title") or d.get("topic") or (topik_lbl[-1] if topik_lbl else mapel),
                "topic": d.get("topic") or "",
                "summary": d.get("difficulty_summary") or d.get("subtitle") or "",
                "questions": d.get("total_questions") or len(d["questions"]),
                "mapel": mapel,
                "kelas": kelas,
                "topik": topik_lbl,
                "path": where,
            })
            for p in validate(d):
                warnings.append(f"{where}: {p}")

    entries.sort(key=lambda e: (natural(e["mapel"]), natural(e["kelas"]) if e["kelas"] else [9999],
                                natural(" ".join(e["topik"])), natural(e["title"])))

    target = os.path.join(ROOT, "daftar.json")
    old = None
    try:
        with open(target, encoding="utf-8") as f:
            old = json.load(f)
    except Exception:
        pass
    if old and old.get("kuis") == entries:
        print("daftar.json sudah terbaru, tidak ada perubahan.")
    else:
        out = {"generated": datetime.datetime.now().isoformat(timespec="seconds"), "kuis": entries}
        with open(target, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=2)
        print(f"daftar.json diperbarui: {len(entries)} kuis")

    print()
    for e in entries:
        print(f"  {e['mapel']:<14} {e['kelas'] or '-':<9} {' › '.join(e['topik']) or '-':<28} {e['questions']:>3} soal  {e['path']}")
    if warnings:
        print("\nPerhatian:")
        for w in warnings:
            print("  -", w)


if __name__ == "__main__":
    sys.exit(main())
