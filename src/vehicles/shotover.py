import global_constants
from road_vehicle import LivestockHauler

consist = LivestockHauler(id='shotover',
                          base_numeric_id=370,
                          title='Shotover [Livestock Tram]',
                          tram_type='ELRL',
                          vehicle_life=40,
                          intro_date=1941)

consist.add_unit(capacity=36,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 10'],
                 repeat=2)

consist.add_model_variant(spritesheet_suffix=0)
