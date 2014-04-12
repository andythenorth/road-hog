import global_constants
from road_vehicle import EngineConsist, CourierTruck

consist = EngineConsist(id = 'tallyho',
              base_numeric_id = 480,
              title = 'Tallyho [Courier Truck]',
              replacement_id = '-none',
              power = 120,
              speed = 60,
              vehicle_life = 40,
              intro_date = 1938,
              graphics_status = '')

consist.add_unit(CourierTruck(consist = consist,
                        weight = 12,
                        capacity_freight = 22,
                        capacity_mail = 45,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
