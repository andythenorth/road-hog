from road_vehicle import MailTruckConsist, DieselRoadVehicle

consist = MailTruckConsist(id='littleduke_mail',
                    base_numeric_id=270,
                    name='Littleduke',
                    power=380,
                    speed=90,
                    vehicle_life=40,
                    gen=5,
                    intro_date_offset=1)  # introduce later than gen epoch by design

consist.add_unit(type=DieselRoadVehicle,
                 capacity=25,
                 vehicle_length=6)
