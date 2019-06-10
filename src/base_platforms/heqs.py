from base_platform import BasePlatform
from road_vehicle import DieselVehicleUnit


class SemiTractorTruckBase(BasePlatform):
    capacity = 0
    always_use_same_spriterow = True
    unit_is_semi_tractor = True


class DieselConventionalCabSemiTractorTruckGen3A(SemiTractorTruckBase):
    type = DieselVehicleUnit
    vehicle_length = 2
    semi_truck_shift_offset_jank = 2
    effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10']
