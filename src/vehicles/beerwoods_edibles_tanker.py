from road_vehicle import EdiblesTankerTruckConsist
from base_platforms.trucks import DieselCaboverRigidTruckGen3A

consist = EdiblesTankerTruckConsist(id='beerwoods_edibles_tanker',
                             base_numeric_id=420,
                             name='Beerwoods',
                             gen=3,
                             intro_date_offset=4)  # introduce later than gen epoch by design

consist.add_unit(base_platform=DieselCaboverRigidTruckGen3A)

consist.add_unit(base_platform=None,
                 vehicle_length=4)
