from road_vehicle import PaxHauler, DieselRoadVehicle

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus

consist = PaxHauler(id='thunder_pax',
                    base_numeric_id=40,
                    name='Thunder',
                    power=160,
                    speed=45,
                    vehicle_life=40,
                    gen=4,
                    intro_date=1935)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=50,
                 vehicle_length=7)
