"""Small worked example; see README.md for scope and evidence."""
import argparse
import json
from pathlib import Path
import sys


def load(path):
    if not path.exists():
        return []
    records = json.loads(path.read_text(encoding='utf-8'))
    if not isinstance(records, list):
        raise ValueError('Expected a task list')
    seen = set()
    for item in records:
        if (not isinstance(item, dict) or set(item) != {'id', 'text', 'done'}
                or type(item['id']) is not int or item['id'] < 1
                or not isinstance(item['text'], str) or not item['text'].strip()
                or type(item['done']) is not bool or item['id'] in seen):
            raise ValueError('Invalid task record')
        seen.add(item['id'])
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, default=Path('tasks.json'))
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('add').add_argument('text')
    commands.add_parser('list').add_argument('--pending', action='store_true')
    commands.add_parser('done').add_argument('id', type=int)
    args = parser.parse_args()
    try:
        records = load(args.data)
        if args.command == 'add':
            text = args.text.strip()
            if not text:
                raise ValueError('Task text must not be empty')
            next_id = max((item['id'] for item in records), default=0) + 1
            records.append({'id': next_id, 'text': text, 'done': False})
            args.data.write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
        elif args.command == 'done':
            selected = next((item for item in records if item['id'] == args.id), None)
            if selected is None:
                raise ValueError('Unknown task ID')
            selected['done'] = True
            args.data.write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
        else:
            for item in records:
                if args.pending and item['done']:
                    continue
                print(f"{item['id']} [{'x' if item['done'] else ' '}] {item['text']}")
    except (ValueError, OSError) as error:
        print(f'Error: {error}', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
