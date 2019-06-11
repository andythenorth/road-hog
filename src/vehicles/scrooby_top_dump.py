from road_vehicle import DumpTramConsist
from base_platforms.trams import SteamEngineTram2

consist = DumpTramConsist(id='scrooby_top_dump',
                   base_numeric_id=700,
                   name='Scrooby Top',
                   gen=1,
                   intro_date_offset=10)  # introduce later than gen epoch by design

consist.add_unit(base_platform=SteamEngineTram2)

consist.add_unit(base_platform=None, # no base platform by design currently
                 vehicle_length=3,
                 repeat=4)
