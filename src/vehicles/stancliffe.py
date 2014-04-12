import global_constants
from road_vehicle import EngineConsist, FoundryHauler

consist = EngineConsist(id = 'stancliffe',
              base_numeric_id = 350,
              title = 'Stancliffe [Foundry Hauler]',
              replacement_id = '-none',
              power = 200,
              speed = 27,
              vehicle_life = 40,
              intro_date = 1928,
              graphics_status = '')

consist.add_unit(FoundryHauler(consist = consist,
                        weight = 20,
                        capacity_freight = 0,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_unit(FoundryHauler(consist = consist,
                        weight = 5,
                        capacity_freight = 20,
                        vehicle_length = 7,
                        spriterow_num = 0), repeat = 5)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
