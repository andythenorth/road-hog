import global_constants
from road_vehicle import EngineConsist, CourierCar

consist = EngineConsist(id = 'littleduke',
              base_numeric_id = 180,
              title = 'Littleduke [Courier Truck]',
              replacement_id = '-none',
              power = 380,
              vehicle_life = 40,
              intro_date = 1998)

consist.add_unit(CourierCar(consist = consist,
                        weight = 7,
                        capacity = 25,
                        vehicle_length = 5,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
