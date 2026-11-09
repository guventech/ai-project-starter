"""Read-only changelog/VERSION consistency checks."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import changelog_release

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/changelog_release.py'


class ChangelogReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'VERSION').write_text('0.1.0\n', encoding='utf-8', newline='\n')
        (self.root / 'CHANGELOG.md').write_text(
            '# Changelog\n\n## [0.1.0] - 2026-11-09\n\n### Added\n\n- Example note.\n',
            encoding='utf-8', newline='\n')

    def run_script(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), '--root', str(self.root), *args],
            capture_output=True, text=True, check=False)

    def snapshot(self):
        return {
            path.relative_to(self.root).as_posix(): (
                path.lstat().st_mtime_ns,
                path.read_bytes() if path.is_file() else None,
            )
            for path in [self.root, *self.root.rglob('*')]
        }

    def test_check_and_notes_succeed_without_writes(self):
        before = self.snapshot()
        check = self.run_script('--check')
        notes = self.run_script()
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(check.returncode, 0, check.stderr)
        self.assertIn('matches VERSION 0.1.0', check.stdout)
        self.assertEqual(notes.returncode, 0, notes.stderr)
        self.assertIn('## [0.1.0] - 2026-11-09', notes.stdout)
        self.assertIn('- Example note.', notes.stdout)

    def test_missing_section_fails(self):
        (self.root / 'VERSION').write_text('9.9.9\n', encoding='utf-8', newline='\n')
        before = self.snapshot()
        result = self.run_script('--check')
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('no release section for VERSION 9.9.9', result.stderr)

    def test_duplicate_section_fails(self):
        (self.root / 'CHANGELOG.md').write_text(
            '## [0.1.0] - 2026-11-09\n\n- one\n\n## [0.1.0] - 2026-11-10\n\n- two\n',
            encoding='utf-8', newline='\n')
        result = self.run_script('--check')
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('duplicate release sections for 0.1.0', result.stderr)

    def test_malformed_heading_fails(self):
        (self.root / 'CHANGELOG.md').write_text(
            '## [0.1.0 extra] - 2026-11-09\n\n- bad\n',
            encoding='utf-8', newline='\n')
        result = self.run_script('--check')
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('Malformed changelog version heading', result.stderr)

    def test_validate_helper_skips_when_files_absent(self):
        empty = Path(self.temp.name) / 'empty'
        empty.mkdir()
        self.assertEqual(changelog_release.validate_changelog(empty), [])

    def test_repository_changelog_matches_version(self):
        self.assertEqual(changelog_release.validate_changelog(ROOT), [])
        result = subprocess.run(
            [sys.executable, str(SCRIPT), '--check'],
            cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
