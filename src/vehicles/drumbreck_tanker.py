from road_vehicle import TankerTramConsist, SteamVehicleUnit

consist = TankerTramConsist(id='drumbreck_tanker',
                     base_numeric_id=800,
                     name='Drumbreck',
                      gen=1,
                     intro_date_offset=4)  # introduce later than gen epoch by design

consist.add_unit(type=SteamVehicleUnit,
                 vehicle_length=4,
                 always_use_same_spriterow=True)

consist.add_unit(vehicle_length=4,
                 repeat=3)
