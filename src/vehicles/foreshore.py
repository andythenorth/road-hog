import global_constants
from road_vehicle import EngineConsist, IntermodalHauler

consist = EngineConsist(id = 'foreshore',
              base_numeric_id = 200,
              title = 'Foreshore [Intermodal Hauler]',
              replacement_id = '-none',
              power = 950,
              speed = 55,
              buy_cost = 69,
              fixed_run_cost_factor = 3.5,
              fuel_run_cost_factor = 1.0,
              vehicle_life = 40,
              intro_date = 1959,
              graphics_status = '')

consist.add_unit(IntermodalHauler(consist = consist,
                        weight = 50,
                        capacity_freight = 50,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
