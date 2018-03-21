from road_vehicle import PaxHauler

consist = PaxHauler(id='fairlop_pax',
                    base_numeric_id=10,
                    name='Fairlop [Passenger Tram]',
                    tram_type='ELRL',
                    vehicle_life=40,
                    intro_date=1903)

consist.add_unit(capacity=30,
                 vehicle_length=6,
                 effects=['EFFECT_SPRITE_ELECTRIC, 0, 0, 12'])

consist.add_unit(capacity=25,
                 vehicle_length=5,
                 repeat=2)

