from road_vehicle import CoveredHopperTruckConsist
from base_platforms.trucks import DieselCaboverSemiTractorTruckGen4A

consist = CoveredHopperTruckConsist(id='ribble_covered_hopper',
                             base_numeric_id=360,
                             name='Ribble',
                             gen=4,
                             intro_date_offset=10)  # introduce later than gen epoch by design

consist.add_unit(base_platform=DieselCaboverSemiTractorTruckGen4A)

consist.add_unit(base_platform=None,
                 vehicle_length=7)
