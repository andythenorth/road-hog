import global_constants
from road_vehicle import EngineConsist, FlatBedHauler

consist = EngineConsist(id = 'chainburn',
              base_numeric_id = 630,
              title = 'Chainburn [Flatbed Truck]',
              replacement_id = '-none',
              power = 120,
              vehicle_life = 40,
              intro_date = 1920)

consist.add_unit(FlatBedHauler(consist = consist,
                        weight = 10,
                        capacity = 10,
                        vehicle_length = 5,
                        effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                        effects = ['EFFECT_SPRITE_STEAM, -3, 0, 12'],
                        spriterow_num = 0))

consist.add_unit(FlatBedHauler(consist = consist,
                        weight = 5,
                        capacity = 15,
                        vehicle_length = 5,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
