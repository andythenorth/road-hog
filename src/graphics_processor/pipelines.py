import os.path
currentdir = os.curdir

from pixa import Spritesheet, pixascan
from PIL import Image

from graphics_processor import registered_pipelines
from graphics_processor import graphics_constants
from graphics_processor import utils as graphics_utils
from graphics_processor.units import SimpleRecolour, SwapCompanyColours, PasteAtMagicPixels, AppendToSpritesheet

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

    def render(self, variant, consist):
        # there are various options for controlling the crop box, I haven't documented them - read example uses to figure them out
        options = variant.graphics_processor.options
        input_path = os.path.join(currentdir, 'src', 'graphics', options['template'])
        units = [] # graphics units not same as consist units ! confusing overlap of terminology :(

        cumulative_spriterow_counts_by_vehicle = 0
        for vehicle_counter, vehicle_rows in enumerate(consist.get_spriterows_for_consist_or_subpart(consist.unique_units)):
            preceding_row_count_this_vehicle = 0
            for spriterow_type, spriterow_count in vehicle_rows:
                unit_row_cluster_height = spriterow_count * graphics_constants.spriterow_height
                if spriterow_type == 'always_use_same_spriterow':
                    base_offset = 10 + cumulative_spriterow_counts_by_vehicle
                    crop_box_source = (0,
                                       base_offset,
                                       graphics_constants.spritesheet_width,
                                       graphics_constants.spriterow_height + base_offset)
                    vehicle_always_use_same_spriterow_input_image = Image.open(input_path).crop(crop_box_source)
                    # vehicle_always_use_same_spriterow_input_image.show() # comment in to see the image when debugging
                    vehicle_always_use_same_spriterow_input_as_spritesheet = self.make_spritesheet_from_image(vehicle_always_use_same_spriterow_input_image)
                    crop_box_dest = (0,
                                     0,
                                     graphics_constants.spritesheet_width,
                                     graphics_constants.spriterow_height)
                    units.append(AppendToSpritesheet(vehicle_always_use_same_spriterow_input_as_spritesheet, crop_box_dest))

                if spriterow_type == 'empty':
                    base_offset = 10 + (30 * cumulative_spriterow_counts_by_vehicle)
                    crop_box_source = (0,
                                       base_offset,
                                       graphics_constants.spritesheet_width,
                                       graphics_constants.spriterow_height + base_offset)
                    vehicle_empty_state_input_image = Image.open(input_path).crop(crop_box_source)
                    #vehicle_empty_state_input_image.show() # comment in to see the image when debugging
                    vehicle_empty_state_input_as_spritesheet = self.make_spritesheet_from_image(vehicle_empty_state_input_image)
                    crop_box_dest = (0,
                                     0,
                                     graphics_constants.spritesheet_width,
                                     graphics_constants.spriterow_height)
                    units.append(AppendToSpritesheet(vehicle_empty_state_input_as_spritesheet, crop_box_dest))

                if spriterow_type == 'bulk':
                    base_offset = 10 + ((cumulative_spriterow_counts_by_vehicle + preceding_row_count_this_vehicle) * graphics_constants.spriterow_height)
                    crop_box_source = (0,
                                       base_offset,
                                       graphics_constants.spritesheet_width,
                                       base_offset + unit_row_cluster_height)
                    vehicle_bulk_cargo_state_input_image = Image.open(input_path).crop(crop_box_source)
                    #vehicle_bulk_cargo_state_input_image.show() # comment in to see the image when debugging
                    vehicle_bulk_cargo_state_input_as_spritesheet = self.make_spritesheet_from_image(vehicle_bulk_cargo_state_input_image)
                    crop_box_dest = (0,
                                     0,
                                     graphics_constants.spritesheet_width,
                                     unit_row_cluster_height)
                    for bulk_cargo_recolour_map in graphics_utils.get_bulk_cargo_recolour_maps():
                        units.append(AppendToSpritesheet(vehicle_bulk_cargo_state_input_as_spritesheet, crop_box_dest))
                        units.append(SimpleRecolour(bulk_cargo_recolour_map))

                preceding_row_count_this_vehicle += spriterow_count
            cumulative_spriterow_counts_by_vehicle += preceding_row_count_this_vehicle

        if options.get('swap_company_colours', False):
            units.append(SwapCompanyColours())
        input_image = Image.open(input_path).crop((0, 0, graphics_constants.spritesheet_width, 10))
        result = self.render_common(variant, consist, input_image, units, options)
        return result

register(ExtendSpriterowsForCompositedCargosPipeline())
