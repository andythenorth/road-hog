import os.path
currentdir = os.curdir

import sys
sys.path.append(os.path.join('src')) # add to the module search path

import math
import inspect # only used for deprecated attempt at partial compiles, remove (and vehicle_module_path var)

from chameleon import PageTemplateLoader # chameleon used in most template cases
# setup the places we look for templates
templates = PageTemplateLoader(os.path.join(currentdir, 'src', 'templates'))

import polar_fox
import global_constants # expose all constants for easy passing to templates
import utils

from gestalt_graphics.gestalt_graphics import GestaltGraphics, GestaltGraphicsVisibleCargo, GestaltGraphicsLiveryOnly, GestaltGraphicsCustom
import gestalt_graphics.graphics_constants as graphics_constants

from rosters import registered_rosters
from vehicles import numeric_id_defender

class Consist(object):
    """
       'Vehicles' (appearing in buy menu) are composed as articulated consists.
       Each consist comprises one or more vehicle 'units'.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.vehicle_module_path = inspect.stack()[2][1]
        # setup properties for this consist (props either shared for all vehicles, or placed on lead vehicle of consist)
        self._name = kwargs.get('name', None) # private as 'name' is an @property method to add type substring
        self.base_numeric_id = kwargs.get('base_numeric_id', None)
        self.road_type = kwargs.get('road_type', None)
        self.tram_type = kwargs.get('tram_type', None)
        if self.road_type is not None and self.tram_type is not None:
            utils.echo_message("Error: " + self.id + ". Vehicles must not have both road_type and tram_type properties set.  Set one of these only")
        # either gen xor intro_date is required, don't set both, one will be interpolated from the other
        self._intro_date = kwargs.get('intro_date', None)
        self._gen = kwargs.get('gen', None)
        print('_gen', self._gen, '_intro_date', self._intro_date)
        # if gen is used, the calculated intro date can be adjusted with +ve or -ve offset
        self.intro_date_offset = kwargs.get('intro_date_offset', None)
        self.vehicle_life = kwargs.get('vehicle_life', None)
        self._power = kwargs.get('power', None)
        # sound effects are faff, they can be set by consist subclass (Bus vs. Coach), or will fall back to a default sound for the vehicle subclass (by power type)
        self._sound_effect = None
        self.default_sound_effect = None # set by unit subclasses
        # suffix for 'Diesel', 'Steam' etc in name string, set by unit subclasses, but stored in consist as it's a consist property
        self._power_type_suffix = None
        # option for multiple default cargos, cascading if first cargo(s) are not available
        self.default_cargos = []
        # semi-trucks need some redistribution of capacity to get correct TE (don't use this of other magic, bad idea)
        self.semi_truck_so_redistribute_capacity = kwargs.get('semi_truck_so_redistribute_capacity', False)
        self._speed = kwargs.get('speed', None)
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
        # multiplier of capacity, used to set consist weight, over-ride in vehicle sub-class as needed
        # set this to the value for road vehicles...trams will be automatically adjusted
        self.weight_multiplier = 0.4
        # create structure to hold the units
        self.units = []
        # create a structure for cargo /livery graphics options
        self.gestalt_graphics = GestaltGraphics()
        # roster is set when the vehicle is registered to a roster, only one roster per vehicle
        self.roster_id = None

    def add_unit(self, repeat=1, **kwargs):
        # how many unique units? (units can be repeated, we are using count for numerid ID, so we want uniques)
        count = len(set(self.units))

        if kwargs.get('type', None) is not None:
            unit = kwargs['type'](consist=self, **kwargs)
        else:
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

    @property
    def name_type_suffix(self):
        # some consist subclasses will over-ride this for special case handling
        result = 'STR_NAME_SUFFIX_' + self._name_type_suffix
        if self.roadveh_flag_tram:
            return result + "_TRAM"
        else:
            return result + "_TRUCK"

    @property
    def power_type_suffix(self):
        if self._power_type_suffix is None:
            utils.echo_message('Consist ' + self.id + ' has no _power_type_suffix set by any of its units')
        else:
            return 'STR_NAME_SUFFIX_' + self._power_type_suffix

    @property
    def name(self):
        return "string(STR_NAME_CONSIST, string(STR_NAME_" + self.id + "), string(" + self.name_type_suffix + "), string(" + self.power_type_suffix +"))"

    def get_spriterows_for_consist_or_subpart(self, units):
        # pass either list of all units in consist, or a slice of the consist starting from front (arbitrary slices not useful)
        # spriterow count is number of output sprite rows from graphics processor, to be used by nml sprite templating
        result = []
        for unit in units:
            unit_rows = []
            if unit.always_use_same_spriterow:
                unit_rows.append(('always_use_same_spriterow', 1))
            else:
                # assumes visible_cargo is used to handle any other rows, no other cases at time of writing, could be changed eh?
                unit_rows.extend(self.gestalt_graphics.get_output_row_counts_by_type())
            result.append(unit_rows)
        return result

    def get_engine_cost_points(self):
        # Up to 20 points for power. 1 point per 100hp
        # Power is therefore capped at 2000hp by design, this isn't a hard limit, but raise a warning
        if self.power > 2000:
            utils.echo_message("Consist " + self.id + " has power > 2000hp, which is too much")
        power_cost_points = self.power / 100

        # Up to 30 points for speed above up to 90mph. 1 point per 3mph
        if self.speed > 90:
            utils.echo_message("Consist " + self.id + " has speed > 90, which is too much")
        speed_cost_points = min(self.speed, 90) / 3

        # Up to 20 points for intro date after 1870. 1 point per 8 years.
        # Intro dates capped at 2030, this isn't a hard limit, but raise a warning
        if self.intro_date > 2030:
            utils.echo_message("Consist " + self.id + " has intro_date > 2030, which is too much")
        date_cost_points = max((self.intro_date - 1870), 0) / 8

        # Up to 20 points for capacity. 1 point per 8t.
        # Capacity capped at 160, this isn't a hard limit, but raise a warning
        if self.total_capacities[1] > 160:
            utils.echo_message("Consist " + self.id + " has capacity > 160, which is too much")
        consist_capacity_points = min(self.total_capacities[1], 160)

        return power_cost_points + speed_cost_points + date_cost_points + consist_capacity_points

    @property
    def buy_cost(self):
        # type_base_buy_cost_points is an arbitrary adjustment that can be applied on a type-by-type basis,
        # there is an arbitrary multiplier applied to get sensible costs in range with Iron Horse
        return 0.5 * self.get_engine_cost_points() + self.type_base_buy_cost_points

    @property
    def running_cost(self):
        # type_base_running_cost_points is an arbitrary adjustment that can be applied on a type-by-type basis,
        return self.get_engine_cost_points()  + self.type_base_running_cost_points

    @property
    def intro_date(self):
        # automatic intro_date, but can over-ride by passing in kwargs for consist
        if self._intro_date:
            print('intro date assert tickled by ', self.id, self.base_track_type)
            #assert(self._gen == None), "%s consist has both gen and intro_date set, which is incorrect" % self.id
            assert(self.intro_date_offset == None), "%s consist has both intro_date and intro_date_offset set, which is incorrect" % self.id
            return self._intro_date
        else:
            assert(self._gen != None), "%s consist has neither gen nor intro_date set, which is incorrect" % self.id
            result = self.roster.intro_dates[self.base_track_type][self.gen - 1]
            if self.intro_date_offset is not None:
                result = result + self.intro_date_offset
            return result

    @property
    def gen(self):
        # gen is usually set in the vehicle, but can be left unset if intro_date is set
        if self._gen:
            assert(self._intro_date == None), "%s consist has both gen and intro_date set, which is incorrect" % self.id
            return self._gen
        else:
            assert(self._intro_date != None), "%s consist has neither gen nor intro_date set, which is incorrect" % self.id
            for gen_counter, intro_date in enumerate(self.roster.intro_dates[self.base_track_type]):
                if self.intro_date < intro_date:
                    return gen_counter
            # if no result is found in list, it's last gen
            return len(self.roster.intro_dates[self.base_track_type])

    @property
    def weight(self):
        mult = self.weight_multiplier
        # trams are 10% heavier per capacity
        if self.roadveh_flag_tram:
            mult = mult + 0.1
        consist_weight = mult * self.total_capacities[1]
        if consist_weight > 63:
            utils.echo_message("Error: consist weight is " + str(consist_weight) + "t for " + self.id + "; must be < 63t")
        return min(consist_weight, 63)

    @property
    def tractive_effort_coefficient(self):
        # vehicles cannot set their own TE coefficients, shouldn't be needed
        # vehicle classes can do it by over-riding this property in their class
        if self.roadveh_flag_tram:
            # for trams, reduced TE compared to rubber-tyred vehicles
            return 0.3
        else:
            # for RVs TE is dibbled up substantially higher than the default 0.3 because RV performance sucks otherwise
            return 0.7

    @property
    def total_capacities(self):
        # total capacity of consist, summed from vehicles (with variants for capacity multipler param)
        # convenience function used only when the total consist capacity is needed rather than per-unit
        result = []
        for i in range(3):
            consist_capacity = 0
            for unit in self.units:
                # possibly fragile assumption that mail vehicles will always have to put mail first in default cargo list
                if self.default_cargos[0] == 'MAIL':
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
                speeds = self.roster.default_tram_speeds
            else:
                speeds = self.roster.default_truck_speeds
            speed = speeds[max([year for year in speeds if self.intro_date >= year])]
            return speed
        else:
            return self._speed

    @property
    def power(self):
        # only trucks have standard power bands, trams are custom
        if self._power is None:
            if self.roadveh_flag_tram is True:
                power_bands = self.roster.default_tram_power_bands
            else:
                power_bands = self.roster.default_truck_power_bands
            power = power_bands[max([year for year in power_bands if self.intro_date >= year])]
            return power
        else:
            return self._power

    @property
    def model_life(self):
        similar_consists = []
        for consist in self.roster.consists:
            if type(consist) == type(self):
                # the order of if statements here is specific and to split tram / road vehicles reliably
                if self.roadveh_flag_tram:
                    if consist.roadveh_flag_tram:
                        # all trams are currently considered compatible, unless/until new tram_types are added
                        similar_consists.append(consist)
                else:
                    if not consist.roadveh_flag_tram:
                        if consist.road_type == self.road_type:
                            # all road_types are currently considered to require exact match, unless/until new road_types are added
                            similar_consists.append(consist)
        replacement_consist = None
        for consist in sorted(similar_consists, key=lambda consist: consist.intro_date):
            if consist.intro_date > self.intro_date:
                replacement_consist = consist
                break
        if replacement_consist is None:
            return 'VEHICLE_NEVER_EXPIRES'
        else:
            # see comments for retire_early
            # model life based on replacement date + 17 for max random intro date of replacement
            return replacement_consist.intro_date - self.intro_date + 17

    @property
    def retire_early(self):
        # affects when vehicle is removed from buy menu (in combination with model life)
        # to understand why this is needed see https://newgrf-specs.tt-wiki.net/wiki/NML:Vehicles#Engine_life_cycle
        # Pikka: that will keep it disappearing from the list at the same time, but extend the period of maximum reliability by n years, ie until the last ones built when they were the current gen are getting old
        # retirement trigger is end of phase 2 - n; n needs to be: length of phase 1 (rnd, up to 3 years) + phase 2 offset (-8)
        # then add 1 for safety with randomisation (ensure overlap is guaranteed with replacement)
        return 3 - 8 - 1 # -ve value here is correct

    @property
    def sound_effect(self):
        # allow custom sound effects (set per subclass or vehicle)
        if self._sound_effect is not None:
            return self._sound_effect
        else:
            return self.default_sound_effect

    @property
    def buy_menu_width (self):
        # max sensible width in buy menu is 64px, but RH templates currently drawn at 36px - legacy stuff
        consist_length = 4 * sum([unit.vehicle_length for unit in self.units])
        if consist_length < global_constants.buy_menu_sprite_width:
            return consist_length
        else:
            return global_constants.buy_menu_sprite_width

    @property
    def roster(self):
        for roster in registered_rosters:
            if roster.id == self.roster_id:
                return roster

    def get_expression_for_roster(self):
        # the working definition is one and only one roster per vehicle
        roster = self.roster
        return 'param[1]==' + str(roster.numeric_id - 1)

    def get_nml_expression_for_default_cargos(self):
        # sometimes first default cargo is not available, so we use a list
        # this avoids unwanted cases like box cars defaulting to mail when goods cargo not available
        # if there is only one default cargo, the list just has one entry, that's no problem
        if len(self.default_cargos) == 1:
            return self.default_cargos[0]
        else:
            # build stacked ternary operators for cargos
            result = self.default_cargos[-1]
            for cargo in reversed(self.default_cargos[0:-1]):
                result = 'cargotype_available("' + cargo + '")?' + cargo + ':' + result
            return result

    def render_articulated_switch(self):
        if len(self.units) > 1:
            template = templates["articulated_parts.pynml"]
            nml_result = template(consist=self, global_constants=global_constants)
            return nml_result
        else:
            return ''

    def render(self):
        # templating
        nml_result = ''
        nml_result = nml_result + self.render_articulated_switch()
        for unit in set(self.units):
            nml_result = nml_result + unit.render()
        return nml_result


class BusCoachMixin(object):
    """
        Stupid mixin for buses / coaches.
        Keep this simple, don't use an __init__, it gets tricky with super.
        Just use class attrs.
    """
    base_track_type = "ROAD"
    roadveh_flag_tram = False
    # over-ride the default sound effect set by RoadVehicle subclass
    # this assumes diesel, and will fail if none-diesel local buses are added
    _sound_effect = 'SOUND_BUS_START_PULL_AWAY_WITH_HORN' # coaches still might over-ride this, eh


class CakeMixin(object):
    # !! the name is deliberately stupid to JFDI things, needs refactored !!
    """
        Stupid mixin for multi-roadtype (HEQS and ROAD).
        Keep this simple, don't use an __init__, it gets tricky with super.
        Just use class attrs.
    """
    base_track_type = "CAKE" # !! fix the label later, JFDI
    roadveh_flag_tram = False


class FeldbahnMixin(object):
    """
        Stupid mixin for feldbahn (industrial trains with tiny gauge, 600mm and similar)
        Keep this simple, don't use an __init__, it gets tricky with super.
        Just use class attrs.
    """
    base_track_type = "HAKE" # !! fix the label later, JFDI
    roadveh_flag_tram = True # feldbahn uses tram newgrf spec


class HEQSMixin(object):
    """
        Stupid mixin for heavy equipment (non-rail).
        Keep this simple, don't use an __init__, it gets tricky with super.
        Just use class attrs.
    """
    base_track_type = "HEQS"
    roadveh_flag_tram = False


class TramMixin(object):
    """
        Stupid mixin for trams.
        Keep this simple, don't use an __init__, it gets tricky with super.
        Just use class attrs.
    """
    base_track_type = "RAIL"
    roadveh_flag_tram = True # tram uses tram newgrf spec


class TruckMixin(object):
    """
        Stupid mixin for trucks.
        Keep this simple, don't use an __init__, it gets tricky with super.
        Just use class attrs.
    """
    base_track_type = "ROAD"
    roadveh_flag_tram = False


class RoadVehicle(object):
    """Base class for all types of road vehicles"""
    def __init__(self, **kwargs):
        self.consist = kwargs.get('consist')

        # setup properties for this road vehicle
        self.numeric_id = kwargs.get('numeric_id', None)
        self.vehicle_length = kwargs.get('vehicle_length', None)
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
        # only set if the graphics processor requires it to generate cargo sprites
        # defines the size of cargo sprite to use
        # if the vehicle cargo area is not an OTTD unit length, use the next size up and the masking will sort it out
        # some longer vehicles may place multiple shorter cargo sprites, e.g. 7/8 vehicle, 2 * 4/8 cargo sprites (with some overlapping)
        self.cargo_length = kwargs.get('cargo_length', None)
        # effects can be specified in detail per vehicle, or fall back to those defined by RoadVehicle subclass
        self._effect_spawn_model = kwargs.get('effect_spawn_model', None)
        self.effects = kwargs.get('effects', []) # default for effects is an empty list
        self.default_effect_sprite = None # default is no effect sprite

    def get_capacity_variations(self, capacity):
        # capacity is variable, controlled by a newgrf parameter
        # we cache the available variations on the vehicle instead of working them out every time - easier
        # allow that integer maths is needed for newgrf cb results; round up for safety
        return [int(math.ceil(capacity * multiplier)) for multiplier in global_constants.capacity_multipliers]

    def get_loading_speed(self, cargo_type, capacity_param):
        # ottd vehicles load at different rates depending on type,
        # normalise default loading time for this set to 240 ticks, regardless of capacity
        # openttd loading rates vary by transport type, look them up in wiki to find value to use here to normalise loading time to 240 ticks
        transport_type_rate = 12 # this is (240 / loading frequency in ticks for transport type) from wiki
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
            result.append(sum([unit_row[1] for unit_row in unit_rows]))
        return sum(result)

    @property
    def vehicle_nml_template(self):
        if not self.always_use_same_spriterow:
            if self.consist.gestalt_graphics.nml_template:
                return self.consist.gestalt_graphics.nml_template
        # default case
        return 'vehicle_default.pynml'

    def get_cargo_suffix(self):
        return 'string(' + self.cargo_units_refit_menu + ')'

    def assert_cargo_labels(self, cargo_labels):
        for i in cargo_labels:
            if i not in global_constants.cargo_labels:
                utils.echo_message("Warning: vehicle " + self.id + " references cargo label " + i + " which is not defined in the cargo table")

    def get_effects(self):
        # provides part of nml switch for effects (smoke), or none if no effects defined in vehicle or RoadVehicle subclass
        result = []
        if len(self.effects) > 0:
            for index, effect in enumerate(self.effects):
                 result.append('STORE_TEMP(create_effect(' + effect + '), 0x10' + str(index) + ')')
        elif self.default_effect_sprite is not None:
            result.append('STORE_TEMP(create_effect(' + self.default_effect_sprite + ', -2, 0, 10), 0x100)')
        # only return a list if there's a list to return :P
        if len(result) > 0:
            return ['[' + ','.join(result) + ']', len(result)]
        else:
            return [0, 0]

    def get_nml_expression_for_cargo_variant_random_switch(self, cargo_id=None):
        switch_id = self.id + "_switch_graphics" + ('_' + str(cargo_id) if cargo_id is not None else '')
        return "SELF," + switch_id + ", bitmask(TRIGGER_VEHICLE_ANY_LOAD)"

    def render(self):
        # integrity tests
        self.assert_cargo_labels(self.consist.label_refits_allowed)
        self.assert_cargo_labels(self.consist.label_refits_disallowed)
        # templating
        template_name = self.vehicle_nml_template
        template = templates[template_name]
        nml_result = template(vehicle=self, consist=self.consist, global_constants=global_constants)
        return nml_result


class SteamRoadVehicle(RoadVehicle):
    """
    Unit for a steam vehicle, with over-rideable smoke
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._effect_spawn_model = 'EFFECT_SPAWN_MODEL_STEAM'
        self.default_effect_sprite = 'EFFECT_SPRITE_STEAM'
        self.consist._power_type_suffix = 'STEAM'
        self.consist.default_sound_effect = 'SOUND_FACTORY_WHISTLE'


class DieselRoadVehicle(RoadVehicle):
    """
    Unit for a diesel vehicle, with over-rideable smoke
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._effect_spawn_model = 'EFFECT_SPAWN_MODEL_DIESEL'
        self.default_effect_sprite = 'EFFECT_SPRITE_DIESEL'
        self.consist._power_type_suffix = 'DIESEL'
        # this can be over-ridden in consist subclasses for e.g. buses using consist._sound_effect
        self.consist.default_sound_effect = 'SOUND_BUS_START_PULL_AWAY' # sound effect mis-named, original base set uses this for trucks


class ElectricRoadVehicle(RoadVehicle):
    """
    Unit for an electric vehicle, with over-rideable sparks
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._effect_spawn_model = 'EFFECT_SPAWN_MODEL_ELECTRIC'
        self.default_effect_sprite = 'EFFECT_SPRITE_ELECTRIC'
        self.consist._power_type_suffix = 'ELECTRIC'
        self.consist.default_sound_effect = 'SOUND_ELECTRIC_SPARK'


class BoxHaulerBase(Consist):
    """
    Base consist for box haulers. Refits express, piece goods cargos, other selected cargos.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name_type_suffix = "BOX"
        self.autorefit = True
        self.class_refit_groups = ['packaged_freight']
        self.label_refits_allowed = ['MAIL', 'GRAI', 'WHEA', 'MAIZ', 'FRUT', 'BEAN', 'NITR'] # Iron Horse compatibility
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['non_freight_special_cases']
        self.default_cargos = global_constants.default_cargos['box']
        self.weight_multiplier = 0.45


class BoxTram(BoxHaulerBase, TramMixin):
    """
    Box tram.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class BoxTruck(BoxHaulerBase, TruckMixin):
    """
    Box truck.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CoveredHopperHaulerBase(Consist):
    """
    Consist base for covered hopper hauler.  Refits bulk powder cargos.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name_type_suffix = "COVERED_HOPPER"
        self.autorefit = True
        self.class_refit_groups = ['covered_hopper_freight']
        self.label_refits_allowed = global_constants.allowed_refits_by_label['covered_hoppers']
        self.label_refits_disallowed = []
        self.default_cargos = global_constants.default_cargos['covered_hopper']
        self.loading_speed_multiplier = 2
        self.weight_multiplier = 0.45


class CoveredHopperTram(CoveredHopperHaulerBase, TramMixin):
    """
    Covered hopper tram.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class CoveredHopperTruck(CoveredHopperHaulerBase, TruckMixin):
    """
    Covered hopper truck.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DumpHaulerBase(Consist):
    """
    Base consist for dump hauler. Limited set of bulk (mineral) cargos.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name_type_suffix = "DUMP"
        self.autorefit = True
        self.class_refit_groups = ['dump_freight']
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['non_dump_bulk']
        self.default_cargos = global_constants.default_cargos['dump']
        self.loading_speed_multiplier = 2
        self.weight_multiplier = 0.45
        # Graphics configuration
        self.gestalt_graphics = GestaltGraphicsVisibleCargo(bulk=True)


class DumpFeldbahn(DumpHaulerBase, FeldbahnMixin):
    """
    Dump feldbahn.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DumpTram(DumpHaulerBase, TramMixin):
    """
    Dump tram.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class DumpTruck(DumpHaulerBase, TruckMixin):
    """
    Dump truck.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class EdiblesTankerBase(Consist):
    """
    Base consist for edibles tankers. Wine, milk, water etc.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name_type_suffix = "EDIBLES_TANKER"
        self.autorefit = True
        self.class_refit_groups = [] # no classes, use explicit labels
        self.label_refits_allowed = global_constants.allowed_refits_by_label['edible_liquids']
        self.label_refits_disallowed = []
        self.default_cargos = global_constants.default_cargos['edibles_tank']
        self.loading_speed_multiplier = 2
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD
        self.weight_multiplier = 0.5


class EdiblesTankerTram(EdiblesTankerBase, TramMixin):
    """
    Edibles tanker tram.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class EdiblesTankerTruck(EdiblesTankerBase, TruckMixin):
    """
    Edibles tanker truck.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class FlatbedHaulerBase(Consist):
    """
    Base consist for flatbed hauler. Refits most cargos, not bulk.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name_type_suffix = "FLATBED"
        self.autorefit = True
        self.class_refit_groups = ['flatbed_freight']
        self.label_refits_allowed = ['GOOD']
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['non_flatbed_freight']
        self.default_cargos = global_constants.default_cargos['flat']
        # Graphics configuration
        self.gestalt_graphics = GestaltGraphicsVisibleCargo(piece='flat')


class FlatbedTram(FlatbedHaulerBase, TramMixin):
    """
    Flatbed tram.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class FlatbedTruck(FlatbedHaulerBase, TruckMixin):
    """
    Flatbed truck.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class FruitVegHaulerBase(Consist):
    """
    Consist base class for fruit and vegetables hauler.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name_type_suffix = "FRUIT_VEG"
        self.autorefit = True
        self.class_refit_groups = [] # no classes, use explicit labels
        self.label_refits_allowed = global_constants.allowed_refits_by_label['fruit_veg']
        self.label_refits_disallowed = []
        self.default_cargos = global_constants.default_cargos['fruit_veg']
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD
        self.weight_multiplier = 0.45


class FruitVegTram(FruitVegHaulerBase, TramMixin):
    """
    Fruit and vegetables tram.  No FruitVegTruck yet as of April 2019.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class IntermodalHauler(Consist):
    """
    Specialist intermodal (container) truck, limited range of cargos.  Keep same refit and speeds as BoxHauler
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name_type_suffix = "INTERMODAL"
        self.autorefit = True
        self.class_refit_groups = ['packaged_freight']
        self.label_refits_allowed = global_constants.allowed_refits_by_label['box_freight']
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['non_freight_special_cases']
        self.default_cargos = global_constants.default_cargos['box']
        self.loading_speed_multiplier = 2


class LivestockHaulerBase(Consist):
    """
    Consist base class for livestock Hauler
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name_type_suffix = "LIVESTOCK"
        self.autorefit = True
        self.class_refit_groups = [] # no classes, use explicit labels
        self.label_refits_allowed = ['LVST']
        self.label_refits_disallowed = []
        self.default_cargos = ['LVST'] # no need for fallbacks, only one cargo
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD
        self.weight_multiplier = 0.45


class LivestockTram(LivestockHaulerBase, TramMixin):
    """
    Livestock tram.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class LivestockTruck(LivestockHaulerBase, TruckMixin):
    """
    Livestock truck.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class LogHaulerBase(Consist):
    """
    Base consist for log hauler.  Wood.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name_type_suffix = "LOG"
        self.autorefit = True
        self.class_refit_groups = [] # no classes, use explicit labels
        self.label_refits_allowed = ['WOOD']
        self.label_refits_disallowed = []
        self.default_cargos = ['WOOD'] # no need for fallbacks, only one cargo
        self.loading_speed_multiplier = 2
        # Cargo graphics
        self.gestalt_graphics = GestaltGraphicsCustom({'WOOD': [0]},
                                                'vehicle_with_visible_cargo.pynml',
                                                generic_rows = [0])


class LogHEQS(LogHaulerBase, HEQSMixin):
    """
    Log hauling heavy equipment.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MailHaulerBase(Consist):
    """
    Consist base class for mail hauler.  Valuables, express cargos etc.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name_type_suffix = "MAIL"
        self.autorefit = True
        self.class_refit_groups = ['mail', 'express_freight']
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = ['TOUR']
        self.default_cargos = global_constants.default_cargos['mail']
        self.weight_multiplier = 0.2
        if not self.roadveh_flag_tram:
            self._sound_effect = 'SOUND_TRUCK_START'


class MailTram(MailHaulerBase, TramMixin):
    """
    Mail tram.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MailTruck(MailHaulerBase, TruckMixin):
    """
    Mail truck.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class MetalHaulerBase(Consist):
    """
    Base consist for specialist heavy hauler, e.g. multiwheel platform, steel mill hauler etc.
    High capacity, not very fast, refits to small subset of finished metal cargos.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name_type_suffix = "METAL"
        self.autorefit = True
        self.class_refit_groups = [] # no classes, use explicit labels
        self.label_refits_allowed = ['STEL', 'COPR', 'IRON', 'SLAG']
        self.label_refits_disallowed = []
        self.default_cargos = global_constants.default_cargos['metal']
        self.loading_speed_multiplier = 2


class MetalTruck(MetalHaulerBase, TruckMixin):
    """
    Metal truck.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class OpenHaulerBase(Consist):
    """
    Base consist for general cargo hauler. Refits everything except mail, pax.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name_type_suffix = "OPEN"
        self.autorefit = True
        self.class_refit_groups = ['all_freight']
        self.label_refits_allowed = [] # no specific labels needed
        self.label_refits_disallowed = ['TOUR']
        self.default_cargos = global_constants.default_cargos['open']
        # Graphics configuration
        self.gestalt_graphics = GestaltGraphicsVisibleCargo(bulk=True,
                                                            piece='open')


class OpenTram(OpenHaulerBase, TramMixin):
    """
    Open tram.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class OpenTruck(OpenHaulerBase, TruckMixin):
    """
    Open truck.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class PaxHaulerBase(Consist):
    """
    Common base class for pax vehicles.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.autorefit = True
        self.class_refit_groups = ['pax']
        self.label_refits_allowed = []
        self.label_refits_disallowed = []
        self.default_cargos = global_constants.default_cargos['pax']


class PaxHaulerLocalBase(PaxHaulerBase):
    """
    Base subclass for fast loading passenger tram or bus.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loading_speed_multiplier = 3
        self.weight_multiplier = 0.17


class PaxLocalBus(PaxHaulerLocalBase, BusCoachMixin):
    """
    Local passenger bus.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def name_type_suffix(self):
        # special case handling for name suffix strings
        return "STR_NAME_SUFFIX_BUS"


class PaxLocalTram(PaxHaulerLocalBase, TramMixin):
    """
    Local passenger tram.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # over-ride the default sound effect set by RoadVehicle subclass
        self._sound_effect = 'SOUND_LEVEL_CROSSING'

    @property
    def name_type_suffix(self):
        # special case handling for name suffix strings
        return "STR_NAME_SUFFIX_PASSENGER_TRAM"


class PaxExpressCoach(PaxHaulerBase, BusCoachMixin):
    """
    Express coach for pax. Express tram wasn't defined as of April 2019.  Split a PaxExpressBase subclass if needed
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD
        self.weight_multiplier = 0.2
        # over-ride the default sound effect set by parent subclasses
        # this assumes diesel, and will fail if none-diesel express coaches are added
        self._sound_effect = 'SOUND_TRUCK_START_2'

    @property
    def name_type_suffix(self):
        return "STR_NAME_SUFFIX_COACH"


class RefrigeratedHaulerBase(Consist):
    """
    Base consist for Refrigerated hauler.
    Refits to limited range of refrigerated cargos, with 'improved' cargo decay rate.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name_type_suffix = "REEFER"
        self.autorefit = True
        self.class_refit_groups = ['refrigerated_freight']
        self.label_refits_allowed = [] # no specific labels needed, refits all cargos that have refrigerated class
        self.label_refits_disallowed = []
        self.default_cargos = global_constants.default_cargos['reefer']
        self.cargo_age_period = 2 * global_constants.CARGO_AGE_PERIOD
        self.weight_multiplier = 0.5


class RefrigeratedTram(RefrigeratedHaulerBase, TramMixin):
    """
    Refrigerated tram.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class RefrigeratedTruck(RefrigeratedHaulerBase, TruckMixin):
    """
    Refrigerated truck.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SuppliesHaulerBase(Consist):
    """
    Base consist for specialist hauler with flatbed + crane or similar, for supplies.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name_type_suffix = "SUPPLIES"
        self.autorefit = True
        self.class_refit_groups = [] # no classes, use explicit labels
        self.label_refits_allowed = ['ENSP', 'FMSP', 'VEHI', 'BDMT']
        self.label_refits_disallowed = []
        self.default_cargos = global_constants.default_cargos['supplies']
        self.loading_speed_multiplier = 2
        self.weight_multiplier = 0.5
        # Graphics configuration
        self.gestalt_graphics = GestaltGraphicsCustom({'ENSP': [0], 'FMSP': [0], 'VEHI': [0]},
                                                       'vehicle_with_visible_cargo.pynml',
                                                       generic_rows = [0])


class SuppliesCake(SuppliesHaulerBase, CakeMixin):
    """
    Supplies hauler (multi-roadtype).  No supplies trams yet as of April 2019.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TankerBase(Consist):
    """
    Ronseal ("does what it says on the tin", for those without extensive knowledge of UK advertising).
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._name_type_suffix = "TANKER"
        # tankers are unrealistically autorefittable, and at no cost
        # Pikka: if people complain that it's unrealistic, tell them "don't do it then"
        # they also change livery at stations if refitted between certain cargo types <shrug>
        self.autorefit = True
        self.class_refit_groups = ['liquids']
        self.label_refits_allowed = []
        self.label_refits_disallowed = global_constants.disallowed_refits_by_label['non_generic_liquids']
        self.default_cargos = global_constants.default_cargos['tank']
        self.loading_speed_multiplier = 2
        self.weight_multiplier = 0.45
        # Graphics configuration
        self.gestalt_graphics = GestaltGraphicsLiveryOnly(recolour_maps=polar_fox.constants.tanker_livery_recolour_maps)


class TankerTram(TankerBase, TramMixin):
    """
    Tanker tram.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TankerTruck(TankerBase, TruckMixin):
    """
    Tanker truck.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


