from road_vehicle import PaxLocalTramConsist, ElectricRoadVehicle

consist = PaxLocalTramConsist(id='fairlop_pax',
                       base_numeric_id=10,
                       name='Fairlop',
                       vehicle_life=40,
                       gen=2,
                       intro_date_offset=3)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=6,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 12'])

consist.add_unit(capacity=25,
                 vehicle_length=5,
                 repeat=2)
