import csv
import unittest
from datetime import date

from _load import ROOT, load

wt = load("01_Deutsch/wortschatz_trainer.py", "wortschatz_trainer")
TODAY = date(2026, 9, 28)


class Sm2Test(unittest.TestCase):
    def test_intervals_grow_1_6_then_by_ef(self):
        card = wt.new_card()
        card = wt.sm2_update(card, 5, TODAY)
        self.assertEqual((card["interval"], card["due"]), (1, "2026-09-29"))
        card = wt.sm2_update(card, 5, TODAY)
        self.assertEqual(card["interval"], 6)
        self.assertEqual(card["ef"], 2.7)
        card = wt.sm2_update(card, 5, TODAY)
        self.assertEqual(card["interval"], round(6 * 2.7))

    def test_failure_resets_and_counts_lapse(self):
        card = {"ef": 2.5, "interval": 30, "reps": 5, "lapses": 0, "due": None}
        card = wt.sm2_update(card, 1, TODAY)
        self.assertEqual((card["reps"], card["interval"], card["lapses"]), (0, 1, 1))
        self.assertLess(card["ef"], 2.5)

    def test_ef_never_below_minimum(self):
        card = wt.new_card()
        for _ in range(20):
            card = wt.sm2_update(card, 0, TODAY)
        self.assertEqual(card["ef"], 1.3)


class CheckAnswerTest(unittest.TestCase):
    def test_exact_and_case_insensitive(self):
        self.assertEqual(wt.check_answer("der Widerstand", "Der Widerstand"), "richtig")

    def test_umlaut_transliteration(self):
        self.assertEqual(wt.check_answer("die Bügelmessschraube", "die Buegelmessschraube"), "richtig")
        self.assertEqual(wt.check_answer("der Maßstab", "der Massstab"), "richtig")

    def test_wrong_or_missing_article(self):
        self.assertEqual(wt.check_answer("der Widerstand", "die Widerstand"), "artikel")
        self.assertEqual(wt.check_answer("der Widerstand", "Widerstand"), "artikel")

    def test_wrong_word(self):
        self.assertEqual(wt.check_answer("der Widerstand", "der Kondensator"), "falsch")


class VocabFileTest(unittest.TestCase):
    def test_csv_is_well_formed(self):
        with open(ROOT / "01_Deutsch/Wortschatz_Fach.csv", encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))
        self.assertEqual(len(rows[0]), 4)
        terms = [r[0] for r in rows[1:]]
        self.assertEqual(len(terms), len(set(terms)), "Có từ bị trùng lặp")
        for r in rows[1:]:
            self.assertEqual(len(r), 4, r)
            self.assertTrue(all(c.strip() for c in r[:3]), r)

    def test_due_cards_limits_new_words(self):
        vocab = [{"de": f"das Wort{i}"} for i in range(5)]
        progress = {"das Wort0": {"due": "2026-09-28"}, "das Wort1": {"due": "2026-10-10"}}
        queue = wt.due_cards(vocab, progress, TODAY, new_limit=2)
        self.assertEqual([w["de"] for w in queue], ["das Wort0", "das Wort2", "das Wort3"])


if __name__ == "__main__":
    unittest.main()
