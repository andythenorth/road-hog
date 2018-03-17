import global_constants
from road_vehicle import CoveredHopperHauler

consist = CoveredHopperHauler(id='limebreach',
                              base_numeric_id=260,
                              title='Limebreach [Covered Hopper Truck]',
                              semi_truck_so_redistribute_capacity=True,
                              vehicle_life=40,
                              intro_date=1949)

consist.add_unit(capacity=0,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 effects=['EFFECT_SPRITE_DIESEL, -2, 1, 10'])

consist.add_unit(capacity=30,
                 vehicle_length=5)

consist.add_model_variant(spritesheet_suffix=0)
