# colour defaults
CC1 = 198
CC2 = 80

# a convenience constant that holds a mapping for swapping CC1 and CC2 around
CC1_CC2_SWAP_MAP = {}
for i in range(8):
    CC1_CC2_SWAP_MAP[CC1 + i] = CC2 + i
    CC1_CC2_SWAP_MAP[CC2 + i] = CC1 + i

body_recolour_CC1 = {136: CC1, 137: CC1+1, 138: CC1+2, 139: CC1+3, 140: CC1+4, 141: CC1+5, 142: CC1+6, 143: CC1+7}
body_recolour_CC1 = {136: CC2, 137: CC2+1, 138: CC2+2, 139: CC2+3, 140: CC2+4, 141: CC2+5, 142: CC2+6, 143: CC2+7}

# facts about 'standard' spritesheets, spritesheets varying from this will be painful
spriterow_height = 30
spritesheet_top_margin = 10
spritesheet_width = 455

# --- Cargo Maps ---- #
# label order matters, so tuples are used not dicts

# Containers
# !! simple recolouring, not cargo specific.  May need work ??  Could be cargo-specific??
container_recolour_maps = ({170 + i: CC1 + i for i in range(8)},
                           {170 + i: CC2 + i for i in range(8)},
                           {170 + i: 8 + i for i in range(8)})

# shared global constants via Polar Fox library - import at end to make the this project's constants easier to work with
# assignments are clunky - they exist to stop pyflakes tripping on 'unused' imports
import polar_fox.constants
bulk_cargo_recolour_maps = polar_fox.constants.bulk_cargo_recolour_maps
piece_sprites_to_cargo_labels_maps = polar_fox.constants.piece_sprites_to_cargo_labels_maps
piece_vehicle_type_to_sprites_maps = polar_fox.constants.piece_vehicle_type_to_sprites_maps
tanker_livery_recolour_maps = polar_fox.constants.tanker_livery_recolour_maps