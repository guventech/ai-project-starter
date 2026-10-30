from pathlib import Path
import shutil
import tempfile
import unittest
from scripts.validate_starter import validate

ROOT = Path(__file__).resolve().parents[1]
class StarterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'starter'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '__pycache__'))

    def test_complete_starter(self):
        self.assertEqual(validate(self.root), [])

    def test_missing_required_file_detected(self):
        (self.root / 'AGENTS.md').unlink()
        self.assertIn('missing AGENTS.md', validate(self.root))

    def test_writable_reviewer_detected(self):
        path = self.root / '.cursor/agents/verifier.md'
        path.write_text(path.read_text().replace('readonly: true', 'readonly: false'))
        self.assertTrue(any('read-only' in e for e in validate(self.root)))

    def test_unscoped_rule_detected(self):
        path = self.root / '.cursor/rules/testing.mdc'
        path.write_text(path.read_text().replace('alwaysApply: false', 'alwaysApply: true'))
        self.assertTrue(any('scoped' in e for e in validate(self.root)))
