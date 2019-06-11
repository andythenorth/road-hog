from road_vehicle import BoxTramConsist
from base_platforms.trams import SteamEngineTram1

consist = BoxTramConsist(id='amblecote_box',
                  base_numeric_id=80,
                  name='Amblecote',
                  gen=1)

consist.add_unit(base_platform=SteamEngineTram1)

consist.add_unit(base_platform=None, # no base platform by design currently
                 vehicle_length=4,
                 repeat=3)
