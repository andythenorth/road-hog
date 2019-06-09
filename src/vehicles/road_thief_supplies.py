from road_vehicle import SuppliesCakeConsist, DieselVehicleUnit

consist = SuppliesCakeConsist(id='road_thief_supplies',
                       base_numeric_id=560,
                       name='Road Thief',
                       power=720,
                       gen=4)

consist.add_unit(type=DieselVehicleUnit,
                 capacity=0,
                 vehicle_length=7,
                 always_use_same_spriterow=True)

consist.add_unit(#capacity=45,
                 vehicle_length=7)
