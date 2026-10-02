#!/usr/bin/env python3
"""
Membuat daftar.json untuk index.html dengan memindai semua folder kuis.

Cara pakai (dari folder Kuis/):   python3 buat-daftar.py

Sebuah folder dianggap "kuis" jika berisi:
  - minimal satu file .html, dan
  - minimal satu file .json yang punya kunci "questions".
"""
import json, os, re, sys, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))

# Folder yang TIDAK ikut didaftarkan (nama folder, di kedalaman mana pun).
# Folder berawalan "." atau "_" juga otomatis diabaikan.
EXCLUDE = {"htmlTemplate", "gambar", "node_modules"}

# Nama tampilan khusus untuk folder tertentu. Jika tidak ada di sini,
# nama dirapikan otomatis (Kelas9 -> Kelas 9, DiagnosticTest -> Diagnostic Test).
LABELS = {
    "tkaEkonomi": "TKA Ekonomi",
}

DEFAULT_JSON = "soal.json"       # file soal yang dibaca kuis tanpa ?data=
PREFERRED_HTML = ["kuis.html", "index.html"]


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


def load_quiz(path):
    try:
        with open(path, encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        return None
    if isinstance(d, dict) and isinstance(d.get("questions"), list):
        return d
    return None


def main():
    entries, warnings = [], []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames
                             if d not in EXCLUDE and not d.startswith((".", "_")))
        rel = os.path.relpath(dirpath, ROOT)
        if rel == ".":
            continue
        htmls = sorted(f for f in filenames if f.lower().endswith(".html"))
        jsons = {f: load_quiz(os.path.join(dirpath, f))
                 for f in sorted(filenames) if f.lower().endswith(".json")}
        jsons = {k: v for k, v in jsons.items() if v}
        if not htmls and not jsons:
            continue
        posix = rel.replace(os.sep, "/")
        if not htmls:
            warnings.append(f"{posix}: ada file soal tetapi tidak ada file .html")
            continue
        if not jsons:
            warnings.append(f"{posix}: ada file .html tetapi tidak ada JSON soal yang valid")
            continue

        html = next((h for p in PREFERRED_HTML for h in htmls if h.lower() == p), htmls[0])
        if len(htmls) > 1 and html not in (h for h in htmls if h.lower() in PREFERRED_HTML):
            warnings.append(f"{posix}: ada beberapa file .html, dipakai '{html}'")

        parts = posix.split("/")
        for jname, d in jsons.items():
            url = f"{posix}/"
            if jname != DEFAULT_JSON:
                url += f"?data={jname}"
            entries.append({
                "title": d.get("title") or d.get("topic") or pretty(parts[-1]),
                "topic": d.get("topic") or "",
                "questions": d.get("total_questions") or len(d["questions"]),
                "mapel": pretty(parts[0]),
                "sub": [pretty(p) for p in parts[1:]],
                "url": url,
            })

    entries.sort(key=lambda e: (natural(e["mapel"]), natural("/".join(e["sub"])), natural(e["title"])))
    out = {"generated": datetime.datetime.now().isoformat(timespec="seconds"), "kuis": entries}
    with open(os.path.join(ROOT, "daftar.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"{len(entries)} kuis ditemukan -> daftar.json\n")
    for e in entries:
        print(f"  [{e['mapel']}] {' / '.join(e['sub']) or '-'}  |  {e['title']}  ({e['questions']} soal)")
    if warnings:
        print("\nPerhatian:")
        for w in warnings:
            print("  -", w)


if __name__ == "__main__":
    sys.exit(main())
