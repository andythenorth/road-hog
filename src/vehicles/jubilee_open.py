from road_vehicle import OpenFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahn1, OpenWagonFeldbahnGen3

consist = OpenFeldbahnConsist(id='jubilee_open',
                       base_numeric_id=580,
                       name='Jubilee',
                       gen=3)

consist.add_unit(base_platform=DieselEngineFeldbahn1)


consist.add_unit(base_platform=OpenWagonFeldbahnGen3,
                 repeat=5)
