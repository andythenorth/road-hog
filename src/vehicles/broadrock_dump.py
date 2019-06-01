from road_vehicle import DumpHEQSConsist, DieselRoadVehicle

consist = DumpHEQSConsist(id='broadrock_dump',
                   base_numeric_id=100,
                   name='Broadrock',
                   power=400,
                   semi_truck_so_redistribute_capacity=True,
                   speed=40,  # dibbled up above RL for game balance
                   type_base_running_cost_points=20,  # dibble running costs for game balance
                   vehicle_life=40,
                   gen=3,
                   intro_date_offset=-3)  # introduce earlier than gen epoch by design

consist.add_unit(type=DieselRoadVehicle,
                 capacity=0,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=3,
                 effects=['EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, 1, 10',
                          'EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, -1, 10'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=55,  # much bigger is not much better here
                 vehicle_length=6)
