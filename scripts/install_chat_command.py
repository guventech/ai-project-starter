"""Install the project-helper command for Cursor without third-party packages."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import secrets
import shutil
import sys

try:
    from skill_inventory import OBSOLETE_REFERENCE_PATHS, WORKFLOWS
except ImportError:  # pragma: no cover - package import when run via tests
    from scripts.skill_inventory import OBSOLETE_REFERENCE_PATHS, WORKFLOWS


ROOT = Path(__file__).resolve().parents[1]
REVIEWERS = ('architect', 'verifier')
MANIFEST_NAME = '.installer-manifest.json'


def reference_text(path):
    text = path.read_text(encoding='utf-8')
    for name in WORKFLOWS:
        text = text.replace(f'../{name}/SKILL.md', f'{name}.md')
        text = text.replace(f'.cursor/skills/{name}/SKILL.md', f'{name}.md')
    return text


def digest_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def is_sha256_digest(value):
    return isinstance(value, str) and len(value) == 64 and all(
        character in '0123456789abcdefABCDEF' for character in value)


def planned_files():
    files = {'SKILL.md': (ROOT / '.cursor/skills/project-helper/SKILL.md').read_text(encoding='utf-8'),
             'LICENSE': (ROOT / 'LICENSE').read_text(encoding='utf-8'),
             'THIRD_PARTY.md': (ROOT / 'THIRD_PARTY.md').read_text(encoding='utf-8')}
    for name in WORKFLOWS:
        files[f'references/{name}.md'] = reference_text(ROOT / '.cursor/skills' / name / 'SKILL.md')
    for name in REVIEWERS:
        files[f'references/{name}.md'] = reference_text(ROOT / '.cursor/agents' / f'{name}.md')
    return files


def managed_relative_paths(files=None):
    files = planned_files() if files is None else files
    return frozenset(files) | {MANIFEST_NAME}


def write_manifest(destination, digests):
    payload = {'files': dict(sorted(digests.items()))}
    path = destination / MANIFEST_NAME
    path.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8', newline='\n')
    return path


def read_manifest(destination):
    path = destination / MANIFEST_NAME
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding='utf-8'))
    files = data.get('files')
    if not isinstance(files, dict):
        raise ValueError(f'Invalid installer manifest at {path}')
    return {str(key): str(value) for key, value in files.items()}


def installed_content_digests(destination):
    digests = {}
    for relative in planned_files():
        path = destination / relative
        if path.is_file():
            digests[relative] = digest_text(path.read_text(encoding='utf-8'))
    return digests


def package_file_relatives(destination):
    relatives = set()
    for path in destination.rglob('*'):
        if path.is_file():
            relatives.add(path.relative_to(destination).as_posix())
    return relatives


def backup_differing_files(destination, planned):
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup_root = destination.parent / f'{destination.name}.bak-{stamp}'
    wrote = False
    for relative, content in planned.items():
        path = destination / relative
        if not path.is_file():
            continue
        current = path.read_text(encoding='utf-8')
        if current == content:
            continue
        target = backup_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(current, encoding='utf-8', newline='\n')
        wrote = True
    return backup_root if wrote else None


def write_package_files(destination, planned, fail_after=None):
    (destination / 'references').mkdir(parents=True, exist_ok=True)
    for relative, content in planned.items():
        if fail_after == relative:
            raise OSError(f'injected failure before writing {relative}')
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8', newline='\n')
    if fail_after == MANIFEST_NAME:
        raise OSError(f'injected failure before writing {MANIFEST_NAME}')
    write_manifest(destination, {relative: digest_text(content) for relative, content in planned.items()})


def validate_written_package(destination, planned):
    expected = set(managed_relative_paths(planned))
    actual = package_file_relatives(destination)
    if actual != expected:
        raise ValueError(
            'Staged package contents do not match the planned managed set: '
            f'missing={sorted(expected - actual)} unexpected={sorted(actual - expected)}')
    for relative, content in planned.items():
        path = destination / relative
        if digest_text(path.read_text(encoding='utf-8')) != digest_text(content):
            raise ValueError(f'Staged package digest mismatch for {relative}')
    manifest = read_manifest(destination)
    if manifest is None:
        raise ValueError('Staged package is missing the installer manifest')
    if set(manifest) != set(planned):
        raise ValueError('Staged installer manifest paths do not match planned files')
    for relative, content in planned.items():
        digest = manifest[relative]
        if not is_sha256_digest(digest) or digest != digest_text(content):
            raise ValueError(f'Staged installer manifest digest invalid for {relative}')


def remove_tree(path):
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def remove_obsolete_reference_files(destination):
    removed = []
    for relative in sorted(OBSOLETE_REFERENCE_PATHS):
        path = destination / relative
        if path.is_file():
            path.unlink()
            removed.append(relative)
    return removed


def install_fresh_package(destination, planned, fail_after=None):
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f'Destination already exists; no files replaced: {destination}')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    staging = destination.parent / f'{destination.name}.staging-{stamp}-{secrets.token_hex(4)}'
    try:
        staging.mkdir(parents=False, exist_ok=False)
        write_package_files(staging, planned, fail_after=fail_after)
        validate_written_package(staging, planned)
        staging.rename(destination)
    except Exception:
        if staging.exists() or staging.is_symlink():
            remove_tree(staging)
        raise
    return destination


def install(destination, upgrade=False, force=False, fail_after=None):
    destination = Path(destination).expanduser().absolute()
    if force and not upgrade:
        raise ValueError('--force requires --upgrade')
    if fail_after is not None and (upgrade and destination.exists()):
        raise ValueError('fail_after applies only to fresh package installs')
    if destination.name != 'project-helper':
        raise ValueError('Destination folder must be named project-helper for Cursor discovery.')
    # Check the lexical path before any resolution: broken links count as occupied.
    if destination.is_symlink():
        raise FileExistsError(f'Destination is a symlink; no files replaced: {destination}')
    planned = planned_files()
    exists = destination.exists()
    if not upgrade:
        if exists:
            raise FileExistsError(f'Destination already exists; no files replaced: {destination}')
        install_fresh_package(destination, planned, fail_after=fail_after)
        return destination, None, False
    if not exists:
        install_fresh_package(destination, planned, fail_after=fail_after)
        return destination, None, False
    if not destination.is_dir():
        raise FileExistsError(f'Destination exists and is not a directory: {destination}')
    extras = sorted(
        package_file_relatives(destination)
        - managed_relative_paths(planned)
        - OBSOLETE_REFERENCE_PATHS)
    if extras:
        raise FileExistsError(
            'Destination has extra files; no files replaced: ' + ', '.join(extras))
    manifest = read_manifest(destination)
    if manifest is None and not force:
        raise FileExistsError(
            'Destination has no installer manifest; refuse upgrade without --force. '
            'Rename/remove the folder for a fresh install, or run with --upgrade --force '
            f'after backing up customizations: {destination}')
    if manifest is not None and not force:
        planned_paths = set(planned)
        manifest_paths = set(manifest) - OBSOLETE_REFERENCE_PATHS
        missing_manifest = sorted(planned_paths - set(manifest))
        if missing_manifest:
            raise FileExistsError(
                'Installer manifest is incomplete; no files replaced. '
                'missing: ' + ', '.join(missing_manifest)
                + '. Renamed skill references need --upgrade --force.')
        unexpected_manifest = sorted(manifest_paths - planned_paths)
        if unexpected_manifest:
            raise FileExistsError(
                'Installer manifest lists unexpected paths; no files replaced: '
                + ', '.join(unexpected_manifest))
        malformed_digests = sorted(
            relative for relative, digest in manifest.items()
            if relative not in OBSOLETE_REFERENCE_PATHS and not is_sha256_digest(digest))
        if malformed_digests:
            raise FileExistsError(
                'Installer manifest has invalid SHA-256 digests; no files replaced: '
                + ', '.join(malformed_digests))
        current = installed_content_digests(destination)
        customized = sorted(
            relative for relative, digest in manifest.items()
            if relative not in OBSOLETE_REFERENCE_PATHS and current.get(relative) != digest)
        if customized:
            raise FileExistsError(
                'Destination managed files do not match the installer manifest; '
                'treat as customized and refuse upgrade without --force. '
                'customized: ' + ', '.join(customized))
    backup_root = None
    if force:
        backup_root = backup_differing_files(destination, planned)
    write_package_files(destination, planned)
    remove_obsolete_reference_files(destination)
    return destination, backup_root, True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path,
                        default=Path.home() / '.cursor/skills/project-helper',
                        help='project-helper folder (default: user-level Cursor skills).')
    parser.add_argument('--upgrade', action='store_true',
                        help='Replace a clean stock package, or install when missing.')
    parser.add_argument('--force', action='store_true',
                        help='With --upgrade, overwrite managed files after backing up diffs.')
    args = parser.parse_args()
    try:
        destination, backup_root, replaced = install(
            args.destination, upgrade=args.upgrade, force=args.force)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f'Installation stopped: {exc}', file=sys.stderr)
        print('Existing package files were left in place when the command stopped. '
              'Fresh installs stage beside the destination and remove that staging '
              'directory after failure; inspect only if a staging folder remains.',
              file=sys.stderr)
        return 1
    action = 'Upgraded' if replaced else 'Installed'
    print(f'{action} /project-helper at {destination}')
    if backup_root is not None:
        print(f'Backed up replaced managed files to {backup_root}')
    print('Reload Cursor or start a new chat, open a project folder, and type /project-helper.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
