import global_constants
from road_vehicle import RefrigeratedHauler

consist = RefrigeratedHauler(id='merrivale',
                             base_numeric_id=300,
                             title='Merrivale [Reefer Truck]',
                             semi_truck_so_redistribute_capacity=True,
                             vehicle_life=40,
                             intro_date=1949)

consist.add_unit(capacity=0,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 visual_effect='VISUAL_EFFECT_DIESEL',
                 always_use_same_spriterow=True)

consist.add_unit(capacity=30,
                 vehicle_length=6)

consist.add_model_variant(intro_date=0,
                          end_date=global_constants.max_game_date,
                          spritesheet_suffix=0)
