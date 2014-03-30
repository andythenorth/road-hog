import global_constants
from road_vehicle import EngineConsist, BulkHauler

consist = EngineConsist(id = 'powerstock',
              base_numeric_id = 240,
              title = 'Powerstock [Dump Truck]',
              str_type_info = 'COASTER',
              replacement_id = '-none',
              power = 650,
              speed = 65,
              buy_cost = 69,
              fixed_run_cost_factor = 3.5,
              fuel_run_cost_factor = 1.0,
              vehicle_life = 40,
              intro_date = 2002,
              graphics_status = '')

consist.add_unit(BulkHauler(consist = consist,
                        weight = 8,
                        capacity_freight = 0,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_unit(BulkHauler(consist = consist,
                        weight = 8,
                        capacity_freight = 45,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
