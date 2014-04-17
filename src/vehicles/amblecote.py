import global_constants
from road_vehicle import EngineConsist, GeneralCargoHauler

consist = EngineConsist(id = 'amblecote',
              base_numeric_id = 90,
              title = 'Amblecote [General Cargo Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 90,
              speed = 20,
              vehicle_life = 40,
              intro_date = 1870,
              graphics_status = '')

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 12,
                        capacity_freight = 0,
                        vehicle_length = 4,
                        spriterow_num = 0))

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 2,
                        capacity_freight = 10,
                        vehicle_length = 3,
                        spriterow_num = 2), repeat = 2)

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 4,
                        capacity_freight = 10,
                        vehicle_length = 3,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
