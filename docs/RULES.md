# Rule triggers and layout coverage

Cursor project rules live in `.cursor/rules/*.mdc`. Each rule here has
`alwaysApply: false` and comma-separated globs. Cursor documents this mode as
auto-attaching a rule when a matching file is in context; a rule can also be
selected through an explicit `@` mention. See the [official rule reference](https://cursor.com/docs/rules).

## Rule inventory

| Rule | Shipped globs | Trigger and intent |
|------|---------------|--------------------|
| architecture | `docs/ARCHITECTURE.md, docs/DECISIONS.md, src/**, app/**, lib/**, cmd/**, internal/**, pkg/**, *.py, *.go` | Matching design documents or source files: module boundaries, dependency direction and recorded tradeoffs. |
| testing | `tests/**, **/test_*.py, **/*.test.*, **/*.spec.*, **/*_test.go, .github/workflows/**` | Matching tests or CI configuration: observable behavior, regression reproduction and isolated checks. |
| security | `src/**, app/**, lib/**, cmd/**, internal/**, pkg/**, *.py, *.go, scripts/**, .github/workflows/**, publish-to-github.*` | Matching source, scripts or CI: input validation, authorization, secrets, query parameterization and dependency provenance. |

These are source-layout defaults, not coverage of every framework or file type.
Source globs can also include colocated tests; a Go test under `internal/` can
match all three rules. Root Python/Go test files can do the same. Unrelated root
`README.md` files match none of these patterns. Shared behavior still comes from
`AGENTS.md`; rule matching does not enforce security or tests.

## Tested sample layouts

The unittest `test_rule_globs_cover_node_python_go_layouts` writes sample files
and evaluates the actual rule metadata with Python `Path.glob`. Its expectations
cover source files for architecture/security and test files for testing:

- Node: `src/index.ts`, `app/page.tsx`, `lib/auth/session.ts`,
  `tests/page.test.ts`, `page.spec.ts`.
- Python: `src/sample/service.py`, `main.py`, `tests/test_service.py`,
  `test_service.py`.
- Go: `main.go`, `cmd/example/main.go`, `internal/auth/session.go`,
  `pkg/client/client.go`, `internal/auth/session_test.go`, `main_test.go`.
- Each layout also checks the two design-document paths, CI workflow and
  `scripts/check.py`, plus the unrelated README exclusion.

These are static scope checks, not Cursor-engine compatibility tests or proof of
automatic attachment. Globs are relative to the project root. Runtime semantics
and path case can differ across hosts; verify the installed Cursor version.

## Adapt the scope

Inspect your source and test roots first. Preserve shared docs, CI and script
patterns where relevant. The following fragments are examples to merge into the
corresponding rule's existing `globs`, not new rule files:

```yaml
# Node: app/lib/src; add packages/** for a workspace monorepo if needed.
# architecture/security source scope:
globs: "src/**, app/**, lib/**"
# testing scope, including colocated root tests:
globs: "tests/**, **/*.test.*, **/*.spec.*"
```

```yaml
# Python: src layout or root modules; replace sample_package with your package.
# architecture/security source scope:
globs: "src/**, sample_package/**, *.py"
# testing scope; add **/*_test.py if that is your naming convention:
globs: "tests/**, **/test_*.py"
```

```yaml
# Go: command/internal/pkg directories and root modules.
# architecture/security source scope:
globs: "cmd/**, internal/**, pkg/**, *.go"
# testing scope for both root and nested package tests:
globs: "**/*_test.go"
```

Arbitrary package roots, `server/`, `packages/`, other test naming conventions and
other languages need a scope decision; they are not implied by these samples.
Avoid blanket `**` or `alwaysApply: true` just to hide a missing match. If the
work has no meaningful path trigger, consider a description-selected rule as a
separate design choice; the current validator requires scoped globs.

## Check attachment in the installed host

1. Record Cursor editor/CLI version, OS, rule revision and sample layout.
2. Open an isolated sample workspace containing copies of the three rules and
   source/test files from a layout above. Do not copy credentials or private data.
3. In a new read-only Ask session, put the sample files in context. Inspect the
   host's attached-rule display or trace; distinguish automatic attachment from
   explicit `@architecture`, `@testing` or `@security` selection and from reading
   `.mdc` files with a tool.
4. Record each rule's observed attachment and any unexpected match. A report of
   matching filenames alone is not evidence of rule loading. An isolated fixture
   may append distinct response markers to rule copies only, then compare fresh
   matching-file and README-only sessions. Markers must not appear in the prompt
   or sample files; inspect the trace for explicit rule reads and prohibited tools.
   A positive/control difference supports implicit inclusion but is behavioral
   evidence, not a direct attachment-field report. Without a trace/display or
   controlled marker evidence, report attachment as unverified. Keep fixture
   observations separate from editor UI verification.

Actual results and limitations belong in `QUALITY_GATES.md`; machine-specific
host observations belong in `SETUP.md`. No live execution result is implied by
the examples on this page.
