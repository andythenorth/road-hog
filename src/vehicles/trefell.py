import global_constants
from road_vehicle import RVConsist, LogHauler

consist = RVConsist(id = 'trefell',
              base_numeric_id = 480,
              title = 'Trefell [Logging Truck]',
              replacement_id = '-none',
              power = 100,
              vehicle_life = 40,
              intro_date = 1910)

consist.add_unit(LogHauler(consist = consist,
                        weight = 7,
                        capacity = 0,
                        vehicle_length = 4,
                        effect_spawn_model = 'EFFECT_SPAWN_MODEL_DIESEL',
                        effects = ['EFFECT_SPRITE_STEAM, -5, 0, 12'],
                        spriterow_num = 0))

consist.add_unit(LogHauler(consist = consist,
                        weight = 3,
                        capacity = 40,
                        vehicle_length = 6,
                        spriterow_num = 3))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
