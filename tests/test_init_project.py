from pathlib import Path
from contextlib import redirect_stdout
from io import StringIO
import json
import os
import shutil
import shlex
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InitProjectTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'application'
        manifest = json.loads((ROOT / 'scripts/project-manifest.json').read_text(encoding='utf-8'))
        for relative in [*manifest['files'], 'scripts/project-manifest.json']:
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / relative, path)

    def run_init(self, *args, external=False):
        source = ROOT if external else self.root
        return subprocess.run(
            [sys.executable, str(source / 'scripts/init_project.py'),
             '--destination', str(self.root), *args],
            capture_output=True, text=True, check=False)

    def snapshot(self):
        return {
            path.relative_to(self.root).as_posix(): (
                path.lstat().st_mtime_ns,
                path.read_bytes() if path.is_file() and not path.is_symlink() else None)
            for path in [self.root, *self.root.rglob('*')]
        }

    def test_preview_lists_actions_without_writes_or_caches(self):
        before = self.snapshot()
        result = self.run_init()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('RESET docs/PRD.md', result.stdout)
        self.assertIn('REMOVE publish-to-github.py', result.stdout)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(list(self.root.parent.glob('application.init-backup-*')), [])

    def assert_refuses_without_writes(self, *args):
        before = self.snapshot()
        result = self.run_init(*args)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(list(self.root.parent.glob('application.init-backup-*')), [])

    def test_apply_cleans_records_preserves_workflows_and_validates(self):
        kept = ('AGENTS.md', 'LICENSE', 'THIRD_PARTY.md', 'docs/SKILLS.md',
                '.cursor/skills/project-helper/SKILL.md')
        before = {path: (self.root / path).read_bytes() for path in kept}
        manifest = json.loads((self.root / 'scripts/project-manifest.json').read_text(encoding='utf-8'))
        originals = {path: (self.root / path).read_bytes()
                     for path in set(manifest['reset']) | set(manifest['remove'])}
        result = self.run_init('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual({path: (self.root / path).read_bytes() for path in kept}, before)
        for path in manifest['remove']:
            self.assertFalse((self.root / path).exists(), path)
        backups = list(self.root.parent.glob('application.init-backup-*'))
        self.assertEqual(len(backups), 1)
        for path, content in originals.items():
            self.assertEqual((backups[0] / path).read_bytes(), content, path)
        for path in self.root.rglob('*'):
            if path.is_file():
                text = path.read_text(encoding='utf-8')
                self.assertNotRegex(text, r'github\.com/guventech/ai-project-starter/(pull|actions/runs)/\d+')
                self.assertNotIn('starter enhancement', text.lower())
                self.assertNotRegex(text, r'(?:/home/|/Users/)[A-Za-z0-9_.-]+/')
        self.assertIn('Avoid these vague words:', (self.root / 'docs/PRD.md').read_text())
        check = subprocess.run(
            [sys.executable, str(self.root / 'scripts/validate_starter.py'), '--project'],
            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'},
            capture_output=True, text=True, check=False)
        self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
        self.assertIn('--project', (self.root / '.github/workflows/ci.yml').read_text())
        self.assertNotIn('unittest', (self.root / '.github/workflows/ci.yml').read_text())
        self.assertEqual(self.run_init('--apply', external=True).returncode, 1)

    def test_modified_missing_extra_and_cache_files_refuse(self):
        path = self.root / 'docs/PRD.md'
        original = path.read_bytes()
        path.write_bytes(original + b'\napplication work\n')
        self.assert_refuses_without_writes('--apply')
        path.unlink()
        self.assert_refuses_without_writes('--apply')
        path.write_bytes(original)
        extra = self.root / '.env'
        extra.write_text('private fixture', encoding='utf-8')
        self.assert_refuses_without_writes('--apply')
        extra.unlink()
        cache = self.root / 'scripts/__pycache__/example.pyc'
        cache.parent.mkdir()
        cache.write_bytes(b'cache')
        self.assert_refuses_without_writes('--apply')

    def test_crlf_stock_preview_preserves_exact_bytes(self):
        for path in self.root.rglob('*'):
            if path.is_file():
                text = path.read_text(encoding='utf-8')
                path.write_bytes(text.replace('\n', '\r\n').encode('utf-8'))
        before = self.snapshot()
        result = self.run_init()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.snapshot(), before)
        original = (self.root / 'docs/PRD.md').read_bytes()
        result = self.run_init('--apply')
        self.assertEqual(result.returncode, 0, result.stderr)
        backup = next(self.root.parent.glob('application.init-backup-*'))
        self.assertEqual((backup / 'docs/PRD.md').read_bytes(), original)

    def test_invalid_manifest_paths_and_duplicate_keys_refuse(self):
        path = self.root / 'scripts/project-manifest.json'
        original = path.read_text(encoding='utf-8')
        for invalid in ('../outside', '/absolute', 'C:/absolute', 'doc:stream',
                        'CON.txt', 'docs/trailing.', 'docs/space ', '.git/config',
                        'docs/../README.md', 'readme.md', '.', 'scripts/PROJECT-MANIFEST.JSON'):
            with self.subTest(path=invalid):
                data = json.loads(original)
                data['files'][invalid] = '0' * 64
                path.write_text(json.dumps(data), encoding='utf-8')
                self.assert_refuses_without_writes('--apply')
        path.write_text(original.replace('"version": 1', '"version": 1, "version": 1'), encoding='utf-8')
        self.assert_refuses_without_writes('--apply')

    def test_linked_file_refuses(self):
        target = self.root.parent / 'outside'
        target.write_text('outside untouched', encoding='utf-8')
        try:
            (self.root / 'linked').symlink_to(target)
        except OSError:
            self.skipTest('Creating symlinks is not permitted on this host')
        self.assert_refuses_without_writes('--apply')
        self.assertEqual(target.read_text(), 'outside untouched')

    def test_verified_backup_and_rollback_preserve_original_bytes(self):
        from scripts.init_project import initialize
        for failure in ('backup', 'README.md', 'publish-to-github.py'):
            with self.subTest(failure=failure):
                before = {p.relative_to(self.root).as_posix(): p.read_bytes()
                          for p in self.root.rglob('*') if p.is_file()}
                kwargs = {'fail_backup_after': 'README.md'} if failure == 'backup' else {'fail_after': failure}
                with self.assertRaises(OSError), redirect_stdout(StringIO()):
                    initialize(self.root, apply=True, **kwargs)
                after = {p.relative_to(self.root).as_posix(): p.read_bytes()
                         for p in self.root.rglob('*') if p.is_file()}
                self.assertEqual(after, before)

    def test_project_mode_retains_four_validation_invariants(self):
        self.assertEqual(self.run_init('--apply').returncode, 0)
        from scripts.validate_starter import validate
        cases = (
            ('docs/SKILLS.md', '\n<!-- drift -->\n', 'docs/SKILLS.md'),
            ('AGENTS.md', '\n## Maintaining this starter\n', 'maintainer-only'),
            ('docs/SETUP.md', '\nC:\\Users\\example\\private\n', 'personal home path'),
        )
        for relative, addition, message in cases:
            path = self.root / relative
            original = path.read_text(encoding='utf-8')
            path.write_text(original + addition, encoding='utf-8')
            try:
                self.assertTrue(any(message in error for error in validate(self.root, project=True)))
            finally:
                path.write_text(original, encoding='utf-8')
        path = self.root / '.cursor/skills/grill-me/SKILL.md'
        path.parent.mkdir()
        path.write_text('---\nname: grill-me\ndescription: Fixture\ndisable-model-invocation: true\n---\nFixture\n')
        self.assertTrue(any('colliding upstream' in error for error in validate(self.root, project=True)))

    def git(self, *args):
        if not shutil.which('git'):
            self.skipTest('Git is unavailable')
        return subprocess.run(
            ['git', '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
             '-c', 'commit.gpgsign=false', '-c', 'core.hooksPath=nonexistent-hooks',
             '-C', str(self.root), *args],
            capture_output=True, text=True, check=True)

    def init_git(self):
        self.git('init', '-b', 'main')
        self.git('add', '.')
        self.git('commit', '-m', 'Fixture')

    def test_upstream_remote_and_dirty_git_refuse(self):
        self.init_git()
        self.git('remote', 'add', 'origin', 'https://github.com/guventech/ai-project-starter.git')
        self.assert_refuses_without_writes('--apply')
        self.git('remote', 'remove', 'origin')
        self.git('remote', 'add', 'origin', 'https://github.com/example/application.git')
        self.git('remote', 'set-url', '--push', 'origin', 'git@github.com:guventech/ai-project-starter.git/')
        self.assert_refuses_without_writes('--apply')
        self.git('remote', 'remove', 'origin')
        path = self.root / 'docs/PRD.md'
        original = path.read_bytes()
        path.write_bytes(original + b'\nfixture staged change\n')
        self.git('add', 'docs/PRD.md')
        path.write_bytes(original)
        self.assert_refuses_without_writes('--apply')

    def test_linked_ancestor_refuses(self):
        alias = self.root.parent / 'alias-parent'
        try:
            alias.symlink_to(self.root.parent, target_is_directory=True)
        except OSError:
            self.skipTest('Creating symlinks is not permitted on this host')
        self.assert_refuses_without_writes('--apply', '--destination', str(alias / self.root.name))

    def test_windows_junction_refuses(self):
        if os.name != 'nt':
            self.skipTest('Windows junction fixture')
        powershell = shutil.which('pwsh') or shutil.which('powershell')
        if not powershell:
            self.skipTest('PowerShell unavailable for junction fixture')
        target = self.root.parent / 'junction-target'
        target.mkdir()
        sentinel = target / 'sentinel'
        sentinel.write_text('untouched', encoding='utf-8')
        junction = self.root / 'docs/junction'
        quote = lambda path: "'" + str(path).replace("'", "''") + "'"
        result = subprocess.run(
            [powershell, '-NoProfile', '-Command',
             f'New-Item -ItemType Junction -Path {quote(junction)} -Target {quote(target)} | Out-Null'],
            capture_output=True, text=True, check=False)
        if result.returncode:
            self.skipTest('Junction creation is unavailable on this host')
        try:
            self.assertTrue(junction.is_junction())
            self.assert_refuses_without_writes('--apply')
            self.assertEqual(sentinel.read_text(), 'untouched')
        finally:
            junction.rmdir()  # Nonrecursive removal of the fixture link only.

    def test_corrupt_backup_refuses_before_mutation(self):
        from unittest.mock import patch
        from scripts.init_project import initialize
        copy = shutil.copy2

        def corrupt(source, destination):
            copy(source, destination)
            if Path(destination).name == 'README.md':
                Path(destination).write_bytes(b'corrupted backup')

        before = self.snapshot()
        with patch('scripts.init_project.shutil.copy2', side_effect=corrupt):
            with self.assertRaisesRegex(OSError, 'Backup verification failed'), redirect_stdout(StringIO()):
                initialize(self.root, apply=True)
        self.assertEqual(self.snapshot(), before)

    def test_git_preview_does_not_run_configured_monitor(self):
        self.init_git()
        hook = self.root.parent / 'monitor.sh'
        marker = self.root.parent / 'monitor-called'
        hook.write_text('#!/bin/sh\ntouch "' + marker.as_posix() + '"\n', encoding='utf-8')
        hook.chmod(0o755)
        self.git('config', 'core.fsmonitor', hook.as_posix())
        before = self.snapshot()
        result = self.run_init()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(marker.exists())
        self.assertEqual(self.snapshot(), before)

    def test_git_preview_does_not_run_content_filters(self):
        self.init_git()
        filter_script = self.root.parent / 'content-filter.py'
        marker = self.root.parent / 'filter-called'
        filter_script.write_text(
            'from pathlib import Path\nimport sys\n'
            f'Path({str(marker)!r}).write_text("called")\n'
            'sys.stdout.buffer.write(sys.stdin.buffer.read())\n', encoding='utf-8')
        command = shlex.quote(sys.executable.replace('\\', '/')) + ' ' + shlex.quote(filter_script.as_posix())
        self.git('config', 'filter.preview.clean', command)
        (self.root / '.git/info/attributes').write_text('README.md filter=preview\n', encoding='utf-8')
        path = self.root / 'README.md'
        stamp = path.stat().st_mtime_ns + 2_000_000_000
        os.utime(path, ns=(stamp, stamp))
        before = self.snapshot()
        result = self.run_init()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(marker.exists(), 'Preview executed a configured clean filter')
        self.assertEqual(self.snapshot(), before)
