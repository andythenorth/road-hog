from road_vehicle import PaxLocalBusConsist, DieselRoadVehicle

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus

consist = PaxLocalBusConsist(id='highgate_pax',
                      base_numeric_id=590,
                      name='Highgate',
                      power=240,
                      speed=50,
                      vehicle_life=40,
                      gen=4,
                      intro_date_offset=-4)  # introduce earlier than gen epoch by design

consist.add_unit(type=DieselRoadVehicle,
                 capacity=60,
                 vehicle_length=7)
