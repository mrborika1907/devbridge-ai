import tempfile
import unittest
from pathlib import Path
from devbridge_ai.analyzer import analyze_source, analyze_path
from devbridge_ai.cli import main
from devbridge_ai.ai import review_with_ai

class AnalyzerTests(unittest.TestCase):
    def test_syntax_error(self):
        self.assertEqual(analyze_source("def broken(:")[0].code, "SYNTAX")

    def test_checks(self):
        codes = {f.code for f in analyze_source("def f():\n try:\n  eval('1')\n except:\n  pass\n")}
        self.assertEqual(codes, {"DOCSTRING", "BARE_EXCEPT", "EVAL"})

    def test_clean(self):
        self.assertEqual(analyze_source('def hello():\n    """Say hello."""\n    return 1\n'), [])

    def test_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "bad.py").write_text("eval('1')")
            (root / "notes.txt").write_text("ignored")
            self.assertEqual([f.code for f in analyze_path(root)], ["EVAL"])

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as temp:
            file = Path(temp) / "ok.py"
            file.write_text("x = 1\n")
            self.assertEqual(main(["check", str(file)]), 0)
            file.write_text("eval('1')\n")
            self.assertEqual(main(["check", str(file), "--json"]), 1)

    def test_ai_endpoint_validation(self):
        with self.assertRaises(ValueError):
            review_with_ai("x=1", model="test", endpoint="http://example.com/v1/chat/completions")

if __name__ == "__main__":
    unittest.main()
