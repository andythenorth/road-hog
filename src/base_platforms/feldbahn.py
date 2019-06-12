from base_platform import BasePlatform
from road_vehicle import DieselVehicleUnit, ElectricVehicleUnit, SteamVehicleUnit


class EngineFeldbahnBase(BasePlatform):
    capacity = 0
    always_use_same_spriterow = True


# engines

class SteamEngineFeldbahn1(EngineFeldbahnBase):
    type = SteamVehicleUnit
    vehicle_length = 4


class SteamEngineFeldbahn2(EngineFeldbahnBase):
    type = SteamVehicleUnit
    vehicle_length = 4


class DieselEngineFeldbahn1(EngineFeldbahnBase):
    type = DieselVehicleUnit
    vehicle_length = 4


class DieselEngineFeldbahn2(EngineFeldbahnBase):
    type = DieselVehicleUnit
    vehicle_length = 4


class ElectricEngineFeldbahn1(EngineFeldbahnBase):
    type = ElectricVehicleUnit
    chassis = 'feldbahn_1_16px'


# wagons

class OpenWagonFeldbahnGen1(BasePlatform):
    vehicle_length = 4
    cargo_length = 3


class OpenWagonFeldbahnGen2(BasePlatform):
    vehicle_length = 4
    cargo_length = 3


class OpenWagonFeldbahnGen3(BasePlatform):
    vehicle_length = 4
    cargo_length = 3


class OpenWagonFeldbahnGen4(BasePlatform):
    vehicle_length = 4
    cargo_length = 3
