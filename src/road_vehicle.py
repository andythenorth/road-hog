import global_constants # expose all constants for easy passing to templates
import utils

import os.path
currentdir = os.curdir

import sys
sys.path.append(os.path.join('src')) # add to the module search path

import math

from chameleon import PageTemplateLoader # chameleon used in most template cases
# setup the places we look for templates
templates = PageTemplateLoader(os.path.join(currentdir, 'src', 'templates'))

import graphics_processor

from vehicles import numeric_id_defender

from rosters import registered_rosters

import inspect

class Consist(object):
    """
       'Vehicles' (appearing in buy menu) are composed as articulated consists.
       Each consist comprises one or more 'units' (visible).
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
        self.power = kwargs.get('power', 0)
        self.tractive_effort_coefficient = kwargs.get('tractive_effort_coefficient', 0.3) # 0.3 is recommended default value
        self._speed = kwargs.get('speed', None)
        self.speed_dibble = kwargs.get('speed_dibble', None)
        # arbitrary adjustments of points that can be applied to adjust buy cost and running cost, over-ride in consist as needed
        # values can be -ve or +ve to dibble specific vehicles (but total calculated points cannot exceed 255)
        self.type_base_buy_cost_points = kwargs.get('type_base_buy_cost_points', 0)
        self.type_base_running_cost_points = kwargs.get('type_base_running_cost_points', 0)
        # create a structure to hold model variants
        self.model_variants = []
        # create structure to hold the slices
        self.slices = []
        # roster is set when the vehicle is registered to a roster, only one roster per vehicle
        self.roster_id = None

    def add_model_variant(self, intro_date, end_date, spritesheet_suffix, graphics_processor=None):
        self.model_variants.append(ModelVariant(intro_date, end_date, spritesheet_suffix, graphics_processor))

    def add_unit(self, vehicle, repeat=1):
        # this is a little overly complex, as it is lifted from Iron Horse, which has more complex vehicles
        count = len(set(self.slices))
        slice = vehicle
        if count == 0:
            slice.id = self.id # first vehicle gets no numeric id suffix - for compatibility with buy menu list ids etc
        else:
            slice.id = self.id + '_' + str(count)
        slice.numeric_id = self.get_and_verify_numeric_id(count)
        slice.slice_length = vehicle.vehicle_length
        slice.spriterow_num = vehicle.spriterow_num

        for repeat_num in range(repeat):
            self.slices.append(slice)

    def get_and_verify_numeric_id(self, offset):
        numeric_id = self.base_numeric_id + offset
        # guard against the ID being too large to build in an articulated consist
        if numeric_id > 16383:
            utils.echo_message("Error: numeric_id " + str(numeric_id) + " for " + self.id + " can't be used (16383 is max ID for articulated vehicles)")
        # non-blocking guard on duplicate IDs
        for id in numeric_id_defender:
            if id == numeric_id:
                utils.echo_message("Error: consist " + self.id + " slice id collides (" + str(numeric_id) + ") with slices in another consist")
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

    def any_slice_offers_autorefit(self):
        offers_autorefit = False
        for slice in self.slices:
            if getattr(slice, 'autorefit', False):
                offers_autorefit = True
        return offers_autorefit

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
        consist_weight = sum([getattr(slice, 'weight', 0) for slice in self.slices])
        if consist_weight > 63:
            utils.echo_message("Error: consist weight is " + str(consist_weight) + "t for " + self.id + "; must be < 63t")
        return consist_weight

    @property
    def total_capacities(self):
        # total capacity of consist, summed from vehicles (with variants for capacity multipler param)
        # convenience function used only when the total consist capacity is needed rather than per-slice
        result = []
        for i in range(3):
            consist_capacity = 0
            for slice in self.slices:
                if slice.default_cargo == 'MAIL':
                    consist_capacity += int(global_constants.mail_multiplier * slice.capacities[i])
                else:
                    consist_capacity += slice.capacities[i]
            result.append(consist_capacity)
        return result

    @property
    def speed(self):
        if self._speed is None:
            if self.roadveh_flag_tram is True:
                speeds = self.get_roster(self.roster_id).default_tram_speeds
            else:
                speeds = self.get_roster(self.roster_id).default_truck_speeds
            speed = speeds[max([year for year in speeds if self.intro_date >= year])]
            if self.speed_dibble == 'plodding':
                speed = speed - 10
            if self.speed_dibble == 'speedy':
                speed = speed + 10
            return speed
        else:
            return self._speed

    @property
    def adjusted_model_life(self):
        return 'VEHICLE_NEVER_EXPIRES'

    @property
    def buy_menu_width (self):
        # max sensible width in buy menu is 64px, but RH templates currently drawn at 36px - legacy stuff
        consist_length = 4 * sum([slice.slice_length for slice in self.slices])
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
        for slice in set(self.slices):
            nml_result = nml_result + slice.render()
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
        self.loading_speed_multiplier = kwargs.get('loading_speed_multiplier', 1)
        self.cargo_age_period = kwargs.get('cargo_age_period', global_constants.CARGO_AGE_PERIOD)
        # spriterow_num, first row = 0
        self.spriterow_num = kwargs.get('spriterow_num', 0)
        # set defaults for props otherwise set by subclass as needed (not set by kwargs as specific models do not over-ride them)
        self.default_cargo = 'PASS' # over-ride in subclass as needed (PASS is sane default)
        self.class_refit_groups = []
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = []
        self.autorefit = False
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
        result = int(self.loading_speed_multiplier * math.ceil(capacity / transport_type_rate))
        return max(result, 1)

    @property
    def availability(self):
        # only show vehicle in buy menu if it is first vehicle in consist
        if self.is_lead_slice_of_consist:
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
    def is_lead_slice_of_consist(self):
        if self.numeric_id == self.consist.base_numeric_id:
            return True
        else:
            return False

    @property
    def special_flags(self):
        special_flags = ['ROADVEH_FLAG_2CC']
        if self.autorefit == True:
            special_flags.append('ROADVEH_FLAG_AUTOREFIT')
        if self.consist.roadveh_flag_tram == True:
            special_flags.append('ROADVEH_FLAG_TRAM')
        return ','.join(special_flags)

    @property
    def refittable_classes(self):
        cargo_classes = []
        # maps lists of allowed classes.  No equivalent for disallowed classes, that's overly restrictive and damages the viability of class-based refitting
        for i in self.class_refit_groups:
            [cargo_classes.append(cargo_class) for cargo_class in global_constants.base_refits_by_class[i]]
        return ','.join(set(cargo_classes)) # use set() here to dedupe

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
    def sg_depot(self):
        suffix = "_switch_graphics_by_year"
        return self.id + suffix

    @property
    def sg_default(self):
        suffix = "_switch_graphics_by_year"
        return self.id + suffix

    def get_label_refits_allowed(self):
        # allowed labels, for fine-grained control in addition to classes
        return ','.join(self.label_refits_allowed)

    def get_label_refits_disallowed(self):
        # disallowed labels, for fine-grained control, knocking out cargos that are allowed by classes, but don't fit for gameplay reasons
        return ','.join(self.label_refits_disallowed)

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

    def render_properties(self):
        template = templates["road_vehicle_properties.pynml"]
        return template(vehicle=self, consist=self.consist, global_constants=global_constants)

    def render_cargo_capacity(self):
        template = templates["capacity_switches.pynml"]
        return template(vehicle=self, global_constants=global_constants)

    def render(self):
        # integrity tests
        self.assert_cargo_labels(self.label_refits_allowed)
        self.assert_cargo_labels(self.label_refits_disallowed)
        # templating
        template_name = self.template
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


class GraphicsProcessorFactory(object):
    # simple class which wraps graphics_processor, which uses pixa library
    # pipeline_name refers to a pipeline class which defines how the processing is done
    # may be reused across consists, so don't store consist info in the pipeline, pass it to pipeline at render time
    # this is kind of factory-pattern-ish, but don't make too much of that, it's not important
    def __init__(self, pipeline_name, options):
        self.pipeline_name = pipeline_name
        self.options = options
        self.pipeline = graphics_processor.registered_pipelines[pipeline_name]


class EngineConsist(Consist):
    """
    Intermediate class for engine consists to subclass from, provides some common properties.
    This class should be sparse - only declare the most limited set of properties common to engine consists.
    """
    def __init__(self, **kwargs):
        super(EngineConsist, self).__init__(**kwargs)


class CourierCar(RoadVehicle):
    """
    Truck or tram for mail, valuables etc.
    """
    def __init__(self, **kwargs):
        super(CourierCar, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['mail', 'express_freight']
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = ['TOUR']
        self.default_cargo = 'MAIL'
        self.default_cargo_capacities = self.capacities


class PaxHauler(RoadVehicle):
    """
    Bus or tram for pax.
    """
    def __init__(self, **kwargs):
        super(PaxHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['pax']
        self.label_refits_allowed = []
        self.label_refits_disallowed = []
        self.default_cargo = 'PASS'
        self.default_cargo_capacities = self.capacities
        self.loading_speed_multiplier = 3


class PaxExpressHauler(RoadVehicle):
    """
    Coach or express tram for pax.
    """
    def __init__(self, **kwargs):
        super(PaxExpressHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['pax']
        self.label_refits_allowed = []
        self.label_refits_disallowed = []
        self.default_cargo = 'PASS'
        self.default_cargo_capacities = self.capacities
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD


class GeneralCargoHauler(RoadVehicle):
    """
    General cargo truck - refits everything except mail, pax.
    """
    def __init__(self, **kwargs):
        super(GeneralCargoHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['all_freight']
        self.label_refits_allowed = ['GRAI', 'WHEA', 'MAIZ'] # Iron Horse compatibility
        self.label_refits_disallowed = ['TOUR', 'MAIL']
        self.default_cargo = 'GOOD'
        self.default_cargo_capacities = self.capacities


class DumpHauler(RoadVehicle):
    """
    Tram, truck or trailer for any bulk cargos.  The refits on this are quite permissive by design.
    """
    def __init__(self, **kwargs):
        super(DumpHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['dump_freight']
        self.label_refits_allowed = ['FMSP']
        self.label_refits_disallowed = []
        self.default_cargo = 'COAL'
        self.default_cargo_capacities = self.capacities
        self.loading_speed_multiplier = 2


class GeneralCargoHauler(RoadVehicle):
    """
    General cargo truck - refits everything except mail, pax.
    """
    def __init__(self, **kwargs):
        super(GeneralCargoHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['all_freight']
        self.label_refits_allowed = ['GRAI', 'WHEA', 'MAIZ'] # Iron Horse compatibility
        self.label_refits_disallowed = ['TOUR', 'MAIL']
        self.default_cargo = 'GOOD'
        self.default_cargo_capacities = self.capacities


class MiningHauler(RoadVehicle):
    """
    Off-highway mining truck or trailer.  Limited set of bulk (mineral) cargos.
    """
    def __init__(self, **kwargs):
        super(MiningHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['dump_freight']
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['non_mining_bulk']
        self.default_cargo = 'COAL'
        self.default_cargo_capacities = self.capacities
        self.loading_speed_multiplier = 2


class FlatBedHauler(RoadVehicle):
    """
    Flatbed tram or truck - refits most cargos, not bulk.
    """
    def __init__(self, **kwargs):
        super(GeneralCargoHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['all_freight']
        self.label_refits_allowed = ['GRAI', 'WHEA', 'MAIZ'] # Iron Horse compatibility
        self.label_refits_disallowed = ['TOUR', 'MAIL']
        self.default_cargo = 'GOOD'
        self.default_cargo_capacities = self.capacities


class BulkPowderHauler(RoadVehicle):
    """
    Covered hopper truck or trailer for bulk powder cargos.
    """
    def __init__(self, **kwargs):
        super(BulkPowderHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['covered_hopper_freight']
        self.label_refits_allowed = ['GRAI', 'WHEA', 'MAIZ', 'FOOD', 'SUGR', 'FMSP', 'RFPR', 'CLAY', 'BDMT', 'BEAN', 'NITR']
        self.label_refits_disallowed = []
        self.default_cargo = 'GRAI'
        self.default_cargo_capacities = self.capacities
        self.loading_speed_multiplier = 2


class LivestockHauler(RoadVehicle):
    """
    Livestock truck or trailer.
    """
    def __init__(self, **kwargs):
        super(LivestockHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ['LVST']
        self.label_refits_disallowed = []
        self.default_cargo = 'LVST'
        self.default_cargo_capacities = self.capacities
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD


class RefrigeratedHauler(RoadVehicle):
    """
    Refrigerated truck or trailer.
    Refits to limited range of refrigerated cargos, with 'improved' cargo decay rate.
    """
    def __init__(self, **kwargs):
        super(RefrigeratedHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['refrigerated_freight']
        self.label_refits_allowed = [] # no specific labels needed, refits all cargos that have refrigerated class
        self.label_refits_disallowed = []
        self.default_cargo = 'FOOD'
        self.default_cargo_capacities = self.capacities
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD


class Tanker(RoadVehicle):
    """
    Ronseal ("does what it says on the tin", for those without extensive knowledge of UK advertising).
    """
    def __init__(self, **kwargs):
        super(Tanker, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['liquids']
        self.label_refits_allowed = []
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['edible_liquids']
        self.default_cargo = 'OIL_'
        self.default_cargo_capacities = self.capacities
        self.loading_speed_multiplier = 2


class EdiblesTanker(RoadVehicle):
    """
    Wine, milk, water etc.
    """
    def __init__(self, **kwargs):
        super(EdiblesTanker, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['liquids']
        self.label_refits_allowed = ['MILK', 'FOOD']
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['non_edible_liquids']
        self.default_cargo = 'WATR'
        self.default_cargo_capacities = self.capacities
        self.loading_speed_multiplier = 2
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD


class LogHauler(RoadVehicle):
    """
    Gets wood.
    """
    def __init__(self, **kwargs):
        super(LogHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ['WOOD']
        self.label_refits_disallowed = []
        self.default_cargo = 'WOOD'
        self.default_cargo_capacities = self.capacities
        self.loading_speed_multiplier = 2


class FoundryHauler(RoadVehicle):
    """
    Specialist heavy haul tram / truck, e.g. multiwheel platform, steel mill hauler etc.
    High capacity, not very fast, refits to small subset of finished metal cargos.
    """
    def __init__(self, **kwargs):
        super(FoundryHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ['STEL', 'COPR']
        self.label_refits_disallowed = []
        self.default_cargo = 'STEL'
        self.default_cargo_capacities = self.capacities
        self.loading_speed_multiplier = 2


class SuppliesHauler(RoadVehicle):
    """
    Specialist tram / truck with flatbed + crane, supplies and building materials.
    """
    def __init__(self, **kwargs):
        super(SuppliesHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ['ENSP', 'FMSP', 'BDMT']
        self.label_refits_disallowed = []
        self.default_cargo = 'ENSP'
        self.default_cargo_capacities = self.capacities
        self.loading_speed_multiplier = 2


class IntermodalHauler(RoadVehicle):
    """
    Specialist intermodal (container) truck, limited range of cargos.
    """
    def __init__(self, **kwargs):
        super(IntermodalHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        # maintain other sets (e.g. IH etc) when changing container refits
        self.class_refit_groups = ['express_freight','packaged_freight']
        self.label_refits_allowed = ['FRUT','WATR']
        self.label_refits_disallowed = ['FISH','LVST','OIL_','TOUR','WOOD']
        self.default_cargo = 'GOOD'
        self.default_cargo_capacities = self.capacities
        self.loading_speed_multiplier = 2


