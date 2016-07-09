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

def bulk_cargo_recolour_maps():
    # we need the labels, and order matters, so use two-tuple not a dict
    # could probably have used orderedict or named tuple, but...blah
    # GRVL is also reused for generic unknown cargos, and is in position 0 for this reason
    # (there is no mapping for unknown cargos, just uses first spriteset)
    # SCMT *is* bulk cargo in this set, realism is not relevant here, went back and forth on this a few times :P
    return (("GRVL", {170: 6, 171: 4, 172: 7, 173: 8, 174: 21, 175: 11, 176: 12}),
            ("IORE", {170: 75, 171: 76, 172: 123, 173: 122, 174: 124, 175: 74, 176: 104}),
            ("CORE", {170: 1, 171: 32, 172: 25, 173: 27, 174: 34, 175: 56, 176: 59}),
            ("AORE", {170: 42, 171: 123, 172: 74, 173: 125, 174: 162, 175: 126, 176: 78}),
            ("SAND", {170: 108, 171: 64, 172: 65, 173: 197, 174: 36, 175: 196, 176: 197}),
            ("COAL", {170: 1, 171: 1, 172: 2, 173: 2, 174: 3, 175: 4, 176: 5}),
            ("CLAY", {170: 57, 171: 57, 172: 57, 173: 77, 174: 78, 175: 78, 176: 79}),
            ("SCMT", {170: 104, 171: 3, 172: 2, 173: 70, 174: 71, 175: 72, 176: 3}),
            ("PHOS", {170: 63, 171: 64, 172: 192, 173: 65, 174: 193, 175: 64, 176: 194}))

piece_cargo_maps = ('WOOD', 'WDPR')
