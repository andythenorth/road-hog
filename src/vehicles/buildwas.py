import global_constants
from road_vehicle import EngineConsist, MiningHauler

consist = EngineConsist(id = 'buildwas',
              base_numeric_id = 120,
              title = 'Buildwas [Mining Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 150,
              vehicle_life = 40,
              intro_date = 1870)

consist.add_unit(MiningHauler(consist = consist,
                        weight = 30,
                        capacity = 0,
                        vehicle_length = 6,
                        effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM',
                        effects = ['EFFECT_SPRITE_STEAM, -3, 0, 12', 'EFFECT_SPRITE_STEAM, 1, 0, 12'],
                        spriterow_num = 0))

# dibble wagons to get 50t total capacity
consist.add_unit(MiningHauler(consist = consist,
                        weight = 2,
                        capacity = 10,
                        vehicle_length = 3,
                        spriterow_num = 1), repeat=5)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
