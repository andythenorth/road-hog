import global_constants
from road_vehicle import EngineConsist, PaxHauler

consist = EngineConsist(id = 'leyburn',
              base_numeric_id = 20,
              title = 'Leyburn [Bus]',
              str_type_info = 'COASTER',
              replacement_id = '-none',
              power = 950,
              speed = 35,
              buy_cost = 69,
              fixed_run_cost_factor = 3.5,
              fuel_run_cost_factor = 1.0,
              vehicle_life = 40,
              intro_date = 1920,
              graphics_status = '')

consist.add_unit(PaxHauler(consist = consist,
                        weight = 10,
                        capacity_pax = 30,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
