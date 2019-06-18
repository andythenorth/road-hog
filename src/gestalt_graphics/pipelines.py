import os.path
currentdir = os.curdir

from PIL import Image

import polar_fox
from polar_fox.graphics_units import SimpleRecolour, AppendToSpritesheet, AddCargoLabel, AddBuyMenuSprite
from polar_fox.pixa import Spritesheet, pixascan
from gestalt_graphics import graphics_constants

DOS_PALETTE = Image.open('palette_key.png').palette

"""
Pipelines can be dedicated to a single task such as simple recolouring
Or they can compose units for more complicated tasks, such as colouring and loading a specific vehicle type
As of Jan 2018 there is just one complex pipeline for vehicles, which handles body recolouring + optional cargo provision
"""


class Pipeline(object):
    def __init__(self):
        # this should be sparse, don't store any consist info in Pipelines, pass at render time
        # actually, there's nothing to do eh :P
        pass

    def make_spritesheet_from_image(self, input_image):
        spritesheet = Spritesheet(width=input_image.size[0], height=input_image.size[1] , palette=DOS_PALETTE)
        spritesheet.sprites.paste(input_image)
        return spritesheet

    @property
    def vehicle_source_input_path(self):
        # I considered having this return the Image, not just the path, but it's not saving much, and is less obvious what it does when used
        return os.path.join(currentdir, 'src', 'graphics', self.consist.roster_id, self.consist.id + '.png')

    @property
    def chassis_input_path(self):
        # convenience method to get the path for the chassis image
        return os.path.join(currentdir, 'src', 'graphics', 'chassis', self.vehicle_unit.chassis + '.png')

    @property
    def base_platform_input_path(self):
        # figure out if there is a base platform and if it provides sprites, if so return the path to spritesheet, otherwise None
        # can only be called if self.vehicle_unit is in scope (should be in valid cases)
        if self.vehicle_unit.base_platform is None:
            return None
        else:
            base_platform_spritesheet_name = self.vehicle_unit.base_platform.get_base_platform_spritesheet_name(self.consist)
            if base_platform_spritesheet_name is not None:
                return os.path.join(currentdir, 'src', 'graphics', 'base_platforms', base_platform_spritesheet_name + '.png')
            else:
                return None

    def get_arbitrary_angles(self, input_image, bounding_boxes):
        # given an image and a list of arbitrary bounding boxes...
        # ...return a list of two tuples with sprite and mask
        # this can then be used for compositing
        # note the arbitrary order of sprites which makes this very flexible
        result = []
        for bounding_box in bounding_boxes:
            sprite = input_image.copy()
            sprite = sprite.crop(bounding_box)
            mask = sprite.copy()
            # !! .point is noticeably slow although not signifcantly so with only 3 cargo types
            # !! check this again if optimisation is a concern - can cargos be processed once and passed to the pipeline?
            # !! as of Oct 2018, I tested commenting out *all* piece cargo processing, including calls to this method
            # !! that cut only 1s from an 11s graphics processing run on single CPU
            # !! so optimising this is TMWFTLB currently; instead simply using multiprocessing cuts graphics run to 2s
            mask = mask.point(lambda i: 0 if i == 0 else 255).convert("1")
            result.append((sprite, mask))
        return result

    def process_buy_menu_sprite(self, spritesheet):
        # this function is passed (uncalled) into the pipeline, and then called at render time
        # this is so that it has the processed spritesheet available, which is essential for creating buy menu sprites
        # n.b if buy menu sprite processing has conditions by vehicle type, could pass a dedicated function for each type of processing
        # these 'source' var names for images are misleading
        buy_menu_image = Image.new("P", (self.consist.buy_menu_width, self.global_constants.buy_menu_sprite_height), 0)
        buy_menu_image.putpalette(Image.open('palette_key.png').palette)

        # hard-coded positions for buy menu sprite (if used - it's optional)
        x_offset = 0
        for counter, unit in enumerate(self.consist.units):
            # !! currently no cap on purchase menu sprite width
            # !! consist has a buy_menu_width prop which caps to 64 which could be used (+1px overlap)

            # !! handle semitractors, where we need to crop the full vehicle, but the x-offset is the length of the cab
            if unit.unit_is_semi_tractor:
                unit_length_in_pixels = 6 * (unit.vehicle_length + unit.semi_truck_shift_offset_jank) # !! hax
                x_offset_increment = 6 * unit.vehicle_length # !! hax
            else:
                unit_length_in_pixels = 4 * unit.vehicle_length
                x_offset_increment = unit_length_in_pixels

            unit_spriterow_offset = unit.spriterow_num * graphics_constants.spriterow_height
            crop_box_src = (227,
                            10 + unit_spriterow_offset,
                            227 + unit_length_in_pixels + 1, # allow for 1px coupler / corrider overhang
                            26 + unit_spriterow_offset)
            crop_box_dest = (x_offset,
                             0,
                             x_offset + unit_length_in_pixels + 1, # allow for 1px coupler / corrider overhang
                             self.global_constants.buy_menu_sprite_height)
            custom_buy_menu_sprite = spritesheet.sprites.copy().crop(crop_box_src)
            # create a mask so that we paste only the vehicle pixels (no blue pixels)
            buy_menu_sprite_mask = custom_buy_menu_sprite.copy()
            buy_menu_sprite_mask = buy_menu_sprite_mask.point(lambda i: 0 if i == 0 else 255).convert("1") # the inversion here of blue and white looks a bit odd, but potato / potato
            buy_menu_image.paste(custom_buy_menu_sprite, crop_box_dest, buy_menu_sprite_mask)
            # increment x offset for pasting in next vehicle
            x_offset += x_offset_increment
        crop_box_dest = (self.consist.buy_menu_x_loc,
                         10,
                         self.consist.buy_menu_x_loc + buy_menu_image.size[0],
                         26)
        spritesheet.sprites.paste(buy_menu_image, crop_box_dest)
        return spritesheet

    def render_common(self, input_image, units):
        # expects to be passed a PIL Image object
        # units is a list of objects, with their config data already baked in (don't have to pass anything to units except the spritesheet)
        # each unit is then called in order, passing in and returning a pixa SpriteSheet
        # finally the spritesheet is saved
        output_path = os.path.join(currentdir, 'generated', 'graphics', self.consist.id + '.png')
        spritesheet = self.make_spritesheet_from_image(input_image)

        for unit in units:
            spritesheet = unit.render(spritesheet)
        # I don't normally leave commented-out code behind, but I'm bored of looking in the PIL docs for how to show the image during compile
        #spritesheet.sprites.show()
        spritesheet.save(output_path)

    def render(self, consist):
        raise NotImplementedError("Implement me in %s" % repr(self))


class PassThroughPipeline(Pipeline):
    """
    Solely opens the input image and saves it, this more of a theoretical case, there's no actual reason to use this.
    """
    def __init__(self):
        # this should be sparse, don't store any consist info in Pipelines, pass at render time
        super().__init__()

    def render(self, consist, global_constants):
        self.units = []
        self.consist = consist
        input_image = Image.open(self.vehicle_source_input_path)
        result = self.render_common(input_image, self.units)
        return result


class CheckBuyMenuOnlyPipeline(Pipeline):
    """
    Opens the input image, inserts a custom buy menu if required, then saves with no other changes.
    """
    def __init__(self):
        # this should be sparse, don't store any consist info in Pipelines, pass at render time
        super().__init__()

    def render(self, consist, global_constants):
        self.units = []
        self.consist = consist
        self.global_constants = global_constants

        if self.consist.buy_menu_x_loc == global_constants.custom_buy_menu_x_loc:
            # !! this currently will cause the vehicle spritesheet buy menu sprites to be copied to the pans spritesheet,
            # !! it needs pixels from the pans spritesheet, but automated buy menu sprites need providing first
            self.units.append(AddBuyMenuSprite(self.process_buy_menu_sprite))

        input_image = Image.open(self.vehicle_source_input_path)
        result = self.render_common(input_image, self.units)
        return result


class ExtendSpriterowsForCompositedSpritesPipeline(Pipeline):
    """"
        Extends a vehicle spritesheet with composited vehicle parts, cargo variations etc.
        In Road Hog, has to handle variations on single-unit trucks, wagon+drags, and trucks where some units don't show cargo (artics).
        There are various options that have to be set per truck to achieve the flexibility.
        Those are as minimal as possible, but unavoidable.
    """
    def __init__(self):
        # this should be sparse, don't store any consist info in Pipelines, pass at render time
        # initing things here is proven to have unexpected results, as the processor will be shared across multiple vehicles
        super().__init__()

    def comp_chassis_and_body(self, body_image):
        # chassis sprites also include cabs / locomotives as needed
        if self.vehicle_unit.chassis is None:
            return body_image

        crop_box_input_1 = (0,
                            10,
                            self.sprites_max_x_extent,
                            10 + graphics_constants.spriterow_height)
        chassis_image = Image.open(self.chassis_input_path).crop(crop_box_input_1)
        #chassis_image.show()

        # the body image has false colour pixels for the chassis, to aid drawing; remove these by converting to white, also convert any blue to white
        body_image = body_image.point(lambda i: 255 if (i in range(178, 192) or i == 0) else i)
        #body_image.show()

        # create a mask so that we paste only the vehicle pixels over the chassis (no blue pixels)
        body_mask = body_image.copy()
        body_mask = body_mask.point(lambda i: 0 if i == 255 else 255).convert("1") # the inversion here of blue and white looks a bit odd, but potato / potato

        #body_mask.show()
        crop_box_chassis_body_comp = (0,
                                 0,
                                 self.sprites_max_x_extent,
                                 0 + graphics_constants.spriterow_height)
        chassis_image.paste(body_image, crop_box_chassis_body_comp, body_mask)

        #chassis_image.show()
        return chassis_image

    def add_generic_spriterow(self):
        crop_box_source = (0,
                           self.vehicle_unit_source_row_yoffs,
                           self.sprites_max_x_extent,
                           self.vehicle_unit_source_row_yoffs + graphics_constants.spriterow_height)
        vehicle_generic_spriterow_input_image = self.comp_chassis_and_body(self.vehicle_unit_source_image.copy().crop(crop_box_source))
        # vehicle_generic_spriterow_input_image.show() # comment in to see the image when debugging
        vehicle_generic_spriterow_input_as_spritesheet = self.make_spritesheet_from_image(vehicle_generic_spriterow_input_image)
        crop_box_dest = (0,
                         0,
                         graphics_constants.spritesheet_width,
                         graphics_constants.spriterow_height)
        self.units.append(AppendToSpritesheet(vehicle_generic_spriterow_input_as_spritesheet, crop_box_dest))
        self.units.append(AddCargoLabel(label='EMPTY',
                                        x_offset=self.sprites_max_x_extent + 5,
                                        y_offset= -1 * graphics_constants.spriterow_height))

    def add_livery_only_spriterows(self, recolour_map):
        # this might be extensible for containers when needed, using simple conditionals
        # or because containers include random options it might need reworking,
        # to be more similar to piece cargo handling, but using recolour not actual sprites
        crop_box_source = (0,
                           self.vehicle_unit_source_row_yoffs,
                           self.sprites_max_x_extent,
                           self.vehicle_unit_source_row_yoffs + graphics_constants.spriterow_height)
        vehicle_livery_only_spriterow_input_image = self.comp_chassis_and_body(self.vehicle_unit_source_image.copy().crop(crop_box_source))
        # vehicle_generic_spriterow_input_image.show() # comment in to see the image when debugging
        vehicle_livery_only_spriterow_input_as_spritesheet = self.make_spritesheet_from_image(vehicle_livery_only_spriterow_input_image)

        for label, recolour_map in self.consist.gestalt_graphics.recolour_maps:
            crop_box_dest = (0,
                             0,
                             graphics_constants.spritesheet_width,
                             graphics_constants.spriterow_height)
            self.units.append(AppendToSpritesheet(vehicle_livery_only_spriterow_input_as_spritesheet, crop_box_dest))
            self.units.append(SimpleRecolour(recolour_map))
            self.units.append(AddCargoLabel(label=label,
                                            x_offset=self.sprites_max_x_extent + 5,
                                            y_offset= -1 * graphics_constants.spriterow_height))

    def add_bulk_cargo_spriterows(self):
        crop_box_source_1 = (0,
                             self.vehicle_unit_source_row_yoffs,
                             self.sprites_max_x_extent,
                             self.vehicle_unit_source_row_yoffs + graphics_constants.spriterow_height)
        crop_box_source_2 = (0,
                             self.vehicle_unit_source_row_yoffs + graphics_constants.spriterow_height,
                             self.sprites_max_x_extent,
                             self.vehicle_unit_source_row_yoffs + (2 * graphics_constants.spriterow_height))
        vehicle_bulk_cargo_input_image_1 = self.comp_chassis_and_body(self.consist_source_image.copy().crop(crop_box_source_1))
        vehicle_bulk_cargo_input_image_2 = self.comp_chassis_and_body(self.consist_source_image.copy().crop(crop_box_source_2))
        #vehicle_bulk_cargo_input_image.show() # comment in to see the image when debugging

        cargo_group_row_height = 2 * graphics_constants.spriterow_height
        bulk_cargo_rows_image = Image.new("P", (graphics_constants.spritesheet_width, cargo_group_row_height), 255)
        bulk_cargo_rows_image.putpalette(DOS_PALETTE)

        crop_box_comp_dest_1 = (0,
                                0,
                                self.sprites_max_x_extent,
                                graphics_constants.spriterow_height)
        crop_box_comp_dest_2 = (0,
                                graphics_constants.spriterow_height,
                                self.sprites_max_x_extent,
                                2 * graphics_constants.spriterow_height)

        # paste the empty state into two rows, then paste the cargo over those rows
        bulk_cargo_rows_image.paste(vehicle_bulk_cargo_input_image_1, crop_box_comp_dest_1)
        bulk_cargo_rows_image.paste(vehicle_bulk_cargo_input_image_2, crop_box_comp_dest_2)

        bulk_cargo_rows_image_as_spritesheet = self.make_spritesheet_from_image(bulk_cargo_rows_image)

        crop_box_dest = (0,
                         0,
                         self.sprites_max_x_extent,
                         cargo_group_row_height)

        for label, recolour_map in polar_fox.constants.bulk_cargo_recolour_maps:
            self.units.append(AppendToSpritesheet(bulk_cargo_rows_image_as_spritesheet, crop_box_dest))
            self.units.append(SimpleRecolour(recolour_map))
            self.units.append(AddCargoLabel(label=label,
                                            x_offset=self.sprites_max_x_extent + 5,
                                            y_offset=  -1 * cargo_group_row_height))

    def add_piece_cargo_spriterows(self):
        # !! this could possibly be optimised by slicing all the cargos once, globally, instead of per-unit
        cargo_group_output_row_height = 2 * graphics_constants.spriterow_height

        # Cargo spritesheets provide multiple lengths, using a specific format of rows
        # given a base set, find the bounding boxes for the rows per length
        cargo_spritesheet_bounding_boxes = {}
        for counter, length in enumerate([3, 4, 5, 6, 7, 8]):
            bb_result = []
            for y_offset in [0, 20]:
                bb_y_offset = (counter * 40) + y_offset
                bb_result.extend(tuple([(i[0], i[1] + bb_y_offset, i[2], i[3] + bb_y_offset) for i in polar_fox.constants.cargo_spritesheet_bounding_boxes_base]))
            cargo_spritesheet_bounding_boxes[length] = bb_result

        # Overview
        # 2 spriterows for the vehicle loading / loaded states, with pink loc points for cargo
        # a mask row for the vehicle, with pink mask area, which is converted to black and white mask image
        # an overlay for the vehicle, created from the vehicle empty state spriterow, and comped with the mask after each cargo has been placed
        # there is a case not handled, where long cargo sprites will cabbed vehicles in / direction with cab at N end, hard to solve
        crop_box_vehicle_cargo_loc_row = (0,
                                          self.vehicle_unit_source_row_yoffs,
                                          graphics_constants.spritesheet_width,
                                          self.vehicle_unit_source_row_yoffs + graphics_constants.spriterow_height)

        vehicle_cargo_loc_image = self.vehicle_unit_source_image.copy().crop(crop_box_vehicle_cargo_loc_row)
        # get the loc points
        loc_points = [pixel for pixel in pixascan(vehicle_cargo_loc_image) if pixel[2] == 226]
        # two cargo rows needed, so extend the loc points list
        loc_points.extend([(pixel[0], pixel[1] + 30, pixel[2]) for pixel in loc_points])
        # sort them in y order, this causes sprites to overlap correctly when there are multiple loc points for an angle
        loc_points = sorted(loc_points, key=lambda x: x[1])

        crop_box_vehicle_body = (0,
                                 self.empty_row_input_yoffs,
                                 self.sprites_max_x_extent,
                                 self.empty_row_input_yoffs + graphics_constants.spriterow_height)
        vehicle_base_image = self.comp_chassis_and_body(self.vehicle_unit_source_image.copy().crop(crop_box_vehicle_body))

        crop_box_mask_source = (0,
                                self.vehicle_unit_source_row_yoffs + graphics_constants.spriterow_height,
                                self.sprites_max_x_extent,
                                self.vehicle_unit_source_row_yoffs + (2 * graphics_constants.spriterow_height))
        crop_box_mask_dest = (0,
                              0,
                              self.sprites_max_x_extent,
                              graphics_constants.spriterow_height)
        # !! this will need a composited mask, combining the chassis mask with the body mask
        vehicle_mask_source = self.vehicle_unit_source_image.copy().crop(crop_box_mask_source).point(lambda i: 255 if i == 226 else 0).convert("1")
        vehicle_mask = Image.new("1", (self.sprites_max_x_extent, graphics_constants.spriterow_height), 0)
        vehicle_mask.paste(vehicle_mask_source, crop_box_mask_dest)
        #vehicle_mask.show()
        #mask and empty state will need pasting once for each of two cargo rows, so two crop boxes needed
        crop_box_comp_dest_1 = (0,
                                0,
                                self.sprites_max_x_extent,
                                graphics_constants.spriterow_height)
        crop_box_comp_dest_2 = (0,
                                graphics_constants.spriterow_height,
                                self.sprites_max_x_extent,
                                2 * graphics_constants.spriterow_height)

        piece_cargo_rows_image = Image.new("P", (graphics_constants.spritesheet_width, cargo_group_output_row_height))
        piece_cargo_rows_image.putpalette(DOS_PALETTE)
        # paste empty states in for the cargo rows (base image = empty state)
        piece_cargo_rows_image.paste(vehicle_base_image, crop_box_comp_dest_1)
        piece_cargo_rows_image.paste(vehicle_base_image, crop_box_comp_dest_2)
        #piece_cargo_rows_image.show()
        crop_box_dest = (0,
                         0,
                         self.sprites_max_x_extent,
                         cargo_group_output_row_height)

        # !! convert to use piece_vehicle_type_to_sprites_maps per Iron Horse ??
        for cargo_labels, cargo_filenames in self.consist.gestalt_graphics.piece_cargo_maps:
            for cargo_filename in cargo_filenames:
                # get a list, with a two-tuple (cargo_sprite, mask) for each of 4 angles
                # cargo sprites are assumed to be symmetrical, only 4 angles are needed
                # cargos with 8 angles (e.g. bulldozers) aren't handled here, assume heavy_items_cargo should handle those (might need extended)
                # loading states are first 4 sprites, loaded are second 4, all in one list, just pick them out as needed
                cargo_sprites_input_path = os.path.join(currentdir, 'src', 'polar_fox', 'cargo_graphics', cargo_filename + '.png')
                cargo_sprites_input_image = Image.open(cargo_sprites_input_path)
                cargo_sprites = self.get_arbitrary_angles(cargo_sprites_input_image, cargo_spritesheet_bounding_boxes[self.vehicle_unit.cargo_length])

                vehicle_comped_image = piece_cargo_rows_image.copy()

                for pixel in loc_points:
                    angle_num = 0
                    for counter, bbox in enumerate(self.global_constants.spritesheet_bounding_boxes):
                        if pixel[0] >= bbox[0]:
                            angle_num = counter
                    # clamp angle_num to 4, cargo sprites are symmetrical, only 4 angles provided
                    if angle_num > 3:
                        angle_num = angle_num % 4
                    cargo_sprite_num = angle_num
                    # loaded sprites are the second block of 4 in the cargo sprites list
                    if pixel[1] >= graphics_constants.spriterow_height:
                        cargo_sprite_num = cargo_sprite_num + 4
                    cargo_width = cargo_sprites[cargo_sprite_num][0].size[0]
                    cargo_height = cargo_sprites[cargo_sprite_num][0].size[1]
                    # the +1s for height adjust the crop box to include the loc point
                    # (needed beause loc points are left-bottom not left-top as per co-ordinate system, makes drawing loc points easier)
                    cargo_bounding_box = (pixel[0],
                                          pixel[1] - cargo_height + 1,
                                          pixel[0] + cargo_width,
                                          pixel[1] + 1)
                    vehicle_comped_image.paste(cargo_sprites[cargo_sprite_num][0], cargo_bounding_box, cargo_sprites[cargo_sprite_num][1])
                # vehicle overlay with mask - overlays any areas where cargo shouldn't show
                vehicle_comped_image.paste(vehicle_base_image, crop_box_comp_dest_1, vehicle_mask)
                vehicle_comped_image.paste(vehicle_base_image, crop_box_comp_dest_2, vehicle_mask)
                #vehicle_comped_image.show()
                vehicle_comped_image_as_spritesheet = self.make_spritesheet_from_image(vehicle_comped_image)
                self.units.append(AppendToSpritesheet(vehicle_comped_image_as_spritesheet, crop_box_dest))
                self.units.append(AddCargoLabel(label=cargo_filename,
                                                x_offset=self.sprites_max_x_extent + 5,
                                                y_offset= -1 * cargo_group_output_row_height))

    def render(self, consist, global_constants):
        self.units = [] # graphics units not same as consist units ! confusing overlap of terminology :(
        self.consist = consist
        self.global_constants = global_constants
        self.sprites_max_x_extent = self.global_constants.sprites_max_x_extent

        self.consist_source_image = Image.open(self.vehicle_source_input_path)

        # the consist_cumulative_source_spriterow_count updates per processed group of spriterows, and is key to making this work
        # !! source_spriterow_count looks a bit weird though; I tried moving it to gestalts, but didn't really work
        consist_cumulative_source_spriterow_count = 0
        for vehicle_counter, vehicle_rows in enumerate(consist.get_spriterows_for_consist_or_subpart(consist.unique_units)):
            # !! ^ this is ugly hax, I didn't want to refactor the iterator above to contain the vehicle, also in Horse
            # 'vehicle_unit' not 'unit' to avoid conflating with graphics processor 'unit'
            self.vehicle_unit = self.consist.unique_units[vehicle_counter]
            vehicle_unit_cumulative_source_spriterow_count = 0
            self.vehicle_unit_source_base_yoffs = 10 + (graphics_constants.spriterow_height * consist_cumulative_source_spriterow_count)
            if self.base_platform_input_path is not None:
                self.vehicle_unit_source_image = Image.open(self.base_platform_input_path)
            else:
                self.vehicle_unit_source_image = self.consist_source_image

            for spriterow_data in vehicle_rows:
                spriterow_type = spriterow_data[0]
                if self.base_platform_input_path is not None:
                    self.vehicle_unit_source_row_yoffs = 10 + (vehicle_unit_cumulative_source_spriterow_count * graphics_constants.spriterow_height)
                    self.empty_row_input_yoffs = 10
                else:
                    self.vehicle_unit_source_row_yoffs = 10 + (graphics_constants.spriterow_height * consist_cumulative_source_spriterow_count)
                    self.empty_row_input_yoffs = self.vehicle_unit_source_base_yoffs

                if spriterow_type == 'always_use_same_spriterow' or spriterow_type == 'empty':
                    source_spriterow_count = 1
                    self.add_generic_spriterow()
                elif spriterow_type == 'livery_only':
                    source_spriterow_count = 1
                    self.add_livery_only_spriterows(consist.gestalt_graphics.recolour_maps)
                elif spriterow_type == 'bulk_cargo':
                    source_spriterow_count = 2
                    self.add_bulk_cargo_spriterows()
                elif spriterow_type == 'piece_cargo':
                    source_spriterow_count = 2
                    self.add_piece_cargo_spriterows()
                consist_cumulative_source_spriterow_count += source_spriterow_count
                vehicle_unit_cumulative_source_spriterow_count += source_spriterow_count

        if self.consist.buy_menu_x_loc == global_constants.custom_buy_menu_x_loc:
            self.units.append(AddBuyMenuSprite(self.process_buy_menu_sprite))

        # for this pipeline, input_image is just blank white 10px high image, to which the vehicle sprites are then appended
        input_image = Image.new("P", (graphics_constants.spritesheet_width, 10), 255)
        input_image.putpalette(DOS_PALETTE)
        result = self.render_common(input_image, self.units)
        return result

def get_pipelines(pipeline_names):
    # add pipelines here when creating new ones
    # this is a bit hokey, there's probably a simpler way to do this but eh
    # looks like it could be replaced by a simple dict lookup directly from gestalt_graphics, but eh, I tried, it's faff
    pipelines = {"pass_through_pipeline": PassThroughPipeline,
                 "check_buy_menu_only": CheckBuyMenuOnlyPipeline,
                 "extend_spriterows_for_composited_sprites_pipeline": ExtendSpriterowsForCompositedSpritesPipeline}
    return [pipelines[pipeline_name]() for pipeline_name in pipeline_names]


def main():
    print("yeah, pipelines.main() does nothing")

if __name__ == '__main__':
    main()
