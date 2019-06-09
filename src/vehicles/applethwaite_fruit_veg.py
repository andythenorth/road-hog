from road_vehicle import FruitVegTramConsist, ElectricVehicleUnit

consist = FruitVegTramConsist(id='applethwaite_fruit_veg',
                       base_numeric_id=940,
                       name='Applethwaite',
                       gen=2,
                       intro_date_offset=1)  # introduce later than gen epoch by design

consist.add_unit(type=ElectricVehicleUnit,
                 vehicle_length=8,
                 repeat=2)
