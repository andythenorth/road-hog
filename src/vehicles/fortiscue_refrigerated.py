from road_vehicle import RefrigeratedHauler

consist = RefrigeratedHauler(id='fortiscue_refrigerated',
                             base_numeric_id=180,
                             name='Fortiscue [Reefer Truck]',
                             vehicle_life=40,
                             intro_date=1972)

consist.add_unit(capacity=25,
                 vehicle_length=6,
                 visual_effect='VISUAL_EFFECT_DIESEL')

consist.add_unit(capacity=15,
                 vehicle_length=4)

