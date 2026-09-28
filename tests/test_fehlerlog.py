import unittest
from datetime import date

from _load import ROOT, load

fl = load("00_DIHK/fehlerlog.py", "fehlerlog")

HEADER = "| Ngày | Môn | Lỗi | Vì sao | Khắc phục |\n| :--- | :--- | :--- | :--- | :--- |\n"


class ParseTest(unittest.TestCase):
    def test_repository_fehlerlog_is_valid(self):
        _, errors = fl.parse_entries((ROOT / "00_DIHK/Fehlerlog.md").read_text(encoding="utf-8"))
        self.assertEqual(errors, [])

    def test_valid_row(self):
        entries, errors = fl.parse_entries(HEADER + "| 01/10/2026 | Điện | a | b | c |\n")
        self.assertEqual(errors, [])
        self.assertEqual(entries[0]["date"], date(2026, 10, 1))

    def test_empty_cell_and_bad_date(self):
        _, errors = fl.parse_entries(HEADER + "| 01/10/2026 | Điện |  | b | c |\n| 2026-10-01 | x | a | b | c |\n")
        self.assertEqual(len(errors), 2)
        self.assertIn("bỏ trống", errors[0])
        self.assertIn("dd/mm/yyyy", errors[1])

    def test_wrong_column_count(self):
        _, errors = fl.parse_entries(HEADER + "| 01/10/2026 | a | b |\n")
        self.assertIn("cột", errors[0])

    def test_format_row_escapes_pipe_and_roundtrips(self):
        row = fl.format_row(date(2026, 10, 1), "Điện", "A | B", "x\ny", "z")
        entries, errors = fl.parse_entries(HEADER + row + "\n")
        self.assertEqual(errors, [])
        self.assertEqual(entries[0]["fehler"], "A \\| B")
        self.assertEqual(entries[0]["ursache"], "x y")

    def test_days_since_last(self):
        entries, _ = fl.parse_entries(HEADER + "| 20/09/2026 | a | b | c | d |\n| 25/09/2026 | a | b | c | d |\n")
        self.assertEqual(fl.days_since_last(entries, date(2026, 9, 28)), 3)
        self.assertIsNone(fl.days_since_last([], date(2026, 9, 28)))


if __name__ == "__main__":
    unittest.main()
