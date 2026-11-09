import hashlib
import json
from pathlib import Path
import sys
import unittest

EVALS = Path(__file__).resolve().parents[1] / 'evals'
sys.path.insert(0, str(EVALS))
import workflow_cases as cases
import workflow_runner as runner


class EvaluationTests(unittest.TestCase):
    def test_live_trials_refuse_before_any_side_effect(self):
        from unittest.mock import patch
        with patch.object(runner, 'model_call') as model, patch.object(runner, 'execute') as docker:
            with self.assertRaisesRegex(RuntimeError, 'live-trials-blocked'):
                runner.trial('bug', 'baseline', None)
        model.assert_not_called()
        docker.assert_not_called()

    def test_live_run_cli_refuses_before_creating_results(self):
        from contextlib import redirect_stderr
        from io import StringIO
        from unittest.mock import patch
        with patch.object(sys, 'argv', ['workflow_runner.py', '--run', 'unused']), \
                patch.object(Path, 'mkdir') as mkdir, patch.object(runner, 'preflight') as preflight, \
                redirect_stderr(StringIO()):
            with self.assertRaises(SystemExit) as stopped:
                runner.main()
        self.assertEqual(stopped.exception.code, 2)
        mkdir.assert_not_called()
        preflight.assert_not_called()

    def test_historical_inputs_match_frozen_manifest(self):
        root = EVALS/'results/2026-11-09-composer25'
        manifest = json.loads((root/'manifest.json').read_text(encoding='utf-8'))
        inputs = json.loads((root/'inputs.json').read_text(encoding='utf-8'))
        for name, digest in manifest['hashes'].items():
            self.assertEqual(hashlib.sha256(inputs[name].encode()).hexdigest(), digest, name)
        for name, field in [('treatment.txt', 'treatment_sha256'), ('protocol.txt', 'protocol_sha256'), ('review.txt', 'review_sha256')]:
            self.assertEqual(hashlib.sha256(inputs[name].encode()).hexdigest(), manifest[field])

    def test_action_rejects_traversal_duplicates_unknown_fields_and_oversize(self):
        for value in ('{"action":"write","path":"../escape","content":"x"}',
                      '{"action":[]}',
                      '{"action":"write","path":[],"content":"x"}',
                      '{"action":"finish","action":"run","summary":"x"}',
                      '{"action":"shell","command":"echo x"}',
                      '{"action":"finish","summary":"x","extra":true}',
                      '{"action":"write","path":"todo.py","content":"' + 'x' * 65537 + '"}'):
            with self.subTest(value=value[:80]), self.assertRaises(ValueError):
                runner.parse_action(value)

    def test_forged_grading_records_do_not_pass(self):
        def forged(*args):
            return {'returncode': 0, 'stdout': '{"passed":true,"complete":true}', 'data': '[]'}
        for case in cases.CASES:
            self.assertFalse(any(item['passed'] for item in cases.grade(case, {}, forged)))

    def test_only_visible_known_text_is_published(self):
        import json
        events = [{'type': 'system', 'model': 'Composer 2.5', 'session_id': 'private-id'},
                  {'type': 'thinking', 'text': 'PRIVATE_REASONING'},
                  {'type': 'user', 'message': 'private echo'},
                  {'type': 'assistant', 'message': {'content': [{'type': 'text', 'text': '{"action":"run"}'}]}},
                  {'type': 'result', 'subtype': 'success', 'is_error': False}]
        raw = '\n'.join(json.dumps(event) for event in events).encode()
        self.assertEqual(runner.visible_reply(raw), ('{"action":"run"}', 'Composer 2.5'))
        for event in ({'type': 'tool_call'}, {'type': 'unknown'},
                      {'type': 'assistant', 'message': {'content': [{'type': 'image', 'data': 'secret'}]}}):
            with self.subTest(event=event), self.assertRaises(ValueError):
                runner.visible_reply(raw + b'\n' + json.dumps(event).encode())
        with self.assertRaises(ValueError):
            runner.visible_reply(raw + b'\n{"truncated"')
        for bad in (b'null\n', b'{"type":"assistant","message":null}\n',
                    '\n'.join(json.dumps(event) for event in events[:-1]).encode()):
            with self.subTest(bad=bad[:80]), self.assertRaises(ValueError):
                runner.visible_reply(bad)
        large = [events[0], {'type': 'assistant', 'message': {'content':
                    [{'type': 'text', 'text': 'x'*40000}, {'type': 'text', 'text': 'x'*40000}]}}, events[-1]]
        with self.assertRaisesRegex(ValueError, 'oversized'):
            runner.visible_reply('\n'.join(json.dumps(event) for event in large).encode())

    def test_cleanup_refuses_wrong_container_or_owner(self):
        info = {'Id': 'a'*64, 'Config': {'Labels': {'starter-f02-owner': 'owned'}}}
        runner.inspect_owned(info, 'a'*64, 'owned')
        for container_id, owner in [('b'*64, 'owned'), ('a'*64, 'wrong')]:
            with self.subTest(owner=owner), self.assertRaises(ValueError):
                runner.inspect_owned(info, container_id, owner)

    def test_stream_bounds_and_timeout_are_failures(self):
        with self.assertRaisesRegex(runner.BoundedFailure, 'output-limit') as overflow:
            runner.bounded([sys.executable, '-c', 'print("x"*20000)'], cap=1000)
        self.assertLessEqual(len(overflow.exception.stdout) + len(overflow.exception.stderr), 1000)
        with self.assertRaisesRegex(runner.BoundedFailure, 'timeout') as timeout:
            runner.bounded([sys.executable, '-c', 'import time; print("partial",flush=True); time.sleep(5)'], timeout=.5)
        self.assertIn(b'partial', timeout.exception.stdout)


if __name__ == '__main__':
    unittest.main()
