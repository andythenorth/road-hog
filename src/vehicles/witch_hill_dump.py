from road_vehicle import DumpHauler, DieselRoadVehicle

consist = DumpHauler(id='witch_hill_dump',
                     base_numeric_id=500,
                     name='Witch Hill',
                     road_type='HAUL',
                     power=900,
                     speed=50,  # dibbled up above RL for game balance
                     type_base_running_cost_points=30,  # dibble running costs for game balance
                     vehicle_life=40,
                     intro_date=2007)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=85,  # much bigger is not much better here
                 vehicle_length=7,
                 effects=['EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, 1, 10', 'EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, -1, 10'])
