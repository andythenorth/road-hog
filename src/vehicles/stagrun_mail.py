from road_vehicle import MailTramConsist, ElectricRoadVehicle

consist = MailTramConsist(id='stagrun_mail',
                   base_numeric_id=840,
                   name='Stagrun',
                   power=360,  # custom power
                   vehicle_life=40,
                   gen=3,
                   intro_date_offset=2)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricRoadVehicle,
                 capacity=18,
                 vehicle_length=4,
                 repeat=2)
