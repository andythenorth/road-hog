from road_vehicle import LivestockHauler

consist = LivestockHauler(id='swineshead_livestock',
                          base_numeric_id=440,
                          title='Swineshead [Livestock Truck]',
                          vehicle_life=40,
                          intro_date=1970)

consist.add_unit(capacity=25,
                 vehicle_length=6,
                 visual_effect='VISUAL_EFFECT_DIESEL')

consist.add_unit(capacity=15,
                 vehicle_length=4)

