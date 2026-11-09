"""Generate docs/SKILLS.md from local skill files and embedded skills-meta blocks."""
from pathlib import Path
import argparse
import re
import sys

try:
    from skill_inventory import REQUIRED_SKILLS, WORKFLOWS
except ImportError:  # pragma: no cover
    from scripts.skill_inventory import REQUIRED_SKILLS, WORKFLOWS

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / '.cursor' / 'skills'
OUTPUT = ROOT / 'docs' / 'SKILLS.md'
META_KEYS = (
    'use_when',
    'do_not_use_when',
    'needs_first',
    'produces',
    'done_when',
    'typical_next',
    'weight',
)
META_PATTERN = re.compile(
    r'<!--\s*skills-meta\s*\n(.*?)\n\s*-->',
    re.DOTALL | re.IGNORECASE,
)
SKILL_ORDER = ('project-helper',) + WORKFLOWS


def parse_frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0] != '---' or '---' not in lines[1:]:
        raise ValueError('missing frontmatter')
    end = lines.index('---', 1)
    data = {}
    for line in lines[1:end]:
        key, sep, value = line.partition(':')
        if not sep:
            continue
        data[key.strip()] = value.strip().strip('"')
    return data


def parse_skills_meta(text):
    match = META_PATTERN.search(text)
    if not match:
        raise ValueError('missing skills-meta block')
    meta = {}
    for line in match.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        key, sep, value = line.partition(':')
        if not sep:
            raise ValueError(f'invalid skills-meta line: {line}')
        meta[key.strip()] = value.strip()
    missing = [key for key in META_KEYS if not meta.get(key)]
    if missing:
        raise ValueError('missing skills-meta keys: ' + ', '.join(missing))
    if meta['weight'] not in {'light', 'standard', 'strict'}:
        raise ValueError(f"invalid weight: {meta['weight']}")
    return meta


def load_skills():
    skills = []
    for name in SKILL_ORDER:
        path = SKILLS_ROOT / name / 'SKILL.md'
        text = path.read_text(encoding='utf-8')
        front = parse_frontmatter(text)
        if front.get('name') != name:
            raise ValueError(f'{path}: frontmatter name mismatch')
        meta = parse_skills_meta(text)
        skills.append({'name': name, 'description': front.get('description', ''), **meta})
    present = {path.parent.name for path in SKILLS_ROOT.glob('*/SKILL.md')}
    unexpected = sorted(present - set(REQUIRED_SKILLS))
    if unexpected:
        raise ValueError('unexpected skills: ' + ', '.join(unexpected))
    missing = sorted(set(REQUIRED_SKILLS) - present)
    if missing:
        raise ValueError('missing skills: ' + ', '.join(missing))
    return skills


def render(skills):
    lines = [
        '# Skill decision guide',
        '',
        'Generated from `.cursor/skills/*/SKILL.md` skills-meta blocks. Do not edit by hand;',
        'run `python scripts/generate_skills_guide.py` after changing skill metadata.',
        '',
        '## Lifecycle',
        '',
        '```mermaid',
        'flowchart TD',
        '  idea[Idea_or_change] --> helper["/project-helper"]',
        '  helper --> prior["/prior-art"]',
        '  prior --> interview["/decision-interview"]',
        '  interview --> plan["/project-planning"]',
        '  plan --> design["/design-review"]',
        '  design --> build["/test-first-change"]',
        '  build --> release["/release-check"]',
        '  build -.-> debug["/hypothesis-debugging"]',
        '  debug -.-> build',
        '  design -.-> audit["/trust-boundary-audit"]',
        '  audit -.-> release',
        '```',
        '',
        'Use `/design-review` only for a new system or material design change.',
        'Use `/trust-boundary-audit` only for sensitive boundaries or an audit request.',
        'Use `/hypothesis-debugging` from any failure loop.',
        '',
        '## Decision table',
        '',
        '| Skill | Use when | Do NOT use when | Needs first | Produces | Done when | Typical next step | Weight |',
        '|---|---|---|---|---|---|---|---|',
    ]
    for skill in skills:
        lines.append(
            f"| `/{skill['name']}` | {skill['use_when']} | {skill['do_not_use_when']} | "
            f"{skill['needs_first']} | {skill['produces']} | {skill['done_when']} | "
            f"{skill['typical_next']} | {skill['weight']} |"
        )
    lines.extend([
        '',
        '## Notes',
        '',
        '- Weights are guidance for ceremony: `light` for tiny edits, `standard` for normal features,',
        '  `strict` for high-risk or sensitive work. `/project-helper` may ask which weight to use later.',
        '- Fresh-context isolation for design and security verification is a host capability; report unverified when unavailable.',
        '',
    ])
    return '\n'.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true',
                        help='Exit non-zero when docs/SKILLS.md is missing or stale.')
    args = parser.parse_args(argv)
    try:
        content = render(load_skills())
    except (OSError, ValueError) as exc:
        print(f'Skills guide generation failed: {exc}', file=sys.stderr)
        return 1
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding='utf-8') != content:
            print('docs/SKILLS.md is missing or out of date; run '
                  'python scripts/generate_skills_guide.py', file=sys.stderr)
            return 1
        print('docs/SKILLS.md is up to date.')
        return 0
    OUTPUT.write_text(content, encoding='utf-8', newline='\n')
    print(f'Wrote {OUTPUT.relative_to(ROOT).as_posix()}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
