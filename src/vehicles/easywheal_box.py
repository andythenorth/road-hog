from road_vehicle import BoxTruckConsist
from base_platforms.trucks import DieselConventionalCabSemiTractorTruckGen3A

consist = BoxTruckConsist(id='easywheal_box',
                   base_numeric_id=160,
                   name='Easywheal',
                   gen=3)

consist.add_unit(base_platform=DieselConventionalCabSemiTractorTruckGen3A)

consist.add_unit(base_platform=None,
                 vehicle_length=5)
