from road_vehicle import TankerTruckConsist, SteamVehicleUnit
from base_platforms.trucks import SteamCaboverSemiTractorTruckGen2A

consist = TankerTruckConsist(id='boilingwell_tanker',
                      base_numeric_id=920,
                      name='Boilingwell',
                      gen=2,
                      intro_date_offset=5)  # introduce later than gen epoch by design

consist.add_unit(base_platform=SteamCaboverSemiTractorTruckGen2A)

consist.add_unit(vehicle_length=5)
