import global_constants
from road_vehicle import EngineConsist, CraneEquippedHauler

consist = EngineConsist(id = 'brigand',
              base_numeric_id = 540,
              title = 'Brigand [Crane Truck]',
              replacement_id = '-none',
              power = 170,
              speed = 50,
              vehicle_life = 40,
              intro_date = 1953)

consist.add_unit(CraneEquippedHauler(consist = consist,
                        weight = 20,
                        capacity = 0,
                        vehicle_length = 7,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(CraneEquippedHauler(consist = consist,
                        weight = 20,
                        capacity = 42,
                        vehicle_length = 7,
                        spriterow_num = 0))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
