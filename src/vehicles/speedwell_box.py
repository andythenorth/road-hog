from road_vehicle import BoxTruckConsist
from base_platforms.trucks import DieselCaboverSemiTractorTruckGen5A

consist = BoxTruckConsist(id='speedwell_box',
                   base_numeric_id=400,
                   name='Speedwell',
                   semi_truck_so_redistribute_capacity=True,
                   gen=5)

consist.add_unit(base_platform=DieselCaboverSemiTractorTruckGen5A)

consist.add_unit(vehicle_length=7)
