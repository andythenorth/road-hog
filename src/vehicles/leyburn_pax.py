from road_vehicle import PaxHauler, DieselRoadVehicle

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus

consist = PaxHauler(id='leyburn_pax',
                    base_numeric_id=20,
                    name='Leyburn',
                    power=100,  # custom power
                    speed=40,
                    vehicle_life=40,
                    intro_date=1909)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=44,
                 vehicle_length=7)
