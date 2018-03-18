from road_vehicle import LivestockHauler

consist = LivestockHauler(id='scrag_end',
                          base_numeric_id=710,
                          title='Scrag End [Livestock Tram]',
                          tram_type='RAIL',
                          vehicle_life=40,
                          intro_date=1865)

consist.add_unit(capacity=0,
                 vehicle_length=4,
                 effect_spawn_model='EFFECT_SPAWN_MODEL_STEAM',
                 effects=['EFFECT_SPRITE_STEAM, -2, 0, 14'])

consist.add_unit(capacity=16,
                 vehicle_length=4,
                 repeat=3)

