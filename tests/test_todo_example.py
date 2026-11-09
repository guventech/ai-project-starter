"""Application-boundary checks for the authored (not agent-scored) example."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

APP = Path(__file__).resolve().parents[1] / 'examples/todo_cli/todo.py'


class TodoExampleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='starter-example-')
        self.addCleanup(self.temp.cleanup)
        self.data = Path(self.temp.name) / 'tasks.json'

    def cli(self, *args):
        return subprocess.run([sys.executable, str(APP), '--data', str(self.data), *args],
                              capture_output=True, text=True, timeout=10)

    def test_add_list_and_reject_empty_task(self):
        result = self.cli('add', 'Review proposal')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.cli('list').stdout, '1 [ ] Review proposal\n')
        before = self.data.read_bytes()
        self.assertEqual(self.cli('add', '  ').returncode, 2)
        self.assertEqual(self.data.read_bytes(), before)

    def test_pending_filters_without_changing_data_or_default_output(self):
        records = [{'id': 4, 'text': 'First', 'done': True},
                   {'id': 19, 'text': 'Second', 'done': False}]
        self.data.write_text(json.dumps(records), encoding='utf-8')
        before = self.data.read_bytes()
        self.assertEqual(self.cli('list', '--pending').stdout, '19 [ ] Second\n')
        self.assertEqual(self.cli('list').stdout, '4 [x] First\n19 [ ] Second\n')
        self.assertEqual(self.data.read_bytes(), before)

    def test_invalid_stored_records_are_rejected_without_mutation(self):
        for records in ({}, [{'id': True, 'text': 'Bad', 'done': False}],
                        [{'id': 1, 'text': 'Bad', 'done': 'false'}],
                        [None], [{'id': 1}],
                        [{'id': 1, 'text': '  ', 'done': False}],
                        [{'id': -1, 'text': 'Bad', 'done': False}],
                        [{'id': 1.5, 'text': 'Bad', 'done': False}],
                        [{'id': 1, 'text': 'Bad', 'done': False, 'extra': 1}],
                        [{'id': 1, 'text': 'Bad', 'done': False}] * 2):
            with self.subTest(records=records):
                self.data.write_text(json.dumps(records), encoding='utf-8')
                before = self.data.read_bytes()
                self.assertEqual(self.cli('add', 'New').returncode, 2)
                self.assertEqual(self.data.read_bytes(), before)

    def test_existing_unsorted_ids_and_unreadable_data(self):
        records = [{'id': 19, 'text': 'First', 'done': False},
                   {'id': 4, 'text': 'Second', 'done': False}]
        self.data.write_text(json.dumps(records), encoding='utf-8')
        self.assertEqual(self.cli('add', ' Third ').returncode, 0)
        self.assertEqual(json.loads(self.data.read_text()),
                         records + [{'id': 20, 'text': 'Third', 'done': False}])
        for content in (b'{broken', b'\xff'):
            self.data.write_bytes(content)
            self.assertEqual(self.cli('add', 'New').returncode, 2)
            self.assertEqual(self.data.read_bytes(), content)

    def test_read_or_rejected_command_does_not_create_missing_file(self):
        self.assertEqual(self.cli('list').returncode, 0)
        self.assertEqual(self.cli('done', '1').returncode, 2)
        self.assertEqual(self.cli('add', ' ').returncode, 2)
        self.assertFalse(self.data.exists())

    def test_done_uses_id_and_unknown_id_preserves_bytes(self):
        records = [{'id': 4, 'text': 'First', 'done': False},
                   {'id': 19, 'text': 'Second', 'done': False}]
        self.data.write_text(json.dumps(records), encoding='utf-8')
        result = self.cli('done', '19')
        self.assertEqual(result.returncode, 0, result.stderr)
        records[1]['done'] = True
        self.assertEqual(json.loads(self.data.read_text()), records)
        before = self.data.read_bytes()
        self.assertEqual(self.cli('done', '5').returncode, 2)
        self.assertEqual(self.data.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
