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

    def test_each_required_skill_removal_detected(self):
        from scripts.skill_inventory import REQUIRED_SKILLS
        for name in sorted(REQUIRED_SKILLS):
            with self.subTest(skill=name):
                path = self.root / '.cursor/skills' / name / 'SKILL.md'
                content = path.read_bytes()
                path.unlink()
                try:
                    self.assertIn(f'missing .cursor/skills/{name}', validate(self.root))
                finally:
                    path.write_bytes(content)

    def test_writable_reviewer_detected(self):
        path = self.root / '.cursor/agents/verifier.md'
        path.write_text(path.read_text().replace('readonly: true', 'readonly: false'))
        self.assertTrue(any('read-only' in e for e in validate(self.root)))

    def test_unscoped_rule_detected(self):
        path = self.root / '.cursor/rules/testing.mdc'
        path.write_text(path.read_text().replace('alwaysApply: false', 'alwaysApply: true'))
        self.assertTrue(any('scoped' in e for e in validate(self.root)))

    def test_skill_inventory_sources_agree(self):
        from scripts.skill_inventory import REQUIRED_SKILLS, WORKFLOWS
        from scripts import install_chat_command, validate_starter

        self.assertEqual(set(WORKFLOWS) | {'project-helper'}, set(REQUIRED_SKILLS))
        self.assertEqual(install_chat_command.WORKFLOWS, WORKFLOWS)
        self.assertEqual(validate_starter.REQUIRED_SKILLS, set(REQUIRED_SKILLS))
        configuration = (ROOT / 'docs/CONFIGURATION.md').read_text(encoding='utf-8')
        readme = (ROOT / 'README.md').read_text(encoding='utf-8')
        for name in REQUIRED_SKILLS:
            self.assertIn(name, configuration, f'{name} missing from CONFIGURATION.md')
            self.assertIn(name, readme, f'{name} missing from README.md')
