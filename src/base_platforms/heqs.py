from base_platform import BasePlatform
from road_vehicle import DieselVehicleUnit


class SemiTractorHaulerBase(BasePlatform):
    capacity = 0
    always_use_same_spriterow = True
    unit_is_semi_tractor = True


class DieselConventionalCabSemiTractorHaulerGen3A(SemiTractorHaulerBase):
    type = DieselVehicleUnit
    vehicle_length = 2
    semi_truck_shift_offset_jank = 3
    effects = ['EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, 1, 10',
               'EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, -1, 10']
