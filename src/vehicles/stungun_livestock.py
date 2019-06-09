from road_vehicle import LivestockTruckConsist
from base_platforms.trucks import DieselCaboverSemiTractorTruckGen5A

consist = LivestockTruckConsist(id='stungun_livestock',
                         base_numeric_id=430,
                         name='Stungun',
                         semi_truck_so_redistribute_capacity=True,
                         gen=5,
                         intro_date_offset=2)  # introduce later than gen epoch by design

consist.add_unit(base_platform=DieselCaboverSemiTractorTruckGen5A)

consist.add_unit(vehicle_length=8)
