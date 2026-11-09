"""Install the project-helper command for Cursor without third-party packages."""
import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ('project-planning', 'grill-me', 'design-review', 'tdd',
             'systematic-debugging', 'security-audit', 'release-check', 'prior-art')
REVIEWERS = ('architect', 'verifier')


def reference_text(path):
    text = path.read_text(encoding='utf-8')
    for name in WORKFLOWS:
        text = text.replace(f'../{name}/SKILL.md', f'{name}.md')
        text = text.replace(f'.cursor/skills/{name}/SKILL.md', f'{name}.md')
    return text


def install(destination):
    destination = Path(destination).expanduser().absolute()
    # Check the lexical path before any resolution: broken links count as occupied.
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f'Destination already exists; no files replaced: {destination}')
    if destination.name != 'project-helper':
        raise ValueError('Destination folder must be named project-helper for Cursor discovery.')
    # Read every required source before creating anything at the destination.
    files = {'SKILL.md': (ROOT / '.cursor/skills/project-helper/SKILL.md').read_text(encoding='utf-8'),
             'LICENSE': (ROOT / 'LICENSE').read_text(encoding='utf-8')}
    for name in WORKFLOWS:
        files[f'references/{name}.md'] = reference_text(ROOT / '.cursor/skills' / name / 'SKILL.md')
    for name in REVIEWERS:
        files[f'references/{name}.md'] = reference_text(ROOT / '.cursor/agents' / f'{name}.md')
    # mkdir refuses an intervening creator as well as an existing destination.
    destination.mkdir(parents=True, exist_ok=False)
    (destination / 'references').mkdir()
    for relative, content in files.items():
        with (destination / relative).open('x', encoding='utf-8', newline='\n') as stream:
            stream.write(content)
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destination', type=Path,
                        default=Path.home() / '.cursor/skills/project-helper',
                        help='New project-helper folder (default: user-level Cursor skills).')
    args = parser.parse_args()
    try:
        destination = install(args.destination)
    except (OSError, ValueError) as exc:
        print(f'Installation stopped: {exc}', file=sys.stderr)
        print('Existing files were not replaced. If a new package is incomplete, inspect it before retrying.',
              file=sys.stderr)
        return 1
    print(f'Installed /project-helper at {destination}')
    print('Reload Cursor or start a new chat, open a project folder, and type /project-helper.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
