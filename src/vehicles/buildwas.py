import global_constants
from road_vehicle import EngineConsist, GeneralCargoHauler

consist = EngineConsist(id = 'buildwas',
              base_numeric_id = 100,
              title = 'Buildwas [General Cargo Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 150,
              speed = 20,
              buy_cost = 69,
              fixed_run_cost_factor = 3.5,
              fuel_run_cost_factor = 1.0,
              vehicle_life = 40,
              intro_date = 1870,
              graphics_status = '')

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 30,
                        capacity_freight = 0,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 2,
                        capacity_freight = 9,
                        vehicle_length = 7,
                        spriterow_num = 0), repeat=8)

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 4,
                        capacity_freight = 0,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
