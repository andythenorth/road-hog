from road_vehicle import PaxExpressHauler, DieselRoadVehicle

# for each generation, bus and coach variants have same power and intro date
# coaches faster, lower capacity than equivalent bus

consist = PaxExpressHauler(id='big_sky_pax_express',
                           base_numeric_id=620,
                           name='Big Sky',
                           power=220,
                           speed=90,
                           vehicle_life=40,
                           intro_date=1990)

consist.add_unit(type=DieselRoadVehicle,
                 capacity=40,  # coaches never need high capacity
                 vehicle_length=7)
