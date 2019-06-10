from road_vehicle import CoveredHopperTruckConsist
from base_platforms.trucks import DieselCaboverSemiTractorTruckGen3A

consist = CoveredHopperTruckConsist(id='limebreach_covered_hopper',
                             base_numeric_id=260,
                             name='Limebreach',
                             gen=3,
                             intro_date_offset=10)  # introduce later than gen epoch by design

consist.add_unit(base_platform=DieselCaboverSemiTractorTruckGen3A)

consist.add_unit(base_platform=None,
                 vehicle_length=5)
