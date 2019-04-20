from road_vehicle import PaxHauler, DieselRoadVehicle

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus

consist = PaxHauler(id='highgate_pax',
                    base_numeric_id=590,
                    name='Highgate',
                    power=240,
                    speed=50,
                    vehicle_life=40,
                    gen=4,
                    intro_date=1964)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=60,
                 vehicle_length=7)
