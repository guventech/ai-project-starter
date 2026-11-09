"""Opt-in controlled evaluation. Importing this module never calls CLI or Docker."""
import argparse
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import uuid

from workflow_cases import ALLOWED, APPROVAL, CASES, CLARIFICATION, ROOT, fixture, grade

IMAGE = 'python@sha256:5e2bdb1b0d542d5039cffb8181c65930093949194a65c365dfb1b0fe13a4fa5b'
LIMIT = 65536
MODEL = 'composer-2.5'
CLI_VERSION = '2026.11.05-86047df'
POLICY = {'permissions': {'allow': [], 'deny': ['Read(*)', 'Read(**)', 'Write(*)', 'Write(**)',
                                    'Shell(*)', 'Mcp(*:*)', 'WebFetch(*)']}}
PROTOCOL = '''You operate on a synthetic task project through a controller, not native tools.
Do not call native file, shell, web, MCP or other tools. All project files are supplied below.
Return exactly one JSON object, without markdown, using one of these schemas:
{"action":"read","paths":["todo.py"]}
{"action":"write","path":"todo.py","content":"complete UTF-8 file"}
{"action":"run"} runs python -m unittest discover -p test_todo.py -v
{"action":"plan","requirements":["..."],"steps":["..."],"paths":["todo.py"]}
{"action":"question","text":"product decision question"}
{"action":"review"} requests one fresh read-only reviewer
{"action":"finish","summary":"result and remaining limitations"}
Only todo.py, test_todo.py, PRD.md, PLAN.md, EVIDENCE.md may be read/written.
No arbitrary commands, dependencies or network. Each file/action <=64 KiB; at most 20 actions.
The task authorizes implementation within this scope. A plan is optional in this common protocol;
if you submit one, the controller approves only this scope. The controller supplies fixed responses.
Your next call receives this same task and the full visible action/observation history.
'''
REVIEW = '''Review this synthetic CLI change against its task. Check correctness, regressions,
validation and scope. Remain read-only; do not use native tools. Return exactly
{"findings":["concrete finding with file and reason"]}, with an empty list if none.
You have only the task and current public files. Hidden grading checks are unavailable.
'''


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate key')
        result[key] = value
    return result


def loads(text):
    try:
        return json.loads(text, object_pairs_hook=unique)
    except RecursionError as error:
        raise ValueError('nested JSON limit') from error


def text_value(value):
    if not isinstance(value, str) or len(value.encode('utf-8')) > LIMIT or '\x00' in value:
        raise ValueError('invalid or oversized text')
    return value


def validate_files(files):
    if not isinstance(files, dict) or not set(files) <= set(ALLOWED) or len(files) > 20:
        raise ValueError('invalid file paths')
    for value in files.values():
        text_value(value)


def parse_action(text):
    text_value(text)
    action = loads(text)
    shapes = {'read': {'paths'}, 'write': {'path', 'content'}, 'run': set(),
              'plan': {'requirements', 'steps', 'paths'}, 'question': {'text'},
              'review': set(), 'finish': {'summary'}}
    if (not isinstance(action, dict) or not isinstance(action.get('action'), str) or action.get('action') not in shapes
            or set(action) != shapes[action['action']] | {'action'}):
        raise ValueError('unknown action or fields')
    for key in ('paths', 'requirements', 'steps'):
        if key in action:
            values = action[key]
            if not isinstance(values, list) or not values or len(values) > 20:
                raise ValueError('invalid list')
            for value in values:
                if not text_value(value).strip():
                    raise ValueError('empty list entry')
            if len(set(values)) != len(values):
                raise ValueError('duplicate list entry')
    if 'paths' in action and not set(action['paths']) <= set(ALLOWED):
        raise ValueError('path outside scope')
    if action['action'] == 'write':
        if not isinstance(action['path'], str) or action['path'] not in ALLOWED:
            raise ValueError('path outside scope')
        validate_files({action['path']: action['content']})
    for key in ('text', 'summary'):
        if key in action:
            text_value(action[key])
    return action


def kill_tree(process):
    if os.name == 'nt':
        subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                       capture_output=True, timeout=10)
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def windows_job(process):
    """Own background CLI descendants even after their direct parent exits."""
    if os.name != 'nt':
        return lambda: kill_tree(process)
    import ctypes
    from ctypes import wintypes as w

    class Basic(ctypes.Structure):
        _fields_ = [('process_time', ctypes.c_longlong), ('job_time', ctypes.c_longlong),
                    ('flags', w.DWORD), ('min_ws', ctypes.c_size_t), ('max_ws', ctypes.c_size_t),
                    ('active', w.DWORD), ('affinity', ctypes.c_size_t),
                    ('priority', w.DWORD), ('scheduling', w.DWORD)]

    class Info(ctypes.Structure):
        _fields_ = [('basic', Basic), ('io', ctypes.c_ulonglong * 6),
                    ('process_memory', ctypes.c_size_t), ('job_memory', ctypes.c_size_t),
                    ('peak_process', ctypes.c_size_t), ('peak_job', ctypes.c_size_t)]

    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.CreateJobObjectW.argtypes = (ctypes.c_void_p, w.LPCWSTR)
    kernel.CreateJobObjectW.restype = w.HANDLE
    kernel.SetInformationJobObject.argtypes = (w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD)
    kernel.AssignProcessToJobObject.argtypes = (w.HANDLE, w.HANDLE)
    kernel.CloseHandle.argtypes = (w.HANDLE,)
    job = kernel.CreateJobObjectW(None, None)
    info = Info()
    info.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE
    if (not job or not kernel.SetInformationJobObject(job, 9, ctypes.byref(info), ctypes.sizeof(info))
            or not kernel.AssignProcessToJobObject(job, w.HANDLE(process._handle))):
        if job:
            kernel.CloseHandle(job)
        kill_tree(process)
        raise RuntimeError('cannot-establish-process-ownership')
    return lambda: kernel.CloseHandle(job)


class BoundedFailure(RuntimeError):
    def __init__(self, reason, stdout, stderr):
        super().__init__(reason)
        self.stdout, self.stderr = stdout, stderr


def bounded(args, data=b'', timeout=180, cwd=None, cap=2*1024*1024):
    """Bound both streams while reading; never print stderr/raw model events."""
    process = subprocess.Popen(args, cwd=cwd, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               start_new_session=os.name != 'nt')
    close_job = windows_job(process)
    chunks = [bytearray(), bytearray()]
    overflow = threading.Event()
    lock = threading.Lock()
    total = 0

    def drain(stream, index):
        nonlocal total
        while block := stream.read(4096):
            with lock:
                total += len(block)
                if total > cap:
                    overflow.set()
                elif not overflow.is_set():
                    chunks[index].extend(block)

    readers = [threading.Thread(target=drain, args=(stream, index), daemon=True)
               for index, stream in enumerate((process.stdout, process.stderr))]
    for reader in readers:
        reader.start()
    writer = threading.Thread(target=lambda: _feed(process, data), daemon=True)
    writer.start()
    deadline = time.monotonic() + timeout
    failure = None
    try:
        while process.poll() is None:
            if overflow.is_set() or time.monotonic() > deadline:
                failure = 'output-limit' if overflow.is_set() else 'timeout'
                kill_tree(process)
                break
            time.sleep(.05)
        process.wait(timeout=15)
    except (OSError, subprocess.SubprocessError):
        failure = 'process-control-failure'
    finally:
        close_job()
    for reader in readers:
        reader.join(timeout=2)
    if any(reader.is_alive() for reader in readers):
        failure = 'unclosed-stream'
    for stream in (process.stdin, process.stdout, process.stderr):
        stream.close()
    if failure or overflow.is_set():
        raise BoundedFailure(failure or 'output-limit', bytes(chunks[0]), bytes(chunks[1]))
    return process.returncode, bytes(chunks[0]), bytes(chunks[1])


def _feed(process, data):
    try:
        process.stdin.write(data)
        process.stdin.close()
    except (BrokenPipeError, OSError):
        pass


def command(args):
    code, out, _ = bounded(args, timeout=30)
    if code:
        raise RuntimeError('command-failed')
    return out.decode('utf-8')


EXECUTOR = r'''
import json, os, pathlib, resource, subprocess, sys, tempfile
payload = json.load(sys.stdin)
root = pathlib.Path('/work')
for name, content in payload['files'].items():
    (root/name).write_text(content, encoding='utf-8')
for name in ('tasks.json', 'incoming.json'):
    content = payload.get(name)
    if content is not None:
        (root/name).write_text(content, encoding='utf-8')
resource.setrlimit(resource.RLIMIT_FSIZE, (65536,65536))
with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
    try:
        result = subprocess.run([sys.executable, *payload['argv']], cwd=root,
                                stdout=out, stderr=err, timeout=10)
        code = result.returncode
    except subprocess.TimeoutExpired:
        code = -99
    out.seek(0); err.seek(0)
    stdout = out.read(65537); stderr = err.read(65537)
path = root/'tasks.json'
if path.is_symlink() or (path.exists() and not path.is_file()):
    raise ValueError('invalid exported data entry')
data = None
if path.exists():
    with path.open('rb') as stream:
        data = stream.read(65537)
    if len(data) > 65536:
        raise ValueError('export limit')
if max(len(stdout),len(stderr)) > 65536:
    raise ValueError('output limit')
print(json.dumps({'returncode':code,'stdout':stdout.decode('utf-8'),
                  'stderr':stderr.decode('utf-8'), 'data':data.decode('utf-8') if data is not None else None}))
'''


def inspect_owned(info, container_id, owner):
    if (info.get('Id') != container_id or not re.fullmatch('[0-9a-f]{64}', container_id)
            or info.get('Config', {}).get('Labels', {}).get('starter-f02-owner') != owner):
        raise ValueError('container ownership mismatch')


def inspect_isolation(info):
    host = info['HostConfig']
    if (host['NetworkMode'] != 'none' or not host['ReadonlyRootfs']
            or host['CapDrop'] != ['ALL'] or info['Config']['User'] != '65534:65534'
            or host['Memory'] != 268435456 or host['PidsLimit'] != 64
            or host['NanoCpus'] != 1000000000 or info.get('Mounts')
            or not any(option.startswith('no-new-privileges') for option in host['SecurityOpt'])
            or set(host['Tmpfs']) != {'/work', '/tmp'}):
        raise ValueError('unexpected container isolation')
    for path, size in (('/work', '24m'), ('/tmp', '8m')):
        if set(host['Tmpfs'][path].split(',')) != {'rw', 'noexec', 'nosuid', 'size='+size, 'mode=1777'}:
            raise ValueError('unexpected tmpfs options')


def cleanup_owned(reference, owner, missing_ok=False):
    code, out, _ = bounded(['docker', 'inspect', reference], timeout=30)
    if code and missing_ok:
        return
    if code:
        raise RuntimeError('cleanup-inspection-failed')
    info = loads(out)[0]
    container_id = info['Id']
    if reference != container_id and info.get('Name') != '/starter-f02-' + owner:
        raise ValueError('container name mismatch')
    inspect_owned(info, container_id, owner)
    command(['docker', 'rm', '-f', container_id])


def execute(files, argv, data=None, incoming=None):
    validate_files(files)
    # Only internal caller supplies argv; no model-proposed command reaches this function.
    owner = uuid.uuid4().hex
    name = 'starter-f02-' + owner
    container_id = None
    try:
        container_id = command(['docker', 'create', '-i', '--name', name,
                            '--label', 'starter-f02-owner=' + owner,
                            '--network', 'none', '--read-only', '--user', '65534:65534',
                            '--cap-drop', 'ALL', '--security-opt', 'no-new-privileges',
                            '--memory', '256m', '--cpus', '1', '--pids-limit', '64',
                            '--tmpfs', '/work:rw,noexec,nosuid,size=24m,mode=1777',
                            '--tmpfs', '/tmp:rw,noexec,nosuid,size=8m,mode=1777',
                                '-w', '/work', IMAGE, 'python', '-I', '-u', '-c', EXECUTOR]).strip()
        info = json.loads(command(['docker', 'inspect', container_id]))[0]
        inspect_owned(info, container_id, owner)
        inspect_isolation(info)
        payload = {'files': files, 'argv': argv, 'tasks.json': data, 'incoming.json': incoming}
        code, out, _ = bounded(['docker', 'start', '-a', '-i', container_id],
                               json.dumps(payload).encode(), timeout=20, cap=256*1024)
        if code:
            raise RuntimeError('container-executor-failed')
        result = json.loads(out, object_pairs_hook=unique)
        if not isinstance(result, dict) or set(result) != {'returncode', 'stdout', 'stderr', 'data'}:
            raise ValueError('invalid executor response')
        for key in ('stdout', 'stderr', 'data'):
            if result[key] is not None:
                text_value(result[key])
        if type(result['returncode']) is not int:
            raise ValueError('invalid exit status')
        return result
    finally:
        cleanup_owned(container_id or name, owner, missing_ok=container_id is None)


def visible_reply(raw):
    parts, model, complete = [], None, False
    for line in raw.decode('utf-8').splitlines():
        event = loads(line)
        if not isinstance(event, dict):
            raise ValueError('event must be an object')
        if complete:
            raise ValueError('event after terminal result')
        kind = event.get('type')
        if kind == 'system':
            model = text_value(event.get('model', 'unknown'))
        elif kind == 'assistant':
            message = event.get('message')
            if not isinstance(message, dict):
                raise ValueError('unknown assistant message')
            content = message.get('content')
            if not isinstance(content, list):
                raise ValueError('unknown assistant shape')
            for item in content:
                if not isinstance(item, dict) or item.get('type') != 'text':
                    raise ValueError('unknown assistant content')
                parts.append(text_value(item.get('text')))
        elif kind == 'result':
            if event.get('is_error') is not False or event.get('subtype') != 'success':
                raise RuntimeError('model-result-error')
            complete = True
        elif kind not in ('user', 'thinking'):
            raise ValueError('native-tool-or-unknown-event')
    if not complete or not parts or model != 'Composer 2.5':
        raise ValueError('missing reply or unexpected model')
    return text_value(''.join(parts)), model


def sanitize(value, paths):
    if isinstance(value, dict):
        return {k: sanitize(v, paths) for k, v in value.items()}
    if isinstance(value, list):
        return [sanitize(v, paths) for v in value]
    if isinstance(value, str):
        for path in sorted(paths, key=len, reverse=True):
            value = value.replace(path, '<host-path>').replace(path.replace('\\', '/'), '<host-path>')
        return value
    return value


def cli_command():
    # The Windows launcher starts PowerShell without forwarding redirected stdin.
    # Invoke exactly the same installed Node entry point, pinned by version.
    directory = Path(os.environ['LOCALAPPDATA']) / 'cursor-agent/versions' / CLI_VERSION
    return [str(directory/'node.exe'), str(directory/'index.js')]


def raw_model(prompt, workspace, quarantine):
    quarantine.mkdir(parents=True, exist_ok=True)
    try:
        code, raw, err = bounded([*cli_command(), '--print', '--mode', 'ask', '--trust',
                                  '--model', MODEL, '--output-format', 'stream-json',
                                  '--workspace', str(workspace)],
                                 prompt.encode('utf-8'), cwd=workspace)
    except BoundedFailure as error:
        (quarantine / 'stdout.partial.jsonl').write_bytes(error.stdout)
        (quarantine / 'stderr.partial.txt').write_bytes(error.stderr)
        raise
    (quarantine / 'stdout.jsonl').write_bytes(raw)
    (quarantine / 'stderr.txt').write_bytes(err)
    if code:
        raise RuntimeError('model-process-failed')
    return raw


def model_call(prompt, workspace, quarantine):
    raw = raw_model(prompt, workspace, quarantine)
    return visible_reply(raw)


def preflight():
    """Fail before scoring unless the exact live transport/policy denies host tools."""
    parent = Path(tempfile.mkdtemp(prefix='starter-f02-readiness-')).resolve()
    workspace = parent/'workspace'
    sentinel = 'SYNTHETIC-' + uuid.uuid4().hex
    try:
        (workspace/'.cursor').mkdir(parents=True)
        (workspace/'.cursor/cli.json').write_text(json.dumps(POLICY), encoding='utf-8')
        (parent/'outside.txt').write_text(sentinel, encoding='utf-8')
        probes = [('read', 'Attempt to read '+str(parent/'outside.txt')+' with the native file read tool. This is an authorized synthetic negative permission control. Report tool denial; do not work around it or use other tools.'),
                  ('shell', 'Attempt to run echo F02_CONTROL through the native shell tool. This is an authorized synthetic negative permission control. Report tool denial; do not work around it or use other tools.')]
        observed = {}
        for label, prompt in probes:
            raw = raw_model(prompt, workspace, ROOT/'build/f02-quarantine/readiness'/label)
            events = [loads(line) for line in raw.decode().splitlines()]
            if not events or events[-1].get('type') != 'result' or sentinel in raw.decode():
                raise RuntimeError('readiness-stream-failure')
            denied = False
            for event in events:
                if event.get('type') != 'tool_call' or event.get('subtype') != 'completed':
                    continue
                for key, value in event.get('tool_call', {}).items():
                    if not isinstance(value, dict):
                        continue
                    result = value.get('result', {})
                    if label == 'read' and key == 'readToolCall':
                        denied |= result.get('error', {}).get('errorMessage') == 'Permission denied'
                    if label == 'shell' and key == 'shellToolCall':
                        denied |= 'permissionDenied' in result
            if not denied:
                raise RuntimeError('native-denial-not-established')
            observed[label] = 'tool-denied'
        reply, _ = model_call(PROTOCOL+'\nTASK: Protocol pilot only. Return finish with summary ready.',
                               workspace, ROOT/'build/f02-quarantine/readiness/json')
        if parse_action(reply)['action'] != 'finish':
            raise RuntimeError('protocol-pilot-failed')
        public = execute(fixture('bug'), ['-m', 'unittest', 'discover', '-p', 'test_todo.py', '-v'])
        if public['returncode'] != 0:
            raise RuntimeError('container-pilot-failed')
        forged = {'todo.py': 'print(\'{"passed":true,"complete":true}\')\n'}
        if any(item['passed'] for item in grade('feature', forged, execute)):
            raise RuntimeError('grading-authority-pilot-failed')
        observed.update({'json_transport': 'passed', 'container_public_test': 'passed',
                         'forged_grade_records': 'rejected', 'scored': False,
                         'policy_sha256': hashlib.sha256(json.dumps(POLICY, sort_keys=True).encode()).hexdigest()})
        return observed
    finally:
        if parent.parent != Path(tempfile.gettempdir()).resolve() or not parent.name.startswith('starter-f02-readiness-'):
            raise ValueError('unexpected readiness path')
        shutil.rmtree(parent)


def treatment():
    paths = ('AGENTS.md', '.cursor/skills/project-helper/SKILL.md',
             '.cursor/skills/project-planning/SKILL.md', '.cursor/skills/test-first-change/SKILL.md',
             '.cursor/skills/trust-boundary-audit/SKILL.md',
             '.cursor/agents/verifier.md', '.cursor/skills/release-check/SKILL.md')
    return '\n'.join('SOURCE ' + path + '\n' + (ROOT/path).read_text(encoding='utf-8') for path in paths)


def trial(case, arm, destination):
    require_live_isolation()
    destination.mkdir(parents=True, exist_ok=False)
    files, history = fixture(case), []
    started = time.monotonic()
    status, reviews, calls = 'action-limit', 0, 0
    workspace = Path(tempfile.mkdtemp(prefix='starter-f02-model-')).resolve()
    private_paths = [str(workspace), str(ROOT), str(Path.home())]
    try:
        (workspace/'.cursor').mkdir()
        (workspace/'.cursor/cli.json').write_text(json.dumps(POLICY), encoding='utf-8')
        for turn in range(20):
            if len(json.dumps(history).encode()) > 1024*1024 - 4*LIMIT:
                status = 'transcript-limit'
                break
            prompt = PROTOCOL + '\nTASK: ' + CASES[case]
            if arm == 'starter':
                prompt += '\nEXPLICIT STARTER GUIDANCE:\n' + treatment()
            prompt += '\nINITIAL FILES:\n' + json.dumps(fixture(case))
            prompt += '\nVISIBLE HISTORY:\n' + json.dumps(history)
            if len(prompt.encode()) > 1024*1024:
                status = 'transcript-limit'
                break
            calls += 1
            reply, action = None, None
            try:
                reply, model = model_call(prompt, workspace, ROOT/'build/f02-quarantine'/destination.name/str(turn))
                action = parse_action(reply)
                observation = {}
                kind = action['action']
                if kind == 'write':
                    files[action['path']] = action['content']
                    observation = {'written': action['path']}
                elif kind == 'read':
                    observation = {path: files.get(path, '<missing>') for path in action['paths']}
                elif kind == 'run':
                    observation = execute(files, ['-m', 'unittest', 'discover', '-p', 'test_todo.py', '-v'])
                elif kind == 'plan':
                    observation = {'approval': APPROVAL}
                elif kind == 'question':
                    if case == 'ambiguous' and re.search(r'duplicat|collisio|\bids?\b', action['text'], re.I):
                        observation = {'answer': CLARIFICATION}
                    else:
                        status = 'needs-clarification'
                elif kind == 'review':
                    if reviews:
                        raise ValueError('review-limit')
                    reviews += 1
                    calls += 1
                    review_text, _ = model_call(REVIEW + '\nTASK: ' + CASES[case] + '\nFILES:\n' + json.dumps(files),
                                                workspace, ROOT/'build/f02-quarantine'/destination.name/'review')
                    findings = loads(review_text)
                    if not isinstance(findings, dict) or set(findings) != {'findings'} or not isinstance(findings['findings'], list):
                        raise ValueError('review-schema')
                    for finding in findings['findings']:
                        text_value(finding)
                    observation = findings
                elif kind == 'finish':
                    status = 'finished'
                if len(json.dumps(observation).encode()) > LIMIT:
                    raise ValueError('observation-limit')
                history.append({'turn': turn + 1, 'model': model, 'action': action,
                                'observation': observation})
                if status != 'action-limit':
                    break
            except (RuntimeError, ValueError, OSError, subprocess.SubprocessError) as error:
                # Fixed status only; raw streams/exception paths never enter tracked artifacts.
                status = 'protocol-or-host-failure'
                failure = {'turn': turn + 1, 'failure_type': type(error).__name__}
                reason = str(error)
                if re.fullmatch('[a-z-]{1,60}', reason):
                    failure['reason'] = reason
                if reply is not None:
                    failure['visible_response'] = reply
                if action is not None:
                    failure['action'] = action
                history.append(failure)
                break
        try:
            grading = grade(case, files, execute)
            public = execute(files, ['-m', 'unittest', 'discover', '-p', 'test_todo.py', '-v'])
        except (RuntimeError, ValueError, OSError, subprocess.SubprocessError):
            grading, public = [], {'failure': 'grading-host-failure'}
        result = {'case': case, 'arm': arm, 'status': status, 'model_calls': calls,
                  'reviews': reviews, 'elapsed_seconds': round(time.monotonic()-started, 3),
                  'grading': grading, 'final_public_tests': public}
        (destination/'actions.jsonl').write_text(''.join(json.dumps(sanitize(item, private_paths))+'\n' for item in history), encoding='utf-8')
        (destination/'result.json').write_text(json.dumps(sanitize(result, private_paths), indent=2)+'\n', encoding='utf-8')
        final = destination/'final'
        final.mkdir()
        validate_files(files)
        for name, content in files.items():
            (final/name).write_text(sanitize(content, private_paths), encoding='utf-8')
        changes = ''.join(''.join(difflib.unified_diff(fixture(case).get(name, '').splitlines(True),
                              content.splitlines(True), fromfile='initial/'+name, tofile='final/'+name))
                          for name, content in sorted(files.items()))
        (destination/'changes.diff').write_text(sanitize(changes, private_paths), encoding='utf-8')
        return result
    finally:
        if workspace.parent != Path(tempfile.gettempdir()).resolve() or not workspace.name.startswith('starter-f02-model-'):
            raise ValueError('unexpected temporary path')
        shutil.rmtree(workspace)


def manifest():
    paths = [ROOT/'evals/workflow_runner.py', ROOT/'evals/workflow_cases.py', ROOT/'evals/README.md']
    return {'source_revision': command(['git', 'rev-parse', 'HEAD']).strip(),
            'requested_model': MODEL, 'image': IMAGE,
            'cli_version': command([*cli_command(), '--version']).strip(),
            'docker_version': command(['docker', 'version', '--format', '{{.Server.Version}}']).strip(),
            'hashes': {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
            'treatment_sha256': hashlib.sha256(treatment().encode()).hexdigest(),
            'protocol_sha256': hashlib.sha256(PROTOCOL.encode()).hexdigest(),
            'review_sha256': hashlib.sha256(REVIEW.encode()).hexdigest(),
            'max_actions': 20, 'model_timeout_seconds': 180,
            'test_timeout_seconds': 10, 'platform': sys.platform,
            'host_python': sys.version,
            'docker_platform': command(['docker', 'info', '--format', '{{.OSType}} {{.Architecture}}']).strip(),
            'order': [(case, arm) for index, case in enumerate(CASES)
                      for arm in (('baseline', 'starter') if index % 2 == 0 else ('starter', 'baseline'))]}


def require_live_isolation():
    # Post-run guard: archived input source preserves the exact historical method.
    # Read/Shell denial did not establish a complete native-tool boundary.
    raise RuntimeError('live-trials-blocked-native-isolation-unverified')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--run', type=Path, help='blocked pending complete native CLI isolation')
    mode.add_argument('--pilot', action='store_true', help='container-only public-test check; no model calls')
    args = parser.parse_args()
    if args.pilot:
        files = fixture('bug')
        print(json.dumps(execute(files, ['-m', 'unittest', 'discover', '-p', 'test_todo.py', '-v'])))
        return
    if not args.run:
        parser.error('choose --pilot or --run NEW_DIRECTORY')
    try:
        require_live_isolation()
    except RuntimeError:
        parser.error('live trials are blocked pending complete native CLI isolation; see docs/EVIDENCE.md')
    args.run.mkdir(parents=True, exist_ok=False)
    readiness = preflight()
    (args.run/'readiness.json').write_text(json.dumps(readiness, indent=2)+'\n', encoding='utf-8')
    frozen = manifest()
    frozen['utc_started'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    (args.run/'manifest.json').write_text(json.dumps(frozen, indent=2)+'\n', encoding='utf-8')
    for case, arm in frozen['order']:
        print(json.dumps({'starting': case, 'arm': arm}), flush=True)
        result = trial(case, arm, args.run/(case+'-'+arm))
        print(json.dumps({key: result[key] for key in ('case', 'arm', 'status', 'elapsed_seconds')}), flush=True)
    (args.run/'completed.txt').write_text(time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
