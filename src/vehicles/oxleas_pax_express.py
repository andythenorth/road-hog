from road_vehicle import PaxExpressCoach, DieselRoadVehicle

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus

consist = PaxExpressCoach(id='oxleas_pax_express',
                          base_numeric_id=610,
                          name='Oxleas',
                          power=240,
                          speed=75,
                          vehicle_life=40,
                          gen=4,
                          intro_date_offset=-4)  # introduce earlier than gen epoch by design

consist.add_unit(type=DieselRoadVehicle,
                 capacity=40,
                 vehicle_length=7)
