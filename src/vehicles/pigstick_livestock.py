from road_vehicle import LivestockHauler

consist = LivestockHauler(id='pigstick_livestock',
                          base_numeric_id=330,
                          name='Pigstick [Livestock Truck]',
                          vehicle_life=40,
                          intro_date=1941)

consist.add_unit(capacity=20,
                 vehicle_length=6,
                 visual_effect='VISUAL_EFFECT_DIESEL')

consist.add_unit(capacity=10,
                 vehicle_length=4)

