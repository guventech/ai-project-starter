"""Validate VERSION against CHANGELOG.md and print that release's notes (read-only)."""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSION_PATH = ROOT / 'VERSION'
CHANGELOG_PATH = ROOT / 'CHANGELOG.md'
HEADING_RE = re.compile(r'^## \[([^\]]+)\](?:\s+-\s+(\S+))?\s*$')


def read_version(path=VERSION_PATH):
    text = path.read_text(encoding='utf-8').strip()
    if not text or any(character.isspace() for character in text):
        raise ValueError(f'Invalid VERSION in {path}')
    return text


def parse_releases(text):
    lines = text.splitlines()
    releases = []
    current = None
    for index, line in enumerate(lines):
        match = HEADING_RE.match(line)
        if match:
            version = match.group(1).strip()
            if not version or version.lower() == 'unreleased':
                current = None
                continue
            if any(character.isspace() for character in version):
                raise ValueError(f'Malformed changelog version heading on line {index + 1}')
            current = {
                'version': version,
                'date': match.group(2),
                'start': index,
                'lines': [],
            }
            releases.append(current)
            continue
        if current is not None:
            current['lines'].append(line)
    return releases


def release_notes(release):
    body = '\n'.join(release['lines']).strip('\n')
    return body.strip() + ('\n' if body.strip() else '')


def select_release(releases, version):
    matches = [item for item in releases if item['version'] == version]
    if not matches:
        raise ValueError(f'CHANGELOG.md has no release section for VERSION {version}')
    if len(matches) > 1:
        raise ValueError(f'CHANGELOG.md has duplicate release sections for {version}')
    versions = [item['version'] for item in releases]
    duplicates = sorted({name for name in versions if versions.count(name) > 1})
    if duplicates:
        raise ValueError('CHANGELOG.md has duplicate release versions: ' + ', '.join(duplicates))
    return matches[0]


def validate_changelog(root=ROOT):
    root = Path(root)
    version_path = root / 'VERSION'
    changelog_path = root / 'CHANGELOG.md'
    if not version_path.is_file() or not changelog_path.is_file():
        return []
    try:
        version = read_version(version_path)
        releases = parse_releases(changelog_path.read_text(encoding='utf-8'))
        select_release(releases, version)
    except (OSError, ValueError) as exc:
        return [f'CHANGELOG.md: {exc}']
    return []


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--check', action='store_true',
        help='Validate VERSION against CHANGELOG.md without printing notes.')
    parser.add_argument(
        '--root', type=Path, default=ROOT,
        help='Repository root containing VERSION and CHANGELOG.md.')
    args = parser.parse_args(argv)
    root = args.root
    version_path = root / 'VERSION'
    changelog_path = root / 'CHANGELOG.md'
    try:
        if not version_path.is_file():
            raise ValueError(f'Missing {version_path}')
        if not changelog_path.is_file():
            raise ValueError(f'Missing {changelog_path}')
        version = read_version(version_path)
        releases = parse_releases(changelog_path.read_text(encoding='utf-8'))
        release = select_release(releases, version)
    except (OSError, ValueError) as exc:
        print(f'Changelog check stopped: {exc}', file=sys.stderr)
        return 2
    if args.check:
        print(f'CHANGELOG.md matches VERSION {version}.')
        return 0
    notes = release_notes(release)
    heading = f'## [{release["version"]}]'
    if release['date']:
        heading += f' - {release["date"]}'
    print(heading)
    if notes:
        print(notes, end='' if notes.endswith('\n') else '\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
