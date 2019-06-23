from base_platform import BasePlatform
from road_vehicle import DieselVehicleUnit, ElectricVehicleUnit, SteamVehicleUnit


class EngineFeldbahnBase(BasePlatform):
    capacity = 0
    always_use_same_spriterow = True

    def get_spritesheet_name_body_or_complete_vehicle(self, consist):
        return self._get_spritesheet_name_from_class_name(consist)


# engines

class SteamEngineFeldbahnGen1A(EngineFeldbahnBase):
    type = SteamVehicleUnit
    vehicle_length = 3


class SteamEngineFeldbahnGen2A(EngineFeldbahnBase):
    type = SteamVehicleUnit
    vehicle_length = 3


class SteamEngineFeldbahnGen2B(EngineFeldbahnBase):
    type = SteamVehicleUnit
    vehicle_length = 4


class DieselEngineFeldbahnGen3A(EngineFeldbahnBase):
    type = DieselVehicleUnit
    vehicle_length = 3


class DieselEngineFeldbahnGen3B(EngineFeldbahnBase):
    type = DieselVehicleUnit
    vehicle_length = 4


class ElectricEngineFeldbahn1(EngineFeldbahnBase):
    type = ElectricVehicleUnit


# wagons

class WagonFeldbahnA(BasePlatform):
    vehicle_length = 3
    cargo_length = 3

    def get_spritesheet_name_body_or_complete_vehicle(self, consist):
        return consist.name_suffix_consist_type.lower() + '_wagon_feldbahn_gen_1'
