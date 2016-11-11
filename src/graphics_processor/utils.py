from graphics_processor import graphics_constants
from graphics_processor import pipelines


class GraphicsProcessorFactory(object):
    # simple class which wraps graphics_processor, which uses pixa library
    # pipeline_name refers to a pipeline class which defines how the processing is done
    # may be reused across consists, so don't store consist info in the pipeline, pass it to pipeline at render time
    # this is kind of factory-pattern-ish, but don't make too much of that, it's not important
    def __init__(self, pipeline_name, options):
        self.pipeline_name = pipeline_name
        self.options = options
        self.pipeline = pipelines.get_pipeline(pipeline_name)


def get_composited_cargo_processors(template):
    # returns two cargo-compositing graphics processors, one of which flips company colours
    # also provides optional 2CC recolor
    graphics_options_1 = {'template': template, 'swap_company_colours': False}
    graphics_options_2 = {'template': template, 'swap_company_colours': True}
    graphics_processor_1 = GraphicsProcessorFactory('extend_spriterows_for_composited_cargos_pipeline', graphics_options_1)
    graphics_processor_2 = GraphicsProcessorFactory('extend_spriterows_for_composited_cargos_pipeline', graphics_options_2)
    return (graphics_processor_1, graphics_processor_2)
