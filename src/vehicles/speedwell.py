import global_constants
from road_vehicle import EngineConsist, GeneralCargoHauler

consist = EngineConsist(id = 'speedwell',
              base_numeric_id = 150,
              title = 'Speedwell [General Cargo Truck]',
              replacement_id = '-none',
              power = 450,
              speed = 65,
              vehicle_life = 40,
              intro_date = 1994,
              graphics_status = '')

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 7,
                        capacity_freight = 0,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 8,
                        capacity_freight = 45,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
