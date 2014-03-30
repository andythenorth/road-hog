import global_constants
from road_vehicle import EngineConsist, Tanker

consist = EngineConsist(id = 'meriden',
              base_numeric_id = 400,
              title = 'Meriden [Tanker Truck]',
              str_type_info = 'COASTER',
              replacement_id = '-none',
              power = 200,
              speed = 60,
              buy_cost = 69,
              fixed_run_cost_factor = 3.5,
              fuel_run_cost_factor = 1.0,
              vehicle_life = 40,
              intro_date = 1962,
              graphics_status = '')

consist.add_unit(Tanker(consist = consist,
                        weight = 20,
                        capacity_freight = 0,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_unit(Tanker(consist = consist,
                        weight = 20,
                        capacity_freight = 40,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
