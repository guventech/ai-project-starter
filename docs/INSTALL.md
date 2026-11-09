# Install the project-helper command

Install once from this repository so `/project-helper` works in other folders:

```sh
python scripts/install_chat_command.py
```

Reload Cursor or start a new chat. The installer writes a self-contained package under `~/.cursor/skills/project-helper` (workflows and reviewer roles bundled as references). It needs no Python packages and refuses to replace an existing installation without `--upgrade`.

## Upgrade

| Situation | Command |
|-----------|---------|
| Clean stock package (manifest matches managed files) | `python scripts/install_chat_command.py --upgrade` |
| Pre-manifest install, incomplete/malformed manifest, edited managed files, or renamed skill references | `python scripts/install_chat_command.py --upgrade --force` |
| Extra files beside the managed set | Move extras out, then upgrade; `--force` still refuses extras |

`--force` requires `--upgrade`. Differing managed files are backed up beside the package before replacement. Symlink destinations are refused. Updates are not automatic; a global install does not travel with GitHub template copies.

See [CONFIGURATION.md](CONFIGURATION.md) for package layout, destination overrides and verification limits. Optional upstream pack commands stay in the [README](../README.md#recommended-additional-skills).
