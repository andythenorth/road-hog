import global_constants
from road_vehicle import LogHauler

consist = LogHauler(id='griff',
                    base_numeric_id=220,
                    title='Griff [Logging Truck]',
                    road_type='HAUL',
                    power=100,  # custom power
                    vehicle_life=40,
                    intro_date=1870)

consist.add_unit(capacity=0,
                 vehicle_length=4,
                 effect_spawn_model='EFFECT_SPAWN_MODEL_STEAM',
                 effects=['EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -5, 0, 12'],
                 always_use_same_spriterow=True)

consist.add_unit(capacity=40,
                 vehicle_length=6)

consist.add_model_variant(intro_date=0,
                          end_date=global_constants.max_game_date,
                          spritesheet_suffix=0)
