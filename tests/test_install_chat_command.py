from pathlib import Path
import json
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

    def run_installer(self, *extra_args):
        return subprocess.run(
            [sys.executable, str(INSTALLER), '--destination', str(self.destination), *extra_args],
            capture_output=True, text=True, check=False)

    def test_installs_self_contained_command_without_duplicate_skill_discovery(self):
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(self.destination.rglob('SKILL.md')),
                         [self.destination / 'SKILL.md'])
        self.assertIn('MIT License', (self.destination / 'LICENSE').read_text(encoding='utf-8'))
        self.assertTrue((self.destination / 'THIRD_PARTY.md').is_file())
        self.assertIn('Third-party notices', (self.destination / 'THIRD_PARTY.md').read_text(encoding='utf-8'))
        from scripts.install_chat_command import package_version
        version = package_version()
        self.assertEqual((self.destination / 'VERSION').read_text(encoding='utf-8'), version + '\n')
        self.assertIn(f'Package version: {version}', result.stdout)
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
        manifest = json.loads((self.destination / '.installer-manifest.json').read_text(encoding='utf-8'))
        self.assertIn('SKILL.md', manifest['files'])
        self.assertIn('THIRD_PARTY.md', manifest['files'])
        self.assertIn('VERSION', manifest['files'])
        self.assertIn('references/prior-art.md', manifest['files'])
        # This procedure has no internal paths to rewrite. Its complete text,
        # including query hygiene, must reach the installed snapshot unchanged.
        prior_art = (ROOT / '.cursor/skills/prior-art/SKILL.md').read_text(encoding='utf-8')
        self.assertEqual((references / 'prior-art.md').read_text(encoding='utf-8'), prior_art)
        from scripts.install_chat_command import digest_text
        self.assertEqual(manifest['files']['references/prior-art.md'], digest_text(prior_art))

    def test_upgrade_replaces_clean_stock_package(self):
        self.assertEqual(self.run_installer().returncode, 0)
        from scripts import install_chat_command as installer
        skill = self.destination / 'SKILL.md'
        expected = installer.planned_files()['SKILL.md']
        skill.write_text(expected + '\n# stale marker\n', encoding='utf-8')
        installer.write_manifest(self.destination, installer.installed_content_digests(self.destination))
        result = self.run_installer('--upgrade')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(skill.read_text(encoding='utf-8'), expected)
        self.assertNotIn('# stale marker', skill.read_text(encoding='utf-8'))

    def check_without_writes(self, expected_code, expected_message, *extra_args):
        def snapshot():
            return {
                path.relative_to(self.root).as_posix(): (
                    path.lstat().st_mtime_ns,
                    path.read_bytes() if path.is_file() and not path.is_symlink() else None,
                )
                for path in [self.root, *self.root.rglob('*')]
            }
        before = snapshot()
        result = self.run_installer('--check', *extra_args)
        self.assertEqual(snapshot(), before, 'check modified the installation or its parent')
        self.assertEqual(result.returncode, expected_code, result.stdout + result.stderr)
        self.assertIn(expected_message, result.stdout + result.stderr)

    def test_check_reports_current_package_without_writes(self):
        self.assertEqual(self.run_installer().returncode, 0)
        self.check_without_writes(0, 'up to date')

    def test_check_reports_changed_missing_extra_and_obsolete_files(self):
        self.assertEqual(self.run_installer().returncode, 0)
        (self.destination / 'SKILL.md').write_text('edited', encoding='utf-8')
        (self.destination / 'LICENSE').unlink()
        (self.destination / 'notes.txt').write_text('keep', encoding='utf-8')
        (self.destination / 'references/grill-me.md').write_text('old', encoding='utf-8')
        self.check_without_writes(1, '4 files differ')

    def test_check_reports_old_stock_snapshot_as_drift(self):
        self.assertEqual(self.run_installer().returncode, 0)
        from scripts import install_chat_command as installer
        (self.destination / 'SKILL.md').write_text('old stock', encoding='utf-8')
        installer.write_manifest(self.destination, installer.installed_content_digests(self.destination))
        self.check_without_writes(1, '1 files differ')

    def test_check_reports_absent_installation_without_creating_it(self):
        self.check_without_writes(1, 'not installed')

    def test_check_reports_missing_manifest_without_writes(self):
        self.assertEqual(self.run_installer().returncode, 0)
        (self.destination / '.installer-manifest.json').unlink()
        self.check_without_writes(1, 'manifest missing')

    def test_check_rejects_invalid_manifests_without_writes(self):
        self.assertEqual(self.run_installer().returncode, 0)
        path = self.destination / '.installer-manifest.json'
        original = json.loads(path.read_text(encoding='utf-8'))
        invalid = [
            '{', 'null', '[]', '{"files": []}',
            json.dumps({'files': {}}),
            json.dumps({'files': {**original['files'], 'SKILL.md': 'invalid'}}),
            json.dumps({'files': {**original['files'], '../../outside': 'a' * 64}}),
        ]
        for content in invalid:
            with self.subTest(content=content):
                path.write_text(content, encoding='utf-8')
                self.check_without_writes(2, 'manifest invalid')

    def test_check_detects_manifest_digest_drift(self):
        self.assertEqual(self.run_installer().returncode, 0)
        path = self.destination / '.installer-manifest.json'
        manifest = json.loads(path.read_text(encoding='utf-8'))
        manifest['files']['SKILL.md'] = '0' * 64
        path.write_text(json.dumps(manifest), encoding='utf-8')
        self.check_without_writes(1, '1 files differ')

    def test_check_rejects_upgrade_flags_without_writes(self):
        for flags in [('--upgrade',), ('--force',), ('--upgrade', '--force')]:
            with self.subTest(flags=flags):
                self.check_without_writes(2, '--check cannot be combined', *flags)

    def test_version_reports_source_version_without_writes(self):
        from scripts.install_chat_command import package_version

        def snapshot():
            return {
                path.relative_to(self.root).as_posix(): (
                    path.lstat().st_mtime_ns,
                    path.read_bytes() if path.is_file() and not path.is_symlink() else None,
                )
                for path in [self.root, *self.root.rglob('*')]
            }

        before = snapshot()
        result = self.run_installer('--version')
        self.assertEqual(snapshot(), before, 'version modified the destination parent')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), package_version())
        self.assertFalse(self.destination.exists())

    def test_version_rejects_mutating_or_check_flags(self):
        for flags in [('--upgrade',), ('--force',), ('--check',), ('--upgrade', '--force')]:
            with self.subTest(flags=flags):
                result = self.run_installer('--version', *flags)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertIn('--version cannot be combined', result.stderr)
                self.assertFalse(self.destination.exists())

    def test_check_reports_invalid_destination_and_unreadable_content(self):
        self.destination.parent.mkdir(parents=True)
        self.destination.write_text('not a directory', encoding='utf-8')
        self.check_without_writes(2, 'not a directory')
        self.destination.unlink()
        self.assertEqual(self.run_installer().returncode, 0)
        (self.destination / 'SKILL.md').write_bytes(b'\xff')
        self.check_without_writes(2, 'Check stopped:')

    def test_check_rejects_linked_entries(self):
        self.assertEqual(self.run_installer().returncode, 0)
        target = self.root / 'outside.txt'
        target.write_text('outside', encoding='utf-8')
        link = self.destination / 'linked.txt'
        try:
            link.symlink_to(target)
        except OSError:
            self.skipTest('Creating symlinks is not permitted on this host')
        self.check_without_writes(2, 'linked entry')

    def test_check_rejects_symlink_destination(self):
        self.destination.parent.mkdir(parents=True)
        target = self.root / 'absent-target'
        try:
            self.destination.symlink_to(target, target_is_directory=True)
        except OSError:
            self.skipTest('Creating symlinks is not permitted on this host')
        self.check_without_writes(2, 'linked destination')

    def test_upgrade_refuses_extra_files(self):
        self.assertEqual(self.run_installer().returncode, 0)
        (self.destination / 'user-notes.txt').write_text('keep', encoding='utf-8')
        result = self.run_installer('--upgrade')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('extra files', result.stderr.lower())
        self.assertEqual((self.destination / 'user-notes.txt').read_text(encoding='utf-8'), 'keep')

    def test_upgrade_refuses_customized_managed_file(self):
        self.assertEqual(self.run_installer().returncode, 0)
        skill = self.destination / 'SKILL.md'
        skill.write_text('user customization', encoding='utf-8')
        result = self.run_installer('--upgrade')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('customized', result.stderr.lower())
        self.assertEqual(skill.read_text(encoding='utf-8'), 'user customization')

    def test_upgrade_refuses_missing_manifest(self):
        self.assertEqual(self.run_installer().returncode, 0)
        (self.destination / '.installer-manifest.json').unlink()
        result = self.run_installer('--upgrade')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('manifest', result.stderr.lower())
        self.assertIn('--force', result.stderr)

    def test_upgrade_refuses_incomplete_manifest(self):
        self.assertEqual(self.run_installer().returncode, 0)
        from scripts import install_chat_command as installer
        skill = self.destination / 'SKILL.md'
        original = skill.read_text(encoding='utf-8')
        skill.write_text(original + '\n# customized outside incomplete manifest\n', encoding='utf-8')
        digests = installer.installed_content_digests(self.destination)
        digests.pop('SKILL.md')
        installer.write_manifest(self.destination, digests)
        result = self.run_installer('--upgrade')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('incomplete', result.stderr.lower())
        self.assertIn('# customized outside incomplete manifest', skill.read_text(encoding='utf-8'))

    def test_upgrade_refuses_malformed_manifest_digest(self):
        self.assertEqual(self.run_installer().returncode, 0)
        from scripts import install_chat_command as installer
        digests = installer.installed_content_digests(self.destination)
        digests['SKILL.md'] = 'not-a-sha256'
        installer.write_manifest(self.destination, digests)
        skill = self.destination / 'SKILL.md'
        original = skill.read_text(encoding='utf-8')
        result = self.run_installer('--upgrade')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('digest', result.stderr.lower())
        self.assertEqual(skill.read_text(encoding='utf-8'), original)

    def test_upgrade_force_backs_up_and_overwrites_customization(self):
        self.assertEqual(self.run_installer().returncode, 0)
        from scripts import install_chat_command as installer
        skill = self.destination / 'SKILL.md'
        expected = installer.planned_files()['SKILL.md']
        skill.write_text('user customization', encoding='utf-8')
        result = self.run_installer('--upgrade', '--force')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(skill.read_text(encoding='utf-8'), expected)
        backups = list(self.destination.parent.glob('project-helper.bak-*'))
        self.assertEqual(len(backups), 1)
        self.assertEqual((backups[0] / 'SKILL.md').read_text(encoding='utf-8'), 'user customization')

    def test_upgrade_force_removes_obsolete_renamed_references(self):
        self.assertEqual(self.run_installer().returncode, 0)
        obsolete = self.destination / 'references/grill-me.md'
        obsolete.write_text('obsolete snapshot', encoding='utf-8', newline='\n')
        result = self.run_installer('--upgrade', '--force')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(obsolete.exists())
        self.assertTrue((self.destination / 'references/decision-interview.md').is_file())

    def test_upgrade_force_still_refuses_extra_files(self):
        self.assertEqual(self.run_installer().returncode, 0)
        (self.destination / 'user-notes.txt').write_text('keep', encoding='utf-8')
        result = self.run_installer('--upgrade', '--force')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('extra files', result.stderr.lower())
        self.assertEqual((self.destination / 'user-notes.txt').read_text(encoding='utf-8'), 'keep')

    def test_force_without_upgrade_is_rejected(self):
        result = self.run_installer('--force')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('--upgrade', result.stderr)

    def test_existing_destination_and_user_content_are_preserved(self):
        self.destination.mkdir(parents=True)
        marker = self.destination / 'user-notes.txt'
        marker.write_text('keep this', encoding='utf-8')
        result = self.run_installer()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('already exists', result.stderr)
        self.assertEqual(marker.read_text(encoding='utf-8'), 'keep this')
        self.assertEqual(list(self.destination.iterdir()), [marker])

    def test_fresh_install_promotes_complete_package(self):
        from scripts import install_chat_command as installer
        destination, backup, replaced = installer.install(self.destination)
        self.assertTrue(destination.samefile(self.destination))
        self.assertIsNone(backup)
        self.assertFalse(replaced)
        planned = installer.planned_files()
        relatives = installer.package_file_relatives(self.destination)
        self.assertEqual(relatives, set(installer.managed_relative_paths(planned)))
        manifest = installer.read_manifest(self.destination)
        self.assertEqual(set(manifest), set(planned))
        for relative, content in planned.items():
            self.assertEqual(manifest[relative], installer.digest_text(content))
            self.assertEqual(
                (self.destination / relative).read_text(encoding='utf-8'), content)
        self.assertFalse(list(self.destination.parent.glob('project-helper.staging-*')))

    def test_fresh_install_write_failure_leaves_no_destination_or_staging(self):
        from scripts import install_chat_command as installer
        with self.assertRaises(OSError):
            installer.install(self.destination, fail_after='SKILL.md')
        self.assertFalse(self.destination.exists())
        self.assertFalse(list(self.destination.parent.glob('project-helper.staging-*')))

    def test_fresh_install_manifest_failure_leaves_no_destination_or_staging(self):
        from scripts import install_chat_command as installer
        with self.assertRaises(OSError):
            installer.install(self.destination, fail_after=installer.MANIFEST_NAME)
        self.assertFalse(self.destination.exists())
        self.assertFalse(list(self.destination.parent.glob('project-helper.staging-*')))

    def test_upgrade_absent_destination_installs_transactionally(self):
        from scripts import install_chat_command as installer
        destination, backup, replaced = installer.install(self.destination, upgrade=True)
        self.assertTrue(destination.samefile(self.destination))
        self.assertIsNone(backup)
        self.assertFalse(replaced)
        self.assertTrue((self.destination / 'SKILL.md').is_file())
        self.assertFalse(list(self.destination.parent.glob('project-helper.staging-*')))

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

    def test_upgrade_refuses_symlink_destination(self):
        target = self.root / 'unrelated'
        target.mkdir()
        self.destination.parent.mkdir()
        try:
            self.destination.symlink_to(target, target_is_directory=True)
        except OSError:
            self.skipTest('Creating symlinks is not permitted on this host')
        result = self.run_installer('--upgrade')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(target.iterdir()), [])
