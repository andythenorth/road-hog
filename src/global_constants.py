# shared lists of allowed classes, shared across multiple vehicle types
# these lists are similar but not identical across Iron Horse, Squid, Road Hog etc
base_refits_by_class = {'empty': [],
                        'all_freight': ['CC_MAIL', 'CC_BULK', 'CC_PIECE_GOODS', 'CC_EXPRESS', 'CC_LIQUID', 'CC_ARMOURED', 'CC_REFRIGERATED', 'CC_COVERED', 'CC_NON_POURABLE'],
                        'pax': ['CC_PASSENGERS'],
                        'mail': ['CC_MAIL'],
                        'liquids': ['CC_LIQUID'],
                        'packaged_freight': ['CC_PIECE_GOODS', 'CC_EXPRESS', 'CC_ARMOURED', 'CC_LIQUID'],
                        'flatbed_freight': ['CC_PIECE_GOODS'],
                        'dump_freight': ['CC_BULK'],
                        'bulk_farm_freight': [], # explicit allowal by label instead
                        'covered_hopper_freight': [], # explicit allowal by label instead
                        'refrigerated_freight': ['CC_REFRIGERATED'],
                        'express_freight': ['CC_EXPRESS','CC_ARMOURED']}

# rather than using disallowed classes (can cause breakage), specific labels are disallowed
# this is done per vehicle type, or added to global_constants for ease of reuse and updating
# these lists are similar but not identical across Iron Horse, Squid, Road Hog etc
disallowed_refits_by_label = {'non_dump_bulk': ['WOOD', 'SGCN', 'FICR', 'BDMT', 'WDPR', 'GRAI', 'WHEA', 'MAIZ', 'FRUT', 'BEAN'],
                              'edible_liquids': ['MILK', 'WATR', 'BEER', 'FOOD', 'EOIL'],
                              'non_flatbed_freight': ['FOOD', 'FISH', 'LVST', 'FRUT', 'BEER', 'MILK', 'JAVA', 'SUGR', 'NUTS', 'EOIL'],
                              'non_edible_liquids': ['RFPR', 'OIL_', 'FMSP', 'PETR', 'RUBR'],
                              'non_freight_special_cases': ['TOUR']}

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
                'SUGR',
                'BEAN',
                'NITR',
                'JAVA',
                'VEHI',
                'EOIL',
                'CASS',
                'NUTS',
                'MNO2',
                'PHOS']

grfid = r"\97\87\EA\FE"

# chameleon templating goes faster if a cache dir is used; this specifies which dir is cache dir
chameleon_cache_dir = 'chameleon_cache'

# specify location for intermediate files generated during build (nml, graphics, lang etc)
generated_files_dir = 'generated'

# this is for nml, don't need to use python path module here
graphics_path = generated_files_dir + '/graphics/'

# cargo aging constant - OTTD default is 185
CARGO_AGE_PERIOD = 185

# cost constants
FIXED_RUN_COST = 500.0
FUEL_RUN_COST = 10.0

# OpenTTD's max date
max_game_date = 5000001

# standard offsets for vehicle
# for 5/8 and 4/8, Capo truck in rev 732 is tested and canonical for offset, spritesheet position and vehicle length
default_road_vehicle_offsets = {'1': [[-6, -23], [0, -17], [12, -10], [6, -11], [-6, -12], [-14, -10], [-14, -10], [-8, -16]], # may need fix
                                '2': [[-6, -23], [-2, -16], [8, -10], [4, -11], [-6, -12], [-14, -10], [-16, -10], [-8, -14]],
                                '3': [[-6, -22], [-4, -17], [2, -10], [2, -11], [-6, -15], [-14, -10], [-16, -10], [-8, -16]],
                                '4': [[-6, -20], [-6, -14], [0, -10], [0, -11], [-6, -12], [-14, -10], [-14, -10], [-8, -14]],
                                '5': [[-6, -17], [-8, -13], [-6, -10], [-2, -11], [-6, -12], [-14, -10], [-14, -10], [-8, -13]],
                                '6': [[-6, -16], [-10, -12], [-8, -10], [-4, -11], [-6, -15], [-14, -10], [-14, -10], [-8, -13]],
                                '7': [[-6, -15], [-12, -12], [-14, -10], [-6, -11], [-6, -15], [-14, -10], [-14, -10], [-8, -11]],
                                '8': [[-6, -13], [-14, -11], [-16, -10], [-8, -11], [-6, -13], [-14, -11], [-16, -10], [-8, -11]]}

semi_truck_offset_jank = [[0, 1], [-2, 1], [-4, 0], [-2, 1], [0, 0], [-2, 1], [-1, 0], [-1, 1]]
