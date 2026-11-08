#!/usr/bin/env python3
"""Resolve missing IH temp register symbols in the RH runtime procedure template."""
from pathlib import Path

path = Path('src/templates/procedures_wagon_recolour_strategies_road.pynml')
if not path.is_file():
    raise SystemExit('Missing step 008b road procedures template; run 008b first')
text = path.read_text()
updated = text
updated = updated.replace('k_addr_wagon_recolour_livery_num_${livery_num}', '${25 + livery_num}')
if 'k_addr_wagon_recolour_livery_num_' in updated:
    raise SystemExit('Unresolved wagon recolour livery temp register')
if updated != text:
    anchor = '<!--! up to 8 random liveries (all 8 must be passed as params when initing the wagon chain -->'
    if updated.count(anchor) != 1:
        raise SystemExit('Could not identify the register allocation comment location')
    updated = updated.replace(anchor, '<!--! CABBAGE352: temporary registers 24 = random livery choice, 25..32 = eight livery candidates, 33 = purchase flag.\n      Verify these allocations against the complete Road Hog temporary-register usage before adding callers. -->\n' + anchor)
    path.write_text(updated)
    print('008b fixed: eight livery candidate temporary-register references')
else:
    print('008b already fixed')
