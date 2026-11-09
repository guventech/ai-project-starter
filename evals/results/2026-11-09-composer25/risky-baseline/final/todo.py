import argparse
import json
from pathlib import Path
import sys


def _validate_task(obj):
    if not isinstance(obj, dict) or set(obj.keys()) != {'id', 'text', 'done'}:
        raise ValueError('Invalid task')
    task_id = obj['id']
    if type(task_id) is not int or task_id <= 0:
        raise ValueError('Invalid id')
    text = obj['text']
    if not isinstance(text, str) or not text.strip():
        raise ValueError('Invalid text')
    done = obj['done']
    if type(done) is not bool:
        raise ValueError('Invalid done')
    return {'id': task_id, 'text': text.strip(), 'done': done}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--data', type=Path, default=Path('tasks.json'))
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('add').add_argument('text')
    sub.add_parser('list')
    sub.add_parser('done').add_argument('id', type=int)
    sub.add_parser('import').add_argument('source', type=Path)
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
        elif a.command == 'import':
            incoming = json.loads(a.source.read_text())
            if not isinstance(incoming, list):
                raise ValueError('Invalid import data')
            validated = []
            seen_incoming = set()
            for item in incoming:
                task = _validate_task(item)
                if task['id'] in seen_incoming:
                    raise ValueError('Duplicate ID')
                seen_incoming.add(task['id'])
                validated.append(task)
            existing_ids = {r['id'] for r in records}
            for task in validated:
                if task['id'] in existing_ids:
                    raise ValueError('Duplicate ID')
                existing_ids.add(task['id'])
            records.extend(validated)
        a.data.write_text(json.dumps(records, indent=2)+'\n')
        return 0
    except (ValueError, OSError, KeyError, TypeError, IndexError) as e:
        print('Error: '+str(e), file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
