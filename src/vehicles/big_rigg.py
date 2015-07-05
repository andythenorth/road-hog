import global_constants
from road_vehicle import EngineConsist, FlatBedHauler

consist = EngineConsist(id = 'big_rigg',
              base_numeric_id = 660,
              title = 'Big Rigg [Flatbed Truck]',
              replacement_id = '-none',
              power = 450,
              vehicle_life = 40,
              intro_date = 1985)

consist.add_unit(FlatBedHauler(consist = consist,
                        weight = 10,
                        capacity = 20,
                        vehicle_length = 5,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(FlatBedHauler(consist = consist,
                        weight = 5,
                        capacity = 20,
                        vehicle_length = 5,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)