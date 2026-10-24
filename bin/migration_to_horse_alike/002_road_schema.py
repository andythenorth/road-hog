"""Install independent road schema/unit classes (no legacy Consist)."""
from _common import PAYLOAD,write
for src, dest in [('schemas_road.py','schemas.py'),('units_road.py','units.py')]:
    write('src/road_vehicle/'+dest,(PAYLOAD/'road_vehicle'/src).read_bytes())
