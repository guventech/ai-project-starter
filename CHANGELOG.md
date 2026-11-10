# Changelog

All notable changes to this starter are recorded here.
This file documents repository history. Publication status and tagged snapshots
are recorded on the repository's GitHub Releases page.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Model-cost guidance alongside process weights, with escalation triggers and optional external-router references; no built-in router or measured savings claim.

## [0.1.0] - 2026-11-10

### Added

- Generated `docs/SKILLS.md` decision guide and process weights (Lite / Standard / Strict).
- Consumer/maintainer doc split (`AGENTS.md`, `docs/INSTALL.md`, `MAINTAINING.md`).
- Third-party attribution notice and installer packaging of `THIRD_PARTY.md`.
- Installer `--check` read-only snapshot status and `--version` reporting from `VERSION`.
- Changelog/VERSION consistency check and release-note extraction (`scripts/changelog_release.py`).
- Installer `--diff` read-only managed-text preview with extra-file and manifest-drift reporting.
- Opt-in project initialization for clean template copies.
- Contribution basics (`CONTRIBUTING.md` and issue templates).
- Bounded workflow evidence artifacts under `examples/` and `evals/` (comparative outcomes remain open).
- First `v0.1.0` GitHub prerelease preparation and publication procedure.

### Changed

- Renamed colliding local skills to `decision-interview`, `test-first-change`, `hypothesis-debugging` and `trust-boundary-audit`.
- Rewrote README entry paths and linked verification/optional-pack detail pages.
- Extended rule-trigger documentation and scoped globs.
- Hardened prior-art search hygiene instructions.

### Deferred

- Remaining F-02 isolated comparative runner.
- Multi-host skill packaging (F-11) and optional brand rename (F-12).

### Verification limits

- This is a Cursor starter/template prerelease, not an application release.
- No controlled comparison establishes workflow superiority; F-02 remains partial
  and live trials are blocked pending a reviewed isolated runner.
- Complete native-tool isolation, universal rule enforcement and every host/version
  remain unverified. Static checks and recorded CLI trials have distinct scopes.
- F-11 multi-host packaging remains deferred. See `docs/VERIFICATION.md` and
  `docs/EVIDENCE.md` for the evidence and exclusions.
