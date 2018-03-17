import global_constants
from road_vehicle import PaxHauler

consist = PaxHauler(id='northbeach',
                    base_numeric_id=690,
                    title='Northbeach [Passenger Tram]',
                    tram_type='ELRL',
                    vehicle_life=40,
                    intro_date=1961)

consist.add_unit(capacity=60,
                 vehicle_length=8,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 12'],
                 repeat=2)

consist.add_model_variant(spritesheet_suffix=0)
