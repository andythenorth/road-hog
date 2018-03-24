from road_vehicle import Tanker, SteamRoadVehicle

consist = Tanker(id='drumbreck_tanker',
                 base_numeric_id=800,
                 name='Drumbreck',
                 tram_type='RAIL',
                 vehicle_life=40,
                 intro_date=1870)

consist.add_unit(type=SteamRoadVehicle,
                 vehicle_length=4,
                 always_use_same_spriterow=True)

consist.add_unit(capacity=16,
                 vehicle_length=4,
                 repeat=3)
