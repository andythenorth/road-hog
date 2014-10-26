import global_constants
from road_vehicle import EngineConsist, CourierCar

consist = EngineConsist(id = 'tallyho',
              base_numeric_id = 450,
              title = 'Tallyho [Courier Truck]',
              replacement_id = '-none',
              power = 120,
              vehicle_life = 40,
              intro_date = 1920)

consist.add_unit(CourierCar(consist = consist,
                        weight = 12,
                        capacity = 22,
                        capacity_mail = 45,
                        vehicle_length = 6,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
