from road_vehicle import OpenFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahnGen3A, WagonFeldbahnA

consist = OpenFeldbahnConsist(id='jubilee_open',
                       base_numeric_id=580,
                       name='Jubilee',
                       gen=3)

consist.add_unit(base_platform=DieselEngineFeldbahnGen3A)


consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=5)
