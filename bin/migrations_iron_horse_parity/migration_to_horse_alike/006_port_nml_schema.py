# CABBAGE Schema implementation belongs here; do not patch NML templates here.
"""Install road-specific NML methods. Never modify templates here."""
from _common import ROOT, PAYLOAD
for name in ('schemas_nml.py','units_nml.py'):
    dest=ROOT/'src/road_vehicle'/name.replace('_nml','')
    old=(PAYLOAD/'road_vehicle'/name.replace('_nml','_road')).read_bytes()
    new=(PAYLOAD/'road_vehicle'/name).read_bytes()
    if dest.read_bytes()==new:
        print('UNCHANGED',dest.relative_to(ROOT)); continue
    if dest.read_bytes()!=old:
        raise RuntimeError('Unrecognised schema/unit state: '+str(dest))
    dest.write_bytes(new)
    print('UPDATED',dest.relative_to(ROOT))
