import global_constants
from road_vehicle import RVConsist, OpenHauler

consist = RVConsist(id = 'yeoman',
              base_numeric_id = 170,
              title = 'Yeoman [Open Truck]',
              replacement_id = '-none',
              vehicle_life = 40,
              intro_date = 1968)

consist.add_unit(OpenHauler(consist = consist,
                        weight = 10,
                        capacity = 10,
                        vehicle_length = 5,
                        effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10'],
                        spriterow_num = 0))

consist.add_unit(OpenHauler(consist = consist,
                        weight = 5,
                        capacity = 15,
                        vehicle_length = 5,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
