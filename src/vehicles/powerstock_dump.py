from road_vehicle import DumpTruckConsist
from base_platforms.trucks import DieselCaboverSemiTractorTruckGen5A

consist = DumpTruckConsist(id='powerstock_dump',
                    base_numeric_id=340,
                    name='Powerstock',
                    semi_truck_so_redistribute_capacity=True,
                    gen=5,
                    intro_date_offset=4)  # introduce later than gen epoch by design

consist.add_unit(base_platform=DieselCaboverSemiTractorTruckGen5A)

consist.add_unit(vehicle_length=7)
