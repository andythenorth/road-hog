from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]

def replace_once(path, old, new):
    original = path.read_text()
    if new in original:
        print(f'UNCHANGED: {path.relative_to(ROOT)}')
        return
    count = original.count(old)
    if count != 1:
        raise RuntimeError(f'{path}: expected exactly one matching source block, found {count}; no file changed')
    path.write_text(original.replace(old, new))
    print(f'UPDATED: {path.relative_to(ROOT)}')
