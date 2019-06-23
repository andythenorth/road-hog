from road_vehicle import FlatbedTramConsist
from base_platforms.trams import SteamEngineTram1

consist = FlatbedTramConsist(id='stakebeck_flat',
                      base_numeric_id=750,
                      name='Stakebeck',
                      gen=1)

consist.add_unit(base_platform=SteamEngineTram1)

consist.add_unit(base_platform=None, # no base platform by design currently
                 vehicle_length=4,
                 cargo_length=4,
                 repeat=3)
