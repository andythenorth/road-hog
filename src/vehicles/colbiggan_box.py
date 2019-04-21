from road_vehicle import BoxTram, ElectricRoadVehicle

consist = BoxTram(id='colbiggan_box',
                  base_numeric_id=880,
                  name='Colbiggan',
                  vehicle_life=40,
                  gen=3)

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=36,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
