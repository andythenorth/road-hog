"""Road-specific schema classes, initially only the bus route is used.

The catalogue makes model variants. These classes give them Road Hog behaviour.
CABBAGE Add more child schemas as the rest of the fleet is converted.
"""

import math
import global_constants
import road_hog
from gestalt_graphics.gestalt_graphics import GestaltGraphics


class RoadVehicleBase:
    """Shared bits for any road vehicle. No train stuff wanted here."""

    def __init__(self, producer, catalogue_entry):
        self.producer = producer
        self.catalogue_entry = catalogue_entry
        self.model_def = producer.catalogue.model_def
        self.roster_id = producer.catalogue.roster_id
        self.units = []
        self.id = catalogue_entry.model_variant_id
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
        # CABBAGE MIGRATION SHIM: legacy Consist default; child schemas override as needed.
        self.loading_speed_multiplier = 1
        self.retire_early = -10
        # Road Hog default, not Iron Horse train default (0.3).
        self.tractive_effort_coefficient = (
            self.model_def.tractive_effort_coefficient or 0.7
        )
        self.roadveh_flag_tram = False
        self.base_track_type_name = "ROAD"
        self.type_base_buy_cost_points = 0
        self.type_base_running_cost_points = 0
        self.weight_multiplier = 0.17

    # Docs use an intro year for the sort and the page date range.
    # CABBAGE Old Road Hog returned 999 here as a shim. Use the real year now;
    # check the docs ordering again when we move vehicles with exact intro dates.
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

    @property
    def refittable_classes(self):
        return ",".join(
            set(
                c
                for group in self.class_refit_groups
                for c in global_constants.base_refits_by_class[group]
            )
        )

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
        # CABBAGE Legacy Consist distinguishes road and tram NML expressions.
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

    # CABBAGE The render entry point is deliberately new-schema only, not a Consist shim.
    # CABBAGE Multi-unit / articulated output needs its own legacy parity fixture.
    def render(self, templates, graphics_path):
        result = []
        # CABBAGE MIGRATION SHIM: define articulated callback before unit property references.
        if len(self.units) > 1:
            result.append(
                templates["articulated_parts.pynml"](
                    model_variant=self, global_constants=global_constants
                )
            )
        seen = set()
        for unit in self.units:
            if unit.id in seen:
                continue
            seen.add(unit.id)
            # Vehicle NML template selection belongs to GestaltGraphics.
            template = templates[self.gestalt_graphics.nml_template]
            result.append(
                template(
                    model_variant=self, unit=unit, global_constants=global_constants
                )
            )
        return "".join(result)

    # CABBAGE MIGRATION SHIM: graphics pipelines expect legacy Consist.unique_units.
    # CABBAGE Remove only when graphics consumers use the new model interface.
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
        if getattr(self, "requires_electricity_supply", False):
            return {"RAIL": "ELRL"}[self.base_track_type_name]
        return self.base_track_type_name

    @property
    def sound_effect(self):
        if getattr(self, "_sound_effect", None) is not None:
            return self._sound_effect
        return getattr(self, "default_sound_effect", None)

    @property
    def name_type_suffix(self):
        return (
            "STR_NAME_SUFFIX_"
            + self.name_suffix_consist_type
            + self.name_suffix_vehicle_type
        )

    @property
    def name(self):
        # CABBAGE Power suffix must be supplied by unit integration in Stage 007.
        # CABBAGE Fail explicitly rather than silently inventing Diesel/Steam.
        suffix = getattr(self, "_power_type_suffix", None)
        if suffix is None:
            raise ValueError("Power suffix not resolved for " + self.model_def.model_id)
        return (
            "string(STR_NAME_CONSIST, string(STR_NAME_"
            + self.model_def.model_id.upper()
            + "), string("
            + self.name_type_suffix
            + "), string(STR_NAME_SUFFIX_"
            + suffix
            + "))"
        )


class PassengerVehicle(RoadVehicleBase):
    """Passenger defaults for buses, coaches and such when they get moved."""

    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.default_cargos = global_constants.default_cargos["pax"]
        self.autorefit = True
        self.loading_speed_multiplier = 3


class Bus(PassengerVehicle):
    """Just bus-specific bits for now. Leyburn is the first one."""

    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.vehicle_role = "bus"
        self._sound_effect = "SOUND_DEPARTURE_OLD_RV_1"
        # CABBAGE Check sound/name defaults against each old bus when moving fleet.

    @property
    def name(self):
        return (
            "string(STR_NAME_CONSIST, string(STR_NAME_"
            + self.model_def.model_id.upper()
            + "), string(STR_NAME_SUFFIX_BUS), string(STR_NAME_SUFFIX_DIESEL))"
        )


# CABBAGE BEGIN GENERATED FLEET SCHEMAS STAGE 005
import polar_fox
import gestalt_graphics.graphics_constants as graphics_constants
from gestalt_graphics.gestalt_graphics import (
    GestaltGraphicsPrecompositedCargo,
    GestaltGraphicsLiveryOnly,
    GestaltGraphicsCustom,
)


# CABBAGE The original track mixins use class attributes; keep that composition.
class TrackTypeMixinBase:
    base_track_type_name = None
    roadveh_flag_tram = False
    tractive_effort_coefficient = None
    name_suffix_vehicle_type = None
    vehicle_role = None


class TrackTypeMixinCake(TrackTypeMixinBase):
    base_track_type_name = "LOLZ"
    tractive_effort_coefficient = 0.7
    name_suffix_vehicle_type = "_TRUCK"
    vehicle_role = "lolz"


class TrackTypeMixinFeldbahn(TrackTypeMixinBase):
    base_track_type_name = "RAIL"
    roadveh_flag_tram = True
    tractive_effort_coefficient = 0.3
    name_suffix_vehicle_type = "_TRAM"
    vehicle_role = "feldbahn"


class TrackTypeMixinHEQS(TrackTypeMixinBase):
    base_track_type_name = "HEQS"
    tractive_effort_coefficient = 0.7
    name_suffix_vehicle_type = "_TRUCK"
    vehicle_role = "freight_truck"


class TrackTypeMixinTram(TrackTypeMixinBase):
    base_track_type_name = "RAIL"
    roadveh_flag_tram = True
    tractive_effort_coefficient = 0.4
    name_suffix_vehicle_type = "_TRAM"
    vehicle_role = "freight_tram"


class TrackTypeMixinTruckBusCoach(TrackTypeMixinBase):
    base_track_type_name = "ROAD"
    tractive_effort_coefficient = 0.7
    name_suffix_vehicle_type = "_TRUCK"
    vehicle_role = "freight_truck"


class BoxHaulerConsistBase(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.name_suffix_consist_type = "BOX"
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = [
            "MAIL",
            "GRAI",
            "WHEA",
            "MAIZ",
            "FRUT",
            "BEAN",
            "NITR",
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
        self.class_refit_groups = []
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
        self.class_refit_groups = []
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
        self.class_refit_groups = []
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
        self.class_refit_groups = []
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
        self.class_refit_groups = []
        self.label_refits_allowed = []
        self.label_refits_disallowed = ["TOUR"]
        self.default_cargos = global_constants.default_cargos["mail"]
        self.weight_multiplier = 0.2


class MetalHaulerConsistBase(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.name_suffix_consist_type = "METAL"
        self.autorefit = True
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
        self.class_refit_groups = []
        self.label_refits_allowed = []
        self.label_refits_disallowed = ["TOUR"]
        self.default_cargos = global_constants.default_cargos["open"]
        self.gestalt_graphics = GestaltGraphicsPrecompositedCargo(bulk=True, piece="open")


class PaxHaulerConsistBase(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.autorefit = True
        self.class_refit_groups = []
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
        self.class_refit_groups = []
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
        self.class_refit_groups = []
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


class BoxFeldbahn(BoxHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinFeldbahn.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinFeldbahn.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinFeldbahn.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinFeldbahn.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinFeldbahn.vehicle_role


class BoxTram(BoxHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTram.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTram.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTram.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinTram.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinTram.vehicle_role


class BoxTruck(BoxHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTruckBusCoach.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTruckBusCoach.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTruckBusCoach.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = (
            TrackTypeMixinTruckBusCoach.name_suffix_vehicle_type
        )
        self.vehicle_role = TrackTypeMixinTruckBusCoach.vehicle_role


class CoveredHopperTram(CoveredHopperHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTram.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTram.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTram.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinTram.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinTram.vehicle_role


class CoveredHopperTruck(CoveredHopperHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTruckBusCoach.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTruckBusCoach.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTruckBusCoach.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = (
            TrackTypeMixinTruckBusCoach.name_suffix_vehicle_type
        )
        self.vehicle_role = TrackTypeMixinTruckBusCoach.vehicle_role


class DumpFeldbahn(DumpHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinFeldbahn.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinFeldbahn.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinFeldbahn.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinFeldbahn.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinFeldbahn.vehicle_role


class DumpHEQS(DumpHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinHEQS.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinHEQS.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinHEQS.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinHEQS.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinHEQS.vehicle_role


class DumpTram(DumpHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTram.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTram.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTram.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinTram.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinTram.vehicle_role


class DumpTruck(DumpHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTruckBusCoach.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTruckBusCoach.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTruckBusCoach.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = (
            TrackTypeMixinTruckBusCoach.name_suffix_vehicle_type
        )
        self.vehicle_role = TrackTypeMixinTruckBusCoach.vehicle_role


class EdiblesTankerTram(EdiblesTankerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTram.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTram.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTram.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinTram.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinTram.vehicle_role


class EdiblesTankerTruck(EdiblesTankerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTruckBusCoach.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTruckBusCoach.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTruckBusCoach.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = (
            TrackTypeMixinTruckBusCoach.name_suffix_vehicle_type
        )
        self.vehicle_role = TrackTypeMixinTruckBusCoach.vehicle_role


class FlatFeldbahn(FlatbedHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinFeldbahn.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinFeldbahn.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinFeldbahn.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinFeldbahn.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinFeldbahn.vehicle_role


class FlatbedTram(FlatbedHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTram.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTram.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTram.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinTram.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinTram.vehicle_role


class FlatbedTruck(FlatbedHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTruckBusCoach.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTruckBusCoach.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTruckBusCoach.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = (
            TrackTypeMixinTruckBusCoach.name_suffix_vehicle_type
        )
        self.vehicle_role = TrackTypeMixinTruckBusCoach.vehicle_role


class FruitVegFeldbahn(FruitVegHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinFeldbahn.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinFeldbahn.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinFeldbahn.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinFeldbahn.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinFeldbahn.vehicle_role


class FruitVegTram(FruitVegHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTram.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTram.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTram.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinTram.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinTram.vehicle_role


class IntermodalHauler(RoadVehicleBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.name_suffix_consist_type = "INTERMODAL"
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = global_constants.allowed_refits_by_label[
            "box_freight"
        ]
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label[
            "legacy_disallowed_express"
        ]
        self.default_cargos = global_constants.default_cargos["box"]
        self.loading_speed_multiplier = 2


class LivestockFeldbahn(LivestockHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinFeldbahn.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinFeldbahn.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinFeldbahn.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinFeldbahn.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinFeldbahn.vehicle_role


class LivestockTram(LivestockHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTram.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTram.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTram.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinTram.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinTram.vehicle_role


class LivestockTruck(LivestockHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTruckBusCoach.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTruckBusCoach.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTruckBusCoach.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = (
            TrackTypeMixinTruckBusCoach.name_suffix_vehicle_type
        )
        self.vehicle_role = TrackTypeMixinTruckBusCoach.vehicle_role


class LogHEQS(LogHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinHEQS.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinHEQS.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinHEQS.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinHEQS.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinHEQS.vehicle_role


class MailTram(MailHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTram.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTram.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTram.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinTram.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinTram.vehicle_role
        self.vehicle_role = "mail_tram"


class MailTruck(MailHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTruckBusCoach.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTruckBusCoach.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTruckBusCoach.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = (
            TrackTypeMixinTruckBusCoach.name_suffix_vehicle_type
        )
        self.vehicle_role = TrackTypeMixinTruckBusCoach.vehicle_role
        self.vehicle_role = "mail_truck"


class OpenFeldbahn(OpenHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinFeldbahn.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinFeldbahn.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinFeldbahn.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinFeldbahn.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinFeldbahn.vehicle_role


class OpenTram(OpenHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTram.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTram.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTram.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinTram.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinTram.vehicle_role


class OpenTruck(OpenHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTruckBusCoach.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTruckBusCoach.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTruckBusCoach.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = (
            TrackTypeMixinTruckBusCoach.name_suffix_vehicle_type
        )
        self.vehicle_role = TrackTypeMixinTruckBusCoach.vehicle_role


class PaxLocalTram(PaxHaulerLocalConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTram.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTram.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTram.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinTram.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinTram.vehicle_role
        self._sound_effect = "SOUND_LEVEL_CROSSING"
        self.vehicle_role = "pax_tram"

    @property
    def name_type_suffix(self):
        return "STR_NAME_SUFFIX_PASSENGER_TRAM"


class PaxExpressCoach(PaxHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTruckBusCoach.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTruckBusCoach.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTruckBusCoach.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = (
            TrackTypeMixinTruckBusCoach.name_suffix_vehicle_type
        )
        self.vehicle_role = TrackTypeMixinTruckBusCoach.vehicle_role
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD
        self.weight_multiplier = 0.2
        self._sound_effect = "SOUND_DEPARTURE_OLD_BUS"
        self.vehicle_role = "coach"

    @property
    def name_type_suffix(self):
        return "STR_NAME_SUFFIX_COACH"


class RefrigeratedTram(RefrigeratedHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTram.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTram.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTram.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinTram.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinTram.vehicle_role


class RefrigeratedTruck(RefrigeratedHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTruckBusCoach.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTruckBusCoach.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTruckBusCoach.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = (
            TrackTypeMixinTruckBusCoach.name_suffix_vehicle_type
        )
        self.vehicle_role = TrackTypeMixinTruckBusCoach.vehicle_role


class SuppliesCake(SuppliesHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinCake.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinCake.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinCake.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinCake.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinCake.vehicle_role


class TankerFeldbahn(TankerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinFeldbahn.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinFeldbahn.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinFeldbahn.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinFeldbahn.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinFeldbahn.vehicle_role


class TankerTram(TankerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTram.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTram.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTram.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinTram.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinTram.vehicle_role


class TankerTruck(TankerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinTruckBusCoach.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinTruckBusCoach.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinTruckBusCoach.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = (
            TrackTypeMixinTruckBusCoach.name_suffix_vehicle_type
        )
        self.vehicle_role = TrackTypeMixinTruckBusCoach.vehicle_role


class MetalHEQSBase(MetalHaulerConsistBase):
    def __init__(self, producer, catalogue_entry):
        super().__init__(producer, catalogue_entry)
        self.base_track_type_name = TrackTypeMixinHEQS.base_track_type_name
        self.roadveh_flag_tram = TrackTypeMixinHEQS.roadveh_flag_tram
        self.tractive_effort_coefficient = (
            TrackTypeMixinHEQS.tractive_effort_coefficient
        )
        self.name_suffix_vehicle_type = TrackTypeMixinHEQS.name_suffix_vehicle_type
        self.vehicle_role = TrackTypeMixinHEQS.vehicle_role


# CABBAGE END GENERATED FLEET SCHEMAS STAGE 005

# CABBAGE BEGIN SCHEMA BEHAVIOUR STAGE 006
# CABBAGE Dynamic method installation is deliberately NOT used: the definitions
# CABBAGE below are added inside their target class bodies by this installer.
# CABBAGE END SCHEMA BEHAVIOUR STAGE 006
