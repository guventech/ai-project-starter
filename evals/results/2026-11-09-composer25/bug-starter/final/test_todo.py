import json
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
            self.assertEqual(cli('list').stdout, '1 [ ] First\n')
            self.assertEqual(cli('done', '1').returncode, 0)
            self.assertEqual(cli('list').stdout, '1 [x] First\n')

if __name__ == '__main__':
    unittest.main()
