from road_vehicle import DumpHEQSConsist, DieselVehicleUnit

consist = DumpHEQSConsist(id='witch_hill_dump',
                   base_numeric_id=500,
                   name='Witch Hill',
                   power=900,
                   speed=50,  # dibbled up above RL for game balance
                   type_base_running_cost_points=30,  # dibble running costs for game balance
                   gen=4,
                   intro_date_offset=17)  # introduce later than gen epoch by design

consist.add_unit(type=DieselVehicleUnit,
                 #capacity=85,  # much bigger is not much better here
                 vehicle_length=7,
                 effects=['EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, 1, 10', 'EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, -1, 10'])
