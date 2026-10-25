"""Run the language renderer and compare against the old output if supplied."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / 'generated/lang/migration_test'
REFERENCE = ROOT / 'lang.reference'

proc = subprocess.run([sys.executable, 'src/render_lang.py', '--grf-name=migration_test'], cwd=ROOT)
if proc.returncode:
    raise SystemExit(f'FAIL: render_lang.py exit code {proc.returncode}')
print('PASS: render_lang.py completed for migration_test')

actual = sorted(OUTPUT.glob('*.lng'))
if not actual:
    raise SystemExit(f'FAIL: no .lng files found in {OUTPUT}')
print(f'PASS: generated {len(actual)} .lng file(s)')

if not REFERENCE.is_dir():
    raise SystemExit('FAIL: lang.reference/ not found at repo root; reference comparison not run')

# Ignore whitespace layout but compare language values, names and pragmas.
# CABBAGE If we ever need to check exact output format, add a separate byte comparison.
def meaningful_lines(path):
    lines = []
    for line in path.read_text(encoding='utf-8-sig').splitlines():
        line = line.strip()
        if not line or line.startswith('//') or line.startswith('#'):
            continue
        if ':' in line and not line.startswith('##'):
            key, value = line.split(':', 1)
            key = key.strip()
            # CABBAGE Git commit count/hash changes after migration; not language data.
            # Only ignore this one dynamic value. Keep the key and all other values strict.
            value = '<git-version>' if key == 'STR_GRF_NAME_VERSIONED' else value.strip()
            line = key + ':' + value
        lines.append(line)
    return lines

refs = {p.name: p for p in REFERENCE.rglob('*.lng')}
if not refs:
    raise SystemExit('FAIL: no reference .lng files in lang.reference/')
missing = sorted(set(refs) - {p.name for p in actual})
extra = sorted({p.name for p in actual} - set(refs))
if missing or extra:
    raise SystemExit(f'FAIL: language file mismatch; missing={missing}, extra={extra}')

import difflib
fail = False
for path in actual:
    expected = meaningful_lines(refs[path.name])
    generated = meaningful_lines(path)
    if expected != generated:
        print(''.join(difflib.unified_diff(expected, generated, fromfile=str(refs[path.name]), tofile=str(path), lineterm='\n')))
        fail = True
    else:
        print(f'PASS: {path.name} matches reference (ignoring whitespace/comments)')
if fail:
    raise SystemExit('FAIL: generated language strings differ from old output')
print('PASS: migration_test language output matches lang.reference')
