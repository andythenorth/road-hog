from road_vehicle import CoveredHopperTruckConsist
from base_platforms.trucks import DieselCaboverSemiTractorTruckGen5A

consist = CoveredHopperTruckConsist(id='mcdowell_covered_hopper',
                             base_numeric_id=280,
                             name='McDowell',
                             semi_truck_so_redistribute_capacity=True,
                             gen=5,
                             intro_date_offset=10)  # introduce later than gen epoch by design

consist.add_unit(base_platform=DieselCaboverSemiTractorTruckGen5A)

consist.add_unit(vehicle_length=7)
