#!/usr/bin/env python3
"""Check the old generated files exist. Don't rewrite them."""
from pathlib import Path
from zipfile import ZipFile
import sys

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / 'generated.reference.zip'
if not REFERENCE.is_file():
    sys.exit('FAIL: put generated.reference.zip in the repo root')
with ZipFile(REFERENCE) as z:
    names = set(z.namelist())
    required = {'generated.reference/road-hog.nml', 'generated.reference/heqs.nml',
                'generated.reference/road-hog.grf', 'generated.reference/heqs.grf'}
    missing = required - names
    if missing:
        sys.exit('FAIL: golden archive missing: ' + ', '.join(sorted(missing)))
    count = lambda prefix, suffix: sum(n.startswith(prefix) and n.endswith(suffix) and not n.startswith('__MACOSX') for n in names)
    print('PASS: legacy archive found; no files overwritten')
    print('Vehicle NML:', count('generated.reference/nml/', '.nml'))
    print('Graphics:', count('generated.reference/graphics/', '.png'))
    print('Language:', count('generated.reference/lang/', '.lng'))
    print('CABBAGE: Golden source was made before model migration. Preserve it as read-only.')
