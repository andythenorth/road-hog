from road_vehicle import MailTruckConsist, DieselRoadVehicle

consist = MailTruckConsist(id='goldmire_mail',
                    base_numeric_id=200,
                    name='Goldmire',
                    power=250,  # custom power
                    speed=75,
                    vehicle_life=40,
                    gen=4,
                    intro_date_offset=1)  # introduce later than gen epoch by design

consist.add_unit(type=DieselRoadVehicle,
                 capacity=25,
                 vehicle_length=6)
