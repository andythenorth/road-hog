import global_constants
from road_vehicle import EngineConsist, MiningHauler

consist = EngineConsist(id = 'coalhall',
              base_numeric_id = 1000,
              title = 'Coalhall [Mining Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 300,
              speed = 35,
              type_base_running_cost_points = 20, # dibble running costs for game balance
              vehicle_life = 40,
              intro_date = 1910)

consist.add_unit(MiningHauler(consist = consist,
                        weight = 30,
                        capacity = 10,
                        vehicle_length = 6,
                        visual_effect = 'VISUAL_EFFECT_ELECTRIC',
                        spriterow_num = 0))

consist.add_unit(MiningHauler(consist = consist,
                        weight = 2,
                        capacity = 20,
                        vehicle_length = 5,
                        spriterow_num = 1), repeat=2)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
