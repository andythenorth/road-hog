from base_platform import BasePlatform
from road_vehicle import DieselVehicleUnit, SteamVehicleUnit


class SemiTractorTruckBase(BasePlatform):
    always_use_same_spriterow = True
    unit_is_semi_tractor = True

    def get_spritesheet_name_body_or_complete_vehicle(self, consist):
        foo = self._get_spritesheet_name_from_class_name(consist)
        if foo == 'diesel_conventional_cab_semi_tractor_truck_gen_4A':
            print(consist.id)
            return foo
        else:
            return None


# semi-trucks

class SteamCaboverSemiTractorTruckGen2A(SemiTractorTruckBase):
    type = SteamVehicleUnit
    vehicle_length = 2
    semi_truck_shift_offset_jank = 2
    effects = ['EFFECT_SPRITE_STEAM, -3, 0, 12']


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

# rigid trucks

class SteamCaboverRigidTruckGen2A(BasePlatform):
    type = SteamVehicleUnit
    vehicle_length = 5
    cargo_length = 3
    effects = ['EFFECT_SPRITE_STEAM, -3, 0, 12']


class DieselCaboverRigidTruckGen3A(BasePlatform):
    type = DieselVehicleUnit
    vehicle_length = 5
    cargo_length = 3
    effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10']


class DieselCaboverRigidTruckGen4A(BasePlatform):
    type = DieselVehicleUnit
    vehicle_length = 5
    cargo_length = 3
    effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10']


class DieselCaboverRigidTruckGen4B(BasePlatform):
    type = DieselVehicleUnit
    vehicle_length = 6
    cargo_length = 4
    effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10']


class DieselCaboverRigidTruckGen5A(BasePlatform):
    type = DieselVehicleUnit
    vehicle_length = 5
    cargo_length = 3
    effects = ['EFFECT_SPRITE_DIESEL, -2, 1, 10', 'EFFECT_SPRITE_DIESEL, -2, -1, 10']
