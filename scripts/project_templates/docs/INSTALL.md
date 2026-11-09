# Install the project-helper command

The repository-local `/project-helper` is available in Cursor. To install the
bundled workflows for use in other folders:

```sh
python scripts/install_chat_command.py
```

Reload Cursor or start a new chat. Inspect an installation without replacing it:

```sh
python scripts/install_chat_command.py --check
```

Check exit codes: 0 means up to date; 1 means drift or absent installation/manifest;
2 means an invalid manifest, unsupported destination, arguments or read error.
The check compares with this checkout, not a remote release.

For a clean stock installation use `--upgrade`. For edited files, a missing
manifest, incomplete path list or invalid digests in a readable files map, inspect
customizations before choosing `--upgrade --force`; differing files are backed up.
Force still reads the manifest. For unparseable JSON or a missing/non-object files
map, preserve the package by moving it aside after inspection, then fresh-install
at the original destination. Extra files still cause refusal.
No update is automatic. The manifest detects accidental edits, not authenticity.
Installation does not grant permission to change another project's instructions.
Optional external packs and their prerequisites are in [OPTIONAL_SKILLS.md](OPTIONAL_SKILLS.md).
