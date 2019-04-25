# capacity multipliers for capacity parameter
capacity_multipliers = (0.67, 1, 1.33)

grfid = r"\97\87\EA\FE"

# cargo aging constant - OTTD default is 185
CARGO_AGE_PERIOD = 185

# cost constants
FIXED_RUN_COST = 500.0
FUEL_RUN_COST = 10.0

# standard offsets for vehicle
# 3/8, 4/8, 5/8, 6/8, 7/8 and 8/8 were adjusted June 2016, tested, all looked correct
default_road_vehicle_offsets = {'1': ((-6, -23), (0, -17), (12, -10), (6, -11), (-6, -12), (-14, -10), (-14, -10), (-8, -16)), # may need fix
                                '2': ((-6, -23), (-2, -16), (8, -10), (4, -11), (-6, -12), (-14, -10), (-16, -10), (-8, -14)),
                                '3': ((-6, -22), (-4, -15), (2, -10), (2, -11), (-6, -15), (-14, -10), (-14, -10), (-8, -15)),
                                '4': ((-6, -20), (-6, -14), (0, -10), (0, -11), (-6, -12), (-14, -10), (-14, -10), (-8, -14)),
                                '5': ((-6, -17), (-8, -13), (-6, -10), (-2, -11), (-6, -12), (-14, -10), (-14, -10), (-8, -13)),
                                '6': ((-6, -16), (-10, -12), (-8, -10), (-4, -11), (-6, -15), (-14, -10), (-14, -10), (-8, -12)),
                                '7': ((-6, -15), (-12, -11), (-14, -10), (-6, -11), (-6, -15), (-14, -10), (-14, -10), (-8, -11)),
                                '8': ((-6, -13), (-14, -10), (-18, -10), (-8, -11), (-6, -13), (-14, -10), (-14, -10), (-8, -10))}

semi_truck_offset_jank = ((0, 1), (-2, 1), (-5, 0), (-2, 1), (0, 0), (-2, 1), (-1, 0), (-1, 1))

# spritesheet bounding boxes, each defined by a 3 tuple (left x, width, height);
# upper y is determined by spritesheet row position, so isn't defined as a constant
spritesheet_bounding_boxes = ((60, 12, 29), (77, 26, 20), (107, 33, 16), (147, 26, 20),
                              (180, 12, 29), (197, 26, 20), (227, 33, 16), (267, 26, 20))

# rather than total spritesheet width, we often need to know the max x extent that actually contains sprites
# this is calculated from bounding boxes
sprites_max_x_extent = spritesheet_bounding_boxes[7][0] + spritesheet_bounding_boxes[7][1]

buy_menu_sprite_width = 36 # 36 is correct, but some spritesheets might have wrong widths due to copy-pasteo etc
buy_menu_sprite_height = 16

# shared global constants via Polar Fox library - import at end to make the this project's constants easier to work with
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
