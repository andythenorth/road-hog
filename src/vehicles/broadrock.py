from road_vehicle import DumpHauler

consist = DumpHauler(id='broadrock',
                     base_numeric_id=100,
                     title='Broadrock [Mining Truck]',
                     road_type='HAUL',
                     power=400,
                     semi_truck_so_redistribute_capacity=True,
                     speed=40,  # dibbled up above RL for game balance
                     type_base_running_cost_points=20,  # dibble running costs for game balance
                     vehicle_life=40,
                     intro_date=1947)

consist.add_unit(capacity=0,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=3,
                 effects=['EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, 1, 10',
                          'EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, -1, 10'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=55,  # much bigger is not much better here
                 vehicle_length=6)

consist.add_model_variant(spritesheet_suffix=0)
consist.add_model_variant(spritesheet_suffix=1,
                          graphics_processor=consist.graphics_processors[1])
