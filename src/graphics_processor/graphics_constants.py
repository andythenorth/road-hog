# colour defaults
CC1 = 198
CC2 = 80

# a convenience constant that holds a mapping for swapping CC1 and CC2 around
CC1_CC2_SWAP_MAP = {}
for i in range(8):
    CC1_CC2_SWAP_MAP[CC1 + i] = CC2 + i
    CC1_CC2_SWAP_MAP[CC2 + i] = CC1 + i

# facts about 'standard' spritesheets, spritesheets varying from this will be painful
spriterow_height = 30
spritesheet_top_margin = 10
spritesheet_width = 455

# --- Cargo Maps ---- #
# label order matters, so tuples are used not dicts
# could probably have used orderedict or named tuple, but...blah

# Bulk
# GRVL is also reused for generic unknown cargos, and is in position 0 for this reason
# other cargos should be in alphabetical order
# SCMT *is* bulk cargo in this set, realism is not relevant here, went back and forth on this a few times :P
bulk_cargo_recolour_maps = (("GRVL", {170: 6, 171: 4, 172: 7, 173: 8, 174: 21, 175: 11, 176: 12}),
                            ("AORE", {170: 42, 171: 123, 172: 74, 173: 125, 174: 162, 175: 126, 176: 78}),
                            ("CLAY", {170: 57, 171: 57, 172: 57, 173: 77, 174: 78, 175: 78, 176: 79}),
                            ("COAL", {170: 1, 171: 1, 172: 2, 173: 2, 174: 3, 175: 4, 176: 5}),
                            ("CORE", {170: 1, 171: 32, 172: 25, 173: 27, 174: 34, 175: 56, 176: 59}),
                            ("IORE", {170: 75, 171: 76, 172: 123, 173: 122, 174: 124, 175: 74, 176: 104}),
                            ("MNO2", {170: 1, 171: 16, 172: 3, 173: 17, 174: 18, 175: 19, 176: 20}),
                            ("NITR", {170: 37, 171: 38, 172: 38, 173: 39, 174: 39, 175: 69, 176: 69}),
                            ("PHOS", {170: 63, 171: 64, 172: 192, 173: 65, 174: 193, 175: 64, 176: 194}),
                            ("PORE", {170: 40, 171: 72, 172: 73, 173: 33, 174: 33, 175: 63, 176: 63}),
                            ("SAND", {170: 108, 171: 64, 172: 65, 173: 197, 174: 36, 175: 196, 176: 197}),
                            ("SCMT", {170: 104, 171: 3, 172: 2, 173: 70, 174: 71, 175: 72, 176: 3}))

# Piece
# 2-tuples, containing 2 lists (['LBL1', 'LBL2'], ['filename_1', 'filename_2'])
# this groups labels and sprites, but there's no obvious problem with that right now
# if a label can't share a group of sprites, it can repeat some filenames, that's just inefficient, but works
piece_cargo_maps = ((['GOOD'], ['crates_1']),
                    (['ENSP', 'FMSP'], ['tarps_blue_1']),
                    (['WOOD'], ['logs']),
                    (['WDPR'], ['lumber_planks']),
                    (['PAPR'], ['paper_coils']),
                    (['COPR'], ['copper_coils']),
                    (['STEL'], ['steel_coils']))

# --- End Cargo Maps --- #
