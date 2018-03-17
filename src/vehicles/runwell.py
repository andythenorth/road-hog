import global_constants
from road_vehicle import BoxHauler

consist = BoxHauler(id='runwell',
                    base_numeric_id=890,
                    title='Runwell [Box Truck]',
                    semi_truck_so_redistribute_capacity=True,
                    vehicle_life=40,
                    intro_date=1910)

consist.add_unit(capacity=0,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 effect_spawn_model='EFFECT_SPAWN_MODEL_STEAM',
                 effects=['EFFECT_SPRITE_STEAM, -3, 0, 12'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=24,
                 vehicle_length=5)

consist.add_model_variant(spritesheet_suffix=0)
