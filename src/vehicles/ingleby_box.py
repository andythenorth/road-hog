from road_vehicle import BoxFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahn1, OpenWagonFeldbahnGen2

consist = BoxFeldbahnConsist(id='ingleby_box',
                       base_numeric_id=1000,
                       name='Ingleby',
                       gen=2)

consist.add_unit(base_platform=DieselEngineFeldbahn1)

consist.add_unit(base_platform=OpenWagonFeldbahnGen2,
                 repeat=5)
