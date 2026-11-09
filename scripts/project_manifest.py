"""Generate/check the stock initialization inventory; no application data belongs here."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'scripts/project-manifest.json'
RESET_TARGETS = (
    'README.md', 'CONTRIBUTING.md', 'MAINTAINING.md',
    'docs/PRD.md', 'docs/TASKS.md', 'docs/QUALITY_GATES.md', 'docs/DECISIONS.md',
    'docs/SETUP.md', 'docs/CONFIGURATION.md', 'docs/INSTALL.md', 'docs/RULES.md',
    '.github/workflows/ci.yml',
)
RESET = {path: f'scripts/project_templates/{path}' for path in RESET_TARGETS}
REMOVE = tuple(sorted((
    'CURSOR_UPDATE_PROMPT.md', 'publish-to-github.py', 'publish-to-github.sh',
    'VERSION', 'CHANGELOG.md',
    'tests/test_starter.py', 'tests/test_install_chat_command.py', 'tests/test_init_project.py',
    'evals/prior-art-search-hygiene.md',
    'docs/superpowers/specs/2026-11-09-maint-002-permission-probe-design.md',
    'docs/superpowers/plans/2026-11-09-maint-002-permission-probe.md',
    '.github/ISSUE_TEMPLATE/bug_report.md', '.github/ISSUE_TEMPLATE/feature_request.md',
    'docs/designs/project-initialization.md', 'docs/INITIALIZE.md', 'docs/VERIFICATION.md',
    'docs/designs/workflow-evidence.md', 'docs/EVIDENCE.md',
    'tests/test_todo_example.py', 'tests/test_workflow_eval.py',
    'scripts/init_project.py', 'scripts/project_manifest.py', MANIFEST,
    *RESET.values(),
)))
MAINTAINER_PREFIXES = ('examples/', 'evals/')


def removal_paths(paths):
    # Classify the checked inventory, never recurse/delete a directory at apply time.
    return sorted(set(REMOVE) | {path for path in paths if path.startswith(MAINTAINER_PREFIXES)})


def valid_path(value):
    if (not isinstance(value, str) or not value or '\\' in value or ':' in value
            or any(ord(char) < 32 for char in value)):
        raise ValueError('Invalid manifest path')
    path = PurePosixPath(value)
    if not path.parts or path.is_absolute() or path.as_posix() != value:
        raise ValueError('Invalid manifest path')
    for part in path.parts:
        if (part in ('.', '..') or part.lower() == '.git' or part.rstrip(' .') != part
                or re.fullmatch(r'(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])', part.split('.')[0])):
            raise ValueError('Invalid manifest path')
    return value


def text_digest(path):
    # Git may change stock text line endings at checkout; preflight never writes.
    return hashlib.sha256(path.read_text(encoding='utf-8').encode('utf-8')).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('Duplicate manifest key')
        result[key] = value
    return result


def read_manifest(root):
    data = json.loads((root / MANIFEST).read_text(encoding='utf-8'), object_pairs_hook=unique_object)
    if (not isinstance(data, dict) or set(data) != {'version', 'files', 'reset', 'remove'}
            or type(data['version']) is not int or data['version'] != 1
            or not isinstance(data['files'], dict) or data['reset'] != RESET):
        raise ValueError('Invalid initialization manifest')
    paths = list(data['files'])
    if (MANIFEST.casefold() in {path.casefold() for path in paths}
            or len({path.casefold() for path in paths}) != len(paths)):
        raise ValueError('Aliased manifest paths')
    for path, digest in data['files'].items():
        valid_path(path)
        if not isinstance(digest, str) or not re.fullmatch('[0-9a-f]{64}', digest):
            raise ValueError('Invalid manifest digest')
    if data['remove'] != removal_paths(paths):
        raise ValueError('Invalid removal inventory')
    required = set(RESET) | set(RESET.values()) | (set(REMOVE) - {MANIFEST})
    if not required <= set(paths):
        raise ValueError('Incomplete initialization manifest')
    return data


def inventory(root):
    if (root / '.git').exists():
        result = subprocess.run(
            ['git', '--no-optional-locks', '-c', 'core.fsmonitor=false',
             '-c', 'core.untrackedCache=false', '-C', str(root), 'ls-files',
             '--cached', '--others', '--exclude-standard', '-z'],
            capture_output=True, check=True)
        paths = result.stdout.decode('utf-8').split('\0')
        return sorted({valid_path(path) for path in paths if path and path != MANIFEST})
    return sorted(read_manifest(root)['files'])


def generate(root):
    paths = inventory(root)
    return {'version': 1, 'files': {path: text_digest(root / path) for path in paths},
            'reset': RESET, 'remove': removal_paths(paths)}


def check_manifest(root):
    try:
        if read_manifest(root) != generate(root):
            return ['initialization baseline is stale; run python scripts/project_manifest.py']
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        return [f'initialization baseline invalid: {exc}']
    return []


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    try:
        if args.check:
            errors = check_manifest(ROOT)
            print('\n'.join(errors) if errors else 'Initialization baseline is up to date.')
            return bool(errors)
        data = generate(ROOT)
        (ROOT / MANIFEST).write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8', newline='\n')
        print('Initialization baseline generated. Review its file inventory before committing.')
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(f'Baseline generation stopped: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
