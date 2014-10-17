import global_constants
from road_vehicle import EngineConsist, LivestockHauler

consist = EngineConsist(id = 'pigstick',
              base_numeric_id = 330,
              title = 'Pigstick [Livestock Truck]',
              replacement_id = '-none',
              power = 180,
              vehicle_life = 40,
              intro_date = 1943)

consist.add_unit(LivestockHauler(consist = consist,
                        weight = 10,
                        capacity = 17,
                        vehicle_length = 6,
                        visual_effect = 'VISUAL_EFFECT_DIESEL',
                        spriterow_num = 0))

consist.add_unit(LivestockHauler(consist = consist,
                        weight = 10,
                        capacity = 18,
                        vehicle_length = 5,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0)
