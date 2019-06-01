from road_vehicle import OpenFeldbahnConsist, DieselRoadVehicle

consist = OpenFeldbahnConsist(id='bahn_face_open',
                       base_numeric_id=140,
                       name='Bahn Face',
                       vehicle_life=40,
                       gen=3)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=0,
                 vehicle_length=4,
                 always_use_same_spriterow=True)

consist.add_unit(capacity=28,
                 vehicle_length=4,
                 cargo_length=3,
                 repeat=3)
