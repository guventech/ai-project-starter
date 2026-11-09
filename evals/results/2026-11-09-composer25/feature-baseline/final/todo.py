import argparse
import json
from pathlib import Path
import sys

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--data', type=Path, default=Path('tasks.json'))
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('add').add_argument('text')
    list_parser = sub.add_parser('list')
    list_parser.add_argument('--pending', action='store_true')
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
                if a.pending and r['done']:
                    continue
                print(str(r['id']) + (' [x] ' if r['done'] else ' [ ] ') + r['text'])
            return 0
        # IMPORT_BODY
        a.data.write_text(json.dumps(records, indent=2)+'\n')
        return 0
    except (ValueError, OSError, KeyError, TypeError, IndexError) as e:
        print('Error: '+str(e), file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
