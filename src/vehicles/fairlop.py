import global_constants
from road_vehicle import PaxHauler

consist = PaxHauler(id = 'fairlop',
                    base_numeric_id = 10,
                    title = 'Fairlop [Passenger Tram]',
                    tram_type = 'ELRL',
                    vehicle_life = 40,
                    intro_date = 1903)

consist.add_unit(capacity = 30,
                 vehicle_length = 6,
                 effects = ['EFFECT_SPRITE_ELECTRIC, 0, 0, 12'])

consist.add_unit(capacity = 25,
                 vehicle_length = 5,
                 repeat = 2)

consist.add_model_variant(intro_date=0,
                          end_date=global_constants.max_game_date,
                          spritesheet_suffix=0)
