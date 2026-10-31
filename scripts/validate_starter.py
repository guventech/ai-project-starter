"""Dependency-free validation of this starter's constrained metadata format."""
from pathlib import Path
import sys

REQUIRED = ['README.md', 'AGENTS.md', 'LICENSE', '.env.example', 'docs/PRD.md', 'docs/ARCHITECTURE.md',
            'docs/DECISIONS.md', 'docs/TASKS.md', 'docs/QUALITY_GATES.md',
            'docs/INTEGRATIONS.md', 'docs/CONFIGURATION.md',
            '.github/workflows/ci.yml', 'publish-to-github.py', 'publish-to-github.sh']
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

def validate(root):
    root = Path(root)
    errors = [f'missing {p}' for p in REQUIRED if not (root / p).is_file()]
    groups = [('.cursor/rules', '*.mdc', {'architecture', 'testing', 'security'}),
              ('.cursor/agents', '*.md', {'architect', 'verifier'}),
              ('.cursor/skills', '*/SKILL.md', {'project-planning', 'systematic-debugging', 'release-check'})]
    for folder, pattern, expected in groups:
        paths = list((root / folder).glob(pattern))
        names = {p.parent.name if p.name == 'SKILL.md' else p.stem for p in paths}
        errors.extend(f'missing {folder}/{n}' for n in sorted(expected - names))
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
    return errors

if __name__ == '__main__':
    errors = validate(Path(__file__).resolve().parents[1])
    print('\n'.join(errors) if errors else 'Starter validation passed.')
    sys.exit(bool(errors))
