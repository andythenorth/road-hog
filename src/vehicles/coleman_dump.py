from road_vehicle import DumpTruckConsist, SteamVehicleUnit
from base_platforms.trucks import SteamCaboverSemiTractorTruckGen2A

consist = DumpTruckConsist(id='coleman_dump',
                    base_numeric_id=910,
                    name='Coleman',
                    gen=2,
                    intro_date_offset=7)  # introduce later than gen epoch by design

consist.add_unit(base_platform=SteamCaboverSemiTractorTruckGen2A)

consist.add_unit(vehicle_length=5)
