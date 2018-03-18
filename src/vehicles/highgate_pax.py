from road_vehicle import PaxHauler

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus

consist = PaxHauler(id='highgate',
                    base_numeric_id=590,
                    title='Highgate [Bus]',
                    power=240,
                    speed=50,
                    vehicle_life=40,
                    intro_date=1964)

consist.add_unit(capacity=60,
                 vehicle_length=7,
                 visual_effect='VISUAL_EFFECT_DIESEL')

