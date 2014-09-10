import global_constants
from road_vehicle import EngineConsist, GeneralCargoHauler

consist = EngineConsist(id = 'dinkey',
              base_numeric_id = 170,
              title = 'Dinkey [General Cargo Truck]',
              replacement_id = '-none',
              power = 220,
              speed = 65,
              vehicle_life = 40,
              intro_date = 1972)

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 7,
                        capacity_freight = 25,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
