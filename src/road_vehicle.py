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


class Consist(object):
    """
       'Vehicles' (appearing in buy menu) are composed as articulated consists.
       Each consist comprises one or more 'units' (visible).
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)

        # setup properties for this consist (props either shared for all vehicles, or placed on lead vehicle of consist)
        self.title = kwargs.get('title', None)
        self.base_numeric_id = kwargs.get('base_numeric_id', None)
        self.str_type_info = kwargs.get('str_type_info', 'COASTER')
        self.intro_date = kwargs.get('intro_date', None)
        self.replacement_id = kwargs.get('replacement_id', None)
        self.vehicle_life = kwargs.get('vehicle_life', None)
        self.power = kwargs.get('power', 0)
        self.tractive_effort_coefficient = kwargs.get('tractive_effort_coefficient', 0.3) # 0.3 is recommended default value
        self.speed = kwargs.get('speed', None)
        self.buy_cost = kwargs.get('buy_cost', None)
        self.fixed_run_cost_factor = kwargs.get('fixed_run_cost_factor', None)
        self.fuel_run_cost_factor = kwargs.get('fuel_run_cost_factor', None)
        # create a structure to hold model variants
        self.model_variants = []
        # create structure to hold the slices
        self.slices = []
        # some project management stuff
        self.graphics_status = kwargs.get('graphics_status', None)
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
            if year in range(variant.intro_date, variant.end_date):
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

    def get_str_type_info(self):
        # makes a string id for nml
        return 'STR_' + self.str_type_info

    def get_str_autorefit(self):
        if self.any_slice_offers_autorefit():
            return 'STR_BUY_MENU_OFFERS_AUTOREFIT'
        else:
            return 'STR_EMPTY'

    def get_name(self):
        return "string(STR_NAME_" + self.id +", string(" + self.get_str_name_suffix() + "))"

    def get_buy_menu_string(self):
        # will need to handle bi-mode locos here, have a look at consist.slice_requires_variable_power(vehicle)
        buy_menu_template = Template(
            "string(STR_BUY_MENU_TEXT, string(${str_type_info}), string(${str_autorefit}), string(STR_EMPTY))"
        )
        return buy_menu_template.substitute(str_type_info=self.get_str_type_info(), str_autorefit=self.get_str_autorefit())

    def any_slice_offers_autorefit(self):
        offers_autorefit = False
        for slice in self.slices:
            if getattr(slice, 'autorefit', False):
                offers_autorefit = True
        return offers_autorefit

    @property
    def running_cost(self):
        # calculate a running cost
        fixed_run_cost = self.fixed_run_cost_factor * global_constants.FIXED_RUN_COST
        fuel_run_cost =  self.fuel_run_cost_factor * global_constants.FUEL_RUN_COST
        calculated_run_cost = int((fixed_run_cost + fuel_run_cost) / 98) # divide by magic constant to get costs as factor in 0-255 range
        return min(calculated_run_cost, 255) # cost factor is a byte, can't exceed 255

    @property
    def weight(self):
        consist_weight = sum([getattr(slice, 'weight', 0) for slice in self.slices])
        if consist_weight > 63:
            utils.echo_message("Error: consist weight is " + str(consist_weight) + "t for " + self.id + "; must be < 63t")
        return consist_weight

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
        self.speed = kwargs.get('speed', 0)
        self.weight = kwargs.get('weight', None)
        # declare capacities for pax, mail and freight, as they are needed later for nml switches
        self.capacities_pax = self.get_capacity_variations(kwargs.get('capacity_pax', 0))
        self.capacities_mail = self.get_capacity_variations(kwargs.get('capacity_mail', 0))
        self.capacities_freight = self.get_capacity_variations(kwargs.get('capacity_freight', 0))
        # spriterow_num, first row = 0
        self.spriterow_num = kwargs.get('spriterow_num', 0)
        # set defaults for props otherwise set by subclass as needed (not set by kwargs as specific models do not over-ride them)
        self.default_cargo = 'PASS' # over-ride in subclass as needed (PASS is sane default)
        self.class_refit_groups = []
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = []
        self.autorefit = False
        self.visual_effect = 'VISUAL_EFFECT_DISABLE' # nml constant
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
        return ','.join(special_flags)

    @property
    def capacity_pax(self):
        return self.capacities_pax[0]
    @property

    def capacity_mail(self):
        return self.capacities_mail[0]

    @property
    def capacity_freight(self):
        return self.capacities_freight[0]

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

    def render_debug_info(self):
        template = templates["debug_info_vehicle.pynml"]
        return template(vehicle=self)

    def render_properties(self):
        template = templates["road_vehicle_properties.pynml"]
        return template(vehicle=self, consist=self.consist, global_constants=global_constants)

    def render_cargo_capacity(self):
        template = templates["capacity_switches.pynml"]
        return template(vehicle=self)

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


class FarmTram(RoadVehicle):
    """
    Tram for farm cargos
    """
    def __init__(self, **kwargs):
        super(FarmTram, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ['LVST']
        self.label_refits_disallowed = []
        self.default_cargo = 'LVST'
        self.default_cargo_capacities = self.capacities_freight
        self.visual_effect = 'VISUAL_EFFECT_DIESEL' # nml constant


class GeneralCargoHauler(RoadVehicle):
    """
    General cargo truck - refits most things.
    """
    def __init__(self, **kwargs):
        super(GeneralCargoHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['express_freight']
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = []
        self.default_cargo = 'PASS'
        self.default_cargo_capacities = self.capacities_freight
        self.visual_effect = 'VISUAL_EFFECT_DIESEL' # nml constant

class ExpressHauler(RoadVehicle):
    """
    Express truck for mail, valuables etc.
    """
    def __init__(self, **kwargs):
        super(ExpressHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['express_freight']
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = []
        self.default_cargo = 'PASS'
        self.default_cargo_capacities = self.capacities_freight
        self.visual_effect = 'VISUAL_EFFECT_DIESEL' # nml constant


class MiningHauler(RoadVehicle):
    """
    Off-highway mining truck or trailer.  Limited set of bulk (mineral) cargos.
    """
    def __init__(self, **kwargs):
        super(MiningHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['express_freight']
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = []
        self.default_cargo = 'PASS'
        self.default_cargo_capacities = self.capacities_freight
        self.visual_effect = 'VISUAL_EFFECT_DIESEL' # nml constant


class BulkHauler(RoadVehicle):
    """
    On-highway dump truck or trailer.  All non-sheltered bulk cargos.
    """
    def __init__(self, **kwargs):
        super(BulkHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['express_freight']
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = []
        self.default_cargo = 'PASS'
        self.default_cargo_capacities = self.capacities_freight
        self.visual_effect = 'VISUAL_EFFECT_DIESEL' # nml constant


class BulkPowderHauler(RoadVehicle):
    """
    Covered hopper truck or trailer for bulk powder cargos.
    """
    def __init__(self, **kwargs):
        super(BulkPowderHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['express_freight']
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = []
        self.default_cargo = 'PASS'
        self.default_cargo_capacities = self.capacities_freight
        self.visual_effect = 'VISUAL_EFFECT_DIESEL' # nml constant

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
        self.default_cargo_capacities = self.capacities_freight
        self.visual_effect = 'VISUAL_EFFECT_DIESEL' # nml constant


class RefrigeratedHauler(RoadVehicle):
    """
    Refrigerated truck or trailer.
    Refits to limited range of refrigerated cargos, with 'improved' cargo decay rate.
    """
    def __init__(self, **kwargs):
        super(RefrigeratedHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ['LVST']
        self.label_refits_disallowed = []
        self.default_cargo = 'LVST'
        self.default_cargo_capacities = self.capacities_freight
        self.visual_effect = 'VISUAL_EFFECT_DIESEL' # nml constant


class Tanker(RoadVehicle):
    """
    Ronseal ("does what it says on the tin", for those without extensive knowledge of UK advertising).
    """
    def __init__(self, **kwargs):
        super(Tanker, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = ['liquids']
        self.label_refits_allowed = ['MILK']
        self.label_refits_disallowed = []
        self.default_cargo = 'OIL_'
        self.default_cargo_capacities = self.capacities_freight
        self.visual_effect = 'VISUAL_EFFECT_DIESEL' # nml constant


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
        self.default_cargo_capacities = self.capacities_freight
        self.visual_effect = 'VISUAL_EFFECT_DIESEL' # nml constant


class HeavyHauler(RoadVehicle):
    """
    Specialist heavy haul truck, e.g. multiwheel platform, steel mill hauler etc.
    High capacity, not very fast, refits to subset of industrial cargos.
    """
    def __init__(self, **kwargs):
        super(HeavyHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ['LVST']
        self.label_refits_disallowed = []
        self.default_cargo = 'LVST'
        self.default_cargo_capacities = self.capacities_freight
        self.visual_effect = 'VISUAL_EFFECT_DIESEL' # nml constant


class IntermodalHauler(RoadVehicle):
    """
    Specialist intermodal (container) truck, limited range of cargos.
    """
    def __init__(self, **kwargs):
        super(IntermodalHauler, self).__init__(**kwargs)
        self.template = 'road_vehicle.pynml'
        self.autorefit = True
        self.class_refit_groups = []
        self.label_refits_allowed = ['LVST']
        self.label_refits_disallowed = []
        self.default_cargo = 'LVST'
        self.default_cargo_capacities = self.capacities_freight
        self.visual_effect = 'VISUAL_EFFECT_DIESEL' # nml constant

