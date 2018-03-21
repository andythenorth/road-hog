from road_vehicle import PaxHauler

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus

consist = PaxHauler(id='thunder_pax',
                    base_numeric_id=40,
                    name='Thunder [Bus]',
                    power=160,
                    speed=45,
                    vehicle_life=40,
                    intro_date=1935)

consist.add_unit(capacity=50,
                 vehicle_length=7,
                 visual_effect='VISUAL_EFFECT_DIESEL')

