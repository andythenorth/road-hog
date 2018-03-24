from road_vehicle import PaxHauler, DieselRoadVehicle

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus

consist = PaxHauler(id='topley_pax',
                    base_numeric_id=60,
                    name='Topley',
                    power=360,
                    speed=55,
                    vehicle_life=40,
                    intro_date=1990)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=72,
                 vehicle_length=7)
