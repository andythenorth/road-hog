import global_constants
from road_vehicle import EngineConsist, GeneralCargoHauler

consist = EngineConsist(id = 'buildwas',
              base_numeric_id = 100,
              title = 'Buildwas [General Cargo Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 150,
              vehicle_life = 40,
              intro_date = 1870)

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 30,
                        capacity_freight = 0,
                        vehicle_length = 6,
                        visual_effect = 'VISUAL_EFFECT_STEAM',
                        spriterow_num = 0))

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 2,
                        capacity_freight = 9,
                        vehicle_length = 4,
                        spriterow_num = 2), repeat=8)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
