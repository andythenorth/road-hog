#!/usr/bin/env python3
"""Check platform value overrides and repeated unit identity."""
from pathlib import Path
import subprocess
import sys
ROOT = Path(__file__).resolve().parents[2]
script = r'''
import sys
import types
# Keep this unit test independent of enabled real rosters.
# road_vehicle.__init__ imports road_hog, whose top-level roster imports
# would otherwise load vehicles while road_vehicle is partly initialised.
# The platform fixture never needs a populated roster manager.
sys.modules['road_hog'] = types.ModuleType('road_hog')
sys.argv = ['verify', '--grf-name=migration_test']
from road_vehicle.model_def import ModelDef
from road_vehicle.catalogue import Catalogue
from road_vehicle.units import DieselVehicleUnit
class FixturePlatform:
    vehicle_length = 4
    capacity = 14
    type = DieselVehicleUnit
    def configure_unit_args(self, **kwargs):
        for key in ('vehicle_length', 'capacity', 'type'):
            kwargs[key] = getattr(self, key)
        kwargs['base_platform'] = self
        return kwargs
m = ModelDef(schema_name='Bus', gen=2, sprites_complete=True,
             model_id='platform_fixture', base_numeric_id=400, name='Fixture')
m.add_unit_def(unit_cls_name='RoadVehicleUnit', base_platform=FixturePlatform,
               vehicle_length=7, capacity=99, repeat=2)
c = Catalogue(m, roster_id='migration_test')
v = c.produce(c[0])
assert len(v.units) == 2
assert v.units[0] is v.units[1]
assert v.units[0].numeric_id == 400
assert type(v.units[0]) is DieselVehicleUnit
assert v.units[0].vehicle_length == 4
assert v.units[0].capacity == 14
assert isinstance(v.units[0].base_platform, FixturePlatform)
assert m.unit_defs[0].vehicle_length == 7 # original declaration wasn't mutated
print('PASS: overrides, resolved unit class, platform instance, repeats, numeric ID')
'''
p = subprocess.run([sys.executable, '-c', script], cwd=ROOT, env=__import__('os').environ | {'PYTHONPATH':str(ROOT/'src')}, text=True)
raise SystemExit(p.returncode)
