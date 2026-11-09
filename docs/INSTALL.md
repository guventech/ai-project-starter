# Install the project-helper command

Install once from this repository so `/project-helper` works in other folders:

```sh
python scripts/install_chat_command.py
```

Reload Cursor or start a new chat. The installer writes a self-contained package under `~/.cursor/skills/project-helper` (workflows and reviewer roles bundled as references). It needs no Python packages and refuses to replace an existing installation without `--upgrade`.

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

| Situation | Command |
|-----------|---------|
| Clean stock package (manifest matches managed files) | `python scripts/install_chat_command.py --upgrade` |
| Pre-manifest install, incomplete/malformed manifest, edited managed files, or renamed skill references | `python scripts/install_chat_command.py --upgrade --force` |
| Extra files beside the managed set | Move extras out, then upgrade; `--force` still refuses extras |

`--force` requires `--upgrade`. Differing managed files are backed up beside the package before replacement. Symlink destinations are refused. Updates are not automatic; a global install does not travel with GitHub template copies.

See [CONFIGURATION.md](CONFIGURATION.md) for package layout, destination overrides and verification limits. Optional upstream pack commands stay in the [README](../README.md#recommended-additional-skills).
