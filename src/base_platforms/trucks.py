from base_platform import BasePlatform
from road_vehicle import DieselVehicleUnit, SteamVehicleUnit


class SemiTractorTruckBase(BasePlatform):
    capacity = 0
    always_use_same_spriterow = True
    semi_truck_so_redistribute_capacity = True

class DieselCaboverSemiTractorTruckGen3A(SemiTractorTruckBase):
    type = DieselVehicleUnit
    vehicle_length = 2
    semi_truck_shift_offset_jank = 2
    effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10']


class DieselCaboverSemiTractorTruckGen4A(SemiTractorTruckBase):
    type = DieselVehicleUnit
    vehicle_length = 2
    semi_truck_shift_offset_jank = 2
    effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10']


class DieselCaboverSemiTractorTruckGen5A(SemiTractorTruckBase):
    type = DieselVehicleUnit
    vehicle_length = 2
    semi_truck_shift_offset_jank = 2
    effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10', 'EFFECT_SPRITE_DIESEL, -2, -1, 10']


class DieselConventionalCabSemiTractorTruckGen3A(SemiTractorTruckBase):
    type = DieselVehicleUnit
    vehicle_length = 2
    semi_truck_shift_offset_jank = 2
    effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10']


class DieselConventionalCabSemiTractorTruckGen4A(SemiTractorTruckBase):
    type = DieselVehicleUnit
    vehicle_length = 2
    semi_truck_shift_offset_jank = 2
    effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10']
