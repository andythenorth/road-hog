from road_vehicle import DumpTramConsist, ElectricVehicleUnit

consist = DumpTramConsist(id='hawkmoor_dump',
                   base_numeric_id=760,
                   name='Hawkmoor',
                   gen=2,
                   intro_date_offset=2)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricVehicleUnit,
                 vehicle_length=8,
                 repeat=2)
