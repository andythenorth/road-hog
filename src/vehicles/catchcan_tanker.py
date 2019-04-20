from road_vehicle import TankerTram, ElectricRoadVehicle

consist = TankerTram(id='catchcan_tanker',
                     base_numeric_id=810,
                     name='Catchcan',
                     tram_type='ELRL',
                     vehicle_life=40,
                     gen=2,
                     intro_date_offset=2)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
