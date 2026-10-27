# shared global constants via Polar Fox library
# done this way so we don't have to pass Polar Fox to templates, we can just pass global_constants
# assignments are clunky - they exist to stop pyflakes tripping on 'unused' imports
import polar_fox.constants

base_refits_by_class = polar_fox.constants.base_refits_by_class
cargo_labels = polar_fox.constants.cargo_labels
chameleon_cache_dir = polar_fox.constants.chameleon_cache_dir
default_cargos = polar_fox.constants.default_cargos
allowed_refits_by_label = polar_fox.constants.allowed_refits_by_label
disallowed_refits_by_label = polar_fox.constants.disallowed_refits_by_label
generated_files_dir = polar_fox.constants.generated_files_dir
graphics_path = polar_fox.constants.graphics_path
mail_multiplier = polar_fox.constants.mail_multiplier
max_game_date = polar_fox.constants.max_game_date
company_colour_maps = polar_fox.constants.company_colour_maps

metadata = {
    "dev_thread_url": "http://www.tt-forums.net/viewtopic.php?f=26&t=70241",
    "repo_url": "https://github.com/andythenorth/road-hog",
    "docs_url": "https://grf.farm/road-hog",
}

# capacity multipliers for capacity parameter
capacity_multipliers = (0.67, 1, 1.33)

# cargo aging constant - OTTD default is 185
CARGO_AGE_PERIOD = 185

# cost constants
FIXED_RUN_COST = 500.0
FUEL_RUN_COST = 10.0

# articulated parts must have a value less than 8192 (13 bit value)
max_articulated_id = 16383

# standard offsets for vehicle
# 3/8, 4/8, 5/8, 6/8, 7/8 and 8/8 were adjusted June 2016, tested, all looked correct
default_road_vehicle_offsets = {
    "1": (
        (-6, -23),
        (0, -17),
        (12, -10),
        (6, -11),
        (-6, -12),
        (-14, -10),
        (-14, -10),
        (-8, -16),
    ),  # may need fix
    "2": (
        (-6, -23),
        (-2, -16),
        (8, -10),
        (4, -11),
        (-6, -12),
        (-14, -10),
        (-16, -10),
        (-8, -14),
    ),
    "3": (
        (-6, -22),
        (-4, -15),
        (2, -10),
        (2, -11),
        (-6, -15),
        (-14, -10),
        (-14, -10),
        (-8, -15),
    ),
    "4": (
        (-6, -20),
        (-6, -14),
        (0, -10),
        (0, -11),
        (-6, -12),
        (-14, -10),
        (-14, -10),
        (-8, -14),
    ),
    "5": (
        (-6, -17),
        (-8, -13),
        (-6, -10),
        (-2, -11),
        (-6, -12),
        (-14, -10),
        (-14, -10),
        (-8, -13),
    ),
    "6": (
        (-6, -16),
        (-10, -12),
        (-8, -10),
        (-4, -11),
        (-6, -15),
        (-14, -10),
        (-14, -10),
        (-8, -12),
    ),
    "7": (
        (-6, -15),
        (-12, -11),
        (-14, -10),
        (-6, -11),
        (-6, -15),
        (-14, -10),
        (-14, -10),
        (-8, -11),
    ),
    "8": (
        (-6, -13),
        (-14, -10),
        (-18, -10),
        (-8, -11),
        (-6, -13),
        (-14, -10),
        (-14, -10),
        (-8, -10),
    ),
}

semi_truck_offset_jank = (
    (0, 1),
    (-2, 1),
    (-5, 0),
    (-2, 1),
    (0, 0),
    (-2, 1),
    (-1, 0),
    (-1, 1),
)

# spritesheet bounding boxes, each defined by a 3 tuple (left x, width, height);
# upper y is determined by spritesheet row position, so isn't defined as a constant
spritesheet_bounding_boxes = (
    (60, 12, 29),
    (77, 26, 20),
    (107, 33, 16),
    (147, 26, 20),
    (180, 12, 29),
    (197, 26, 20),
    (227, 33, 16),
    (267, 26, 20),
)

# rather than total spritesheet width, we often need to know the max x extent that actually contains sprites
# this is calculated from bounding boxes
sprites_max_x_extent = (
    spritesheet_bounding_boxes[7][0] + spritesheet_bounding_boxes[7][1]
)

# !! possibly deprecated - moved to graphics constants?  Horse doesn't have these constants
docs_sprite_max_width = (
    64  # cap how wide a buy_menu sprite can be, as some consists are long
)
docs_sprite_height = 16
custom_buy_menu_x_loc = 320

temp_storage_map = dict(
    wagon_recolour_random_livery_choice_num=24,
    wagon_recolour_livery_num_0=25,
    wagon_recolour_livery_num_1=26,
    wagon_recolour_livery_num_2=27,
    wagon_recolour_livery_num_3=28,
    wagon_recolour_livery_num_4=29,
    wagon_recolour_livery_num_5=30,
    wagon_recolour_livery_num_6=31,
    wagon_recolour_livery_num_7=32,
    flag_context_is_purchase=33,
)

# CABBAGE352 step 008a: IH runtime colour definitions (ordered)
custom_wagon_recolour_sprite_maps = {
    "custom_dark_brown": (105, 106, 33, 34, 35, 36, 37, 38),
    "custom_dark_pink": (40, 41, 42, 43, 44, 45, 46, 47),
    "custom_light_pink": (43, 44, 45, 46, 47, 166, 167, 168),
    "custom_dark_grey": (3, 16, 17, 18, 19, 20, 21, 22),
    "custom_dark_yellow": (60, 61, 62, 64, 65, 66, 67, 68),
    "custom_dark_white": (18, 7, 8, 10, 11, 12, 13, 14),
    "custom_light_purple": (
        105,
        136,
        54,
        172,
        173,
        174,
        143,
        39,
    ),
    "custom_light_mauve": (129, 130, 131, 132, 133, 134, 135, 14),
    "custom_dark_orange": (62, 63, 64, 193, 194, 195, 196, 197),
    "custom_dark_cream": (112, 113, 114, 116, 117, 118, 119, 120),
    # can't name it dark_green cos that conflates with DARK_GREEN
    "custom_green": (
        80,
        82,
        83,
        84,
        85,
        86,
        207,
        209,
    ),
    # can't name it dark_blue cos that conflates with DARK_BLUE
    "custom_blue": (
        147,
        148,
        149,
        150,
        151,
        152,
        153,
        210,
    ),
    # can't name it dark_light_blue cos that would be silly
    "custom_light_blue": (
        155,
        156,
        157,
        158,
        159,
        160,
        161,
        210,
    ),
    # can't name it light_dark_blue cos that would be silly
    "custom_dark_blue": (
        199,
        200,
        201,
        202,
        203,
        204,
        205,
        152,
    ),
    "custom_dark_red": (180, 181, 182, 183, 164, 165, 166, 167),
    "custom_pale_green": (97, 98, 99, 100, 101, 102, 103, 14),
    "custom_dark_green": (89, 90, 91, 92, 93, 94, 95, 31),
    "custom_rust": (104, 24, 106, 61, 62, 116, 36, 37),
    "custom_light_rust": (70, 40, 122, 73, 62, 115, 118, 119),
    "custom_oxide": (1, 24, 122, 41, 74, 76, 118, 119),
    "custom_faded_oxide": (1, 2, 106, 41, 74, 116, 36, 37),
    "custom_nightshade": (104, 2, 25, 17, 18, 19, 20, 10),
    "custom_light_nightshade": (1, 2, 106, 17, 18, 7, 20, 10),
    "custom_teal": (88, 97, 98, 157, 158, 159, 160, 103),
    "custom_dark_teal": (88, 97, 156, 157, 158, 101, 102, 103),
    "custom_ocean_teal": (105, 33, 155, 157, 158, 159, 160, 14),
    "custom_dark_ocean_teal": (104, 88, 155, 156, 158, 159, 102, 31),
    "custom_violet": (
        105,
        136,
        54,
        172,
        173,
        174,
        143,
        39,
    ),
    "custom_faded_violet": (105, 107, 109, 141, 174, 143, 176, 177),
    "custom_silver": (2, 18, 19, 20, 21, 22, 23, 14),
    "custom_dark_silver": (2, 4, 35, 19, 21, 22, 23, 14),
    "custom_pewter": (2, 3, 18, 19, 20, 21, 22, 13),
    "custom_dark_pewter": (2, 114, 18, 19, 20, 21, 22, 13),
    "custom_sulphur": (62, 62 + 1, 62 + 2, 62 + 3, 62 + 4, 62 + 5, 62 + 6, 62 + 7),
    "custom_dark_sulphur": (62, 62 + 1, 62 + 2, 193, 194, 50, 51, 52),
    "custom_obsidian": (1, 2, 24, 4, 5, 6, 7, 8),
    "custom_faded_obsidian": (1, 70, 16, 4, 26, 6, 19, 8),
    "custom_oil_black": (1, 2, 106, 4, 5, 6, 7, 8),
    "custom_faded_oil_black": (1, 70, 106, 4, 18, 6, 20, 9),
    "custom_ochre": (60, 61, 62, 63, 192, 193, 194, 196),
    "custom_faded_ochre": (60, 61, 62, 117, 192, 193, 196, 197),
    "custom_clover": (96, 97, 98, 99, 100, 101, 102, 103),
    "custom_faded_clover": (97, 98, 99, 100, 101, 102, 103, 14),
    "custom_cloud": (3, 17, 19, 20, 21, 22, 13, 69),
    "custom_faded_cloud": (24, 25, 35, 20, 21, 22, 13, 15),
    "custom_mist": (2, 4, 18, 20, 21, 22, 13, 69),
    "custom_faded_mist": (2, 107, 7, 20, 21, 22, 13, 69),
}


colour_sets = {
    "dark_blue": ["COLOUR_DARK_BLUE", "custom_dark_blue"],
    "pale_green": ["COLOUR_PALE_GREEN", "custom_pale_green"],
    "pink": ["COLOUR_PINK", "custom_dark_pink"],
    "yellow": ["COLOUR_YELLOW", "custom_dark_yellow"],
    "red": ["COLOUR_RED", "custom_dark_red"],
    "light_blue": ["COLOUR_LIGHT_BLUE", "custom_light_blue"],
    "green": ["COLOUR_GREEN", "custom_green"],
    "dark_green": ["COLOUR_DARK_GREEN", "custom_dark_green"],
    "blue": ["COLOUR_BLUE", "custom_blue"],
    "cream": ["COLOUR_CREAM", "custom_dark_cream"],
    "mauve": ["COLOUR_MAUVE", "custom_light_mauve"],
    "purple": ["COLOUR_PURPLE", "custom_light_purple"],
    "orange": ["COLOUR_ORANGE", "custom_dark_orange"],
    "brown": ["COLOUR_BROWN", "custom_dark_brown"],
    "grey": ["COLOUR_GREY", "custom_dark_grey"],
    "white": ["COLOUR_WHITE", "custom_dark_white"],
    "freight_rust": ["custom_rust", "custom_light_rust"],
    "freight_oxide": ["custom_oxide", "custom_faded_oxide"],
    "freight_grey": ["custom_dark_grey", "COLOUR_GREY"],
    "freight_nightshade": ["custom_nightshade", "custom_light_nightshade"],
    "freight_teal": ["custom_teal", "custom_dark_teal"],
    "freight_ocean_teal": ["custom_ocean_teal", "custom_dark_ocean_teal"],
    "freight_violet": ["custom_violet", "custom_faded_violet"],
    "freight_silver": ["custom_silver", "custom_dark_silver"],
    "freight_pewter": ["custom_pewter", "custom_dark_pewter"],
    "freight_sulphur": ["custom_sulphur", "custom_dark_sulphur"],
    "freight_obsidian": ["custom_obsidian", "custom_faded_obsidian"],
    "freight_oil_black": ["custom_oil_black", "custom_faded_oil_black"],
    "freight_ochre": ["custom_ochre", "custom_faded_ochre"],
    "freight_sand": ["COLOUR_BROWN", "custom_dark_brown"],
    "freight_clover": ["custom_clover", "custom_faded_clover"],
    "freight_cloud": ["custom_cloud", "custom_faded_cloud"],
    "freight_mist": ["custom_mist", "custom_faded_mist"],
    # this is a hack to match express intermodal to industrial yellow
    "freight_industrial_yellow": ["COLOUR_YELLOW", "COLOUR_YELLOW"],
}


complements_to_company_colours = {
    "COLOUR_DARK_BLUE": "COLOUR_BLUE",
    "COLOUR_PALE_GREEN": "COLOUR_GREEN",
    "COLOUR_PINK": "COLOUR_RED",
    "COLOUR_YELLOW": "COLOUR_ORANGE",
    "COLOUR_RED": "COLOUR_PINK",
    "COLOUR_LIGHT_BLUE": "COLOUR_BLUE",
    "COLOUR_GREEN": "COLOUR_DARK_GREEN",
    "COLOUR_DARK_GREEN": "COLOUR_GREEN",
    "COLOUR_BLUE": "COLOUR_DARK_BLUE",
    "COLOUR_CREAM": "COLOUR_BROWN",
    "COLOUR_MAUVE": "COLOUR_PURPLE",
    "COLOUR_PURPLE": "COLOUR_MAUVE",
    "COLOUR_ORANGE": "COLOUR_YELLOW",
    "COLOUR_BROWN": "COLOUR_CREAM",
    "COLOUR_GREY": "COLOUR_BROWN",  # more likely we want to complement grey with brown than white
    "COLOUR_WHITE": "COLOUR_GREY",
}


freight_wagon_liveries = {
    "COMPANY_COLOUR": {
        "colour_set_names": ["company_colour"],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "COMPLEMENT_COMPANY_COLOUR": {
        "colour_set_names": ["complement_company_colour"],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "RANDOM_LIVERIES_COMPLEMENT_COMPANY_COLOUR": {
        "colour_set_names": ["company_colour", "complement_company_colour"],
        "purchase_swatch_colour_set_names": [
            "company_colour",
            "complement_company_colour",
        ],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "RANDOM_LIVERIES_VARIETY_GEMSTONE": {
        # colour set names weighted for random weighting
        "colour_set_names": [
            "freight_violet",
            "freight_cloud",
            "freight_cloud",
            "freight_cloud",
            "freight_cloud",
            "freight_teal",
            "freight_ocean_teal",
            "freight_mist",
        ],
        "purchase_swatch_colour_set_names": [
            "freight_violet",
            "freight_cloud",
            "freight_ocean_teal",
        ],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "RANDOM_LIVERIES_VARIETY_LIMEWASH": {
        "colour_set_names": [
            "freight_sand",
            "freight_sand",  # random weighting balance
            "freight_mist",
            "freight_cloud",
        ],
        "purchase_swatch_colour_set_names": ["freight_sand", "freight_cloud"],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "RANDOM_LIVERIES_VARIETY_FERROUS": {
        "colour_set_names": [
            "freight_sand",
            "freight_oil_black",
            "freight_obsidian",
            "freight_nightshade",
            "freight_ochre",
        ],
        "purchase_swatch_colour_set_names": ["freight_sand", "freight_ochre", "freight_oil_black"],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "RANDOM_LIVERIES_BUMBLEBEE": {
        # colour set names weighted for random weighting
        "colour_set_names": [
            "freight_oil_black",
            "freight_nightshade",
            "freight_nightshade",
            "freight_obsidian",
            "freight_ochre",
            "freight_sulphur",
            "freight_sulphur",
            "freight_sand",
        ],
        "purchase_swatch_colour_set_names": [
            "freight_sand",
            "freight_oil_black",
            "freight_ochre",
        ],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "RANDOM_LIVERIES_GREY_RUST_NIGHTSHADE": {
        "colour_set_names": [
            "freight_grey",
            "freight_rust",
            "freight_rust",  # for random weighting balance
            "freight_nightshade",
        ],
        "purchase_swatch_colour_set_names": [
            "freight_grey",
            "freight_oil_black",
            "freight_rust",
        ],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "RANDOM_LIVERIES_VIOLET_TEAL_OCEAN_TEAL": {
        "colour_set_names": [
            "freight_teal",  # ordered for random weighting to teal
            "freight_ocean_teal",
            "freight_violet",
        ],
        "purchase_swatch_colour_set_names": ["freight_violet", "freight_ocean_teal"],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "RANDOM_LIVERIES_SILVER_PEWTER": {
        "colour_set_names": ["freight_silver", "freight_pewter"],
        "purchase_swatch_colour_set_names": ["freight_silver"],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "RANDOM_LIVERIES_CLOVER_OCHRE_SILVER": {
        "colour_set_names": [
            "freight_clover",
            "freight_clover",
            "freight_silver",
            "freight_ochre",
        ],
        "purchase_swatch_colour_set_names": [
            "freight_clover",
            "freight_silver",
            "freight_ochre",
        ],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "RANDOM_LIVERIES_CLOVER_OCHRE_SAND": {
        "colour_set_names": [
            "freight_clover",
            "freight_clover",  # for random weighting balance
            "freight_ochre",
            "freight_sand",
        ],
        "purchase_swatch_colour_set_names": [
            "freight_clover",
            "freight_ochre",
            "freight_sand",
        ],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "RANDOM_LIVERIES_CLOVER_OCHRE_SULPHUR": {
        "colour_set_names": [
            "freight_clover",
            "freight_clover",  # for random weighting balance
            "freight_ochre",
            "freight_sulphur",
        ],
        "purchase_swatch_colour_set_names": [
            "freight_clover",
            "freight_ochre",
            "freight_sulphur",
        ],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "RANDOM_LIVERIES_SULPHUR_OCHRE": {
        "colour_set_names": ["freight_sulphur", "freight_ochre"],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "RANDOM_LIVERIES_OIL_BLACK_OBSIDIAN_NIGHTSHADE": {
        "colour_set_names": [
            "freight_oil_black",
            "freight_obsidian",
            "freight_nightshade",
        ],
        "purchase_swatch_colour_set_names": ["freight_oil_black"],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "RANDOM_LIVERIES_OIL_BLACK_OBSIDIAN": {
        "colour_set_names": [
            "freight_oil_black",
            "freight_obsidian",
        ],
        "purchase_swatch_colour_set_names": ["freight_oil_black"],
        "proxy_livery_for_badge_display_and_filter": "RANDOM_LIVERIES_OIL_BLACK_OBSIDIAN_NIGHTSHADE",
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "RANDOM_LIVERIES_OCHRE_SAND": {
        "colour_set_names": ["freight_ochre", "freight_sand"],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "RANDOM_LIVERIES_TEAL_PEWTER_SILVER": {
        "colour_set_names": [
            "freight_teal",
            "freight_teal",  # double teal for random balance, don't bother using freight_ocean_teal, too much variation then
            "freight_pewter",
            "freight_silver",
        ],
        "purchase_swatch_colour_set_names": ["freight_teal", "freight_silver"],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    # generally we use bonus teal, but occasionally we want this to bounce teal to first group level
    "RANDOM_LIVERIES_TEAL_OCEAN_TEAL": {
        "colour_set_names": [
            "freight_ocean_teal",
            "freight_teal",
        ],
        "purchase_swatch_colour_set_names": ["freight_ocean_teal"],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "RANDOM_LIVERIES_SILVER_GREY_PEWTER": {
        "colour_set_names": [
            "freight_silver",
            "freight_grey",
            "freight_pewter",
            "freight_pewter",  # double pewter for random balance
        ],
        "purchase_swatch_colour_set_names": ["freight_silver", "freight_pewter"],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "RANDOM_LIVERIES_OXIDE_RUST": {
        "colour_set_names": ["freight_oxide", "freight_rust"],
        "purchase_swatch_colour_set_names": [
            "freight_oxide"
        ],  # best choice, contrasts with rust if used in random mix
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "FREIGHT_MIST": {
        "colour_set_names": [
            "freight_mist",
            "freight_cloud",
        ],
        "purchase_swatch_colour_set_names": ["freight_mist"],
        "proxy_livery_for_badge_display_and_filter": "RANDOM_LIVERIES_SILVER_PEWTER",
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "FREIGHT_KALE": {
        "colour_set_names": ["freight_clover"],
        "purchase_swatch_colour_set_names": ["freight_clover"],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
    "FREIGHT_RED": {
        "colour_set_names": ["red"],
        "docs_image_input_cc": [
            ("COLOUR_BLUE", "COLOUR_BLUE"),
            ("COLOUR_RED", "COLOUR_WHITE"),
        ],
    },
}
