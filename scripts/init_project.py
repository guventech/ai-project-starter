"""Preview initialization of a stock template copy; use --apply to replace its records."""
import sys
sys.dont_write_bytecode = True  # Preview must not create a local import cache.

import argparse
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tempfile

try:
    from project_manifest import MANIFEST, read_manifest, text_digest, valid_path
except ImportError:
    from scripts.project_manifest import MANIFEST, read_manifest, text_digest, valid_path

ROOT = Path(__file__).resolve().parents[1]


def linked(path):
    return path.is_symlink() or path.is_junction()


def checked_path(root, relative):
    path = root / valid_path(relative)
    for parent in (path, *path.parents):
        if linked(parent):
            raise ValueError('Linked path; use an isolated stock copy')
        if parent == root:
            break
    if not path.resolve().is_relative_to(root):
        raise ValueError('Path leaves the project')
    return path


def git_preflight(root):
    if not (root / '.git').exists():
        return
    args = ['git', '--no-optional-locks', '-c', 'core.fsmonitor=false',
            '-c', 'core.untrackedCache=false', '-C', str(root)]
    version = subprocess.run(args + ['--version'], capture_output=True, text=True, check=True)
    match = re.search(r'git version (\d+)\.(\d+)', version.stdout)
    if not match or tuple(map(int, match.groups())) < (2, 36):
        raise ValueError('Git 2.36+ is required for a Git-backed copy')
    remotes = subprocess.run(args + ['config', '--get-regexp', r'^remote\..*\.(url|pushurl)$'],
                             capture_output=True, text=True, check=False)
    if remotes.returncode not in (0, 1):
        raise ValueError('Cannot inspect repository remotes')
    if re.search(r'(?i)[/:]guventech/ai-project-starter(?:\.git)?/*\s*$', remotes.stdout, re.MULTILINE):
        raise ValueError('Refusing the upstream repository; initialize a template copy')
    partial = subprocess.run(args + ['config', '--get-regexp',
                                    r'^(extensions\.partialclone|remote\..*\.promisor)$'],
                             capture_output=True, text=True, check=False)
    if partial.returncode != 1:
        raise ValueError('Partial-clone/promisor configuration is unsupported')
    # Worktree content was already checked against the stock manifest. Status
    # would re-read it through configured clean/process filters, so inspect only
    # index/HEAD metadata here and disable external diff/text conversion.
    staged = subprocess.run(args + ['diff-index', '--cached', '--quiet', '--no-ext-diff',
                                    '--no-textconv', '--ignore-submodules=all', 'HEAD', '--'],
                            capture_output=True, text=True, check=False)
    if staged.returncode != 0:
        raise ValueError('Git worktree must be clean before initialization')
    index = subprocess.run(args + ['ls-files', '--stage', '-z'],
                           capture_output=True, text=True, check=True)
    filemode = subprocess.run(args + ['config', '--bool', '--get', 'core.filemode'],
                              capture_output=True, text=True, check=False)
    if filemode.returncode not in (0, 1):
        raise ValueError('Cannot inspect Git file-mode policy')
    check_mode = filemode.returncode == 1 or filemode.stdout.strip() == 'true'
    paths = set()
    for entry in index.stdout.split('\0'):
        if not entry:
            continue
        metadata, relative = entry.split('\t', 1)
        mode, _, stage = metadata.split()
        path = checked_path(root, relative)
        if stage != '0' or mode not in ('100644', '100755'):
            raise ValueError('Unsupported or unmerged Git entry')
        if check_mode and bool(path.stat().st_mode & stat.S_IXUSR) != (mode == '100755'):
            raise ValueError('Git file mode differs from the index')
        paths.add(relative)
    if paths != set(read_manifest(root)['files']) | {MANIFEST}:
        raise ValueError('Git index must contain exactly the stock files')


def preflight(destination):
    lexical = Path(destination).expanduser().absolute()
    if any(linked(path) for path in (lexical, *lexical.parents)):
        raise ValueError('Linked project root or ancestor')
    root = lexical.resolve(strict=True)
    checked_path(root, MANIFEST)
    manifest = read_manifest(root)
    if root != ROOT and manifest != read_manifest(ROOT):
        raise ValueError('Destination manifest differs from this initializer')
    actual = set()
    pending = [root]
    while pending:
        for path in pending.pop().iterdir():
            if linked(path):
                raise ValueError('Linked entry in project')
            if path == root / '.git':
                continue
            if path.is_dir():
                pending.append(path)
            elif path.is_file():
                actual.add(path.relative_to(root).as_posix())
            else:
                raise ValueError('Unsupported project entry')
    if actual != set(manifest['files']) | {MANIFEST}:
        raise ValueError('Missing or extra files; use a fresh stock copy (no bytecode caches)')
    for relative, digest in manifest['files'].items():
        if text_digest(checked_path(root, relative)) != digest:
            raise ValueError(f'Modified stock file: {relative}')
    git_preflight(root)
    replacements = {path: checked_path(root, source).read_bytes()
                    for path, source in manifest['reset'].items()}
    originals = {path: checked_path(root, path).read_bytes()
                 for path in set(replacements) | set(manifest['remove'])}
    return root, manifest, replacements, originals


def atomic_write(path, content):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix='.init-', delete=False) as output:
            temporary = Path(output.name)
            output.write(content)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def initialize(destination, apply=False, fail_after=None, fail_backup_after=None):
    root, manifest, replacements, originals = preflight(destination)
    for relative in sorted(replacements):
        print(f'RESET {relative}')
    for relative in manifest['remove']:
        print(f'REMOVE {relative}')
    if not apply:
        print('Preview only. Use --apply in a fresh copy to perform this plan.')
        return None
    backup = Path(tempfile.mkdtemp(prefix=f'{root.name}.init-backup-', dir=root.parent)).resolve()
    if backup.parent != root.parent or not backup.name.startswith(f'{root.name}.init-backup-'):
        raise ValueError('Unexpected backup boundary')
    print(f'Recovery backup: {backup}', flush=True)
    for relative, content in originals.items():
        destination_path = checked_path(backup, relative)
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(checked_path(root, relative), destination_path)
        if fail_backup_after == relative:
            raise OSError('injected backup failure; project unchanged')
    if any(checked_path(backup, path).read_bytes() != content for path, content in originals.items()):
        raise OSError('Backup verification failed; project unchanged')
    try:
        for relative, content in replacements.items():
            atomic_write(checked_path(root, relative), content)
            if fail_after == relative:
                raise OSError('injected replacement failure')
        for relative in manifest['remove']:
            checked_path(root, relative).unlink()
            if fail_after == relative:
                raise OSError('injected removal failure')
    except OSError as exc:
        try:
            for relative in originals:
                shutil.copy2(checked_path(backup, relative), checked_path(root, relative))
        except OSError as recovery:
            raise OSError(f'Apply and rollback failed; inspect recovery backup: {backup}') from recovery
        raise OSError(f'Apply failed; originals restored; backup retained: {backup}') from exc
    print('Project records initialized. Configure application requirements and checks before building.')
    return backup


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path, default=ROOT)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    try:
        initialize(args.destination, args.apply)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f'Initialization stopped: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
