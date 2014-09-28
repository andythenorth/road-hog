# set (roster) <-> numeric id mapping
# vehicle IDs are in format nxxx where n is set numeric id
# first 1k IDs reserved, IDs must be < 16383, with 500 IDs allocated per set for main roster, and 500 per set for extras, so max 15 sets
# also serves as the parameter number for action 14
vehicle_set_id_mapping = {'brit': 1, 'wasteland': 2}


# shared lists of allowed classes, shared across multiple vehicle types
# these lists are similar but not identical across Iron Horse, Squid, Road Hog etc
base_refits_by_class = {'empty': [],
                        'all_freight': ['CC_MAIL', 'CC_BULK', 'CC_PIECE_GOODS', 'CC_EXPRESS', 'CC_LIQUID', 'CC_ARMOURED', 'CC_REFRIGERATED', 'CC_COVERED', 'CC_NON_POURABLE'],
                        'pax': ['CC_PASSENGERS'],
                        'mail': ['CC_MAIL'],
                        'liquids': ['CC_LIQUID'],
                        'packaged_freight': ['CC_PIECE_GOODS', 'CC_EXPRESS', 'CC_ARMOURED', 'CC_LIQUID'],
                        'flatcar_freight': ['CC_PIECE_GOODS', 'CC_EXPRESS'],
                        'hopper_freight': ['CC_BULK'],
                        'bulk_farm_freight': [], # explicit allowal by label instead
                        'covered_hopper_freight': [], # explicit allowal by label instead
                        'refrigerated_freight': ['CC_REFRIGERATED'],
                        'express_freight': ['CC_EXPRESS','CC_ARMOURED']}

# rather than using disallowed classes (can cause breakage), specific labels are disallowed
# this is done per vehicle type, or added to global_constants for ease of reuse and updating
# these lists are similar but not identical across Iron Horse, Squid, Road Hog etc
disallowed_refits_by_label = {'non_hopper_bulk_freight': ['WOOD', 'SGCN', 'FICR', 'BDMT', 'WDPR', 'GRAI', 'WHEA', 'MAIZ', 'SGBT'],
                              'edible_liquids': ['MILK', 'WATR', 'BEER', 'FOOD'],
                              'non_edible_liquids': ['RFPR', 'OIL_', 'FMSP', 'PETR', 'RUBR']}

# capacity multipliers for capacity parameter
capacity_multipliers = [0.67, 1, 1.33]
# mailbags are < 1t, multiply capacity appropriately
mail_multiplier = 2

# used to construct the cargo table automatically
# ! order is significant ! - openttd will cascade through default cargos in the order specified by the cargo table
cargo_labels = ['PASS', # pax first
                'TOUR',
                # "the mail must get through"
                'MAIL',
                # all other cargos - append new ones to end, don't change order
                'COAL',
                'IORE',
                'GRVL',
                'SAND',
                'AORE',
                'CORE',
                'CLAY',
                'SCMT',
                'WOOD',
                'LIME',
                'GOOD',
                'FOOD',
                'STEL',
                'FMSP',
                'ENSP',
                'BEER',
                'BDMT',
                'MNSP',
                'PAPR',
                'WDPR',
                'VEHI',
                'COPR',
                'DYES',
                'OIL_',
                'RFPR',
                'PETR',
                'PLAS',
                'WATR',
                'FISH',
                'CERE',
                'FICR',
                'FRVG',
                'FRUT',
                'GRAI',
                'LVST',
                'MAIZ',
                'MILK',
                'RUBR',
                'SGBT',
                'SGCN',
                'WHEA',
                'WOOL',
                'OLSD',
                'SUGR']

grfid = r"\97\87\EA\FE"

# chameleon templating goes faster if a cache dir is used; this specifies which dir is cache dir
chameleon_cache_dir = 'chameleon_cache'

# specify location for intermediate files generated during build (nml, graphics, lang etc)
generated_files_dir = 'generated'

# this is for nml, don't need to use python path module here
graphics_path = generated_files_dir + '/graphics/'

# cost constants
FIXED_RUN_COST = 500.0
FUEL_RUN_COST = 10.0

# OpenTTD's max date
max_game_date = 5000001

# standard offsets for vehicle
default_road_vehicle_offsets = {'1': [[-3, -12], [-14, -14], [-16, -11], [-8, -15], [-3, -12], [-14, -14], [-16, -11], [-8, -15]], # needs fix
                                '2': [[-3, -12], [-14, -14], [-16, -11], [-8, -15], [-3, -12], [-14, -14], [-16, -11], [-8, -15]], # needs fix
                                '3': [[-3, -12], [-14, -14], [-16, -11], [-8, -15], [-3, -12], [-14, -14], [-16, -11], [-8, -15]], # needs fix
                                '4': [[-6, -20], [-6, -15], [0, -11], [0, -11], [-6, -12], [-14, -10], [-16, -11], [-8, -14]],
                                '5': [[-6, -17], [-8, -14], [-4, -11], [-2, -11], [-6, -12], [-14, -10], [-16, -11], [-8, -14]],
                                '6': [[-6, -16], [-10, -12], [-8, -10], [-4, -10], [-6, -15], [-14, -10], [-16, -10], [-8, -12]],
                                '7': [[-6, -15], [-12, -12], [-14, -10], [-6, -11], [-6, -15], [-14, -10], [-14, -10], [-8, -12]],
                                '8': [[-6, -13], [-14, -11], [-16, -10], [-8, -11], [-6, -13], [-14, -11], [-16, -10], [-8, -11]],
                                '9': [[-3, -12], [-14, -14], [-16, -11], [-8, -15], [-3, -12], [-14, -14], [-16, -11], [-8, -15]], # needs fix
                                '10': [[-3, -12], [-14, -14], [-16, -11], [-8, -15], [-3, -12], [-14, -14], [-16, -11], [-8, -15]]} # needs fix
