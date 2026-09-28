import io
import tempfile
import unicodedata
import unittest
from pathlib import Path
from unittest import mock

from _load import load

ac = load("agent_classifier.py", "agent_classifier")


class ClassifyTest(unittest.TestCase):
    def test_real_handout_names(self):
        self.assertEqual(ac.classify_document("BAI TAP DTCB.docx", "")[0], "Điện tử cơ bản")
        self.assertEqual(ac.classify_document("bia kts.docx", "")[0], "Kỹ thuật số")

    def test_underscore_filenames(self):
        self.assertEqual(ac.classify_document("bai_tap_dtcb.docx", "")[0], "Điện tử cơ bản")

    def test_nfd_filename_from_macos(self):
        nfd = unicodedata.normalize("NFD", "Bài tập Kỹ thuật điện.pdf")
        self.assertEqual(ac.classify_document(nfd, "")[0], "Kỹ thuật điện")

    def test_content_keywords(self):
        content = "Áp dụng định luật Ohm và định luật Kirchhoff để tính dòng điện trong mạch điện."
        folder, de, score = ac.classify_document("scan_001.pdf", content)
        self.assertEqual((folder, de), ("Kỹ thuật điện", "Elektrotechnik"))
        self.assertGreaterEqual(score, 4)

    def test_whole_word_matching(self):
        # "hàn" (welding) must not match inside "thực hành" (practice)
        self.assertEqual(ac.score_subjects("x.txt", "buổi thực hành")["Cơ khí cơ bản"], 0)
        # "led" must not match "called"/"controlled"
        self.assertEqual(ac.score_subjects("x.txt", "this is called controlled")["Điện tử cơ bản"], 0)
        self.assertGreater(ac.score_subjects("x.txt", "đèn led đỏ")["Điện tử cơ bản"], 0)

    def test_unknown_document(self):
        self.assertEqual(ac.classify_document("IMG_2024.jpg", ""), (None, "", 0))


class SafetyTest(unittest.TestCase):
    def test_notification_does_not_embed_text_in_script(self):
        evil = 'x" & do shell script "touch /tmp/pwned" & "'
        with mock.patch.object(ac.subprocess, "run") as run:
            ac.send_macos_notification("Zalo Study Agent", evil)
        argv = run.call_args[0][0]
        scripts = [argv[i + 1] for i, a in enumerate(argv) if a == "-e"]
        self.assertTrue(all(evil not in s for s in scripts))
        self.assertEqual(argv[-1], evil)

    def test_pdf_path_passed_as_argument(self):
        with mock.patch.object(ac.subprocess, "run") as run:
            run.return_value.stdout = ""
            ac.extract_text_from_pdf(Path('/tmp/a"b.pdf'))
        argv = run.call_args[0][0]
        self.assertNotIn('a"b', argv[argv.index("-e") + 1])
        self.assertTrue(argv[-1].endswith('a"b.pdf'))


class ProcessFileTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.workspace = Path(self.tmp.name)
        self.buffer = self.workspace / "_Zalo_Raw"
        self.buffer.mkdir()
        patches = [
            mock.patch.object(ac, "WORKSPACE_DIR", self.workspace),
            mock.patch.object(ac, "BUFFER_DIR", self.buffer),
            mock.patch.object(ac, "send_macos_notification"),
            mock.patch.object(ac.time, "sleep"),
            mock.patch("sys.stdout", new_callable=io.StringIO),
        ]
        for p in patches:
            p.start()
            self.addCleanup(p.stop)
        self.addCleanup(self.tmp.cleanup)

    def test_moves_classified_file(self):
        src = self.buffer / "on_tap.txt"
        src.write_text("Bảng chân lý của cổng logic và flip-flop", encoding="utf-8")
        ac.process_file(src)
        self.assertFalse(src.exists())
        self.assertTrue((self.workspace / "Kỹ thuật số" / "on_tap.txt").exists())

    def test_does_not_overwrite_existing_file(self):
        target = self.workspace / "Kỹ thuật số"
        target.mkdir()
        (target / "on_tap.txt").write_text("cũ", encoding="utf-8")
        src = self.buffer / "on_tap.txt"
        src.write_text("cổng logic, flip-flop", encoding="utf-8")
        ac.process_file(src)
        self.assertEqual((target / "on_tap.txt").read_text(encoding="utf-8"), "cũ")
        self.assertEqual(len(list(target.iterdir())), 2)

    def test_keeps_unclassified_file_in_buffer(self):
        src = self.buffer / "anh_chup.txt"
        src.write_text("không liên quan", encoding="utf-8")
        ac.process_file(src)
        self.assertTrue(src.exists())


if __name__ == "__main__":
    unittest.main()
