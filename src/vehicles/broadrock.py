import global_constants
import graphics_processor.utils as graphics_utils
from road_vehicle import EngineConsist, MiningHauler, GraphicsProcessorFactory

# !! experimental pixa support
# !! should this be per consist, or per unit?  It's one spritesheet per consist, so I'm thinking per-consist is more logical, but is it easiest?
# !! most of this should be per-vehicle, which is repetitious, but allows different models to be handled appropriately
# !! e.g. single-trailer trucks, multiple-trailer trucks, unitised trucks
# cargo rows 0 indexed - 0 = first set of loaded sprites
# GRVL is in first position as it is re-used for generic unknown cargos
# mining trucks *do* transport SCMT in this set, realism is not relevant here, went back and forth on this a few times :P
cargo_graphics_mappings = {'GRVL': [0], 'IORE': [1], 'CORE': [2], 'AORE': [3],
                   'SAND': [4], 'COAL': [5], 'CLAY': [6], 'SCMT': [7]}

def get_graphics_processors(template):
    recolour_maps = graphics_utils.get_bulk_cargo_recolour_maps()
    graphics_options_master = {'template': '',
                               'recolour_maps': (recolour_maps),
                               'copy_block_top_offset': 60,
                               'num_rows_per_unit': 2,
                               'num_unit_types': 1}

    graphics_options_1 = dict((k, v) for (k, v) in graphics_options_master.items())
    graphics_options_1['template'] = template
    graphics_options_2 = dict((k, v) for (k, v) in graphics_options_1.items())
    graphics_options_2['swap_company_colours'] = True
    graphics_processor_1 = GraphicsProcessorFactory('extend_spriterows_for_recoloured_cargos_pipeline', graphics_options_1)
    graphics_processor_2 = GraphicsProcessorFactory('extend_spriterows_for_recoloured_cargos_pipeline', graphics_options_2)
    return (graphics_processor_1, graphics_processor_2)

graphics_processor = get_graphics_processors('broadrock_template.png')[1]

consist = EngineConsist(id = 'broadrock',
              base_numeric_id = 100,
              title = 'Broadrock [Mining Truck]',
              replacement_id = '-none',
              power = 600,
              speed = 45,
              type_base_running_cost_points = 20, # dibble running costs for game balance
              vehicle_life = 40,
              intro_date = 1951)

consist.add_unit(MiningHauler(consist = consist,
                        weight = 35,
                        capacity = 0,
                        vehicle_length = 2,
                        semi_truck_shift_offset_jank = 3,
                        effects = ['EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, 1, 10', 'EFFECT_SPRITE_AIRCRAFT_BREAKDOWN_SMOKE, -2, -1, 10'],
                        spriterow_num = 0))

consist.add_unit(MiningHauler(consist = consist,
                        weight = 0, # put the weight on the truck to compensate for lack of TE when loaded
                        capacity = 85,
                        vehicle_length = 6,
                        spriterow_num = 1))

consist.add_model_variant(intro_date=0,
                       end_date=global_constants.max_game_date,
                       spritesheet_suffix=0,
                       graphics_processor=graphics_processor)
