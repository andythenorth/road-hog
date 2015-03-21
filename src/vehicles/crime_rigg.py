import global_constants
from road_vehicle import EngineConsist, SuppliesHauler
# 'inspired by' Scammell 100t low loader, but much smaller

consist = EngineConsist(id = 'crime_rigg',
              base_numeric_id = 530,
              title = 'Crime Rigg [Supplies Truck]',
              replacement_id = '-none',
              power = 240,
              speed = 35,
              vehicle_life = 40,
              intro_date = 1920)

consist.add_unit(SuppliesHauler(consist = consist,
                        weight = 10,
                        capacity = 0,
                        vehicle_length = 5,
                        effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                        effects = ['EFFECT_SPRITE_STEAM, -3, 0, 12'],
                        spriterow_num = 0))

consist.add_unit(SuppliesHauler(consist = consist,
                        weight = 7,
                        capacity = 45,
                        vehicle_length = 7,
                        spriterow_num = 1))

consist.add_unit(SuppliesHauler(consist = consist,
                        weight = 10,
                        capacity = 0,
                        vehicle_length = 5,
                        effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                        effects = ['EFFECT_SPRITE_STEAM, -5, 0, 12'],
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
