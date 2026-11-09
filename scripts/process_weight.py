"""Infer Lite / Standard / Strict process weight from a stated goal."""
from __future__ import annotations

import argparse
import re
import sys

WEIGHTS = ('lite', 'standard', 'strict')

STRICT_PATTERNS = (
    re.compile(r'\bpayments?\b', re.I),
    re.compile(r'\bstripe\b', re.I),
    re.compile(r'\bbilling\b', re.I),
    re.compile(r'\bcheckout\b', re.I),
    re.compile(r'\bauthenticat\w*\b', re.I),
    re.compile(r'\bauthoriz\w*\b', re.I),
    re.compile(r'\boauth\b', re.I),
    re.compile(r'\bpasswords?\b', re.I),
    re.compile(r'\bsecrets?\b', re.I),
    re.compile(r'\bcredentials?\b', re.I),
    re.compile(r'\bapi[ -]?keys?\b', re.I),
    re.compile(r'\bforce[ -]?push\b', re.I),
    re.compile(r'\bdrop\b.{0,40}\bdatabases?\b', re.I),
    re.compile(r'\bdestructive\b', re.I),
    re.compile(r'\bwipe\b', re.I),
    re.compile(r'\bdelete\b.{0,40}\bproduction\b', re.I),
)

LITE_PATTERNS = (
    re.compile(r'\btypos?\b', re.I),
    re.compile(r'\bspelling\b', re.I),
    re.compile(
        r'\brename\b.{0,60}\b(functions?|methods?|variables?|symbols?|identifiers?|files?)\b',
        re.I,
    ),
    re.compile(
        r'\b(functions?|methods?|variables?|symbols?|identifiers?|files?)\b.{0,60}\brename\b',
        re.I,
    ),
    re.compile(r'\bdocs?[ -]?only\b', re.I),
    re.compile(r'\bdocumentation[ -]?only\b', re.I),
    re.compile(r'\bci[ /-]?(config|bump)\b', re.I),
    re.compile(r'\bcomment[ -]?only\b', re.I),
    re.compile(r'\bwhitespace\b', re.I),
)


def infer_process_weight(goal: str) -> str | None:
    """Return lite/standard/strict when markers determine it; otherwise None."""
    text = (goal or '').strip()
    if not text:
        return None
    if any(pattern.search(text) for pattern in STRICT_PATTERNS):
        return 'strict'
    if any(pattern.search(text) for pattern in LITE_PATTERNS):
        return 'lite'
    return None


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('goal', nargs='?', default='', help='Stated goal or change summary')
    args = parser.parse_args(argv)
    weight = infer_process_weight(args.goal)
    if weight is None:
        print('undetermined')
        return 2
    print(weight)
    return 0


if __name__ == '__main__':
    sys.exit(main())
