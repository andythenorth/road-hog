import os.path
currentdir = os.curdir

from pixa import Spritesheet, pixascan
from PIL import Image

from graphics_processor import registered_pipelines
from graphics_processor import graphics_constants
from graphics_processor import utils as graphics_utils
from graphics_processor.units import SimpleRecolour, SwapCompanyColours, AppendToSpritesheet

DOS_PALETTE = Image.open('palette_key.png').palette

def register(pipeline):
    registered_pipelines[pipeline.name] = pipeline

"""
Pipelines can be dedicated to a single task such as SimpleRecolourPipeline
Or they can compose units for more complicated tasks, such as colouring and loading a specific vehicle type
"""


class Pipeline(object):
    def __init__(self, name):
        # this should be sparse, don't store any consist or variant info in Pipelines, pass them at render time
        self.name = name

    def make_spritesheet_from_image(self, input_image):
        spritesheet = Spritesheet(width=input_image.size[0], height=input_image.size[1] , palette=DOS_PALETTE)
        spritesheet.sprites.paste(input_image)
        return spritesheet

    def render_common(self, variant, consist, input_image, units, options):
        # expects to be passed a PIL Image object
        # options is a dict and can be used abitrarily to pass options wherever needed in the pipeline
        # units is a list of objects, with their config data already baked in (don't have to pass anything to units except the spritesheet)
        # each unit is then called in order, passing in and returning a pixa SpriteSheet
        # finally the spritesheet is saved
        output_path = os.path.join(currentdir, 'generated', 'graphics', variant.get_spritesheet_name(consist))
        spritesheet = self.make_spritesheet_from_image(input_image)

        for unit in units:
            spritesheet = unit.render(spritesheet)
        # I don't normally leave commented-out code behind, but I'm bored of looking in the PIL docs for how to show the image during compile
        #spritesheet.sprites.show()
        spritesheet.save(output_path)

    def render(self, variant, consist):
        raise NotImplementedError("Implement me in %s" % repr(self))

class PassThroughPipeline(Pipeline):
    def __init__(self):
        # this should be sparse, don't store any consist or variant info in Pipelines, pass them at render time
        super(PassThroughPipeline, self).__init__("pass_through_pipeline")

    def render(self, variant, consist):
        options = variant.graphics_processor.options
        input_path = os.path.join(currentdir, 'src', 'graphics', options['template'])
        input_image = Image.open(input_path)
        units = []
        result = self.render_common(variant, consist, input_image, units, options)
        return result

register(PassThroughPipeline())


class SimpleRecolourPipeline(Pipeline):
    """ Swaps colours using the recolour map (dict {colour index: replacement colour}) """
    def __init__(self):
        # this should be sparse, don't store any consist or variant info in Pipelines, pass them at render time
        super(SimpleRecolourPipeline, self).__init__("simple_recolour_pipeline")

    def render(self, variant, consist):
        options = variant.graphics_processor.options
        input_path = os.path.join(currentdir, 'src', 'graphics', options['template'])
        input_image = Image.open(input_path)
        units = [SimpleRecolour(options['recolour_map'])]
        result = self.render_common(variant, consist, input_image, units, options)
        return result

register(SimpleRecolourPipeline())


class SwapCompanyColoursPipeline(Pipeline):
    """ Swaps 1CC and 2CC colours """
    def __init__(self):
        # this should be sparse, don't store any consist or variant info in Pipelines, pass them at render time
        super(SwapCompanyColoursPipeline, self).__init__("swap_company_colours_pipeline")

    def render(self, variant, consist):
        options = variant.graphics_processor.options
        input_path = os.path.join(currentdir, 'src', 'graphics', options['template'])
        input_image = Image.open(input_path)
        units = [SwapCompanyColours()]
        result = self.render_common(variant, consist, input_image, units, options)
        return result

register(SwapCompanyColoursPipeline())


class ExtendSpriterowsForCompositedCargosPipeline(Pipeline):
    """"
        Extends a cargo carrier spritesheet with variations on cargo colours.
        Became convoluted - was copied from Iron Horse where the case is simple, always just 1 wagon.
        In Road Hog, has to handle variations on single-unit trucks, wagon+drags, and trucks where some units don't show cargo (artics).
        There are various options that have to be set per truck to achieve the flexibility.
        Those are as minimal as possible, but unavoidable.
    """
    def __init__(self):
        # this should be sparse, don't store any consist or variant info in Pipelines, pass them at render time
        super(ExtendSpriterowsForCompositedCargosPipeline, self).__init__("extend_spriterows_for_composited_cargos_pipeline")
        self.units = [] # graphics units not same as consist units ! confusing overlap of terminology :(

    def add_generic_spriterow(self):
        crop_box_source = (0,
                           self.base_offset,
                           graphics_constants.spritesheet_width,
                           graphics_constants.spriterow_height + self.base_offset)
        vehicle_generic_spriterow_input_image = Image.open(self.input_path).crop(crop_box_source)
        # vehicle_generic_spriterow_input_image.show() # comment in to see the image when debugging
        vehicle_generic_spriterow_input_as_spritesheet = self.make_spritesheet_from_image(vehicle_generic_spriterow_input_image)
        crop_box_dest = (0,
                         0,
                         graphics_constants.spritesheet_width,
                         graphics_constants.spriterow_height)
        self.units.append(AppendToSpritesheet(vehicle_generic_spriterow_input_as_spritesheet, crop_box_dest))

    def add_bulk_cargo_spriterows(self):
        crop_box_source = (0,
                           self.base_offset,
                           graphics_constants.spritesheet_width,
                           self.base_offset + self.unit_row_cluster_height)
        vehicle_bulk_cargo_state_input_image = Image.open(self.input_path).crop(crop_box_source)
        #vehicle_bulk_cargo_state_input_image.show() # comment in to see the image when debugging
        vehicle_bulk_cargo_state_input_as_spritesheet = self.make_spritesheet_from_image(vehicle_bulk_cargo_state_input_image)
        crop_box_dest = (0,
                         0,
                         graphics_constants.spritesheet_width,
                         self.unit_row_cluster_height)
        for bulk_cargo_recolour_map in graphics_constants.bulk_cargo_recolour_maps():
            self.units.append(AppendToSpritesheet(vehicle_bulk_cargo_state_input_as_spritesheet, crop_box_dest))
            self.units.append(SimpleRecolour(bulk_cargo_recolour_map))

    def add_piece_cargo_spriterows(self):
        crop_box_source = (0,
                           self.base_offset,
                           graphics_constants.spritesheet_width,
                           self.base_offset + self.unit_row_cluster_height)
        vehicle_bulk_cargo_state_input_image = Image.open(self.input_path).crop(crop_box_source)
        #vehicle_bulk_cargo_state_input_image.show() # comment in to see the image when debugging
        vehicle_bulk_cargo_state_input_as_spritesheet = self.make_spritesheet_from_image(vehicle_bulk_cargo_state_input_image)
        crop_box_dest = (0,
                         0,
                         graphics_constants.spritesheet_width,
                         self.unit_row_cluster_height)
        for bulk_cargo_recolour_map in graphics_constants.bulk_cargo_recolour_maps():
            self.units.append(AppendToSpritesheet(vehicle_bulk_cargo_state_input_as_spritesheet, crop_box_dest))
            self.units.append(SimpleRecolour(bulk_cargo_recolour_map))

    def render(self, variant, consist):
        # there are various options for controlling the crop box, I haven't documented them - read example uses to figure them out
        self.options = variant.graphics_processor.options
        self.input_path = os.path.join(currentdir, 'src', 'graphics', self.options['template'])

        # the cumulative_spriterow_count updates per processed group of spriterows, and is key to making this work
        cumulative_spriterow_count = 0
        for vehicle_counter, vehicle_rows in enumerate(consist.get_spriterows_for_consist_or_subpart(consist.unique_units)):
            for spriterow_type, spriterow_count in vehicle_rows:
                self.unit_row_cluster_height = spriterow_count * graphics_constants.spriterow_height
                self.base_offset = 10 + (graphics_constants.spriterow_height * cumulative_spriterow_count)
                if spriterow_type == 'always_use_same_spriterow' or spriterow_type == 'empty':
                    self.add_generic_spriterow()
                elif spriterow_type == 'bulk_cargo':
                    self.add_bulk_cargo_spriterows()
                elif spriterow_type == 'piece_cargo':
                    self.add_piece_cargo_spriterows()
                cumulative_spriterow_count += spriterow_count

        if self.options.get('swap_company_colours', False):
            units.append(SwapCompanyColours())
        input_image = Image.open(self.input_path).crop((0, 0, graphics_constants.spritesheet_width, 10))
        result = self.render_common(variant, consist, input_image, self.units, self.options)
        return result

register(ExtendSpriterowsForCompositedCargosPipeline())
