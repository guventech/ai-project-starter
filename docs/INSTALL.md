# Install the project-helper command

Install once from this repository so `/project-helper` works in other folders:

```sh
python scripts/install_chat_command.py
```

Reload Cursor or start a new chat. The installer writes a self-contained package under `~/.cursor/skills/project-helper` (workflows and reviewer roles bundled as references). It needs no Python packages and refuses to replace an existing installation without `--upgrade`. Successful install and upgrade print `Package version:` from the repository `VERSION` file and ship that `VERSION` inside the package.

## Package version

```sh
python scripts/install_chat_command.py --version
```

Prints the current checkout's `VERSION` and exits without writing files. It cannot be combined with `--check`, `--diff`, `--upgrade` or `--force`. Repository history notes live in [CHANGELOG.md](../CHANGELOG.md); check consistency with `python scripts/changelog_release.py --check` and print the current section with `python scripts/changelog_release.py`. Tagged snapshots and publication status appear on [GitHub Releases](https://github.com/guventech/ai-project-starter/releases); `v0.1.0` is designated as a prerelease. Check out the desired tag before installing if you need its exact snapshot. Installations do not update themselves.

## Check an installation

From this checkout, inspect the installed snapshot without changing it:

```sh
python scripts/install_chat_command.py --check
```

Use `--destination <folder>/project-helper` to inspect another installation.
The command compares with this checkout, not a remote release. It reports:

- `up to date` (exit 0): managed content matches this checkout and the manifest.
- `N files differ` (exit 1): counts distinct changed, missing, extra or obsolete
  file paths, including managed files whose manifest digest differs from their
  installed content. A stock older snapshot can match its own manifest and still
  differ from this checkout.
- `not installed` or `manifest missing` (exit 1): no installation or no manifest
  was found; nothing is created or repaired.
- `manifest invalid` (exit 2): malformed JSON, invalid digests, missing current
  managed paths or unknown manifest paths. Pre-rename manifests that lack current
  paths fall into this category.
- `Check stopped: ...` (exit 2): unsupported destination, linked destination or
  entry (including Windows junctions), or a file read error. Invalid arguments
  also exit 2. `--check` cannot be combined with `--upgrade` or `--force`.

Missing or invalid manifests take precedence over content-drift reports. The
manifest detects accidental edits; it does not establish authenticity or protect
against tampering. Check mode does not print file contents or perform upgrades.
An up-to-date result is a snapshot observation, not a guarantee against concurrent
changes to the installation.

## Upgrade

### Preview text changes

```sh
python scripts/install_chat_command.py --diff
```

This opt-in inspection prints unified diffs from `installed/` to `checkout/`
for changed or missing managed text files. It marks missing final newlines.
Extra and obsolete files appear by relative name with their contents omitted;
manifest-only digest drift appears as `Manifest digest differs: <path>`.
The comparison uses this checkout and normalizes line endings like `--check`.
The output is an inspection snapshot, not an executable patch or a guarantee
that an upgrade will succeed. Managed-file customizations appear in the output;
review it before sharing logs.

Exit codes and manifest/link/read-error handling match `--check`: 0 for current,
1 for differences or absent installation/manifest, 2 for invalid input or an
inspection error. Absent or invalid manifests stop content previews. `--diff`
cannot be combined with `--check`, `--version`, `--upgrade` or `--force`.
It writes no installation files, backups or staging directories. Use
`--destination <folder>/project-helper` to inspect another package.

| Situation | Command |
|-----------|---------|
| Clean stock package (manifest matches managed files) | `python scripts/install_chat_command.py --upgrade` |
| Missing manifest, incomplete path list, invalid digest values in a readable files map, edited managed files, or renamed skill references | `python scripts/install_chat_command.py --upgrade --force` |
| Unparseable JSON, missing files map or a files value that is not an object | Preserve the old package by moving it aside after inspection, then run a fresh install at the original destination |
| Extra files beside the managed set | Move extras out, then upgrade; `--force` still refuses extras |

`--force` requires `--upgrade`. Differing managed files are backed up beside the package before replacement. Symlink destinations are refused. Updates are not automatic; a global install does not travel with GitHub template copies.

Force still reads an existing manifest. It cannot recover an unreadable structure;
keep that package intact outside the destination before choosing a fresh install.

## Renamed workflow references

Former local names grill-me, tdd, systematic-debugging and security-audit were
renamed to avoid collisions with optional packs. The current names and intended
uses are in [SKILLS.md](SKILLS.md). An existing global install containing obsolete
reference snapshots needs one `python scripts/install_chat_command.py --upgrade --force`
after inspecting customizations; differing managed files are backed up first.

See [CONFIGURATION.md](CONFIGURATION.md) for package layout and destination overrides,
[VERIFICATION.md](VERIFICATION.md) for evidence limits and [OPTIONAL_SKILLS.md](OPTIONAL_SKILLS.md)
for optional pack commands and prerequisites.
