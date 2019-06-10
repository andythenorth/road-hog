from road_vehicle import DumpTruckConsist
from base_platforms.trucks import DieselCaboverSemiTractorTruckGen4A

consist = DumpTruckConsist(id='wookey_dump',
                    base_numeric_id=490,
                    name='Wookey',
                    gen=4,
                    intro_date_offset=6)  # introduce later than gen epoch by design

consist.add_unit(base_platform=DieselCaboverSemiTractorTruckGen4A)

consist.add_unit(base_platform=None,
                 vehicle_length=7)
