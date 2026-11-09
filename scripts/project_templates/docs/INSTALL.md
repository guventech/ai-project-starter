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

For a clean stock installation use `--upgrade`. For edited files or an invalid
manifest, inspect your customizations before choosing `--upgrade --force`;
differing managed files are backed up first. Extra files still cause refusal.
No update is automatic. The manifest detects accidental edits, not authenticity.
Installation does not grant permission to change another project's instructions.
