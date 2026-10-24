from pathlib import Path
import hashlib
import sys
ROOT = Path(__file__).resolve().parents[2]
PAYLOAD = Path(__file__).resolve().parent / 'payload'

def write(path, data):
    path = ROOT / path
    if path.exists():
        if path.read_bytes() == data:
            print('UNCHANGED', path.relative_to(ROOT)); return
        raise RuntimeError(f'Refusing to replace modified file: {path}')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    print('CREATED', path.relative_to(ROOT))

def replace(path, old, new):
    path = ROOT / path
    src = path.read_text()
    if new in src and old not in src:
        print('UNCHANGED',path.relative_to(ROOT)); return
    if src.count(old) != 1:
        raise RuntimeError(f'Expected exactly one source match in {path}, found {src.count(old)}')
    path.write_text(src.replace(old,new))
    print('UPDATED',path.relative_to(ROOT))
