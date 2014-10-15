import global_constants
from road_vehicle import EngineConsist, MiningHauler

consist = EngineConsist(id = 'broadrock',
              base_numeric_id = 330,
              title = 'Broadrock [Mining Truck]',
              replacement_id = '-none',
              power = 600,
              speed = 45,
              type_base_running_cost_points = 20, # dibble running costs for game balance
              vehicle_life = 40,
              intro_date = 1951)

consist.add_unit(MiningHauler(consist = consist,
                        weight = 20,
                        capacity = 0,
                        vehicle_length = 2,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(MiningHauler(consist = consist,
                        weight = 15,
                        capacity = 75,
                        vehicle_length = 6,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
