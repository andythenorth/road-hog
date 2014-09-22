import global_constants
from road_vehicle import EngineConsist, GeneralCargoHauler

consist = EngineConsist(id = 'jinglepot',
              base_numeric_id = 120,
              title = 'Jinglepot [General Cargo Truck]',
              replacement_id = '-none',
              power = 100,
              speed = 35,
              vehicle_life = 40,
              intro_date = 1925,
              vehicle_generation=3)

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 10,
                        capacity_freight = 15,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_STEAM',
                        spriterow_num = 0))

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 5,
                        capacity_freight = 15,
                        vehicle_length = 7,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
