from road_vehicle import OpenTramConsist, SteamVehicleUnit

consist = OpenTramConsist(id='buildwas_open',
                   base_numeric_id=120,
                   name='Buildwas',
                   vehicle_life=40,
                   gen=1)

consist.add_unit(type=SteamVehicleUnit,
                 capacity=0,
                 vehicle_length=4,
                 always_use_same_spriterow=True)

consist.add_unit(vehicle_length=4,
                 cargo_length=4,
                 repeat=3)
