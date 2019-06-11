from road_vehicle import FruitVegTramConsist
from base_platforms.trams import SteamEngineTram1

consist = FruitVegTramConsist(id='plumley_fruit_veg',
                       base_numeric_id=950,
                       name='Plumley',
                       gen=1,
                       intro_date_offset=1)  # introduce later than gen epoch by design

consist.add_unit(base_platform=SteamEngineTram1)

consist.add_unit(base_platform=None, # no base platform by design currently
                 vehicle_length=4,
                 repeat=3)
