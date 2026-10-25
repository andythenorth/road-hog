"""Road Hog unit calculations adapted from src/road_vehicle.py.

UnitDef, not a Consist, provides declared vehicle_length/capacity/chassis.
"""

import math
import global_constants


class RoadVehicleUnit:
    def __init__(self, model_variant, unit_def, id, numeric_id):
        self.model_variant = model_variant
        self.unit_def = unit_def
        self.id = id
        self.numeric_id = numeric_id
        self.unit_position_in_consist = len(model_variant.units)
        self.effects = unit_def.effects or []
        self.default_effect_sprite = None
        self._effect_spawn_model = None
        self.semi_truck_shift_offset_jank = None
        self.unit_num_providing_spriterow_num = None
        self.always_use_same_spriterow = False
        self.unit_is_semi_tractor = False

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


class DieselVehicleUnit(RoadVehicleUnit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._effect_spawn_model = "EFFECT_SPAWN_MODEL_DIESEL"
        self.default_effect_sprite = "EFFECT_SPRITE_DIESEL"
