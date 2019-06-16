from road_vehicle import BoxFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahnGen3A, WagonFeldbahnA

consist = BoxFeldbahnConsist(id='elterwater_box',
                       base_numeric_id=970,
                       name='Elterwater',
                       gen=3)

consist.add_unit(base_platform=DieselEngineFeldbahnGen3A)

consist.add_unit(base_platform=WagonFeldbahnA,
                 repeat=5)
