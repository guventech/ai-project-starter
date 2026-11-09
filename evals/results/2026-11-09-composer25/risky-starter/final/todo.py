import argparse
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
            for r in json.loads(a.source.read_text()):
                records.append(r)
                a.data.write_text(json.dumps(records))
        a.data.write_text(json.dumps(records, indent=2)+'\n')
        return 0
    except (ValueError, OSError, KeyError, TypeError, IndexError) as e:
        print('Error: '+str(e), file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
