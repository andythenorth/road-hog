import global_constants
from road_vehicle import RVConsist, MiningHauler

consist = RVConsist(id = 'witch_hill',
              base_numeric_id = 500,
              title = 'Witch Hill [Mining Truck]',
              replacement_id = '-none',
              power = 1200,
              speed = 55, # dibbled up above RL for game balance
              type_base_running_cost_points = 30, # dibble running costs for game balance
              vehicle_life = 40,
              intro_date = 1989)

consist.add_unit(MiningHauler(consist = consist,
                        weight = 60,
                        capacity = 120,
                        vehicle_length = 7,
                        effects = ['EFFECT_SPRITE_DIESEL, -3, 0, 13'],
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
