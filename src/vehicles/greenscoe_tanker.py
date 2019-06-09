from road_vehicle import TankerTruckConsist, DieselVehicleUnit

consist = TankerTruckConsist(id='greenscoe_tanker',
                      base_numeric_id=210,
                      name='Greenscoe',
                      semi_truck_so_redistribute_capacity=True,
                      gen=3,
                      intro_date_offset=3)  # introduce later than gen epoch by design

consist.add_unit(type=DieselVehicleUnit,
                 vehicle_length=2,
                 semi_truck_shift_offset_jank=2,
                 effects=['EFFECT_SPRITE_DIESEL, -3, 1, 10'],
                 always_use_same_spriterow=True)

consist.add_unit(vehicle_length=5)
