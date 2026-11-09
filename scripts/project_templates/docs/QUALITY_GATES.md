# Quality gates

## Workflow configuration checks

Requires Python 3.12, with no Python packages:

```sh
python scripts/validate_starter.py --project
```

The included Windows/Linux CI runs this static configuration check. It retains
skill-name collision detection, generated-guide freshness, consumer-only AGENTS
rules and documentation home-path checks. It does not test an application or
prove Cursor loading, context isolation or security enforcement.

## Application checks

Unconfigured. After stack selection, record exact commands and owners for tests,
formatting, linting, build and relevant security/accessibility checks; add them to
CI. Missing checks are unconfigured, never passed. Select repository protections
for this project; none are inherited from a template copy.

## Requirement evidence

| Requirement | Verification method | Evidence |
|-------------|---------------------|----------|

No checks or workflow executions have been recorded for this project. Record
actual results, skipped checks and host versions before claiming readiness.
