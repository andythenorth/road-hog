from base_platform import BasePlatform
from road_vehicle import DieselVehicleUnit, SteamVehicleUnit


class SteamEngineFeldbahn1(BasePlatform):
    type = SteamVehicleUnit
    vehicle_length = 4
    capacity = 0
    always_use_same_spriterow = True


class DieselEngineFeldbahn1(BasePlatform):
    type = DieselVehicleUnit
    vehicle_length = 4
    capacity = 0
    always_use_same_spriterow = True


class OpenWagonFeldbahnGen1(BasePlatform):
    vehicle_length = 4
    cargo_length = 3
    capacity = 28


class OpenWagonFeldbahnGen2(BasePlatform):
    vehicle_length = 4
    cargo_length = 3
    capacity = 28


class OpenWagonFeldbahnGen3(BasePlatform):
    vehicle_length = 4
    cargo_length = 3
    capacity = 28


class OpenWagonFeldbahnGen4(BasePlatform):
    vehicle_length = 4
    cargo_length = 3
    capacity = 28
