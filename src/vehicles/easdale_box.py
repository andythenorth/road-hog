from road_vehicle import BoxFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahn1, OpenWagonFeldbahnGen1

consist = BoxFeldbahnConsist(id='easdale_box',
                       base_numeric_id=620,
                       name='Easdale',
                       gen=1)

consist.add_unit(base_platform=DieselEngineFeldbahn1)

consist.add_unit(base_platform=OpenWagonFeldbahnGen1,
                 repeat=5)
