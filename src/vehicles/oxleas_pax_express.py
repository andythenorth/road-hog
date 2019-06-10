from road_vehicle import PaxExpressCoachConsist, DieselVehicleUnit

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus

consist = PaxExpressCoachConsist(id='oxleas_pax_express',
                          base_numeric_id=610,
                          name='Oxleas',
                          power=240,
                          speed=75,
                          gen=4,
                          intro_date_offset=-4)  # introduce earlier than gen epoch by design

consist.add_unit(base_platform=None, # coaches have no base platform by design currently
                 type=DieselVehicleUnit,
                 vehicle_length=7)
