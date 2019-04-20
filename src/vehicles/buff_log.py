from road_vehicle import LogHauler, DieselRoadVehicle

consist = LogHauler(id='buff_log',
                    base_numeric_id=110,
                    name='Buff',
                    road_type='HAUL',
                    power=550,
                    speed=60,
                    vehicle_life=40,
                    gen=4,
                    intro_date=1994)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=40,
                 vehicle_length=7)

consist.add_unit(capacity=35,
                 vehicle_length=8)
