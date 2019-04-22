from road_vehicle import OpenFeldbahn, DieselRoadVehicle

consist = OpenFeldbahn(id='bahn_face_open',
                       base_numeric_id=140,
                       name='Bahn Face',
                       vehicle_life=40,
                       gen=3)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 always_use_same_spriterow=True)

consist.add_unit(capacity=36,
                 vehicle_length=6,
                 cargo_length=3,
                 repeat=2)
