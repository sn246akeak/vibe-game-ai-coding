import tempfile
import subprocess
import sys
import unittest
from pathlib import Path

from scripts.diff_content import compare, read_rows


class ContentDiffTests(unittest.TestCase):
    def test_cli_report_is_read_only_and_never_overwrites_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            before, after, output = root / "before.csv", root / "after.csv", root / "report.json"
            before.write_text("id,cost\na,1\n", encoding="utf-8")
            after.write_text("id,cost\na,2\n", encoding="utf-8")
            original = after.read_bytes()
            command = [sys.executable, str(Path(__file__).resolve().parents[1] / "scripts/diff_content.py"),
                       str(before), str(after), "--fields", "cost", "--output", str(output)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 2)
            self.assertEqual(after.read_bytes(), original)

    def test_reorder_is_not_change_and_fields_are_bounded(self):
        old = [{"id": "a", "cost": 1, "label": "A"}, {"id": "b", "cost": 2}]
        self.assertFalse(compare(old, list(reversed(old)), "id", ["cost"])["changed"])
        new = [{"id": "a", "cost": 3, "label": "New"}, {"id": "c", "cost": 4}]
        result = compare(old, new, "id", ["cost"])
        self.assertEqual(result["changed"][0]["field"], "cost")
        self.assertEqual(result["ignored_fields"][0]["field"], "label")
        self.assertEqual(result["added"][0]["id"], "c")
        self.assertEqual(result["removed"][0]["id"], "b")

    def test_bad_ids_or_missing_fields_are_rejected(self):
        for rows in ([{"cost": 1}], [{"id": "a"}],
                     [{"id": "a", "cost": 1}, {"id": "a", "cost": 2}]):
            with self.assertRaises(ValueError):
                compare(rows, [], "id", ["cost"])

    def test_csv_bom_and_malformed_rows(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "cards.csv"
            path.write_text("id,cost\na,2\n", encoding="utf-8-sig")
            self.assertEqual(read_rows(path), [{"id": "a", "cost": "2"}])
            path.write_text("id,cost\na,2,unexpected\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                read_rows(path)
