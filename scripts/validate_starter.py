"""Dependency-free validation of this starter's constrained metadata format."""
from pathlib import Path
import argparse
import re
import sys

try:
    from skill_inventory import COLLIDING_UPSTREAM_NAMES, REQUIRED_SKILLS
except ImportError:  # pragma: no cover - package import when run via tests
    from scripts.skill_inventory import COLLIDING_UPSTREAM_NAMES, REQUIRED_SKILLS

REQUIRED = ['README.md', 'AGENTS.md', 'MAINTAINING.md', 'LICENSE', '.env.example',
            'docs/PRD.md', 'docs/ARCHITECTURE.md',
            'docs/DECISIONS.md', 'docs/TASKS.md', 'docs/QUALITY_GATES.md',
            'docs/INTEGRATIONS.md', 'docs/CONFIGURATION.md', 'docs/SKILLS.md',
            'docs/INSTALL.md', 'docs/RULES.md',
            '.github/workflows/ci.yml', 'publish-to-github.py', 'publish-to-github.sh',
            'scripts/install_chat_command.py', 'scripts/skill_inventory.py',
            'scripts/generate_skills_guide.py', 'scripts/process_weight.py']
MAINTAINER_REQUIRED = {
    'publish-to-github.py', 'publish-to-github.sh', 'scripts/init_project.py',
    'scripts/project_manifest.py', 'scripts/project-manifest.json',
    'docs/INITIALIZE.md', 'docs/designs/project-initialization.md', 'docs/VERIFICATION.md',
    'VERSION', 'CHANGELOG.md', 'scripts/changelog_release.py',
}
HOME_PATH_PATTERNS = (
    re.compile(r'(?i)C:\\Users\\'),
    re.compile(r'(?i)C:/Users/'),
    re.compile(r'/Users/[^/\s]+/'),
    re.compile(r'/home/[^/\s]+/'),
)
PUBLIC_DOC_GLOBS = ('README.md', 'AGENTS.md', 'MAINTAINING.md', 'docs/**/*.md')
AGENTS_MAINTAINER_MARKERS = (
    'Maintaining this starter',
    'pull requests and both starter CI',
    'COLLIDING_UPSTREAM_NAMES',
    'npx skills add',
    'docs/SETUP.md',
)


def metadata(path):
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines()
    if not lines or lines[0] != '---' or '---' not in lines[1:]:
        raise ValueError('missing frontmatter delimiters')
    end = lines.index('---', 1)
    data = {}
    for line in lines[1:end]:
        key, sep, value = line.partition(':')
        if not sep or key in data or not value.strip():
            raise ValueError('invalid or duplicate scalar metadata')
        data[key] = value.strip().strip('"')
    if not '\n'.join(lines[end + 1:]).strip():
        raise ValueError('missing instructions')
    return data


def public_doc_paths(root):
    paths = []
    for pattern in PUBLIC_DOC_GLOBS:
        paths.extend(path for path in root.glob(pattern) if path.is_file())
    return sorted({path.resolve(): path for path in paths}.values(), key=lambda path: path.as_posix())


def home_path_errors(root):
    errors = []
    for path in public_doc_paths(root):
        text = path.read_text(encoding='utf-8')
        if any(pattern.search(text) for pattern in HOME_PATH_PATTERNS):
            errors.append(f'{path.relative_to(root).as_posix()}: personal home path')
    return errors


def validate(root, project=False):
    root = Path(root)
    required = set(REQUIRED) | MAINTAINER_REQUIRED
    if project:
        required -= MAINTAINER_REQUIRED
    errors = [f'missing {p}' for p in sorted(required) if not (root / p).is_file()]
    groups = [('.cursor/rules', '*.mdc', {'architecture', 'testing', 'security'}),
              ('.cursor/agents', '*.md', {'architect', 'verifier'}),
              ('.cursor/skills', '*/SKILL.md', set(REQUIRED_SKILLS))]
    for folder, pattern, expected in groups:
        paths = list((root / folder).glob(pattern))
        names = {p.parent.name if p.name == 'SKILL.md' else p.stem for p in paths}
        errors.extend(f'missing {folder}/{n}' for n in sorted(expected - names))
        if folder == '.cursor/skills':
            errors.extend(f'unexpected {folder}/{n}' for n in sorted(names - expected))
            collisions = sorted(names & COLLIDING_UPSTREAM_NAMES)
            errors.extend(
                f'colliding upstream skill name .cursor/skills/{n}' for n in collisions)
        for p in paths:
            try:
                data = metadata(p)
                if not data.get('description'):
                    raise ValueError('missing description')
                if p.suffix == '.mdc':
                    if data.get('alwaysApply') != 'false' or not data.get('globs'):
                        raise ValueError('rule must be scoped with globs')
                elif data.get('name') != (p.parent.name if p.name == 'SKILL.md' else p.stem):
                    raise ValueError('name must match path')
                elif p.name == 'SKILL.md':
                    if data.get('disable-model-invocation') != 'true':
                        raise ValueError('skills require explicit invocation')
                elif data.get('readonly') != 'true':
                    raise ValueError('review agents must be read-only')
            except ValueError as exc:
                errors.append(f'{p.relative_to(root)}: {exc}')
    errors.extend(home_path_errors(root))
    agents = root / 'AGENTS.md'
    if agents.is_file():
        agents_text = agents.read_text(encoding='utf-8')
        agents_lines = agents_text.splitlines()
        if len(agents_lines) > 50:
            errors.append(f'AGENTS.md: too long ({len(agents_lines)} lines; max 50)')
        for marker in AGENTS_MAINTAINER_MARKERS:
            if marker in agents_text:
                errors.append(f'AGENTS.md: maintainer-only content ({marker})')
    guide = root / 'scripts' / 'generate_skills_guide.py'
    if guide.is_file():
        import subprocess
        result = subprocess.run(
            [sys.executable, str(guide), '--check'],
            cwd=root, capture_output=True, text=True, check=False)
        if result.returncode:
            detail = (result.stderr or result.stdout or 'skills guide check failed').strip()
            errors.append(f'docs/SKILLS.md: {detail}')
    if not project:
        try:
            from changelog_release import validate_changelog
        except ImportError:
            from scripts.changelog_release import validate_changelog
        errors.extend(validate_changelog(root))
    if not project and (root / 'scripts/project_manifest.py').is_file():
        try:
            from project_manifest import check_manifest
        except ImportError:
            from scripts.project_manifest import check_manifest
        errors.extend(check_manifest(root))
    return errors

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', action='store_true',
                        help='Check reusable workflow configuration after project initialization.')
    args = parser.parse_args()
    errors = validate(Path(__file__).resolve().parents[1], project=args.project)
    print('\n'.join(errors) if errors else 'Starter validation passed.')
    sys.exit(bool(errors))
