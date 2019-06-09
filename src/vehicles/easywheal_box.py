from road_vehicle import BoxTruckConsist
from base_platforms.trucks import DieselConventionalCabSemiTractorTruckGen4A

consist = BoxTruckConsist(id='easywheal_box',
                   base_numeric_id=160,
                   name='Easywheal',
                   gen=3)

consist.add_unit(base_platform=DieselConventionalCabSemiTractorTruckGen4A)

consist.add_unit(vehicle_length=5)
