from road_vehicle import PaxHauler

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus

consist = PaxHauler(id='topley_pax',
                    base_numeric_id=60,
                    name='Topley [Bus]',
                    power=360,
                    speed=55,
                    vehicle_life=40,
                    intro_date=1990)

consist.add_unit(capacity=72,
                 vehicle_length=7,
                 visual_effect='VISUAL_EFFECT_DIESEL')

