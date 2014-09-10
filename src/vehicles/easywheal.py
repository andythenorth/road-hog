import global_constants
from road_vehicle import EngineConsist, GeneralCargoHauler

consist = EngineConsist(id = 'easywheal',
              base_numeric_id = 130,
              title = 'Easywheal [General Cargo Truck]',
              replacement_id = '-none',
              power = 170,
              speed = 50,
              vehicle_life = 40,
              intro_date = 1944)

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 12,
                        capacity_freight = 20,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 5,
                        capacity_freight = 15,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
