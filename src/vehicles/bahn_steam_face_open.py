from road_vehicle import OpenFeldbahn, SteamRoadVehicle

consist = OpenFeldbahn(id='bahn_steam_face_open',
                       base_numeric_id=970,
                       name='Bahn Steam Face',
                       vehicle_life=40,
                       gen=2)

consist.add_unit(type=SteamRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 always_use_same_spriterow=True)

consist.add_unit(capacity=25,
                 vehicle_length=4,
                 cargo_length=3,
                 repeat=3)
