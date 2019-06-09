from road_vehicle import PaxExpressCoachConsist, DieselVehicleUnit

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus

consist = PaxExpressCoachConsist(id='acton_pax_express',
                          base_numeric_id=600,
                          name='Acton',
                          power=360,
                          speed=90,
                          vehicle_life=40,
                          gen=5,
                          intro_date_offset=-7)  # introduce earlier than gen epoch by design

consist.add_unit(type=DieselVehicleUnit,
                 vehicle_length=7)
