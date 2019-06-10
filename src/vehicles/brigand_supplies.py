from road_vehicle import SuppliesCakeConsist, DieselVehicleUnit
# equiv. Scammell Highwayman or Explorer with dolly low loader trailer - not huge

consist = SuppliesCakeConsist(id='brigand_supplies',
                       base_numeric_id=540,
                       name='Brigand',
                       power=480,
                       gen=3)

consist.add_unit(base_platform=None, # no base platform by design currently
                 type=DieselVehicleUnit,
                 capacity=0,
                 vehicle_length=6,
                 always_use_same_spriterow=True)

consist.add_unit(base_platform=None, # no base platform by design currently
                 #capacity=45,
                 vehicle_length=7)

consist.add_unit(base_platform=None, # no base platform by design currently
                 type=DieselVehicleUnit,
                 capacity=0,
                 vehicle_length=6,
                 unit_num_providing_spriterow_num=0,
                 always_use_same_spriterow=True)
