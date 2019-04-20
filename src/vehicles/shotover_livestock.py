from road_vehicle import LivestockHauler, ElectricRoadVehicle

consist = LivestockHauler(id='shotover_livestock',
                          base_numeric_id=370,
                          name='Shotover',
                          tram_type='ELRL',
                          vehicle_life=40,
                          gen=4,
                          intro_date=1941)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=36,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
