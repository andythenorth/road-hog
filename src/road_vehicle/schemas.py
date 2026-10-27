"""Road-specific schema classes.

The catalogue makes model variants. These classes give them Road Hog behaviour.
"""

from functools import cached_property

import global_constants
import road_hog
from gestalt_graphics.gestalt_graphics import GestaltGraphics


class RoadVehicleBase:
    """Shared bits for any road vehicle. No train stuff wanted here."""

    def __init__(self, producer, catalogue_entry):
        self.producer = producer
        self.catalogue_entry = catalogue_entry
        self.units = []
        # The normal bus sprite pipeline just reads and writes the sprite sheet.
        # Other graphics types can choose a different GestaltGraphics later.
        self.gestalt_graphics = GestaltGraphics()
        self.sprites_complete = bool(getattr(self.model_def, "sprites_complete", False))
        self.sprites_additional_liveries_potential = False
        # CABBAGE Sprite file names still use the base model id, not variant ids.
        # Check this when model variants get different graphics/liveries.
        self.graphics_file_id = self.model_def.model_id
        self.label_refits_allowed = []
        self.label_refits_disallowed = []
        self.class_refit_groups = []
        self.cargo_age_period = global_constants.CARGO_AGE_PERIOD
        self.vehicle_life = 40
        self.loading_speed_multiplier = 1
        self.retire_early = -10
        self.type_base_buy_cost_points = 0
        self.type_base_running_cost_points = 0
        self.weight_multiplier = 0.17

    # Docs use an intro year for the sort and the page date range.
    # CABBAGE: Future Iron Horse fixed running-cost API; deliberately unused
    # by the current Road Hog running_cost formula.
    @property
    def fixed_run_cost_points(self):
        if self.model_def.fixed_run_cost_points is not None:
            return self.model_def.fixed_run_cost_points
        return 180

    @property
    def intro_year(self):
        return self.intro_date

    @property
    def roster(self):
        return road_hog.roster_manager.get_roster_by_id(self.roster_id)

    @property
    def intro_date(self):
        return self.roster.intro_dates[self.base_track_type_name][
            self.model_def.gen - 1
        ] + (self.model_def.intro_year_offset or 0)

    @property
    def tractive_effort_coefficient(self):
        if self.model_def.tractive_effort_coefficient is not None:
            return self.model_def.tractive_effort_coefficient

        return self.default_tractive_effort_coefficient

    @property
    def power(self):
        # Iron Horse style power_by_power_source was not implemented as of Oct 2026
        if self.model_def.power is not None:
            return self.model_def.power
        return self.roster.power_bands[self.base_track_type_name][
            self.model_def.gen - 1
        ]

    @property
    def speed(self):
        return (
            self.model_def.speed
            or self.roster.speeds[self.base_track_type_name][self.model_def.gen - 1]
        )

    @property
    def total_capacity(self):
        capacity = sum(u.capacity for u in self.units)
        if self.default_cargos and self.default_cargos[0] == "MAIL":
            return int(global_constants.mail_multiplier * capacity)
        return capacity

    @property
    def weight(self):
        return self.weight_multiplier * self.total_capacity

    def get_engine_cost_points(self):
        return (
            self.power / 100
            + min(self.speed, 90) / 3
            + max(self.intro_date - 1870, 0) / 8
            + min(self.total_capacity, 255)
        )

    @property
    def buy_cost(self):
        return 0.5 * self.get_engine_cost_points() + self.type_base_buy_cost_points

    @property
    def running_cost(self):
        return int(self.get_engine_cost_points() + self.type_base_running_cost_points)

    @property
    def model_life(self):
        return "VEHICLE_NEVER_EXPIRES"

    def get_label_refits_allowed(self):
        return ",".join(self.label_refits_allowed)

    def get_label_refits_disallowed(self):
        return ",".join(self.label_refits_disallowed)

    def get_nml_expression_for_default_cargos(self):
        if len(self.default_cargos) == 1:
            return self.default_cargos[0]
        result = self.default_cargos[-1]
        for cargo in reversed(self.default_cargos[:-1]):
            result = 'cargotype_available("' + cargo + '")?' + cargo + ":" + result
        return result

    @property
    def get_expression_for_road_or_tram_type(self):
        prefix = "tram_type:" if self.roadveh_flag_tram else "road_type:"
        return prefix + self.track_type + ";"

    def get_expression_for_roster(self):
        return "param[1]==" + str(self.roster.numeric_id - 1)

    @property
    def buy_menu_x_loc(self):
        if len(self.units) > 1:
            return global_constants.custom_buy_menu_x_loc
        return global_constants.spritesheet_bounding_boxes[6][0]

    @property
    def buy_menu_width(self):
        length = 4 * sum(unit.vehicle_length for unit in self.units)
        return min(length, global_constants.docs_sprite_max_width)

    def render(self, templates, graphics_path):
        template = templates["model_variant_entry_point.pynml"]
        return template(model_variant=self, global_constants=global_constants)

    @property
    def unique_units(self):
        unique_units = []
        for unit in self.units:
            if unit not in unique_units:
                unique_units.append(unit)
        return unique_units

    @property
    def track_type(self):
        # CABBAGE Preserve the legacy electricity-supply roadtype translation.
        if getattr(self.units[0], "requires_electricity_supply", False):
            return {"RAIL": "ELRL"}[self.base_track_type_name]
        return self.base_track_type_name

    @property
    def livery_def(self):
        return self.catalogue_entry.livery_def

    @property
    def catalogue(self):
        return self.catalogue_entry.catalogue

    @property
    def model_id(self):
        return self.catalogue.model_id

    @property
    def model_def(self):
        return self.catalogue.model_def

    @property
    def roster_id(self):
        return self.catalogue.roster_id

    @property
    def id(self):
        return self.catalogue_entry.model_variant_id

    @property
    def base_numeric_id(self):
        return self.model_def.base_numeric_id

    @property
    def is_default_model_variant(self):
        return self.catalogue.is_default_model_variant(self)

    @property
    def name(self):
        return self.model_def.name

    @property
    def str_name_suffix(self):
        if getattr(self, "_str_name_suffix", None) is not None:
            return self._str_name_suffix
        else:
            return None

    def get_name_parts(self, context):
        return ["STR_NAME_" + self.model_id.upper()]

    @cached_property
    def name_as_nml_prop(self):
        name_parts = self.get_name_parts(context="default_name")
        if len(name_parts) == 1:
            result = f"string({name_parts[0]})"
        else:
            result = f"string(STR_NAME_TWO_PARTS, string({name_parts[0]}), string({name_parts[1]}))"
        return result


import polar_fox
import gestalt_graphics.graphics_constants as graphics_constants
from gestalt_graphics.gestalt_graphics import (
    GestaltGraphicsPrecompositedCargo,
    GestaltGraphicsLiveryOnly,
    GestaltGraphicsCustom,
)


class TrackTypeMixinBase:
    base_track_type_name = None
    roadveh_flag_tram = False
    default_tractive_effort_coefficient = None
    vehicle_role = None


class TrackTypeMixinCake(TrackTypeMixinBase):
    base_track_type_name = "LOLZ"
    default_tractive_effort_coefficient = 0.7
    vehicle_role = "lolz"


class TrackTypeMixinFeldbahn(TrackTypeMixinBase):
    base_track_type_name = "RAIL"
    roadveh_flag_tram = True
    default_tractive_effort_coefficient = 0.3
    vehicle_role = "feldbahn"


class TrackTypeMixinHEQS(TrackTypeMixinBase):
    base_track_type_name = "HEQS"
    default_tractive_effort_coefficient = 0.7
    vehicle_role = "freight_truck"


class TrackTypeMixinTram(TrackTypeMixinBase):
    base_track_type_name = "RAIL"
    roadveh_flag_tram = True
    default_tractive_effort_coefficient = 0.4
    vehicle_role = "freight_tram"


class TrackTypeMixinTruckBusCoach(TrackTypeMixinBase):
    base_track_type_name = "ROAD"
    default_tractive_effort_coefficient = 0.7
    vehicle_role = "freight_truck"


class BoxHaulerConsistBase(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.name_suffix_consist_type = "BOX"
        self.autorefit = True
        self.class_refit_groups = ["packaged_freight"]
        self.label_refits_allowed = global_constants.allowed_refits_by_label[
            "legacy_box_freight"
        ]
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label[
            "legacy_disallowed_express"
        ]
        self.default_cargos = global_constants.default_cargos["box"]
        self.weight_multiplier = 0.45
        self.gestalt_graphics = GestaltGraphicsLiveryOnly(
            recolour_maps=polar_fox.constants.tanker_livery_recolour_maps
        )


class CoveredHopperHaulerConsistBase(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.name_suffix_consist_type = "COVERED_HOPPER"
        self.autorefit = True
        self.class_refit_groups = ["covered_hopper_freight_any_grade"]
        self.label_refits_allowed = list(
            set(
                polar_fox.constants.allowed_refits_by_label[
                    "legacy_allowed_covered_hoppers_any_non_food"
                ]
            )
            | set(
                polar_fox.constants.allowed_refits_by_label[
                    "legacy_allowed_covered_hoppers_non_mineral_non_food"
                ]
            )
            | set(
                polar_fox.constants.allowed_refits_by_label[
                    "allowed_farm_food_products"
                ]
            )
        )
        self.label_refits_disallowed = polar_fox.constants.disallowed_refits_by_label[
            "legacy_disallowed_covered_hoppers_all_types"
        ]
        self.default_cargos = global_constants.default_cargos["covered_mineral"]
        self.loading_speed_multiplier = 2
        self.weight_multiplier = 0.45
        self.gestalt_graphics = GestaltGraphicsLiveryOnly(
            recolour_maps=graphics_constants.livestock_livery_recolour_maps
        )


class DumpHaulerConsistBase(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.name_suffix_consist_type = "DUMP"
        self.autorefit = True
        self.class_refit_groups = ["open_bulk_non_food_grade"]
        self.label_refits_allowed = []
        self.label_refits_disallowed = polar_fox.constants.disallowed_refits_by_label[
            "legacy_disallowed_open_bulk"
        ]
        self.default_cargos = global_constants.default_cargos["dump"]
        self.loading_speed_multiplier = 2
        self.weight_multiplier = 0.45
        self.gestalt_graphics = GestaltGraphicsPrecompositedCargo(bulk=True)


class EdiblesTankerConsistBase(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.name_suffix_consist_type = "EDIBLES_TANKER"
        self.autorefit = True
        self.class_refit_groups = ["liquids_food_grade"]
        self.label_refits_allowed = polar_fox.constants.allowed_refits_by_label[
            "legacy_allowed_food_grade_liquid_bulk"
        ]
        self.label_refits_disallowed = polar_fox.constants.disallowed_refits_by_label[
            "legacy_disallowed_food_grade_liquid_bulk"
        ]
        self.default_cargos = global_constants.default_cargos["edibles_tank"]
        self.loading_speed_multiplier = 2
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD
        self.weight_multiplier = 0.5


class FlatbedHaulerConsistBase(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.name_suffix_consist_type = "FLATBED"
        self.autorefit = True
        self.class_refit_groups = ["flatbed_freight"]
        self.label_refits_allowed = polar_fox.constants.allowed_refits_by_label[
            "legacy_allowed_flatbed"
        ]
        self.label_refits_disallowed = []
        self.default_cargos = global_constants.default_cargos["flat"]
        self.gestalt_graphics = GestaltGraphicsPrecompositedCargo(piece="flat")


class FruitVegHaulerConsistBase(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.name_suffix_consist_type = "FRUIT_VEG"
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = polar_fox.constants.allowed_refits_by_label[
            "allowed_farm_food_products"
        ]
        self.label_refits_disallowed = polar_fox.constants.disallowed_refits_by_label[
            "legacy_disallowed_farm_food_products"
        ]
        self.default_cargos = global_constants.default_cargos["farm_products_box"]
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD
        self.weight_multiplier = 0.45
        self.gestalt_graphics = GestaltGraphicsLiveryOnly(
            recolour_maps=graphics_constants.livestock_livery_recolour_maps
        )


class LivestockHaulerConsistBase(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.name_suffix_consist_type = "LIVESTOCK"
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ["LVST"]
        self.label_refits_disallowed = []
        self.default_cargos = ["LVST"]
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD
        self.weight_multiplier = 0.45
        self.gestalt_graphics = GestaltGraphicsLiveryOnly(
            recolour_maps=graphics_constants.livestock_livery_recolour_maps
        )


class LogHaulerConsistBase(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.name_suffix_consist_type = "LOG"
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ["WOOD"]
        self.label_refits_disallowed = []
        self.default_cargos = ["WOOD"]
        self.loading_speed_multiplier = 2
        self.gestalt_graphics = GestaltGraphicsCustom(
            {"WOOD": [0]}, "vehicle_with_precomposited_cargo.pynml", generic_rows=[0]
        )


class MailHaulerConsistBase(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.name_suffix_consist_type = "MAIL"
        self.autorefit = True
        self.class_refit_groups = ["mail", "express_freight"]
        self.label_refits_allowed = []
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label[
            "legacy_disallowed_express"
        ]
        self.default_cargos = global_constants.default_cargos["mail"]
        self.weight_multiplier = 0.2


class MetalHaulerConsistBase(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.name_suffix_consist_type = "METAL"
        self.autorefit = True
        # CABBAGE: Consider consolidating specialist metal labels in Polar Fox.
        self.class_refit_groups = []
        self.label_refits_allowed = ["STEL", "COPR", "IRON", "SLAG"]
        self.label_refits_disallowed = []
        self.default_cargos = global_constants.default_cargos["metal"]
        self.loading_speed_multiplier = 2


class OpenHaulerConsistBase(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.name_suffix_consist_type = "OPEN"
        self.autorefit = True
        self.class_refit_groups = ["all_freight"]
        self.label_refits_allowed = []
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label[
            "legacy_disallowed_express"
        ]
        self.default_cargos = global_constants.default_cargos["open"]
        self.gestalt_graphics = GestaltGraphicsPrecompositedCargo(
            bulk=True, piece="open"
        )


class PaxHaulerConsistBase(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.autorefit = True
        self.class_refit_groups = ["pax"]
        self.label_refits_allowed = []
        self.label_refits_disallowed = []
        self.default_cargos = global_constants.default_cargos["pax"]


class PaxHaulerLocalConsistBase(PaxHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.loading_speed_multiplier = 3
        self.weight_multiplier = 0.17


class RefrigeratedHaulerConsistBase(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.name_suffix_consist_type = "REEFER"
        self.autorefit = True
        self.class_refit_groups = ["refrigerated_freight"]
        self.label_refits_allowed = []
        self.label_refits_disallowed = []
        self.default_cargos = global_constants.default_cargos["reefer"]
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD
        self.weight_multiplier = 0.5
        self.gestalt_graphics = GestaltGraphicsLiveryOnly(
            recolour_maps=graphics_constants.livestock_livery_recolour_maps
        )


class SuppliesHaulerConsistBase(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.name_suffix_consist_type = "SUPPLIES"
        self.autorefit = True
        # CABBAGE: Consider consolidating specialist supplies labels in Polar Fox.
        self.class_refit_groups = []
        self.label_refits_allowed = ["ENSP", "FMSP", "VEHI", "BDMT"]
        self.label_refits_disallowed = []
        self.default_cargos = global_constants.default_cargos["supplies"]
        self.loading_speed_multiplier = 2
        self.weight_multiplier = 0.5
        self.gestalt_graphics = GestaltGraphicsCustom(
            {"ENSP": [0], "FMSP": [0], "VEHI": [0]},
            "vehicle_with_precomposited_cargo.pynml",
            generic_rows=[0],
        )


class TankerConsistBase(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.name_suffix_consist_type = "TANKER"
        self.autorefit = True
        self.class_refit_groups = ["liquids_non_food_grade"]
        self.label_refits_allowed = polar_fox.constants.allowed_refits_by_label[
            "allowed_tanker_products"
        ]
        self.label_refits_disallowed = polar_fox.constants.disallowed_refits_by_label[
            "legacy_disallowed_liquid_bulk"
        ]
        self.default_cargos = global_constants.default_cargos["tank"]
        self.loading_speed_multiplier = 2
        self.weight_multiplier = 0.45
        self.gestalt_graphics = GestaltGraphicsLiveryOnly(
            recolour_maps=polar_fox.constants.tanker_livery_recolour_maps
        )


class BoxFeldbahn(TrackTypeMixinFeldbahn, BoxHaulerConsistBase):
    pass


class BoxTram(TrackTypeMixinTram, BoxHaulerConsistBase):
    pass


class BoxTruck(TrackTypeMixinTruckBusCoach, BoxHaulerConsistBase):
    pass


class CoveredHopperTram(TrackTypeMixinTram, CoveredHopperHaulerConsistBase):
    pass


class CoveredHopperTruck(TrackTypeMixinTruckBusCoach, CoveredHopperHaulerConsistBase):
    pass


class DumpFeldbahn(TrackTypeMixinFeldbahn, DumpHaulerConsistBase):
    pass


class DumpHEQS(TrackTypeMixinHEQS, DumpHaulerConsistBase):
    pass


class DumpTram(TrackTypeMixinTram, DumpHaulerConsistBase):
    pass


class DumpTruck(TrackTypeMixinTruckBusCoach, DumpHaulerConsistBase):
    pass


class EdiblesTankerTram(TrackTypeMixinTram, EdiblesTankerConsistBase):
    pass


class EdiblesTankerTruck(TrackTypeMixinTruckBusCoach, EdiblesTankerConsistBase):
    pass


class FlatFeldbahn(TrackTypeMixinFeldbahn, FlatbedHaulerConsistBase):
    pass


class FlatbedTram(TrackTypeMixinTram, FlatbedHaulerConsistBase):
    pass


class FlatbedTruck(TrackTypeMixinTruckBusCoach, FlatbedHaulerConsistBase):
    pass


class FruitVegFeldbahn(TrackTypeMixinFeldbahn, FruitVegHaulerConsistBase):
    pass


class FruitVegTram(TrackTypeMixinTram, FruitVegHaulerConsistBase):
    pass


class IntermodalHauler(TrackTypeMixinTruckBusCoach, RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.name_suffix_consist_type = "INTERMODAL"
        self.autorefit = True
        self.class_refit_groups = ["all_freight"]
        self.label_refits_allowed = []
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label[
            "legacy_disallowed_express"
        ]
        self.default_cargos = global_constants.default_cargos["box"]
        self.loading_speed_multiplier = 2


class LivestockFeldbahn(TrackTypeMixinFeldbahn, LivestockHaulerConsistBase):
    pass


class LivestockTram(TrackTypeMixinTram, LivestockHaulerConsistBase):
    pass


class LivestockTruck(TrackTypeMixinTruckBusCoach, LivestockHaulerConsistBase):
    pass


class LogHEQS(TrackTypeMixinHEQS, LogHaulerConsistBase):
    pass


class MailTram(TrackTypeMixinTram, MailHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.vehicle_role = "mail_tram"


class MailTruck(TrackTypeMixinTruckBusCoach, MailHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.vehicle_role = "mail_truck"


class OpenFeldbahn(TrackTypeMixinFeldbahn, OpenHaulerConsistBase):
    pass


class OpenTram(TrackTypeMixinTram, OpenHaulerConsistBase):
    pass


class OpenTruck(TrackTypeMixinTruckBusCoach, OpenHaulerConsistBase):
    pass


class PaxLocalBus(TrackTypeMixinTruckBusCoach, PaxHaulerLocalConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self._sound_effect = "SOUND_DEPARTURE_OLD_RV_1"
        self.vehicle_role = "bus"


class PaxLocalTram(TrackTypeMixinTram, PaxHaulerLocalConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self._sound_effect = "SOUND_LEVEL_CROSSING"
        self.vehicle_role = "pax_tram"


class PaxExpressCoach(TrackTypeMixinTruckBusCoach, PaxHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD
        self.weight_multiplier = 0.2
        self._sound_effect = "SOUND_DEPARTURE_OLD_BUS"
        self.vehicle_role = "coach"


class RefrigeratedTram(TrackTypeMixinTram, RefrigeratedHaulerConsistBase):
    pass


class RefrigeratedTruck(TrackTypeMixinTruckBusCoach, RefrigeratedHaulerConsistBase):
    pass


class SuppliesCake(TrackTypeMixinCake, SuppliesHaulerConsistBase):
    pass


class TankerFeldbahn(TrackTypeMixinFeldbahn, TankerConsistBase):
    pass


class TankerTram(TrackTypeMixinTram, TankerConsistBase):
    pass


class TankerTruck(TrackTypeMixinTruckBusCoach, TankerConsistBase):
    pass


class MetalHEQSBase(TrackTypeMixinHEQS, MetalHaulerConsistBase):
    pass
