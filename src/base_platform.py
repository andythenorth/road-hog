class BasePlatform(object):
    """
    Vehicles can optionally use a base platform.
    This can be e.g.
    - a complete locomotive, wagon, semi-tractor etc
    - a chassis and cab to which the body is composited
    """

    # no init needed, BasePlatform subclasses use only class attrs

    def configure_unit_args(self, **kwargs):
        # pull the class attrs off using a list, this keeps the attribute declarations ni subclasses of BasePlatforms
        for key in ['always_use_same_spriterow',
                    'capacity',
                    'cargo_length',
                    'chassis',
                    'effects',
                    'semi_truck_shift_offset_jank',
                    'unit_is_semi_tractor',
                    'type',
                    'vehicle_length']:
            value = getattr(self, key, False)
            if value is not False:
                kwargs[key] = value
        kwargs['base_platform'] = self # replace the class name with this class instance
        return kwargs

    def get_spritesheet_name_body_or_complete_vehicle(self, consist):
        # over-ride this in subclasses to provide spritesheet names according to arbitrary rules per platform type
        return None

    """
    def __init__(self, **kwargs):
        self.consist = kwargs.get('consist')

        # setup properties for this road vehicle
        self.numeric_id = kwargs.get('numeric_id', None)

        # vehicle_length is either derived from chassis length or similar, or needs to be set explicitly as kwarg
        self._vehicle_length = kwargs.get('vehicle_length', None)

        self.semi_truck_shift_offset_jank = kwargs.get('semi_truck_shift_offset_jank', None)
        # capacities variable by parameter
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
        # optional - only set if the graphics processor generates the vehicle chassis
        self.chassis = kwargs.get('chassis', None)
        # only set if the graphics processor requires it to generate cargo sprites
        # defines the size of cargo sprite to use
        # if the vehicle cargo area is not an OTTD unit length, use the next size up and the masking will sort it out
        # some longer vehicles may place multiple shorter cargo sprites, e.g. 7/8 vehicle, 2 * 4/8 cargo sprites (with some overlapping)
        self.cargo_length = kwargs.get('cargo_length', None)
        # effects can be specified in detail per vehicle, or fall back to those defined by RoadVehicle subclass
        self._effect_spawn_model = kwargs.get('effect_spawn_model', None)
        self.effects = kwargs.get('effects', []) # default for effects is an empty list
        self.default_effect_sprite = None # default is no effect sprite
    """
