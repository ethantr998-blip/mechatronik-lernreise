#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FEHLERLOG-WERKZEUG — Kiểm tra, ghi mới và ôn tập Nhật ký lỗi sai (Fehlerlog.md).

    python3 fehlerlog.py check [--max-tage 7] [--streng]
    python3 fehlerlog.py neu               (hỏi từng cột)
    python3 fehlerlog.py neu --fach "Kỹ thuật điện" --fehler "..." --ursache "..." --korrektur "..."
    python3 fehlerlog.py wiederholen [--anzahl 3]
"""

import argparse
import random
import re
import sys
from collections import Counter
from datetime import date, datetime
from pathlib import Path

FEHLERLOG = Path(__file__).resolve().parent / "Fehlerlog.md"
COLUMNS = ("Ngày", "Môn học / Chủ đề", "Lỗi sai cụ thể", "Bản chất vì sao sai", "Cách khắc phục chuẩn DIN")
DATE_FMT = "%d/%m/%Y"
SEPARATOR_ROW = re.compile(r"^\|\s*:?-+")


def split_row(line: str) -> list:
    inner = line.strip()[1:-1] if line.strip().endswith("|") else line.strip()[1:]
    cells = re.split(r"(?<!\\)\|", inner)
    return [c.strip() for c in cells]


def parse_entries(text: str) -> tuple:
    """Trả về (entries, errors). entries: list[dict]; errors: list[str] mô tả dòng lỗi định dạng."""
    entries, errors = [], []
    header_seen = False
    for lineno, line in enumerate(text.splitlines(), start=1):
        if not line.strip().startswith("|"):
            continue
        if not header_seen:
            header_seen = True
            continue
        if SEPARATOR_ROW.match(line.strip()):
            continue
        cells = split_row(line)
        if len(cells) != len(COLUMNS):
            errors.append(f"Dòng {lineno}: có {len(cells)} cột, cần đúng {len(COLUMNS)} cột.")
            continue
        missing = [COLUMNS[i] for i, c in enumerate(cells) if not c]
        if missing:
            errors.append(f"Dòng {lineno}: bỏ trống cột {', '.join(missing)}.")
            continue
        try:
            day = datetime.strptime(cells[0], DATE_FMT).date()
        except ValueError:
            errors.append(f"Dòng {lineno}: ngày '{cells[0]}' sai định dạng dd/mm/yyyy.")
            continue
        entries.append({"line": lineno, "date": day, "fach": cells[1], "fehler": cells[2],
                        "ursache": cells[3], "korrektur": cells[4]})
    return entries, errors


def days_since_last(entries: list, today: date):
    if not entries:
        return None
    return (today - max(e["date"] for e in entries)).days


def escape_cell(text: str) -> str:
    return " ".join(text.split()).replace("|", "\\|")


def format_row(day: date, fach: str, fehler: str, ursache: str, korrektur: str) -> str:
    cells = [day.strftime(DATE_FMT), fach, fehler, ursache, korrektur]
    return "| " + " | ".join(escape_cell(c) for c in cells) + " |"


def append_entry(path: Path, row: str) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text + row + "\n", encoding="utf-8")


def cmd_check(args) -> int:
    entries, errors = parse_entries(FEHLERLOG.read_text(encoding="utf-8"))
    for err in errors:
        print(f"❌ {err}")
    if errors:
        print("→ Sửa lại cho đủ 5 cột, không bỏ trống, ngày dạng dd/mm/yyyy.")
        return 1
    age = days_since_last(entries, date.today())
    print(f"✔ Fehlerlog hợp lệ: {len(entries)} mục.")
    if age is not None and age > args.max_tage:
        print(f"⚠️  Đã {age} ngày chưa ghi lỗi mới (ngưỡng {args.max_tage} ngày). "
              "Tuần này không sai gì, hay chưa ghi lại?")
        return 1 if args.streng else 0
    return 0


def cmd_neu(args) -> int:
    values = {}
    prompts = {"fach": COLUMNS[1], "fehler": COLUMNS[2], "ursache": COLUMNS[3], "korrektur": COLUMNS[4]}
    for key, label in prompts.items():
        value = getattr(args, key) or ""
        while not value.strip():
            value = input(f"{label}: ")
        values[key] = value
    row = format_row(date.today(), **values)
    append_entry(FEHLERLOG, row)
    print(f"✔ Đã ghi: {row}")
    return 0


def cmd_wiederholen(args) -> int:
    entries, errors = parse_entries(FEHLERLOG.read_text(encoding="utf-8"))
    if errors:
        return cmd_check(argparse.Namespace(max_tage=7, streng=False))
    if not entries:
        print("Fehlerlog đang trống.")
        return 0
    print("📊 Số lỗi theo môn (môn nhiều lỗi nhất = ưu tiên ôn):")
    for fach, n in Counter(e["fach"] for e in entries).most_common():
        print(f"  {n:>3} × {fach}")
    print(f"\n🔁 Ôn lại {min(args.anzahl, len(entries))} lỗi ngẫu nhiên — tự trả lời 'vì sao sai' trước khi xem:")
    for e in random.sample(entries, min(args.anzahl, len(entries))):
        print(f"\n[{e['date'].strftime(DATE_FMT)}] {e['fach']}: {e['fehler']}")
        input("  (Nghĩ bản chất vì sao sai, rồi nhấn Enter...)")
        print(f"  → Bản chất : {e['ursache']}")
        print(f"  → Khắc phục: {e['korrektur']}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Công cụ Fehlerlog Mechatronik")
    sub = parser.add_subparsers(dest="cmd")
    p_check = sub.add_parser("check", help="Kiểm tra định dạng & nhắc nếu lâu chưa ghi")
    p_check.add_argument("--max-tage", type=int, default=7)
    p_check.add_argument("--streng", action="store_true", help="Trả mã lỗi nếu quá hạn chưa ghi")
    p_neu = sub.add_parser("neu", help="Ghi một lỗi mới (ngày = hôm nay)")
    for key in ("fach", "fehler", "ursache", "korrektur"):
        p_neu.add_argument(f"--{key}")
    p_rev = sub.add_parser("wiederholen", help="Ôn tập lỗi cũ hàng tuần")
    p_rev.add_argument("--anzahl", type=int, default=3)
    parser.set_defaults(cmd="check", max_tage=7, streng=False)
    args = parser.parse_args(argv)
    return {"check": cmd_check, "neu": cmd_neu, "wiederholen": cmd_wiederholen}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
