from road_vehicle import PaxExpressHauler

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus

consist = PaxExpressHauler(id='glenmore_pax_express',
                           base_numeric_id=50,
                           name='Glenmore [Coach]',
                           power=160,
                           speed=55,
                           vehicle_life=40,
                           intro_date=1935)

consist.add_unit(capacity=30,
                 vehicle_length=7,
                 visual_effect='VISUAL_EFFECT_DIESEL')

