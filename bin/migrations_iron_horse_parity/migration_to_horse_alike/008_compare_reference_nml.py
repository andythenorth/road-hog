"""Compare rendered Leyburn NML against the old compile. Names can change, values can't."""
from pathlib import Path
import difflib
import sys
from _common import ROOT

# CABBAGE This is a single Leyburn fixture. A fleet-wide comparer needs model-specific IDs.
reference = ROOT / 'migration_test.reference.nml'
rendered = ROOT / 'generated/migration_test.nml'
if not reference.is_file():
    raise SystemExit(f'Missing reference NML: {reference} (copy old compile here)')
if not rendered.is_file():
    raise SystemExit(f'Missing rendered NML: {rendered} (run 007 first)')
old = reference.read_text()
new = rendered.read_text()
# CABBAGE The catalogue adds a model variant and unit suffix. Normalise just this
# CABBAGE known name change, not numeric IDs, path names, formulas or properties.
new = new.replace('leyburn_pax_mv_0_unit_0', 'leyburn_pax')
# CABBAGE Template comment refers to the new schema name. Ignore only this
# CABBAGE comment wording, not any NML properties or expressions.
new = new.replace(' // model_variant just supplies intro year', ' // consist just supplies intro year')
if old == new:
    print('PASS: Leyburn NML matches reference after known identifier rename')
else:
    diff = list(difflib.unified_diff(old.splitlines(), new.splitlines(),
                                     fromfile='migration_test.reference.nml',
                                     tofile='generated/migration_test.nml (names normalised)',
                                     lineterm=''))
    print('\n'.join(diff[:180]))
    if len(diff) > 180:
        print(f'... {len(diff)-180} more diff lines')
    print('FAIL: rendered NML differs from legacy reference after identifier rename')
    sys.exit(1)
