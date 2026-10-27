"""Road Hog unit calculations adapted from src/road_vehicle.py.

UnitDef, not a Consist, provides declared vehicle_length/capacity/chassis.
"""

import math
import global_constants


class RoadVehicleUnit:
    provisions_unit_def = False

    def __init__(self, model_variant, unit_def, id, numeric_id):
        self.model_variant = model_variant
        self.unit_def = unit_def
        self.always_use_same_spriterow = bool(unit_def.always_use_same_spriterow)
        self.unit_is_semi_tractor = bool(unit_def.unit_is_semi_tractor)
        self.semi_truck_shift_offset_jank = unit_def.semi_truck_shift_offset_jank
        self.cargo_length = unit_def.cargo_length
        self.id = id
        self.numeric_id = numeric_id
        self.unit_position_in_consist = len(model_variant.units)
        self.effects = unit_def.effects or []
        self.default_effect_sprite = None
        self._effect_spawn_model = None
        self.unit_num_providing_spriterow_num = None

    def get_cargo_classes_as_nml_prop(self, allow_disallow_key):
        result = []
        for class_refit_group in self.model_variant.class_refit_groups:
            for cargo_class in global_constants.base_refits_by_class[
                class_refit_group
            ][allow_disallow_key]:
                result.append(cargo_class)
        return "bitmask(" + ",".join(result) + ")"

    @property
    def chassis(self):
        # CABBAGE MIGRATION SHIM: legacy pipeline expects unit.chassis.
        return self.unit_def.chassis

    @property
    def vehicle_length(self):
        if self.unit_def.chassis:
            return int(int(self.unit_def.chassis[-4:-2]) / 4)
        if self.unit_def.vehicle_length is None:
            raise ValueError("UnitDef must specify vehicle_length or chassis")
        return self.unit_def.vehicle_length

    @property
    def capacity(self):
        if self.unit_def.capacity is not None:
            return self.unit_def.capacity
        model = self.model_variant
        return model.roster.unit_capacity_per_vehicle_type[model.vehicle_role][
            model.model_def.gen - 1
        ]

    def get_loading_speed(self, cargo_type, capacity_multiplier):
        capacity = self.capacity * capacity_multiplier
        if cargo_type == "mail":
            capacity = int(global_constants.mail_multiplier * capacity)
        return max(
            int(self.model_variant.loading_speed_multiplier * math.ceil(capacity / 12)),
            1,
        )

    @property
    def is_lead_unit_of_consist(self):
        return self is self.model_variant.units[0]

    @property
    def availability(self):
        return "ALL_CLIMATES" if self.is_lead_unit_of_consist else "NO_CLIMATE"

    @property
    def effect_spawn_model(self):
        return self._effect_spawn_model or "EFFECT_SPAWN_MODEL_DIESEL"

    @property
    def special_flags(self):
        flags = ["ROADVEH_FLAG_2CC"]
        if self.model_variant.autorefit:
            flags.append("ROADVEH_FLAG_AUTOREFIT")
        if self.model_variant.roadveh_flag_tram:
            flags.append("ROADVEH_FLAG_TRAM")
        return ",".join(flags)

    @property
    def offsets(self):
        return global_constants.default_road_vehicle_offsets[str(self.vehicle_length)]

    @property
    def spriterow_num(self):
        return self.model_variant.units.index(self)

    def get_effects(self):
        effects = []
        for index, effect in enumerate(self.effects):
            effects.append(
                "STORE_TEMP(create_effect(" + effect + "), 0x10" + str(index) + ")"
            )
        if not effects and self.default_effect_sprite:
            effects.append(
                "STORE_TEMP(create_effect("
                + self.default_effect_sprite
                + ", -2, 0, 10), 0x100)"
            )
        return ["[" + ",".join(effects) + "]", len(effects)] if effects else [0, 0]

    def get_spritesheet_name_body_or_complete_vehicle(self):
        return None

    def get_spriteset_template_name(self, reversed, y):
        # Road Hog spriteset templates are named by unit ID, not train symmetry.
        # CABBAGE: migrate spriteset templates to the Iron Horse reusable symmetry-based approach.
        # The current road template does not distinguish reversed variants.
        return "spriteset_template_" + self.id + "(" + str(y) + ")"



class DieselVehicleUnit(RoadVehicleUnit):
    default_sound_effect = "SOUND_DEPARTURE_OLD_RV_1"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._effect_spawn_model = "EFFECT_SPAWN_MODEL_DIESEL"
        self.default_effect_sprite = "EFFECT_SPRITE_DIESEL"


class SteamVehicleUnit(RoadVehicleUnit):
    default_sound_effect = "SOUND_FACTORY"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._effect_spawn_model = "EFFECT_SPAWN_MODEL_STEAM"
        self.default_effect_sprite = "EFFECT_SPRITE_STEAM"


class ElectricVehicleUnit(RoadVehicleUnit):
    default_sound_effect = "SOUND_POWER_STATION"
    requires_electricity_supply = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._effect_spawn_model = "EFFECT_SPAWN_MODEL_ELECTRIC"
        self.default_effect_sprite = "EFFECT_SPRITE_ELECTRIC"




# CABBAGE: generated concrete unit subclasses from former BasePlatform data

class SteamCaboverSemiTractorTruckGen2A(SteamVehicleUnit):
    provisions_unit_def = True
    _always_use_same_spriterow = True
    _unit_is_semi_tractor = True
    _vehicle_length = 2
    _semi_truck_shift_offset_jank = 2
    _effects = ["EFFECT_SPRITE_STEAM, -3, 0, 12"]

    def get_spritesheet_name_body_or_complete_vehicle(self):
        return 'steam_cabover_semi_tractor_truck_gen_2A'


class DieselCaboverSemiTractorTruckGen3A(DieselVehicleUnit):
    provisions_unit_def = True
    _always_use_same_spriterow = True
    _unit_is_semi_tractor = True
    _vehicle_length = 2
    _semi_truck_shift_offset_jank = 2
    _effects = ["EFFECT_SPRITE_DIESEL, -2, 1, 10"]

    def get_spritesheet_name_body_or_complete_vehicle(self):
        return 'diesel_cabover_semi_tractor_truck_gen_3A'


class DieselCaboverSemiTractorTruckGen4A(DieselVehicleUnit):
    provisions_unit_def = True
    _always_use_same_spriterow = True
    _unit_is_semi_tractor = True
    _vehicle_length = 2
    _semi_truck_shift_offset_jank = 2
    _effects = ["EFFECT_SPRITE_DIESEL, -2, 1, 10"]

    def get_spritesheet_name_body_or_complete_vehicle(self):
        return 'diesel_cabover_semi_tractor_truck_gen_4A'


class DieselCaboverSemiTractorTruckGen5A(DieselVehicleUnit):
    provisions_unit_def = True
    _always_use_same_spriterow = True
    _unit_is_semi_tractor = True
    _vehicle_length = 2
    _semi_truck_shift_offset_jank = 2
    _effects = ["EFFECT_SPRITE_DIESEL, -2, 1, 10", "EFFECT_SPRITE_DIESEL, -2, -1, 10"]

    def get_spritesheet_name_body_or_complete_vehicle(self):
        return 'diesel_cabover_semi_tractor_truck_gen_5A'


class DieselConventionalCabSemiTractorTruckGen3A(DieselVehicleUnit):
    provisions_unit_def = True
    _always_use_same_spriterow = True
    _unit_is_semi_tractor = True
    _vehicle_length = 2
    _semi_truck_shift_offset_jank = 2
    _effects = ["EFFECT_SPRITE_DIESEL, -2, 1, 10"]

    def get_spritesheet_name_body_or_complete_vehicle(self):
        return 'diesel_conventional_cab_semi_tractor_truck_gen_3A'


class DieselConventionalCabSemiTractorTruckGen4A(DieselVehicleUnit):
    provisions_unit_def = True
    _always_use_same_spriterow = True
    _unit_is_semi_tractor = True
    _vehicle_length = 2
    _semi_truck_shift_offset_jank = 2
    _effects = ["EFFECT_SPRITE_DIESEL, -2, 1, 10"]

    def get_spritesheet_name_body_or_complete_vehicle(self):
        return 'diesel_conventional_cab_semi_tractor_truck_gen_4A'


class SteamCaboverRigidTruckGen2A(SteamVehicleUnit):
    provisions_unit_def = True
    _vehicle_length = 5
    _cargo_length = 3
    _effects = ["EFFECT_SPRITE_STEAM, -3, 0, 12"]


class DieselCaboverRigidTruckGen3A(DieselVehicleUnit):
    provisions_unit_def = True
    _vehicle_length = 5
    _cargo_length = 3
    _effects = ["EFFECT_SPRITE_DIESEL, -2, 1, 10"]


class DieselCaboverRigidTruckGen4A(DieselVehicleUnit):
    provisions_unit_def = True
    _vehicle_length = 5
    _cargo_length = 3
    _effects = ["EFFECT_SPRITE_DIESEL, -2, 1, 10"]


class DieselCaboverRigidTruckGen4B(DieselVehicleUnit):
    provisions_unit_def = True
    _vehicle_length = 6
    _cargo_length = 4
    _effects = ["EFFECT_SPRITE_DIESEL, -2, 1, 10"]


class DieselCaboverRigidTruckGen5A(DieselVehicleUnit):
    provisions_unit_def = True
    _vehicle_length = 5
    _cargo_length = 3
    _effects = ["EFFECT_SPRITE_DIESEL, -2, 1, 10", "EFFECT_SPRITE_DIESEL, -2, -1, 10"]


class SteamEngineFeldbahnGen1A(SteamVehicleUnit):
    provisions_unit_def = True
    _capacity = 0
    _always_use_same_spriterow = True
    _vehicle_length = 3

    def get_spritesheet_name_body_or_complete_vehicle(self):
        return 'steam_engine_feldbahn_gen_1A'


class SteamEngineFeldbahnGen2A(SteamVehicleUnit):
    provisions_unit_def = True
    _capacity = 0
    _always_use_same_spriterow = True
    _vehicle_length = 3

    def get_spritesheet_name_body_or_complete_vehicle(self):
        return 'steam_engine_feldbahn_gen_2A'


class SteamEngineFeldbahnGen2B(SteamVehicleUnit):
    provisions_unit_def = True
    _capacity = 0
    _always_use_same_spriterow = True
    _vehicle_length = 4

    def get_spritesheet_name_body_or_complete_vehicle(self):
        return 'steam_engine_feldbahn_gen_2B'


class DieselEngineFeldbahnGen3A(DieselVehicleUnit):
    provisions_unit_def = True
    _capacity = 0
    _always_use_same_spriterow = True
    _vehicle_length = 3

    def get_spritesheet_name_body_or_complete_vehicle(self):
        return 'diesel_engine_feldbahn_gen_3A'


class DieselEngineFeldbahnGen3B(DieselVehicleUnit):
    provisions_unit_def = True
    _capacity = 0
    _always_use_same_spriterow = True
    _vehicle_length = 4

    def get_spritesheet_name_body_or_complete_vehicle(self):
        return 'diesel_engine_feldbahn_gen_3B'


class ElectricEngineFeldbahn1(ElectricVehicleUnit):
    provisions_unit_def = True
    _capacity = 0
    _always_use_same_spriterow = True

    def get_spritesheet_name_body_or_complete_vehicle(self):
        return 'electric_engine_feldbah_n1'


class WagonFeldbahnA(RoadVehicleUnit):
    provisions_unit_def = True
    _vehicle_length = 3
    _cargo_length = 3

    def get_spritesheet_name_body_or_complete_vehicle(self):
        return self.model_variant.name_suffix_consist_type.lower() + "_wagon_feldbahn_gen_1"


class SteamEngineTram1(SteamVehicleUnit):
    provisions_unit_def = True
    _capacity = 0
    _always_use_same_spriterow = True
    _vehicle_length = 4


class SteamEngineTram2(SteamVehicleUnit):
    provisions_unit_def = True
    _capacity = 0
    _always_use_same_spriterow = True
    _vehicle_length = 4


class ElectricMotorTram1(ElectricVehicleUnit):
    provisions_unit_def = True
    _vehicle_length = 8


class ElectricMotorTram2(ElectricVehicleUnit):
    provisions_unit_def = True
    _vehicle_length = 8
    _cargo_length = 3


class ElectricMotorTram3(ElectricVehicleUnit):
    provisions_unit_def = True
    _vehicle_length = 8
    _cargo_length = 3


class ElectricMotorTram4(ElectricVehicleUnit):
    provisions_unit_def = True
    _vehicle_length = 8
    _cargo_length = 3


class DieselConventionalCabSemiTractorHaulerGen3A(DieselVehicleUnit):
    provisions_unit_def = True
    _always_use_same_spriterow = True
    _unit_is_semi_tractor = True
    _vehicle_length = 2
    _semi_truck_shift_offset_jank = 3
    _effects = [
        "EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, 1, 10",
        "EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, -1, 10",
    ]

class ElectricTrailerUnit(RoadVehicleUnit):
    @property
    def effect_spawn_model(self):
        return "EFFECT_SPAWN_MODEL_ELECTRIC"

