"""Validate model/IDs/repeat behaviour without pretending NML cutover works."""
from _common import ROOT
import sys
import types
# Load the framework without executing the legacy road_vehicle package initializer.
pkg=types.ModuleType("road_vehicle")
pkg.__path__=[str(ROOT/"src"/"road_vehicle")]
sys.modules["road_vehicle"]=pkg
from road_vehicle.model_def import ModelDef
from road_vehicle.catalogue import Catalogue
m=ModelDef(schema_name='Bus',gen=2,sprites_complete=True,model_id='fixture',base_numeric_id=20)
m.add_unit_def(unit_cls_name='DieselVehicleUnit',repeat=3,vehicle_length=7)
m.add_unit_def(unit_cls_name='DieselVehicleUnit',repeat=1,vehicle_length=6)
c=Catalogue(m,'migration_test')
assert c[0].unit_numeric_ids==[20,21]
v=c.produce(c[0])
assert len(v.units)==4
assert v.units[0] is v.units[1] is v.units[2]
assert v.units[0].numeric_id==20 and v.units[3].numeric_id==21
assert not hasattr(v,'consist')
from road_vehicle.schemas import Bus, PassengerVehicle, RoadVehicleBase
assert isinstance(v, Bus) and isinstance(v, PassengerVehicle) and isinstance(v, RoadVehicleBase)
print('PASS model, catalogue-owned IDs, physical unit repeats')
print('NOT VERIFIED: NML rendering, GRF build, road property equivalence')
