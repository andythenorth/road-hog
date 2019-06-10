from road_vehicle import FlatbedTruckConsist
from base_platforms.trucks import DieselConventionalCabSemiTractorTruckGen4A

consist = FlatbedTruckConsist(id='towerhouse_flat',
                       base_numeric_id=650,
                       name='Towerhouse',
                       gen=4)

consist.add_unit(base_platform=DieselConventionalCabSemiTractorTruckGen4A)

consist.add_unit(base_platform=None,
                 vehicle_length=7,
                 cargo_length=4)  # some cargo overlap eh?
