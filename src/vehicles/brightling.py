import global_constants
from road_vehicle import EngineConsist, GeneralCargoHauler

consist = EngineConsist(id = 'brightling',
              base_numeric_id = 110,
              title = 'Brightling [General Cargo Tram]',
              roadveh_flag_tram = True,
              replacement_id = '-none',
              power = 220,
              vehicle_life = 40,
              intro_date = 1900,)

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 12,
                        capacity_freight = 12,
                        vehicle_length = 6,
                        visual_effect = 'VISUAL_EFFECT_ELECTRIC',
                        spriterow_num = 0), repeat=1)

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 4,
                        capacity_freight = 12,
                        vehicle_length = 4,
                        spriterow_num = 2), repeat=2)

consist.add_unit(GeneralCargoHauler(consist = consist,
                        weight = 4,
                        capacity_freight = 12,
                        vehicle_length = 4,
                        spriterow_num = 1), repeat=2)

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
