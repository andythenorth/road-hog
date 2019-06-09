from road_vehicle import OpenTramConsist, ElectricVehicleUnit

consist = OpenTramConsist(id='portland_open',
                   base_numeric_id=860,
                   name='Portland',
                   gen=2)

consist.add_unit(type=ElectricVehicleUnit,
                 vehicle_length=8,
                 cargo_length=3,
                 repeat=2)
