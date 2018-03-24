from road_vehicle import PaxExpressHauler, DieselRoadVehicle

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus

consist = PaxExpressHauler(id='oxleas_pax_express',
                           base_numeric_id=610,
                           name='Oxleas',
                           power=240,
                           speed=75,
                           vehicle_life=40,
                           intro_date=1964)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=40,
                 vehicle_length=7)
