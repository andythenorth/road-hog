import global_constants
from road_vehicle import EngineConsist, CourierCar

consist = EngineConsist(id = 'stagrun',
              base_numeric_id = 840,
              title = 'Stagrun [Courier Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 300,
              vehicle_life = 40,
              intro_date = 1932)

consist.add_unit(CourierCar(consist = consist,
                        weight = 10,
                        capacity = 40,
                        vehicle_length = 6,
                        effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
