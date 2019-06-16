from road_vehicle import FlatFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahn2, OpenWagonFeldbahnGen2

consist = FlatFeldbahnConsist(id='newbiggin_flat',
                       base_numeric_id=1110,
                       name='Newbiggin',
                       gen=2)

consist.add_unit(base_platform=DieselEngineFeldbahn2)

consist.add_unit(base_platform=OpenWagonFeldbahnGen2,
                 repeat=12)
