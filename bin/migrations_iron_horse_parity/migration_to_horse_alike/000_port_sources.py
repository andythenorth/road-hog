# CABBAGE Source port step: Iron Horse reference stays in the installer payload.
"""Install ModelDef and keep the legacy module byte-identical."""
from _common import ROOT, PAYLOAD, write
p=ROOT/'src/road_vehicle.py'; dest=ROOT/'src/road_vehicle/__init__.py'
if p.exists() and not dest.exists():
    write('src/road_vehicle/__init__.py',p.read_bytes())
    p.unlink()
elif not p.exists() and dest.exists():
    pass
else:
    raise RuntimeError('Expected src/road_vehicle.py OR its migrated package, not both/neither')
write('src/road_vehicle/model_def.py',(PAYLOAD/'road_vehicle/model_def.py').read_bytes())
# CABBAGE The large Iron Horse source references stay in the migration payload only.
# CABBAGE Do not copy them to src/road_vehicle: they are not runnable Road Hog code,
# and installing them makes the repo diff huge for no runtime benefit.
print('Iron Horse reference source remains in the migration payload only.')
