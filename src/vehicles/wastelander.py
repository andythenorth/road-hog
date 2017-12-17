import global_constants
from road_vehicle import OpenHauler

consist = OpenHauler(id='wastelander',
                     base_numeric_id=1010,
                     title='Wastelander [General Cargo Tram]',
                     roadveh_flag_tram=True,
                     power=90,
                     vehicle_life=40,
                     intro_date=1870)

consist.add_unit(capacity=0,
                 vehicle_length=4,
                 visual_effect='VISUAL_EFFECT_STEAM')

consist.add_unit(capacity=10,
                 vehicle_length=3,
                 repeat=2)

consist.add_unit(capacity=10,
                 vehicle_length=3)

consist.add_model_variant(intro_date=0,
                          end_date=global_constants.max_game_date,
                          spritesheet_suffix=0)
