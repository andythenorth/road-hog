import global_constants
from road_vehicle import EngineConsist, LogHauler

consist = EngineConsist(id = 'knockdown',
              base_numeric_id = 430,
              title = 'Knockdown [Logging Truck]',
              str_type_info = 'COASTER',
              replacement_id = '-none',
              power = 950,
              speed = 45,
              buy_cost = 69,
              fixed_run_cost_factor = 3.5,
              fuel_run_cost_factor = 1.0,
              vehicle_life = 40,
              intro_date = 1962,
              graphics_status = '')

consist.add_unit(LogHauler(consist = consist,
                        weight = 10,
                        capacity_freight = 45,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
