"""Single source of truth for required Cursor skills in this starter."""

WORKFLOWS = (
    'project-planning',
    'decision-interview',
    'design-review',
    'test-first-change',
    'hypothesis-debugging',
    'trust-boundary-audit',
    'release-check',
    'prior-art',
)
REQUIRED_SKILLS = frozenset((*WORKFLOWS, 'project-helper'))

# Former local names that collide with optional upstream packs / popular skills.
COLLIDING_UPSTREAM_NAMES = frozenset({
    'grill-me',
    'tdd',
    'systematic-debugging',
    'security-audit',
})

SKILL_RENAMES = {
    'grill-me': 'decision-interview',
    'tdd': 'test-first-change',
    'systematic-debugging': 'hypothesis-debugging',
    'security-audit': 'trust-boundary-audit',
}

OBSOLETE_REFERENCE_PATHS = frozenset(
    f'references/{old}.md' for old in SKILL_RENAMES
)
