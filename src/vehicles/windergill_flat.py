from road_vehicle import FlatHauler, DieselRoadVehicle

consist = FlatHauler(id='windergill_flat',
                        base_numeric_id=640,
                        name='Windergill',
                        vehicle_life=40,
                        intro_date=1939)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=15,
                 vehicle_length=5,
                 cargo_length=3)

consist.add_unit(capacity=15,
                 vehicle_length=4,
                 cargo_length=4)
