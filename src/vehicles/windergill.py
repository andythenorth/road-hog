import global_constants
from road_vehicle import FlatHauler

consist = FlatHauler(id='windergill',
                        base_numeric_id=640,
                        title='Windergill [Flatbed Truck]',
                        vehicle_life=40,
                        intro_date=1939)

consist.add_unit(capacity=15,
                 vehicle_length=5,
                 cargo_length=3,
                 visual_effect='VISUAL_EFFECT_DIESEL')

consist.add_unit(capacity=15,
                 vehicle_length=4,
                 cargo_length=4)

consist.add_model_variant(intro_date=0,
                          end_date=global_constants.max_game_date,
                          spritesheet_suffix=0,
                          graphics_processor=consist.graphics_processors[0])
