#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WORTSCHATZ-TRAINER — Ôn từ vựng kỹ thuật Đức theo lịch lặp ngắt quãng (SM-2).

    python3 wortschatz_trainer.py lernen [--neu 10] [--richtung mix|de|vi]
    python3 wortschatz_trainer.py status
    python3 wortschatz_trainer.py anki [--ausgabe Wortschatz_Anki.txt]
"""

import argparse
import csv
import json
import random
import unicodedata
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
VOCAB_CSV = HERE / "Wortschatz_Fach.csv"
PROGRESS_JSON = HERE / "wortschatz_fortschritt.json"
ARTICLES = ("der", "die", "das")

# Nút tự chấm kiểu Anki -> chất lượng SM-2 (0..5)
GRADE_TO_QUALITY = {"1": 0, "2": 3, "3": 4, "4": 5}


def load_vocab(path: Path = VOCAB_CSV) -> list:
    with open(path, encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        next(reader)
        return [
            {"de": r[0].strip(), "en": r[1].strip(), "vi": r[2].strip(),
             "note": r[3].strip() if len(r) > 3 else ""}
            for r in reader if r and r[0].strip()
        ]


def load_progress(path: Path = PROGRESS_JSON) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_progress(progress: dict, path: Path = PROGRESS_JSON) -> None:
    path.write_text(json.dumps(progress, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")


def new_card() -> dict:
    return {"ef": 2.5, "interval": 0, "reps": 0, "lapses": 0, "due": None}


def sm2_update(card: dict, quality: int, today: date) -> dict:
    """Thuật toán SuperMemo-2: quality 0..5, < 3 nghĩa là quên -> học lại từ đầu."""
    card = dict(card)
    if quality < 3:
        card["reps"] = 0
        card["interval"] = 1
        card["lapses"] += 1
    else:
        if card["reps"] == 0:
            card["interval"] = 1
        elif card["reps"] == 1:
            card["interval"] = 6
        else:
            card["interval"] = round(card["interval"] * card["ef"])
        card["reps"] += 1
    card["ef"] = max(1.3, card["ef"] + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    card["ef"] = round(card["ef"], 3)
    card["due"] = (today + timedelta(days=card["interval"])).isoformat()
    return card


def normalize_german(text: str) -> str:
    """So khớp không phân biệt hoa/thường; chấp nhận gõ ae/oe/ue/ss thay cho ä/ö/ü/ß."""
    text = unicodedata.normalize("NFC", text).strip().lower()
    for src, dst in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        text = text.replace(src, dst)
    return " ".join(text.split())


def split_article(term: str) -> tuple:
    parts = term.split(maxsplit=1)
    if len(parts) == 2 and parts[0] in ARTICLES:
        return parts[0], parts[1]
    return None, term


def check_answer(expected: str, answer: str) -> str:
    """Trả về 'richtig', 'artikel' (đúng danh từ nhưng sai/thiếu mạo từ) hoặc 'falsch'."""
    exp, ans = normalize_german(expected), normalize_german(answer)
    if exp == ans:
        return "richtig"
    exp_art, exp_noun = split_article(exp)
    ans_art, ans_noun = split_article(ans)
    if exp_art and exp_noun == ans_noun:
        return "artikel"
    return "falsch"


def due_cards(vocab: list, progress: dict, today: date, new_limit: int) -> list:
    due, fresh = [], []
    for word in vocab:
        card = progress.get(word["de"])
        if card is None:
            fresh.append(word)
        elif date.fromisoformat(card["due"]) <= today:
            due.append(word)
    return due + fresh[:new_limit]


def ask_typed(word: dict) -> int:
    print(f"\n🇻🇳 {word['vi']}   🇬🇧 {word['en']}")
    answer = input("🇩🇪 Tiếng Đức (kèm der/die/das): ")
    result = check_answer(word["de"], answer)
    if result == "richtig":
        print(f"  ✅ Richtig! {word['de']}")
        return 5
    if result == "artikel":
        print(f"  ⚠️  Sai mạo từ (Artikel)! Đúng là: {word['de']}")
        return 2
    print(f"  ❌ Falsch. Đáp án: {word['de']}")
    return 1


def ask_self_graded(word: dict) -> int:
    print(f"\n🇩🇪 {word['de']}")
    input("  (Nghĩ nghĩa tiếng Việt/Anh rồi nhấn Enter...)")
    print(f"  → {word['vi']} | {word['en']}")
    grade = ""
    while grade not in GRADE_TO_QUALITY:
        grade = input("  Tự chấm [1=Quên  2=Khó  3=Nhớ  4=Dễ]: ").strip()
    return GRADE_TO_QUALITY[grade]


def cmd_lernen(args) -> None:
    vocab = load_vocab()
    progress = load_progress()
    today = date.today()
    queue = due_cards(vocab, progress, today, args.neu)
    random.shuffle(queue)
    if not queue:
        print("🎉 Hôm nay không còn thẻ nào đến hạn. Quay lại vào ngày mai!")
        return
    print(f"📚 {len(queue)} thẻ cần ôn hôm nay. Nhấn Ctrl+C để dừng (tiến độ vẫn được lưu).")
    done = 0
    try:
        for word in queue:
            direction = args.richtung if args.richtung != "mix" else random.choice(("de", "vi"))
            quality = ask_typed(word) if direction == "vi" else ask_self_graded(word)
            if word["note"]:
                print(f"  💡 {word['note']}")
            progress[word["de"]] = sm2_update(progress.get(word["de"], new_card()), quality, today)
            save_progress(progress)
            done += 1
    except (KeyboardInterrupt, EOFError):
        print()
    print(f"\n✔ Đã ôn {done}/{len(queue)} thẻ.")


def cmd_status(_args) -> None:
    vocab = load_vocab()
    progress = load_progress()
    today = date.today()
    learned = [w for w in vocab if w["de"] in progress]
    due = [w for w in learned if date.fromisoformat(progress[w["de"]]["due"]) <= today]
    mature = [w for w in learned if progress[w["de"]]["interval"] >= 21]
    print(f"Tổng số từ     : {len(vocab)}")
    print(f"Chưa học       : {len(vocab) - len(learned)}")
    print(f"Đến hạn hôm nay: {len(due)}")
    print(f"Đã thuộc (≥21d): {len(mature)}")
    hardest = sorted(learned, key=lambda w: (-progress[w["de"]]["lapses"], progress[w["de"]]["ef"]))
    hardest = [w for w in hardest if progress[w["de"]]["lapses"] > 0][:5]
    if hardest:
        print("\n🔥 Từ hay quên nhất (nên ghi vào Fehlerlog nếu là lỗi bản chất):")
        for w in hardest:
            print(f"  - {w['de']} ({w['vi']}) — quên {progress[w['de']]['lapses']} lần")


def cmd_anki(args) -> None:
    vocab = load_vocab()
    out = Path(args.ausgabe)
    lines = ["#separator:tab", "#html:true", "#tags:Mechatronik Fachdeutsch"]
    for w in vocab:
        back = f"{w['vi']}<br><i>{w['en']}</i>"
        if w["note"]:
            back += f"<br><small>{w['note']}</small>"
        lines.append(f"{w['de']}\t{back}".replace("\n", " "))
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✔ Đã xuất {len(vocab)} thẻ -> {out}")
    print("  Anki: File > Import > chọn file này (loại thẻ 'Basic (and reversed card)').")


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Wortschatz-Trainer Mechatronik (SM-2)")
    sub = parser.add_subparsers(dest="cmd")
    p_learn = sub.add_parser("lernen", help="Ôn các thẻ đến hạn")
    p_learn.add_argument("--neu", type=int, default=10, help="Số từ mới tối đa mỗi ngày")
    p_learn.add_argument("--richtung", choices=("mix", "de", "vi"), default="mix",
                         help="de: nhìn tiếng Đức đoán nghĩa | vi: gõ tiếng Đức từ nghĩa")
    sub.add_parser("status", help="Thống kê tiến độ")
    p_anki = sub.add_parser("anki", help="Xuất file để import vào Anki")
    p_anki.add_argument("--ausgabe", default=str(HERE / "Wortschatz_Anki.txt"))
    parser.set_defaults(cmd="lernen", neu=10, richtung="mix")
    args = parser.parse_args(argv)
    {"lernen": cmd_lernen, "status": cmd_status, "anki": cmd_anki}[args.cmd](args)


if __name__ == "__main__":
    main()
