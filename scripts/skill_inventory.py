"""Single source of truth for required Cursor skills in this starter."""

WORKFLOWS = ('project-planning', 'grill-me', 'design-review', 'tdd',
             'systematic-debugging', 'security-audit', 'release-check', 'prior-art')
REQUIRED_SKILLS = frozenset((*WORKFLOWS, 'project-helper'))
