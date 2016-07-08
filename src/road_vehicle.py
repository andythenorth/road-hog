import global_constants # expose all constants for easy passing to templates
import utils
import graphics_processor.pipelines
import graphics_processor.utils as graphics_utils

import os.path
currentdir = os.curdir
import sys
sys.path.append(os.path.join('src')) # add to the module search path
import math
import inspect

from chameleon import PageTemplateLoader # chameleon used in most template cases
# setup the places we look for templates
templates = PageTemplateLoader(os.path.join(currentdir, 'src', 'templates'))


from vehicles import numeric_id_defender
from rosters import registered_rosters


class Consist(object):
    """
       'Vehicles' (appearing in buy menu) are composed as articulated consists.
       Each consist comprises one or more vehicle 'units'.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.vehicle_module_path = inspect.stack()[2][1]
        # setup properties for this consist (props either shared for all vehicles, or placed on lead vehicle of consist)
        self.title = kwargs.get('title', None)
        self.base_numeric_id = kwargs.get('base_numeric_id', None)
        self.roadveh_flag_tram = kwargs.get('roadveh_flag_tram', None)
        self.intro_date = kwargs.get('intro_date', None)
        self.replacement_id = kwargs.get('replacement_id', None)
        self.vehicle_life = kwargs.get('vehicle_life', None)
        self._power = kwargs.get('power', None)
        # semi-trucks need some redistribution of capacity to get correct TE (don't use this of other magic, bad idea)
        self.semi_truck_so_redistribute_capacity = kwargs.get('semi_truck_so_redistribute_capacity', False)
        self._speed = kwargs.get('speed', None)
        self.default_cargo = 'PASS' # over-ride in subclass as needed (PASS is sane default)
        self.class_refit_groups = []
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = []
        self.autorefit = False
        self.loading_speed_multiplier = kwargs.get('loading_speed_multiplier', 1)
        self.cargo_age_period = kwargs.get('cargo_age_period', global_constants.CARGO_AGE_PERIOD)
        # arbitrary adjustments of points that can be applied to adjust buy cost and running cost, over-ride in consist as needed
        # values can be -ve or +ve to dibble specific vehicles (but total calculated points cannot exceed 255)
        self.type_base_buy_cost_points = kwargs.get('type_base_buy_cost_points', 0)
        self.type_base_running_cost_points = kwargs.get('type_base_running_cost_points', 0)
        # create a structure to hold model variants
        self.model_variants = []
        # create structure to hold the units
        self.units = []
        # cargo /livery graphics options
        self.cargo_graphics_options = {}
        self.num_cargo_sprite_variants = 0 # over-ridden by subclass when needed
        self.num_spriterows_per_cargo_variant = 2 # assume loading/loaded is the common case
        self.has_empty_state_spriterow = True # assume empty state is common case
        self.vehicle_nml_template = None # use the default template by default
        # roster is set when the vehicle is registered to a roster, only one roster per vehicle
        self.roster_id = None

    def add_model_variant(self, intro_date, end_date, spritesheet_suffix, graphics_processor=None):
        self.model_variants.append(ModelVariant(intro_date, end_date, spritesheet_suffix, graphics_processor))

    def add_unit(self, repeat=1, **kwargs):
        # how many unique units? (units can be repeated, we are using count for numerid ID, so we want uniques)
        count = len(set(self.units))

        unit = RoadVehicle(consist=self, **kwargs)

        if count == 0:
            unit.id = self.id # first vehicle gets no numeric id suffix - for compatibility with buy menu list ids etc
        else:
            unit.id = self.id + '_' + str(count)
        unit.numeric_id = self.get_and_verify_numeric_id(count)

        if self.semi_truck_so_redistribute_capacity:
            if count == 0 and kwargs.get('capacity', 0) != 0:
                # guard against lead unit having capacity set in declared props (won't break, just wrong)
                utils.echo_message("Error: " + self.id + ".  First unit of semi-truck must have capacity 0")
            if count == 1:
                # semi-trucks need some capacity moved to lead unit to gain sufficient TE
                # this automagically does that, allowing capacities to be defined simply on the trailer in the vehicle definition
                # sometimes a greater good requires a small evil, although this will probably go wrong eh?
                if repeat != 1:
                    # guard against unintended application of this to anything except first trailer
                    utils.echo_message("Error: " + self.id + ".  Semi-truck cannot repeat first trailer in consist")
                specified_capacities = unit.capacities
                unit.capacities = [int(math.floor(0.5 * capacity)) for capacity in specified_capacities]
                self.units[0].capacities = [int(math.ceil(0.5 * capacity)) for capacity in specified_capacities]

        for repeat_num in range(repeat):
            self.units.append(unit)

    @property
    def unique_units(self):
        # units may be repeated in the consist, sometimes we need an ordered list of unique units
        # set() doesn't preserve list order, which matters, so do it the hard way
        unique_units = []
        for unit in self.units:
            if unit not in unique_units:
                unique_units.append(unit)
        return unique_units


    def get_and_verify_numeric_id(self, offset):
        numeric_id = self.base_numeric_id + offset
        # guard against the ID being too large to build in an articulated consist
        if numeric_id > 16383:
            utils.echo_message("Error: numeric_id " + str(numeric_id) + " for " + self.id + " can't be used (16383 is max ID for articulated vehicles)")
        # non-blocking guard on duplicate IDs
        for id in numeric_id_defender:
            if id == numeric_id:
                utils.echo_message("Error: consist " + self.id + " unit id collides (" + str(numeric_id) + ") with units in another consist")
        numeric_id_defender.append(numeric_id)
        return numeric_id

    def get_reduced_set_of_variant_dates(self):
        # find all the unique dates that will need a switch constructing
        years = set()
        for variant in self.model_variants:
            years.update((variant.intro_date, variant.end_date))
        years = sorted(years)
        # quick integrity check
        if years[0] != 0:
            utils.echo_message(self.id + " doesn't have at least one model variant with intro date 0 (required for nml switches to work)")
        return years

    def get_num_spritesets(self):
        return len(set([i.spritesheet_suffix for i in self.model_variants]))

    def get_variants_available_for_specific_year(self, year):
        # put the data in a format that's easy to render as switches
        result = []
        for variant in self.model_variants:
            if variant.intro_date <= year < variant.end_date:
                result.append(variant.spritesheet_suffix)
        return result # could call set() here, but I didn't bother, shouldn't be needed if model variants set up correctly

    def get_nml_random_switch_fragments_for_model_variants(self, vehicle):
        # return fragments of nml for use in switches
        result = []
        years = self.get_reduced_set_of_variant_dates()
        for index, year in enumerate(years):
            if index < len(years) - 1:
                from_date = year
                until_date = years[index + 1] - 1
                result.append(str(from_date) + '..' + str(until_date) + ':' + vehicle.id + '_switch_graphics_random_' + str(from_date))
        return result

    def get_name_substr(self):
        # relies on name being in format "Foo [Bar]" for Name [Type Suffix]
        return self.title.split('[')[0]

    def get_str_name_suffix(self):
        # used in vehicle name string only, relies on name property value being in format "Foo [Bar]" for Name [Type Suffix]
        type_suffix = self.title.split('[')[1].split(']')[0]
        type_suffix = type_suffix.upper()
        type_suffix = '_'.join(type_suffix.split(' '))
        return 'STR_NAME_SUFFIX_' + type_suffix

    def get_name(self):
        return "string(STR_NAME_" + self.id +", string(" + self.get_str_name_suffix() + "))"

    def get_spriterows_for_consist_or_subpart(self, units):
        # pass either list of all units in consist, or a slice of the consist starting from front (arbitrary slices not useful)
        # spriterow count is number of output sprite rows from graphics processor, to be used by nml sprite templating
        # returns counts of rows from the template and keys to what they are
        result = []
        for unit in units:
            unit_rows = []
            if unit.always_use_same_spriterow:
                unit_rows.append(('always_use_same_spriterow', 1))
            elif 'livery_only' in self.cargo_graphics_options.keys():
                # some vehicles have livery variation only, no cargo sprites (nor empty sprite)
                # provide the count of _all_ the liveries here, no calculating later
                unit_rows.append(('livery_only', self.num_cargo_sprite_variants))
            else:
                if self.has_empty_state_spriterow:
                    unit_rows.append(('empty', 1))
                # provide the number of output rows per cargo group, total row count for the group is calculated later as needed
                if 'bulk_cargo' in self.cargo_graphics_options.keys():
                    unit_rows.append(('bulk_cargo', 2))
                if 'piece_cargo' in self.cargo_graphics_options.keys():
                    unit_rows.append(('piece_cargo', 2))
                # custom is to allow for manually drawn cargos
                if 'custom_cargo' in self.cargo_graphics_options.keys():
                    unit_rows.append(('custom_cargo', 2))
            result.append(list(unit_rows))
        return result

    @property
    def graphics_processors(self):
        # wrapper to get the graphics processors
        template = self.id + '_template.png'
        return graphics_utils.get_composited_cargo_processors(template = template)

    def get_engine_cost_points(self):
        # Up to 40 points for power. 1 point per 50hp
        # Power is therefore capped at 2000hp by design, this isn't a hard limit, but raise a warning
        if self.power > 2000:
            utils.echo_message("Consist " + self.id + " has power > 2000hp, which is too much")
        power_cost_points = self.power / 50

        # Up to 30 points for speed above up to 90mph. 1 point per 3mph
        if self.speed > 90:
            utils.echo_message("Consist " + self.id + " has speed > 90, which is too much")
        speed_cost_points = min(self.speed, 90) / 3

        # Up to 20 points for intro date after 1870. 1 point per 8 years.
        # Intro dates capped at 2030, this isn't a hard limit, but raise a warning
        if self.intro_date > 2030:
            utils.echo_message("Consist " + self.id + " has intro_date > 2030, which is too much")
        date_cost_points = max((self.intro_date - 1870), 0) / 8

        return power_cost_points + speed_cost_points + date_cost_points

    @property
    def buy_cost(self):
        # type_base_buy_cost_points is an arbitrary adjustment that can be applied on a type-by-type basis,
        return self.get_engine_cost_points() + self.type_base_buy_cost_points

    @property
    def running_cost(self):
        consist_capacity_points = min(self.total_capacities[1], 160)
        # type_base_running_cost_points is an arbitrary adjustment that can be applied on a type-by-type basis,
        return self.get_engine_cost_points() + consist_capacity_points + self.type_base_running_cost_points

    @property
    def weight(self):
        consist_weight = sum([getattr(unit, 'weight', 0) for unit in self.units])
        if consist_weight > 63:
            utils.echo_message("Error: consist weight is " + str(consist_weight) + "t for " + self.id + "; must be < 63t")
        return consist_weight

    @property
    def tractive_effort_coefficient(self):
        # vehicles cannot set their own TE coefficients, shouldn't be needed
        # vehicle classes can do it by over-riding this property in their class
        # TE is dibbled up substantially higher than the default 0.3 because RV performance sucks otherwise
        # dubious use of @property here, eh?
        return 0.7

    @property
    def total_capacities(self):
        # total capacity of consist, summed from vehicles (with variants for capacity multipler param)
        # convenience function used only when the total consist capacity is needed rather than per-unit
        result = []
        for i in range(3):
            consist_capacity = 0
            for unit in self.units:
                if self.default_cargo == 'MAIL':
                    consist_capacity += int(global_constants.mail_multiplier * unit.capacities[i])
                else:
                    consist_capacity += unit.capacities[i]
            result.append(consist_capacity)
        return result

    @property
    def refittable_classes(self):
        cargo_classes = []
        # maps lists of allowed classes.  No equivalent for disallowed classes, that's overly restrictive and damages the viability of class-based refitting
        for i in self.class_refit_groups:
            [cargo_classes.append(cargo_class) for cargo_class in global_constants.base_refits_by_class[i]]
        return ','.join(set(cargo_classes)) # use set() here to dedupe

    def get_label_refits_allowed(self):
        # allowed labels, for fine-grained control in addition to classes
        return ','.join(self.label_refits_allowed)

    def get_label_refits_disallowed(self):
        # disallowed labels, for fine-grained control, knocking out cargos that are allowed by classes, but don't fit for gameplay reasons
        return ','.join(self.label_refits_disallowed)

    @property
    def speed(self):
        if self._speed is None:
            if self.roadveh_flag_tram is True:
                speeds = self.get_roster(self.roster_id).default_tram_speeds
            else:
                speeds = self.get_roster(self.roster_id).default_truck_speeds
            speed = speeds[max([year for year in speeds if self.intro_date >= year])]
            return speed
        else:
            return self._speed

    @property
    def power(self):
        # only trucks have standard power bands, trams are custom
        if self._power is None:
            if self.roadveh_flag_tram is True:
                power_bands = self.get_roster(self.roster_id).default_tram_power_bands
            else:
                power_bands = self.get_roster(self.roster_id).default_truck_power_bands
            power = power_bands[max([year for year in power_bands if self.intro_date >= year])]
            return power
        else:
            return self._power

    @property
    def adjusted_model_life(self):
        return 'VEHICLE_NEVER_EXPIRES'

    @property
    def buy_menu_width (self):
        # max sensible width in buy menu is 64px, but RH templates currently drawn at 36px - legacy stuff
        consist_length = 4 * sum([unit.vehicle_length for unit in self.units])
        if consist_length < 36:
            return consist_length + 1 # +1 is pure jank to handle clipped Greenscoe sprite, cba to fix it properly
        else:
            return 36

    def get_roster(self, roster_id):
        for roster in registered_rosters:
            if roster_id == roster.id:
                return roster

    def get_expression_for_roster(self):
        # the working definition is one and only one roster per vehicle
        roster = self.get_roster(self.roster_id)
        return 'param[1]==' + str(roster.numeric_id - 1)

    def render_articulated_switch(self):
        template = templates["add_articulated_parts.pynml"]
        nml_result = template(consist=self, global_constants=global_constants)
        return nml_result

    def render(self):
        # templating
        nml_result = ''
        nml_result = nml_result + self.render_articulated_switch()
        for unit in set(self.units):
            nml_result = nml_result + unit.render()
        return nml_result


class RoadVehicle(object):
    """Base class for all types of road vehicles"""
    def __init__(self, **kwargs):
        self.consist = kwargs.get('consist')

        # setup properties for this road vehicle
        self.numeric_id = kwargs.get('numeric_id', None)
        self.vehicle_length = kwargs.get('vehicle_length', None)
        self.weight = kwargs.get('weight', None)
        self.semi_truck_shift_offset_jank = kwargs.get('semi_truck_shift_offset_jank', None)
        # capacities variable by parameter
        self.capacities = self.get_capacity_variations(kwargs.get('capacity', 0))
        # optional - some consists have sequences like A1-B-A2, where A1 and A2 look the same but have different IDs for implementation reasons
        # avoid duplicating sprites on the spritesheet by forcing A2 to use A1's spriterow_num, fiddly eh?
        # ugly, but eh.  Zero-indexed, based on position in units[]
        # watch out for repeated vehicles in the consist when calculating the value for this)
        # !! I don't really like this solution, might be better to have the graphics processor duplicate this?, with a simple map of [source:duplicate_to]
        self.unit_num_providing_spriterow_num = kwargs.get('unit_num_providing_spriterow_num', None)
        # optional - force always using same spriterow
        # for cases where the template handles cargo, but some units in the consist might not show cargo, e.g. tractor units etc
        # can also be used to suppress compile failures during testing when spritesheet is unfinished (missing rows etc)
        self.always_use_same_spriterow = kwargs.get('always_use_same_spriterow', False)
        self._effect_spawn_model = kwargs.get('effect_spawn_model', None)
        self.effects = kwargs.get('effects', []) # default for effects is an empty list

    def get_capacity_variations(self, capacity):
        # capacity is variable, controlled by a newgrf parameter
        # we cache the available variations on the vehicle instead of working them out every time - easier
        # allow that integer maths is needed for newgrf cb results; round up for safety
        return [int(math.ceil(capacity * multiplier)) for multiplier in global_constants.capacity_multipliers]

    def get_loading_speed(self, cargo_type, capacity_param):
        # ottd vehicles load at different rates depending on type,
        # normalise default loading time for this set to 240 ticks, regardless of capacity
        transport_type_rate = 12 # openttd loading rates vary by transport type, look them up in wiki to find value to use here to normalise loading time to 240 ticks
        capacity = self.capacities[capacity_param]
        if cargo_type == 'mail':
            capacity = int(global_constants.mail_multiplier * capacity)
        result = int(self.consist.loading_speed_multiplier * math.ceil(capacity / transport_type_rate))
        return max(result, 1)

    @property
    def availability(self):
        # only show vehicle in buy menu if it is first vehicle in consist
        if self.is_lead_unit_of_consist:
            return "ALL_CLIMATES"
        else:
            return "NO_CLIMATE"

    @property
    def effect_spawn_model(self):
        if self._effect_spawn_model:
            return self._effect_spawn_model
        else:
            if self.consist.roadveh_flag_tram == True:
                # trams electric by default, over-ride in vehicle as needed
                return 'EFFECT_SPAWN_MODEL_ELECTRIC'
            else:
                # other vehicles diesel by default, over-ride in vehicle as needed
                return 'EFFECT_SPAWN_MODEL_DIESEL'

    @property
    def is_lead_unit_of_consist(self):
        # could be refactored - 'if self.consist.units.index(self.id) == 0:'
        if self.numeric_id == self.consist.base_numeric_id:
            return True
        else:
            return False

    @property
    def special_flags(self):
        special_flags = ['ROADVEH_FLAG_2CC']
        if self.consist.autorefit == True:
            special_flags.append('ROADVEH_FLAG_AUTOREFIT')
        if self.consist.roadveh_flag_tram == True:
            special_flags.append('ROADVEH_FLAG_TRAM')
        return ','.join(special_flags)

    @property
    def offsets(self):
        if self.semi_truck_shift_offset_jank:
            result = []
            for i in range (0, 8):
                base_offsets = global_constants.default_road_vehicle_offsets[str(self.vehicle_length)][i]
                offset_deltas = [self.semi_truck_shift_offset_jank * offset for offset in global_constants.semi_truck_offset_jank[i]]
                result.append([base_offsets[0] + offset_deltas[0], base_offsets[1] + offset_deltas[1]])
            return result
        else:
            return global_constants.default_road_vehicle_offsets[str(self.vehicle_length)]

    @property
    def spriterow_num(self):
        # ugly forcing of over-ride for out-of-sequence repeating vehicles
        if self.unit_num_providing_spriterow_num is not None:
            return self.unit_num_providing_spriterow_num

        preceding_spriterows = self.consist.get_spriterows_for_consist_or_subpart(self.consist.units[0:self.consist.units.index(self)])
        result = []
        for unit_rows in preceding_spriterows:
            for spriterow_type, spriterow_count in unit_rows:
                if spriterow_type == 'empty' or spriterow_type == 'always_use_same_spriterow':
                    result.append(spriterow_count)
                elif spriterow_type == 'livery_only':
                    # 'livery_only' provides the count of all liveries, no further calculation
                    result.append(spriterow_count)
                else:
                    result.append(spriterow_count * self.consist.num_cargo_sprite_variants)
        return sum(result)

    @property
    def vehicle_nml_template(self):
        if self.consist.vehicle_nml_template is not None:
            if self.always_use_same_spriterow:
                return 'vehicle_default.pynml'
            else:
                return self.consist.vehicle_nml_template
        else:
            return 'vehicle_default.pynml'

    @property
    def sg_depot(self):
        suffix = "_switch_graphics_by_year"
        return self.id + suffix

    @property
    def sg_default(self):
        suffix = "_switch_graphics_by_year"
        return self.id + suffix

    def get_cargo_suffix(self):
        return 'string(' + self.cargo_units_refit_menu + ')'

    def assert_cargo_labels(self, cargo_labels):
        for i in cargo_labels:
            if i not in global_constants.cargo_labels:
                utils.echo_message("Warning: vehicle " + self.id + " references cargo label " + i + " which is not defined in the cargo table")

    def get_expression_for_effects(self):
        # provides part of nml switch for effects (smoke), or none if no effects defined
        if len(self.effects) > 0:
            result = []
            for index, effect in enumerate(self.effects):
                 result.append('STORE_TEMP(create_effect(' + effect + '), 0x10' + str(index) + ')')
            return '[' + ','.join(result) + ']'
        else:
            return 0

    def get_nml_expression_for_cargo_variant_random_switch(self, variation_num, cargo_id=None):
        switch_id = self.id + "_switch_graphics_" + str(variation_num) + ('_' + str(cargo_id) if cargo_id is not None else '')
        return "SELF," + switch_id + ", bitmask(TRIGGER_VEHICLE_NEW_LOAD)"

    def render_properties(self):
        template = templates["road_vehicle_properties.pynml"]
        return template(vehicle=self, consist=self.consist, global_constants=global_constants)

    def render_cargo_capacity(self):
        template = templates["capacity_switches.pynml"]
        return template(vehicle=self, global_constants=global_constants)

    def render(self):
        # integrity tests
        self.assert_cargo_labels(self.consist.label_refits_allowed)
        self.assert_cargo_labels(self.consist.label_refits_disallowed)
        # templating
        template_name = self.vehicle_nml_template
        template = templates[template_name]
        nml_result = template(vehicle=self, consist=self.consist, global_constants=global_constants)
        return nml_result


class ModelVariant(object):
    # simple class to hold model variants
    # variants are mostly randomised or date-sensitive graphics
    # must be a minimum of one variant per vehicle
    # at least one variant must have intro date 0 (for nml switch defaults to work)
    def __init__(self, intro_date, end_date, spritesheet_suffix, graphics_processor):
        self.intro_date = intro_date
        self.end_date = end_date
        self.spritesheet_suffix = spritesheet_suffix # use digits for these - to match spritesheet filenames
        self.graphics_processor = graphics_processor

    def get_spritesheet_name(self, consist):
        return consist.id + '_' + str(self.spritesheet_suffix) + '.png'


class CourierCar(Consist):
    """
    Truck or tram for mail, valuables etc.
    """
    def __init__(self, **kwargs):
        super(CourierCar, self).__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['mail', 'express_freight']
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = ['TOUR']
        self.default_cargo = 'MAIL'


class PaxHauler(Consist):
    """
    Bus or tram for pax.
    """
    def __init__(self, **kwargs):
        super(PaxHauler, self).__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['pax']
        self.label_refits_allowed = []
        self.label_refits_disallowed = []
        self.default_cargo = 'PASS'
        self.loading_speed_multiplier = 3


class PaxExpressHauler(Consist):
    """
    Coach or express tram for pax.
    """
    def __init__(self, **kwargs):
        super(PaxExpressHauler, self).__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['pax']
        self.label_refits_allowed = []
        self.label_refits_disallowed = []
        self.default_cargo = 'PASS'
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD


class OpenHauler(Consist):
    """
    General cargo tram or truck - refits everything except mail, pax.
    """
    def __init__(self, **kwargs):
        super(OpenHauler, self).__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['all_freight']
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = ['TOUR', 'MAIL']
        self.default_cargo = 'GOOD'


class BoxHauler(Consist):
    """
    Box tram or truck - refits express, piece goods cargos, other selected cargos.
    """
    def __init__(self, **kwargs):
        super(BoxHauler, self).__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['packaged_freight']
        self.label_refits_allowed = ['MAIL', 'GRAI', 'WHEA', 'MAIZ', 'FRUT', 'BEAN', 'NITR'] # Iron Horse compatibility
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['non_freight_special_cases']
        self.default_cargo = 'GOOD'


class DumpHauler(Consist):
    """
    Tram or truck for limited set of bulk (mineral) cargos.
    """
    def __init__(self, **kwargs):
        super(DumpHauler, self).__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['dump_freight']
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['non_dump_bulk']
        self.default_cargo = 'COAL'
        self.loading_speed_multiplier = 2
        self.vehicle_nml_template = 'vehicle_with_visible_cargo.pynml'
        # cargo rows 0 indexed - 0 = first set of loaded sprites
        # GRVL is in first position as it is re-used for generic unknown cargos
        # mining trucks *do* transport SCMT in this set, realism is not relevant here, went back and forth on this a few times :P
        self.cargo_graphics_mappings = {'GRVL': [0], 'IORE': [1], 'CORE': [2], 'AORE': [3],
                   'SAND': [4], 'COAL': [5], 'CLAY': [6], 'SCMT': [7], 'PHOS': [8]}
        self.num_cargo_sprite_variants = 9
        self.generic_cargo_rows = [0]
        self.cargo_graphics_options = {'bulk_cargo': True}


class FlatBedHauler(Consist):
    """
    Flatbed tram or truck - refits most cargos, not bulk.
    """
    def __init__(self, **kwargs):
        super(FlatBedHauler, self).__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['flatbed_freight']
        self.label_refits_allowed = ['GOOD']
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['non_flatbed_freight']
        self.default_cargo = 'STEL'
        self.vehicle_nml_template = 'vehicle_with_visible_cargo.pynml'
        self.cargo_graphics_mappings = {'WOOD': [0], 'WDPR': [1]}
        self.num_cargo_sprite_variants = 2
        self.generic_cargo_rows = [0]

        self.cargo_graphics_options = {'piece_cargo': True}
        """
        self.vehicle_nml_template = 'vehicle_with_visible_cargo.pynml'
        # cargo rows 0 indexed - 0 = first set of loaded sprites
        self.cargo_graphics_mappings = {'GOOD': [0]}
        self.num_cargo_sprite_variants = 1
        self.generic_cargo_rows = [0]
        self.cargo_graphics_options = {'piece': True}
        """

class BulkPowderHauler(Consist):
    """
    Covered hopper truck or trailer for bulk powder cargos.
    """
    def __init__(self, **kwargs):
        super(BulkPowderHauler, self).__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['covered_hopper_freight']
        self.label_refits_allowed = ['GRAI', 'WHEA', 'MAIZ', 'FOOD', 'SUGR', 'FMSP', 'RFPR', 'CLAY', 'BDMT', 'BEAN', 'NITR', 'RUBR', 'SAND']
        self.label_refits_disallowed = []
        self.default_cargo = 'GRAI'
        self.loading_speed_multiplier = 2


class LivestockHauler(Consist):
    """
    Livestock truck or trailer.
    """
    def __init__(self, **kwargs):
        super(LivestockHauler, self).__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ['LVST']
        self.label_refits_disallowed = []
        self.default_cargo = 'LVST'
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD


class RefrigeratedHauler(Consist):
    """
    Refrigerated truck or trailer.
    Refits to limited range of refrigerated cargos, with 'improved' cargo decay rate.
    """
    def __init__(self, **kwargs):
        super(RefrigeratedHauler, self).__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['refrigerated_freight']
        self.label_refits_allowed = [] # no specific labels needed, refits all cargos that have refrigerated class
        self.label_refits_disallowed = []
        self.default_cargo = 'FOOD'
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD


class Tanker(Consist):
    """
    Ronseal ("does what it says on the tin", for those without extensive knowledge of UK advertising).
    """
    def __init__(self, **kwargs):
        super(Tanker, self).__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['liquids']
        # tankers are unrealistically autorefittable, and at no cost
        # Pikka: if people complain that it's unrealistic, tell them "don't do it then"
        # they also change livery at stations if refitted between certain cargo types <shrug>
        self.cargo_graphics_mappings = {'OIL_': [0], 'PETR': [1], 'RFPR': [2]}
        self.num_cargo_sprite_variants = len(self.cargo_graphics_mappings)
        self.num_spriterows_per_cargo_variant = 1 # no loading/loaded state for tankers, just cargo-specific liveries
        self.has_empty_state_spriterow = False
        self.generic_cargo_rows = [0]
        self.label_refits_allowed = []
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['edible_liquids']
        self.default_cargo = 'OIL_'
        self.loading_speed_multiplier = 2
        self.vehicle_nml_template = 'vehicle_with_cargo_specific_liveries.pynml'
        # !! as of July 2016, this wasn't provided for graphics_processor, but only as a hack supporting get_spriterows_for_consist_or_subpart
        # it overlaps imho with has_empty_state_spriterow, num_cargo_sprite_variants and num_spriterows_per_cargo_variant
        self.cargo_graphics_options = {'livery_only': True}


class EdiblesTanker(Consist):
    """
    Wine, milk, water etc.
    """
    def __init__(self, **kwargs):
        super(EdiblesTanker, self).__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['liquids']
        self.label_refits_allowed = ['MILK', 'FOOD']
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['non_edible_liquids']
        self.default_cargo = 'WATR'
        self.loading_speed_multiplier = 2
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD


class LogHauler(Consist):
    """
    Gets wood.
    """
    def __init__(self, **kwargs):
        super(LogHauler, self).__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ['WOOD']
        self.label_refits_disallowed = []
        self.default_cargo = 'WOOD'
        self.loading_speed_multiplier = 2
        self.num_cargo_sprite_variants = 1
        self.cargo_graphics_mappings = {'WOOD': [0]}
        self.generic_cargo_rows = [0]
        self.vehicle_nml_template = 'vehicle_with_visible_cargo.pynml'
        self.cargo_graphics_options = {'custom_cargo': True}


class FoundryHauler(Consist):
    """
    Specialist heavy haul tram / truck, e.g. multiwheel platform, steel mill hauler etc.
    High capacity, not very fast, refits to small subset of finished metal cargos.
    """
    def __init__(self, **kwargs):
        super(FoundryHauler, self).__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ['STEL', 'COPR']
        self.label_refits_disallowed = []
        self.default_cargo = 'STEL'
        self.loading_speed_multiplier = 2


class SuppliesHauler(Consist):
    """
    Specialist tram / truck with flatbed + crane, supplies and building materials.
    """
    def __init__(self, **kwargs):
        super(SuppliesHauler, self).__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ['ENSP', 'FMSP', 'VEHI', 'BDMT']
        self.label_refits_disallowed = []
        self.default_cargo = 'ENSP'
        self.loading_speed_multiplier = 2


class IntermodalHauler(Consist):
    """
    Specialist intermodal (container) truck, limited range of cargos.
    """
    def __init__(self, **kwargs):
        super(IntermodalHauler, self).__init__(**kwargs)
        self.autorefit = True
        # maintain other sets (e.g. IH etc) when changing container refits
        self.class_refit_groups = ['express_freight','packaged_freight']
        self.label_refits_allowed = ['FRUT','WATR']
        self.label_refits_disallowed = ['FISH','LVST','OIL_','TOUR','WOOD']
        self.default_cargo = 'GOOD'
        self.loading_speed_multiplier = 2


