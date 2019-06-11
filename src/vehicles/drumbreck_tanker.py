from road_vehicle import TankerTramConsist
from base_platforms.trams import SteamEngineTram1

consist = TankerTramConsist(id='drumbreck_tanker',
                     base_numeric_id=800,
                     name='Drumbreck',
                      gen=1,
                     intro_date_offset=4)  # introduce later than gen epoch by design

consist.add_unit(base_platform=SteamEngineTram1)

consist.add_unit(base_platform=None, # no base platform by design currently
                 vehicle_length=4,
                 repeat=3)
