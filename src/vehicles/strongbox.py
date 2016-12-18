import global_constants
from road_vehicle import CourierCar

consist = CourierCar(id = 'strongbox',
                     base_numeric_id = 830,
                     title = 'Strongbox [Courier Tram]',
                     roadveh_flag_tram = True,
                     tram_type = 'ELTR',
                     power = 480, # custom power
                     vehicle_life = 40,
                     intro_date = 1961)

consist.add_unit(capacity = 36,
                 vehicle_length = 8,
                 effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'])

consist.add_model_variant(intro_date=0,
                          end_date=global_constants.max_game_date,
                          spritesheet_suffix=0)
