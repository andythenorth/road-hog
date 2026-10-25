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
        powers = self.model_def.power_by_power_source
        if powers:
            return sum(powers.values())
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
        return "road_type:" + self.base_track_type_name + ";"

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
        seen = set()
        for unit in self.units:
            if unit.id in seen:
                continue
            seen.add(unit.id)
            template = templates["vehicle_default.pynml"]
            result.append(
                template(
                    model_variant=self, unit=unit, global_constants=global_constants
                )
            )
        if len(self.units) > 1:
            result.append(
                templates["articulated_parts.pynml"](
                    model_variant=self, global_constants=global_constants
                )
            )
        return "".join(result)


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
        self.sound_effect = "SOUND_DEPARTURE_OLD_RV_1"
        # CABBAGE Check sound/name defaults against each old bus when moving fleet.

    @property
    def name(self):
        return (
            "string(STR_NAME_CONSIST, string(STR_NAME_"
            + self.model_def.model_id.upper()
            + "), string(STR_NAME_SUFFIX_BUS), string(STR_NAME_SUFFIX_DIESEL))"
        )
