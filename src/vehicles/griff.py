import global_constants
from road_vehicle import EngineConsist, LogHauler

consist = EngineConsist(id = 'griff',
              base_numeric_id = 420,
              title = 'Griff [Logging Truck]',
              replacement_id = '-none',
              power = 100,
              vehicle_life = 40,
              intro_date = 1870)

consist.add_unit(LogHauler(consist = consist,
                        weight = 7,
                        capacity = 0,
                        vehicle_length = 4,
                        effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                        effects = ['EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -5, 0, 12'],
                        spriterow_num = 0))

consist.add_unit(LogHauler(consist = consist,
                        weight = 3,
                        capacity = 40,
                        vehicle_length = 6,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
