# Rule triggers

All three .cursor/rules files retain alwaysApply false and scoped globs.

- architecture: `docs/ARCHITECTURE.md, docs/DECISIONS.md, src/**, app/**, lib/**, cmd/**, internal/**, pkg/**, *.py, *.go` — module boundaries and recorded design choices.
- testing: `tests/**, **/test_*.py, **/*.test.*, **/*.spec.*, **/*_test.go, .github/workflows/**` — observable behavior, regression checks and isolated tests.
- security: `src/**, app/**, lib/**, cmd/**, internal/**, pkg/**, *.py, *.go, scripts/**, .github/workflows/**, publish-to-github.*` — input boundaries, authorization, secrets and dependency provenance.

Adapt source/test roots after choosing this project's layout. These defaults
cover common src/app/lib and Go cmd/internal/pkg conventions, not arbitrary
packages or all languages. Matching files may receive multiple rules.

Inspect actual attachment in your installed Cursor version. Static validation
does not prove host behavior or rule enforcement. Record observations in SETUP.md.
