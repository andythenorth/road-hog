"""Run the docs build, check real pages and two bus sprites exist."""
from pathlib import Path
import subprocess
import sys
from _common import ROOT

cmd = [sys.executable, 'src/render_docs.py', '--pool_workers=0', '--grf-name=migration_test']
print('RUN:', ' '.join(cmd), flush=True)
result = subprocess.run(cmd, cwd=ROOT)
if result.returncode:
    raise SystemExit(result.returncode)

base = ROOT / 'docs/migration_test'
required = [
    base / 'html/road_vehicles.html',
    base / 'html/code_reference.html',
]
for path in required:
    if not path.is_file() or path.stat().st_size == 0:
        raise SystemExit(f'FAIL: missing or empty docs file: {path}')

# CABBAGE Don't accept "it ran" without the bus present in both key pages.
for path in required:
    content = path.read_text(encoding='utf8')
    if 'Leyburn' not in content:
        raise SystemExit(f'FAIL: Leyburn missing in {path}')

images = sorted((base / 'html/static/img').glob('*leyburn*_*.png'))
if len(images) < 2:
    raise SystemExit(f'FAIL: expected two Leyburn docs images, got {len(images)}')

print('PASS: render_docs.py completed; Leyburn appears in both pages; two docs sprites written')
print('NOT VERIFIED: exact HTML/pixel parity to old docs (supply a docs reference to compare)')
