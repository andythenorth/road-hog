from road_vehicle import TankerTruckConsist
from base_platforms.trucks import DieselConventionalCabSemiTractorTruckGen4A

consist = TankerTruckConsist(id='greenscoe_tanker',
                      base_numeric_id=210,
                      name='Greenscoe',
                      gen=3,
                      intro_date_offset=3)  # introduce later than gen epoch by design

consist.add_unit(base_platform=DieselConventionalCabSemiTractorTruckGen4A)

consist.add_unit(vehicle_length=5)
