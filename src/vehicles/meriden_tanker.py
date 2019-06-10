from road_vehicle import TankerTruckConsist
from base_platforms.trucks import DieselCaboverSemiTractorTruckGen4A

consist = TankerTruckConsist(id='meriden_tanker',
                      base_numeric_id=290,
                      name='Meriden',
                      gen=4,
                      intro_date_offset=6)  # introduce later than gen epoch by design

consist.add_unit(base_platform=DieselCaboverSemiTractorTruckGen4A)

consist.add_unit(base_platform=None,
                 vehicle_length=7)
