import global_constants
from road_vehicle import EngineConsist, CourierTruck

consist = EngineConsist(id = 'goldmire',
              base_numeric_id = 490,
              title = 'Goldmire [Courier Truck]',
              replacement_id = '-none',
              power = 180,
              speed = 75,
              vehicle_life = 40,
              intro_date = 1971,
              graphics_status = '')

consist.add_unit(CourierTruck(consist = consist,
                        weight = 14,
                        capacity_freight = 25,
                        capacity_mail = 50,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
