from road_vehicle import PaxLocalBusConsist, DieselVehicleUnit

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus

consist = PaxLocalBusConsist(id='leyburn_pax',
                      base_numeric_id=20,
                      name='Leyburn',
                      power=100,  # custom power
                      speed=40,
                      gen=2,
                      intro_date_offset=-1)  # introduce earlier than gen epoch by design

consist.add_unit(base_platform=None, # buses have no base platform by design currently
                 type=DieselVehicleUnit,
                 vehicle_length=7)
