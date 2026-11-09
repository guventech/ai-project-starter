from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


from scripts.skill_inventory import WORKFLOWS

ROOT = Path(__file__).resolve().parents[1]
INSTALLER = ROOT / 'scripts/install_chat_command.py'


class InstallCommandTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.destination = self.root / 'skills/project-helper'

    def run_installer(self):
        return subprocess.run(
            [sys.executable, str(INSTALLER), '--destination', str(self.destination)],
            capture_output=True, text=True, check=False)

    def test_installs_self_contained_command_without_duplicate_skill_discovery(self):
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(self.destination.rglob('SKILL.md')),
                         [self.destination / 'SKILL.md'])
        self.assertIn('MIT License', (self.destination / 'LICENSE').read_text(encoding='utf-8'))
        expected = {f'{name}.md' for name in (*WORKFLOWS, 'architect', 'verifier')}
        references = self.destination / 'references'
        self.assertEqual({p.name for p in references.iterdir()}, expected)
        for name in WORKFLOWS:
            content = (references / f'{name}.md').read_text(encoding='utf-8')
            self.assertIn(f'name: {name}', content)
            self.assertNotIn('../', content)
            self.assertNotIn('.cursor/skills/', content)
        self.assertIn('/project-helper', result.stdout)
        self.assertFalse(list(self.destination.rglob('.env*')))

    def test_existing_destination_and_user_content_are_preserved(self):
        self.destination.mkdir(parents=True)
        marker = self.destination / 'user-notes.txt'
        marker.write_text('keep this', encoding='utf-8')
        result = self.run_installer()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('already exists', result.stderr)
        self.assertEqual(marker.read_text(encoding='utf-8'), 'keep this')
        self.assertEqual(list(self.destination.iterdir()), [marker])

    def test_second_install_does_not_replace_modified_command(self):
        self.assertEqual(self.run_installer().returncode, 0)
        command = self.destination / 'SKILL.md'
        command.write_text('user customization', encoding='utf-8')
        self.assertNotEqual(self.run_installer().returncode, 0)
        self.assertEqual(command.read_text(encoding='utf-8'), 'user customization')

    def test_symlink_destination_is_rejected(self):
        target = self.root / 'unrelated'
        target.mkdir()
        self.destination.parent.mkdir()
        try:
            self.destination.symlink_to(target, target_is_directory=True)
        except OSError:
            self.skipTest('Creating symlinks is not permitted on this host')
        result = self.run_installer()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(target.iterdir()), [])
