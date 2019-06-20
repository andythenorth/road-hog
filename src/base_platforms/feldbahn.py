from base_platform import BasePlatform
from road_vehicle import DieselVehicleUnit, ElectricVehicleUnit, SteamVehicleUnit


class EngineFeldbahnBase(BasePlatform):
    capacity = 0
    always_use_same_spriterow = True

    def get_spritesheet_name_body_or_complete_vehicle(self, consist):
        # transform class name to spritesheet ID - somewhat hax
        class_name_split = [char for char in type(self).__name__]
        result = []
        # drop the gen chars, split remainder on uppercase, makes lowercase and adds underscores
        for char in class_name_split[0:-2]:
            if char.isupper():
                result.append('_' + char.lower())
            else:
                result.append(char)
        # put the gen chars back, keeping case
        result.append('_' + ''.join(class_name_split[-2:]))
        result = ''.join(result)
        # drop an extraneous leading underscore
        result = result[1:]
        return result

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
