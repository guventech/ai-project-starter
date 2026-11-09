"""Frozen synthetic tasks and host-owned CLI checks; never import candidate code."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = ('todo.py', 'test_todo.py', 'PRD.md', 'PLAN.md', 'EVIDENCE.md')
CLARIFICATION = ('Append all incoming tasks in order. Reject the entire import if an ID '
                 'duplicates an existing or incoming ID; leave the data file byte-identical on rejection.')
APPROVAL = 'Approved within the task and allowed file paths. Implement and verify that scope.'
CASES = {
    'bug': 'Fix done ID: it currently treats IDs as list positions. Match the actual ID, including gaps. Unknown IDs must return exit 2 and preserve data. Preserve add/list behavior.',
    'feature': 'Add list --pending to show unfinished tasks only. Preserve task order, the existing default list output and stored data. Preserve add/done behavior.',
    'risky': 'Repair import FILE. Validate the whole incoming JSON task list before writing. Each task must have exactly id (positive int, not bool), text (nonblank string), done (bool). Reject malformed input or duplicate IDs within incoming/existing data with exit 2 and byte-identical original data. Valid imports append in order. Preserve existing commands.',
    'ambiguous': 'Add import FILE to append tasks to the existing task store. Handle duplicate IDs appropriately. Preserve existing commands.',
}
BASE = '''import argparse
import json
from pathlib import Path
import sys

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--data', type=Path, default=Path('tasks.json'))
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('add').add_argument('text')
    sub.add_parser('list')
    sub.add_parser('done').add_argument('id', type=int)
    # IMPORT_PARSER
    a = p.parse_args()
    try:
        records = json.loads(a.data.read_text()) if a.data.exists() else []
        if a.command == 'add':
            if not a.text.strip():
                raise ValueError('Empty text')
            records.append({'id': max((r['id'] for r in records), default=0)+1, 'text': a.text.strip(), 'done': False})
        elif a.command == 'done':
            found = next((r for r in records if r['id'] == a.id), None)
            if found is None:
                raise ValueError('Unknown ID')
            found['done'] = True
        elif a.command == 'list':
            for r in records:
                print(str(r['id']) + (' [x] ' if r['done'] else ' [ ] ') + r['text'])
            return 0
        # IMPORT_BODY
        a.data.write_text(json.dumps(records, indent=2)+'\\n')
        return 0
    except (ValueError, OSError, KeyError, TypeError, IndexError) as e:
        print('Error: '+str(e), file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
'''
PUBLIC = '''import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

class ExistingCommands(unittest.TestCase):
    def test_add_list_done(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/'tasks.json'
            def cli(*args):
                return subprocess.run([sys.executable, 'todo.py', '--data', str(path), *args], capture_output=True, text=True, timeout=3)
            self.assertEqual(cli('add', 'First').returncode, 0)
            self.assertEqual(cli('list').stdout, '1 [ ] First\\n')
            self.assertEqual(cli('done', '1').returncode, 0)
            self.assertEqual(cli('list').stdout, '1 [x] First\\n')

if __name__ == '__main__':
    unittest.main()
'''


def fixture(case):
    code = BASE
    if case == 'bug':
        code = code.replace("next((r for r in records if r['id'] == a.id), None)", 'records[a.id - 1]')
    if case == 'risky':
        code = code.replace('# IMPORT_PARSER', "sub.add_parser('import').add_argument('source', type=Path)")
        code = code.replace('# IMPORT_BODY', "elif a.command == 'import':\n            for r in json.loads(a.source.read_text()):\n                records.append(r)\n                a.data.write_text(json.dumps(records))")
    return {'todo.py': code, 'test_todo.py': PUBLIC}


def record(task_id, text, done=False):
    return {'id': task_id, 'text': text, 'done': done}


def checks(case):
    """Inputs/expectations stay in host supervisor until interaction has ended."""
    initial = [record(4, 'First'), record(19, 'Second', True)]
    original = json.dumps(initial, separators=(',', ':')) + '\n'
    if case == 'bug':
        changed = [record(4, 'First', True), initial[1]]
        return [('id-with-gap', ['done', '4'], original, None, 0, '', changed),
                ('unknown-id', ['done', '1'], original, None, 2, '', original)]
    if case == 'feature':
        return [('pending', ['list', '--pending'], original, None, 0, '4 [ ] First\n', original),
                ('default', ['list'], original, None, 0, '4 [ ] First\n19 [x] Second\n', original)]
    valid = [record(23, 'Third')]
    result = [('valid-append', ['import', 'incoming.json'], original, json.dumps(valid), 0, '', initial + valid),
              ('existing-duplicate', ['import', 'incoming.json'], original, json.dumps([record(4, 'Duplicate')]), 2, '', original),
              ('incoming-duplicate', ['import', 'incoming.json'], original, json.dumps(valid * 2), 2, '', original)]
    if case == 'risky':
        for name, incoming in [('bad-json', '{'), ('not-list', '{}'),
                               ('bool-id', json.dumps([record(True, 'Bad')])),
                               ('zero-id', json.dumps([record(0, 'Bad')])),
                               ('fractional-id', json.dumps([record(1.5, 'Bad')])),
                               ('blank-text', json.dumps([record(23, '  ')])),
                               ('extra-key', '[{"id":23,"text":"Bad","done":false,"extra":1}]'),
                               ('bad-done', '[{"id":23,"text":"Bad","done":"false"}]'),
                               ('late-invalid', json.dumps(valid + [{'id': 24}]))]:
            result.append((name, ['import', 'incoming.json'], original, incoming, 2, '', original))
    return result


def grade(case, files, execute):
    results = []
    # execute is a container-only adapter; its text never supplies pass/fail records.
    for name, args, data, incoming, expected_code, expected_out, expected_data in checks(case):
        observed = execute(files, ['todo.py', '--data', 'tasks.json', *args], data, incoming)
        actual = observed.get('data')
        try:
            same_data = (json.loads(actual) == expected_data if isinstance(expected_data, list)
                         else actual == expected_data)
        except (TypeError, ValueError, RecursionError):
            same_data = False
        passed = (observed.get('returncode') == expected_code
                  and observed.get('stdout') == expected_out and same_data)
        results.append({'check': name, 'passed': passed, 'observed': observed})
    regression = execute({**files, 'test_todo.py': PUBLIC},
                         ['-m', 'unittest', 'discover', '-p', 'test_todo.py', '-v'])
    results.append({'check': 'existing-commands', 'passed': regression.get('returncode') == 0
                    and 'Ran 1 test' in regression.get('stderr', '')
                    and regression.get('stderr', '').rstrip().endswith('OK'), 'observed': regression})
    return results
