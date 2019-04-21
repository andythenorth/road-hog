from road_vehicle import FruitVegTram, ElectricRoadVehicle

consist = FruitVegTram(id='applethwaite_fruit_veg',
                       base_numeric_id=940,
                       name='Applethwaite',
                       vehicle_life=40,
                       gen=2,
                       intro_date_offset=1)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=30,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)
