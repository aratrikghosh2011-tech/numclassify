#!/usr/bin/env python3
"""
Fix UTF-8 BOM in playground JS files.
Run once from repo root:
    python tools/fix_encoding.py
"""
from pathlib import Path


FILES = [
    'docs/playground-guide.js',
    'docs/playground-core.js',
    'docs/playground-tabs.js',
]


def main():
    for filepath in FILES:
        p = Path(filepath)
        if not p.exists():
            print(f'SKIP: {filepath} not found')
            continue

        raw = p.read_bytes()

        if raw[:3] == b'\xef\xbb\xbf':
            raw = raw[3:]
            print(f'Stripped BOM: {filepath}')
        else:
            print(f'No BOM: {filepath}')

        text = raw.decode('utf-8')
        p.write_text(text, encoding='utf-8')
        print(f'  Saved as UTF-8 (no BOM): {filepath}')

    print('\nDone.')


if __name__ == '__main__':
    main()
