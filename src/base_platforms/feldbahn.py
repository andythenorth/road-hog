from base_platform import BasePlatform
from road_vehicle import DieselVehicleUnit, ElectricVehicleUnit, SteamVehicleUnit


class EngineFeldbahnBase(BasePlatform):
    capacity = 0
    always_use_same_spriterow = True


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
    chassis = 'feldbahn_1_16px'


# wagons

class WagonFeldbahnA(BasePlatform):
    vehicle_length = 3
    cargo_length = 3
    base_platform_spritesheet_name = 'open_wagon_feldbhan_gen_1'
