"""Publish a fresh extracted starter as a PUBLIC GitHub template. Requires gh and git."""
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
def run(*args):
    subprocess.run(args, cwd=ROOT, check=True)

def main():
    if len(sys.argv) != 2 or not re.fullmatch(r'[A-Za-z0-9-]+/[A-Za-z0-9_.-]+', sys.argv[1]):
        raise SystemExit('Usage: python publish-to-github.py OWNER/REPOSITORY (creates a PUBLIC repository)')
    repo = sys.argv[1]
    for command in ('git', 'gh'):
        if not shutil.which(command):
            raise SystemExit(f'Install {command} first.')
    if any((p / '.git').exists() for p in [ROOT, *ROOT.parents]):
        raise SystemExit('Use a fresh extracted copy outside any Git repository. No changes made.')
    run(sys.executable, 'scripts/validate_starter.py')
    run(sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v')
    run('gh', 'auth', 'status', '--hostname', 'github.com')
    print(f'Publishing PUBLIC template: https://github.com/{repo}', flush=True)
    run('git', 'init', '-b', 'main')
    # Stage only template files, never arbitrary files added beside them.
    run('git', 'add', 'AGENTS.md', 'README.md', '.cursor', '.github', 'docs', 'scripts',
        'tests', 'src', '.gitignore', '.gitattributes', '.editorconfig',
        'publish-to-github.py', 'publish-to-github.sh')
    run('git', 'commit', '-m', 'Add Cursor AI project starter')
    run('gh', 'repo', 'create', repo, '--public', '--source', '.', '--remote', 'origin', '--push')
    run('gh', 'repo', 'edit', repo, '--template')
    run('gh', 'repo', 'view', repo, '--json', 'url,isTemplate,visibility')

if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as exc:
        raise SystemExit(f'Command failed ({exc.returncode}). Inspect its output; no remote deletion or overwrite was attempted.')
