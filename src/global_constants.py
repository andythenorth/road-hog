
buy_menu_sort_order_locos = [# brit vehicles
                           'broadrock',
                           'mcdowell',
                           'witch_hill',
                           'pigstick',
                           'huntsman',
                           'stungun',
                           'silvertop',
                           'california',
                           ]

# set (roster) <-> numeric id mapping
# vehicle IDs are in format nxxx where n is set numeric id
# first 1k IDs reserved, IDs must be < 16383, with 500 IDs allocated per set for main roster, and 500 per set for extras, so max 15 sets
vehicle_set_id_mapping = {'brit': 1}


# shared lists of allowed classes, shared across multiple ship types
base_refits_by_class = {'empty': [],
                        'all_freight': ['CC_BULK', 'CC_PIECE_GOODS', 'CC_EXPRESS', 'CC_LIQUID', 'CC_ARMOURED', 'CC_REFRIGERATED', 'CC_COVERED', 'CC_NON_POURABLE'],
                        'pax': ['CC_PASSENGERS'],
                        'mail': ['CC_MAIL'],
                        'liquids': ['CC_LIQUID'],
                        'packaged_freight': ['CC_PIECE_GOODS', 'CC_EXPRESS', 'CC_ARMOURED', 'CC_LIQUID'],
                        'flatcar_freight': ['CC_PIECE_GOODS', 'CC_EXPRESS'],
                        'hopper_freight': ['CC_BULK'],
                        'covered_hopper_freight': [],
                        'refrigerated_freight': [],
                        'express_freight': ['CC_EXPRESS','CC_ARMOURED']}


# capacity multipliers for capacity parameter
capacity_multipliers = [0.67, 1, 1.33]

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
                                '4': [[-3, -20], [-6, -18], [0, -11], [-8, -15], [-3, -12], [-14, -14], [-17, -11], [-8, -19]],
                                '5': [[-3, -18], [-8, -17], [-4, -11], [-8, -15], [-3, -12], [-14, -14], [-17, -11], [-8, -18]],
                                '6': [[-3, -16], [-10, -16], [-8, -11], [-8, -15], [-3, -12], [-14, -14], [-17, -11], [-8, -17]],
                                '7': [[-3, -14], [-12, -15], [-12, -11], [-8, -15], [-3, -12], [-14, -14], [-17, -11], [-8, -15]],
                                '8': [[-3, -12], [-14, -14], [-16, -11], [-8, -15], [-3, -12], [-14, -14], [-16, -11], [-8, -15]],
                                '9': [[-3, -12], [-14, -14], [-16, -11], [-8, -15], [-3, -12], [-14, -14], [-16, -11], [-8, -15]], # needs fix
                                '10': [[-3, -12], [-14, -14], [-16, -11], [-8, -15], [-3, -12], [-14, -14], [-16, -11], [-8, -15]]} # needs fix
