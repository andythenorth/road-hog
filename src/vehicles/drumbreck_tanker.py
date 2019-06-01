from road_vehicle import TankerTramConsist, SteamRoadVehicle

consist = TankerTramConsist(id='drumbreck_tanker',
                     base_numeric_id=800,
                     name='Drumbreck',
                     vehicle_life=40,
                     gen=1,
                     intro_date_offset=4)  # introduce later than gen epoch by design

consist.add_unit(type=SteamRoadVehicle,
                 vehicle_length=4,
                 always_use_same_spriterow=True)

consist.add_unit(capacity=16,
                 vehicle_length=4,
                 repeat=3)
