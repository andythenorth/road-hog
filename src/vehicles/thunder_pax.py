from road_vehicle import PaxLocalBusConsist, DieselVehicleUnit

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus

consist = PaxLocalBusConsist(id='thunder_pax',
                      base_numeric_id=40,
                      name='Thunder',
                      power=160,
                      speed=45,
                      vehicle_life=40,
                      gen=3,
                      intro_date_offset=-4)  # introduce earlier than gen epoch by design

consist.add_unit(type=DieselVehicleUnit,
                 capacity=50,
                 vehicle_length=7)
