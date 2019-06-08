from road_vehicle import OpenFeldbahnConsist
from base_platforms.feldbahn import DieselEngineFeldbahn1, OpenWagonFeldbahnGen3

consist = OpenFeldbahnConsist(id='bahn_face_open',
                       base_numeric_id=140,
                       name='Bahn Face',
                       vehicle_life=40,
                       gen=3)

consist.add_unit(base_platform=DieselEngineFeldbahn1)


consist.add_unit(base_platform=OpenWagonFeldbahnGen3,
                 repeat=3)
