import global_constants # expose all constants for easy passing to templates
import utils

import os.path
currentdir = os.curdir

import sys
sys.path.append(os.path.join('src')) # add to the module search path

import codecs

import math
from string import Template # python builtin templater might be used in some utility cases

from chameleon import PageTemplateLoader # chameleon used in most template cases
# setup the places we look for templates
templates = PageTemplateLoader(os.path.join(currentdir, 'src', 'templates'))

import graphics_processor

from vehicles import registered_consists, registered_wagon_generations

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
        # arbitrary adjustments of points that can be applied to adjust buy cost and running cost, over-ride in consist as needed
        # values can be -ve or +ve to dibble specific vehicles (but total calculated points cannot exceed 255)
        self.type_base_buy_cost_points = kwargs.get('type_base_buy_cost_points', 0)
        self.type_base_running_cost_points = kwargs.get('type_base_running_cost_points', 0)
        # create a structure to hold model variants
        self.model_variants = []
        # create structure to hold the slices
        self.slices = []
        # register consist with this module so other modules can use it, with a non-blocking guard on duplicate IDs
        for consist in registered_consists:
            if consist.base_numeric_id == self.base_numeric_id:
                utils.echo_message("Error: consist " + self.id + " shares duplicate id (" + str(self.base_numeric_id) + ") with consist " + consist.id)
        registered_consists.append(self)

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
        # guard against ID collisions with other vehicles
        for consist in registered_consists:
            for slice in consist.slices:
                if numeric_id == slice.numeric_id:
                    utils.echo_message("Error: numeric_id collision (" + str(numeric_id) + ") for slices in consist " + self.id + " and " + consist.id)
        return numeric_id

    def get_reduced_set_of_variant_dates(self):
        # find all the unique dates that will need a switch constructing
        years = sorted(reduce(set.union, [(variant.intro_date, variant.end_date) for variant in self.model_variants], set()))
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
            if year >= variant.intro_date and year < variant.end_date:
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
                speeds = self.roster.default_tram_speeds
            else:
                speeds = self.roster.default_truck_speeds
            return speeds[max([year for year in speeds if self.intro_date >= year])]
        else:
            return self._speed

    @property
    def adjusted_model_life(self):
        # handles keeping the buy menu tidy, relies on magic from Eddi
        if self.replacement_id != None and self.replacement_id != '-none' and self.replacement_id != '':
            for i in registered_consists:
                if i.id == self.replacement_id:
                    model_life = i.intro_date - self.intro_date
                    return model_life + self.vehicle_life
        else:
            return 'VEHICLE_NEVER_EXPIRES'

    @property
    def buy_menu_width (self):
        # max sensible width in buy menu is 64px, but RH templates currently drawn at 36px - legacy stuff
        consist_length = 4 * sum([slice.slice_length for slice in self.slices])
        if consist_length < 36:
            return consist_length
        else:
            return 36

    @property
    def roster(self):
        # vehicles can be in one roster by design; to repeat a vehicle in another roster, copy it
        # this makes it simple for rosters to handle things like common speeds and capacity at compile time
        result = []
        for roster in registered_rosters:
            if self.id in roster.buy_menu_sort_order:
                result.append(roster)
        if len(result) > 1:
            utils.echo_message("Warning: vehicle " + self.id + " appears in more than one roster " + str(result))
        return result[0]

    def render_debug_info(self):
        template = templates["debug_info_consist.pynml"]
        return template(consist=self)

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
        self.loading_speed = kwargs.get('loading_speed', 5) # 5 is default vehicle loading speed
        self.vehicle_length = kwargs.get('vehicle_length', None)
        self.weight = kwargs.get('weight', None)
        self.visual_effect = kwargs.get('visual_effect', 'VISUAL_EFFECT_DISABLE') # nml constant
        # capacities variable by parameter
        self.capacities = self.get_capacity_variations(kwargs.get('capacity', 0))
        # spriterow_num, first row = 0
        self.spriterow_num = kwargs.get('spriterow_num', 0)
        # set defaults for props otherwise set by subclass as needed (not set by kwargs as specific models do not over-ride them)
        self.default_cargo = 'PASS' # over-ride in subclass as needed (PASS is sane default)
        self.class_refit_groups = []
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = []
        self.autorefit = False
        self.visual_effect_offset = 0

    def get_capacity_variations(self, capacity):
        # capacity is variable, controlled by a newgrf parameter
        # we cache the available variations on the vehicle instead of working them out every time - easier
        # allow that integer maths is needed for newgrf cb results; round up for safety
        return [int(math.ceil(capacity * multiplier)) for multiplier in global_constants.capacity_multipliers]

    @property
    def availability(self):
        # only show vehicle in buy menu if it is first vehicle in consist
        if self.is_lead_slice_of_consist:
            return "ALL_CLIMATES"
        else:
            return "NO_CLIMATE"

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
        # offsets can also be over-ridden on a per-model basis by providing this property in the model class
        return global_constants.default_road_vehicle_offsets[str(self.vehicle_length)]

    @property
    def sg_depot(self):
        # legacy - copied from IH, allows special handling of depot sprites
        suffix = "_switch_graphics_by_year"
        return self.id + suffix

    @property
    def sg_default(self):
        # legacy - copied from IH, related to special handling of depot sprites
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

    def get_expression_for_roster(self):
        return 'param_roster=='+str(registered_rosters.index(self.consist.roster))

    def render_debug_info(self):
        template = templates["debug_info_vehicle.pynml"]
        return template(vehicle=self)

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
        id = kwargs.get('id', None)
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
        self.label_refits_disallowed = []
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
        self.label_refits_disallowed = []
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
        self.class_refit_groups = ['hopper_freight']
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['non_hopper_bulk_freight']
        self.default_cargo = 'COAL'
        self.default_cargo_capacities = self.capacities


class BulkFarmHauler(RoadVehicle):
    """
    Tram, truck or trailer for bulk farm cargos (pourable uncountable crops).
    """
    def __init__(self, **kwargs):
        super(BulkFarmHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['bulk_farm_freight']
        self.label_refits_allowed = ['FICR', 'GRAI', 'WHEA', 'MAIZ', 'SGBT', 'SGCN', 'SUGR', 'FRUT', 'FMSP']
        self.label_refits_disallowed = []
        self.default_cargo = 'GRAI'
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
        self.label_refits_allowed = ['GRAI', 'WHEA', 'MAIZ', 'FOOD', 'SUGR', 'FMSP', 'RFPR', 'CLAY', 'BDMT']
        self.label_refits_disallowed = []
        self.default_cargo = 'GRAI'
        self.default_cargo_capacities = self.capacities


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


class EdiblesTanker(RoadVehicle):
    """
    Wine, milk, water etc.
    """
    def __init__(self, **kwargs):
        super(EdiblesTanker, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['liquids']
        self.label_refits_allowed = ['MILK']
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['non_edible_liquids']
        self.default_cargo = 'WATR'
        self.default_cargo_capacities = self.capacities


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


class FoundryHauler(RoadVehicle):
    """
    Specialist heavy haul truck, e.g. multiwheel platform, steel mill hauler etc.
    High capacity, not very fast, refits to small subset of industrial cargos.
    """
    def __init__(self, **kwargs):
        super(FoundryHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ['STEL', 'SCMT', 'ENSP', 'MNSP']
        self.label_refits_disallowed = []
        self.default_cargo = 'STEL'
        self.default_cargo_capacities = self.capacities


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


