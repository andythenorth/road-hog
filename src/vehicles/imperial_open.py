from road_vehicle import OpenFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahn2, OpenWagonFeldbahnGen2

consist = OpenFeldbahnConsist(id='imperial_open',
                       base_numeric_id=1090,
                       name='Imperial',
                       gen=2)

consist.add_unit(base_platform=DieselEngineFeldbahn2)


consist.add_unit(base_platform=OpenWagonFeldbahnGen2,
                 repeat=12)
