from road_vehicle import FlatFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahn1, OpenWagonFeldbahnGen3

consist = FlatFeldbahnConsist(id='stawell_flat',
                       base_numeric_id=1050,
                       name='Stawell',
                       gen=2)

consist.add_unit(base_platform=DieselEngineFeldbahn1)

consist.add_unit(base_platform=OpenWagonFeldbahnGen3,
                 repeat=5)
