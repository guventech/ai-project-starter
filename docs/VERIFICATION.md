# Verification scope and limits

This page summarizes evidence for the starter itself. It does not establish
results for an application copied from it. Initialization removes this overview
and replaces project requirements, tasks and check records with unfilled versions.
Keep licence/attribution records as provenance, not application verification.

## Static checks and disposable copies

For starter development, the configured commands are:

```sh
python scripts/validate_starter.py
python -m unittest discover -s tests -v
```

Default validation also checks the generated skill guide and initialization
baseline. [QUALITY_GATES.md](QUALITY_GATES.md) records actual local results,
skipped symlink cases and the Python 3.12 Windows/Linux CI evidence. The initializer
was delivered through [PR #27](https://github.com/guventech/ai-project-starter/pull/27).
Its fixtures cover stock-copy refusal, retained safeguards, exact backups and
ordinary-error recovery. They do not establish protection against hostile
concurrent changes, killed processes or disk failure during rollback.

These commands validate the starter; they do not lint, test, build, secure or
release an application. Initialize a fresh template copy before running developer
checks that could create bytecode caches. After initialization, use the explicit
`python scripts/validate_starter.py --project` profile for retained configuration
checks, then define the application's own tests/build and relevant security,
accessibility or migration checks.

## Observed Cursor execution

[SETUP.md](SETUP.md) records versions, modes, inputs and bounded observations:

- CLI attachment and bundled-reference loading, including new/existing project
  routing and nonempty-folder conversational boundaries.
- Native reviewer invocation and behavioral write refusal; a separate matched-pair
  trial observed a verifier Write attempt denied by the host while a writable
  control succeeded.
- A Go source/test session returned fixture-only rule markers; a fresh README-only
  control returned none. Per-read attachment arrays were empty, so this is
  controlled behavioral evidence of implicit inclusion, not a direct UI report.

The routing example in README summarizes the calculator-fixture trial in that
record. It ran in Ask mode and produced findings/proposed checks without edits;
it is not a completed application implementation or a reconstructed exact quote.
Some historical trials used pre-rename skill names. Source revisions and limits
remain in the detailed record rather than being treated as current global-install state.

## Check your installed host

1. Confirm discovery and source selection for the local skills and two reviewer
   definitions in your installed Cursor version; optional packs have their own setup.
2. Test selected procedures on synthetic fixtures. Separate file loading, behavior,
   host permission denial and OS-level isolation in the results.
3. Record fresh-review context setup. A new name or a canary result alone does not
   establish universal context isolation. Report unavailable host capabilities as unverified.
4. Check your installed snapshot with `python scripts/install_chat_command.py --check`
   before choosing an upgrade. Follow [INSTALL.md](INSTALL.md) for edited/old packages.

Editor UI behavior, every supported host/version, complete upstream plugin execution
and universal enforcement are not established by the recorded trials. User-level
settings, account configuration and branch protections do not transfer with a copy.

## Outcome evidence

No controlled comparison currently establishes better software, fewer defects or
faster delivery than a bare prompt. F-02 now has a worked application example and
eight recorded paired attempts: seven protocol failures and one accepted finish.
The [evidence report](EVIDENCE.md) separates final-artifact checks from protocol
completion. Live trials are blocked pending complete native CLI isolation; useful
comparative outcome evidence remains open. The synthetic prior-art scenario is
still a test specification marked not run, not a comparative result.

Treat upstream feature descriptions in the README comparison as scope descriptions,
and its fit recommendations as editorial judgments. The comparison is not a ranking
of measured effectiveness or a claim of full upstream compatibility.
