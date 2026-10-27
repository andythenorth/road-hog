import polar_fox
import gestalt_graphics.graphics_constants as graphics_constants
from gestalt_graphics import pipelines
import utils


class GestaltGraphics(object):
    """
    Simple stub class, which is extended in sub-classes to configure:
     - base vehicle recolour (if any)
     - cargo graphics (if any)
    """

    def __init__(self):
        # by default, check for buy menu only
        self.pipelines = pipelines.get_pipelines(["check_buy_menu_only"])
        # sometimes processing may depend on another generated vehicle spritesheet, so there are multiple processing priorities, 1 = highest
        # see Horse for how this can be set to other values as needed
        self.processing_priority = 1

    def get_buy_menu_unit_input_row_num(self, pipeline, unit):
        return unit.spriterow_num

    def buy_menu_row_map(self, pipeline):
        # Iron Horse row-map contract, adapted to Road Hog's single purchase row.
        return [
            {
                "spriterow_num_dest": 0,
                "source_vehicles_and_input_spriterow_nums": [
                    (unit, self.get_buy_menu_unit_input_row_num(pipeline, unit))
                    for unit in pipeline.consist.units
                ],
            }
        ]

    @property
    def nml_template(self):
        # over-ride in sub-classes as needed
        return "vehicle_default.pynml"

    @property
    def num_cargo_sprite_variants(self, cargo_type=None):
        # rows can be reused across multiple cargo labels, so find uniques (assumes row nums are identical when reused across labels)
        unique_row_nums = []
        for row_nums in self.cargo_row_map.values():
            if row_nums not in unique_row_nums:
                unique_row_nums.append(row_nums)
        return sum([len(i) for i in unique_row_nums])


    def get_output_row_types(self):
        return ["single_row"]


    def get_spriterow_types_for_units(self, units):
        return [
            ["always_use_same_spriterow"]
            if unit.always_use_same_spriterow
            else self.get_output_row_types()
            for unit in units
        ]



class GestaltGraphicsPrecompositedCargo(GestaltGraphics):
    """
    Used for vehicle with visible cargos
    Supports *only* pixa-generated cargos; mixing with custom cargo rows isn't handled, TMWFTLB
    """

    def __init__(self, **kwargs):
        super().__init__()
        # as of Jan 2018 only one pipeline is used, but support is in place for alternative pipelines
        self.pipelines = pipelines.get_pipelines(
            ["extend_spriterows_for_composited_sprites_pipeline"]
        )
        # default body recolour to CC1, pass param to over-ride as needed
        self.body_recolour_map = kwargs.get(
            "body_recolour_map", graphics_constants.body_recolour_CC1
        )
        # cargo flags
        self.has_bulk = kwargs.get("bulk", False)
        self.has_piece = kwargs.get("piece", None) is not None
        if self.has_piece:
            self.piece_type = kwargs.get("piece")
        # required if piece is set, cargo sprites are available in multiple lengths, set the most appropriate
        self.cargo_length = kwargs.get("cargo_length", None)
        # State needed by the copied Iron Horse row-enumeration methods.
        self.covered_vehicle_body = kwargs.get("covered_vehicle_body", False)
        self.weathered_states = kwargs.get(
            "weathered_states", {"unweathered": self.body_recolour_map}
        )
        # CABBAGE: the Road Hog compositor does not yet emit covered or multiple weathering rows.
        if self.covered_vehicle_body:
            raise NotImplementedError(
                "Visible-cargo covered_vehicle_body requires compositor migration"
            )
        if len(self.weathered_states) != 1:
            raise NotImplementedError(
                "Visible-cargo multiple weathered_states require compositor migration"
            )

    def get_buy_menu_unit_input_row_num(self, pipeline, unit):
        # Output row ownership is defined by GestaltGraphics, not unit indices.
        return sum(
            self.get_output_row_count_for_unit(previous_unit)
            for previous_unit in pipeline.consist.units[: pipeline.consist.units.index(unit)]
        )

    @property
    def generic_rows(self):
        # map unknown cargos to sprites for some other label
        # assume that piece > input_spriterow_count, it's acceptable to show something like tarps for bulk, but not gravel for piece
        if self.has_piece:
            return self.cargo_row_map["DFLT"]
        elif self.has_bulk:
            return self.cargo_row_map["GRVL"]
        else:
            # shouldn't reach here, but eh,
            utils.echo_message("generic_rows hit an unknown result in GestaltGraphics")
            return [0]

    @property
    def nml_template(self):
        return "vehicle_with_precomposited_cargo.pynml"



    @property
    def cargo_row_map(self):
        result = {}
        counter = 0
        if self.has_bulk:
            for cargo_map in polar_fox.constants.bulk_cargo_recolour_maps:
                result[cargo_map[0]] = [counter]
                counter += 1
        if self.has_piece:
            for cargo_filename in polar_fox.constants.piece_vehicle_type_to_sprites_maps[
                self.piece_type
            ]:
                for cargo_label in polar_fox.constants.piece_sprites_to_cargo_labels_maps[
                    cargo_filename
                ]:
                    result.setdefault(cargo_label, []).append(counter)
                counter += 1
        return result


    def get_spriterow_types_for_units(self, units):
        result = []
        for unit in units:
            if unit.always_use_same_spriterow:
                # CABBAGE: Road Hog fixed-row articulated units have no equivalent
                # in the copied Iron Horse precomposited-cargo row-type contract.
                result.append(["always_use_same_spriterow"])
            else:
                result.append(self.get_output_row_types())
        return result

    def get_output_row_types(self):
        # note that this is *types* of rows, in order, not counts - counts are delegated elsehwere
        result = []
        # for e.g. tarpaulin cars, covered coil cars, insert a specific spriterow to show the cover when 100% loaded or travelling
        if self.covered_vehicle_body:
            result.append("covered_vehicle_body")
        # 1 empty spriterow
        result.append("empty_vehicle_body")
        if self.has_bulk:
            result.append("bulk_cargo")
        if self.has_piece:
            result.append("piece_cargo")
        return result

    def get_output_row_count_for_unit(self, unit):
        # Count the rows emitted by the current Road Hog compositor, using
        # the same row types that drive its dispatch.
        if unit.always_use_same_spriterow:
            return 1
        result = 0
        for row_type in self.get_output_row_types():
            if row_type == "empty_vehicle_body":
                result += 1
            elif row_type == "bulk_cargo":
                result += 2 * len(polar_fox.constants.bulk_cargo_recolour_maps)
            elif row_type == "piece_cargo":
                result += 2 * len(
                    polar_fox.constants.piece_vehicle_type_to_sprites_maps[
                        self.piece_type
                    ]
                )
            elif row_type == "covered_vehicle_body":
                # CABBAGE: Road Hog compositor has no covered-body row handler.
                # Preserve the current non-emitting behaviour until implemented.
                continue
            else:
                raise ValueError(f"Unknown visible-cargo row type: {row_type}")
        return result

    def get_unique_spritesets(self, unit):
        # the template for this gestalt was getting complex with loops and logic where logic shouldn't be
        # so instead we delegate that logic here and simplify the loop
        # this builds heavily on the row numbers already in cargo_row_map, reformatting that data to make it easy to render in the template
        row_nums_seen = []
        result = []
        for row_nums in self.cargo_row_map.values():
            for row_num in row_nums:
                row_nums_seen.append(row_num)
        unique_cargo_rows = sorted(set(row_nums_seen))

        row_height = graphics_constants.spriterow_height

        start_y_cumulative = graphics_constants.spritesheet_top_margin

        if self.covered_vehicle_body:
            # add rows for covered sprite
            for weathered_state in self.weathered_states.keys():
                result.append(["has_cover_" + weathered_state, start_y_cumulative])
                start_y_cumulative += row_height

        # add rows for empty sprite
        for weathered_state in self.weathered_states.keys():
            result.append(["empty_" + weathered_state, start_y_cumulative])
            start_y_cumulative += row_height

        for row_num in unique_cargo_rows:
            result.append(
                [
                    "loading_" + str(row_num),
                    start_y_cumulative,
                ]
            )
            result.append(
                [
                    "loaded_" + str(row_num),
                    start_y_cumulative + row_height,
                ]
            )
            start_y_cumulative += 2 * row_height

        # vehicles with multiple units might need an offset to their sprites
        # to handle that we post-process the y-offsets in result
        # we make an assumption that the spriterows will always be vertically contiguous
        # so we can take the last value of start_y_cumulative, apply the offset multiplier, then rewrite the y values in result
        # n.b. by default force_spriterow_group_in_output_spritesheet = 0, so this has no effect unless explicitly set
        vehicle_y_offset = unit.unit_def.force_spriterow_group_in_output_spritesheet * (
            start_y_cumulative - graphics_constants.spritesheet_top_margin
        )
        preceding_output_rows = 0
        for preceding_unit in unit.model_variant.units:
            if preceding_unit is unit:
                break
            preceding_output_rows += self.get_output_row_count_for_unit(
                preceding_unit
            )
        else:
            raise ValueError("Unit not found in model variant: " + unit.id)

        preceding_y_offset = preceding_output_rows * row_height
        if unit.always_use_same_spriterow:
            # The compositor emits one row for this unit, but the existing NML
            # switches still need empty/loading/loaded spriteset names.
            fixed_y = (
                graphics_constants.spritesheet_top_margin + preceding_y_offset
            )
            for row_map in result:
                row_map[1] = fixed_y
        else:
            for row_map in result:
                row_map[1] += preceding_y_offset + vehicle_y_offset
        return result


class GestaltGraphicsCustom(GestaltGraphics):
    # CABBAGE: Road Hog's custom gestalt/pipeline diverges from the newer Iron Horse implementation; consider unifying later.
    """
    This would be better deprecated, it's not really needed, all worthwhile cases can be met by generation.
    Used to handle (rare) cases with hand-drawn cargo (no pixa-generated cargos).
    There is currently no graphics processing for this:
    - just a simple pass-through, and an interface to the nml templates
    - this could get support for body recolouring if needed
    - this should not get support for compositing custom rows, TMWFTLB, just draw them in the vehicle spritesheet
    """
    # CABBAGE: Road Hog custom gestalt/pipeline diverges from newer Iron Horse; consider unifying later.

    def __init__(self, _cargo_row_map, _nml_template, generic_rows):
        super().__init__()
        # this attempts to use the buy menu generation pipeline, if that doesn't work, then it's probably time to sack off this gestalt type tbh
        self.pipelines = pipelines.get_pipelines(["check_buy_menu_only"])
        # options
        self._nml_template = _nml_template
        self._cargo_row_map = _cargo_row_map
        self._generic_rows = generic_rows

    @property
    def generic_rows(self):
        # generic rows is normally automated, but for custom, get it from a manully specified property
        return self._generic_rows

    @property
    def nml_template(self):
        return self._nml_template


    def get_output_row_types(self):
        return ["empty", "custom_cargo"]

    @property
    def cargo_row_map(self):
        return self._cargo_row_map

class GestaltGraphicsSimpleBodyColourRemaps(GestaltGraphics):
    # IH constructor interface; RH uses an existing compositor for the
    # single unweathered freight CC1 row. CC-ready passenger sprites need none.
    def __init__(self, recolour_map=None, weathered_states=None, catalogue_entry=None, **kwargs):
        super().__init__()
        self.catalogue_entry = catalogue_entry
        self.recolour_map = recolour_map
        self.weathered_states = weathered_states if weathered_states is not None else {"unweathered": recolour_map}
        if set(self.weathered_states) != {"unweathered"}:
            raise NotImplementedError("Road Hog only supports unweathered body recolouring")
        unweathered_map = self.weathered_states["unweathered"]
        if recolour_map is not None and unweathered_map != recolour_map:
            raise ValueError("recolour_map differs from unweathered weathered_states")
        if unweathered_map is not None:
            self.pipelines = pipelines.get_pipelines(
                ["extend_spriterows_for_composited_sprites_pipeline"]
            )
            # CABBAGE352: compositor calls this legacy output type livery_only.
            self.recolour_maps = [("DFLT", unweathered_map)]

    def get_output_row_types(self):
        if self.weathered_states["unweathered"] is not None:
            return ["livery_only"]
        return super().get_output_row_types()

    @property
    def nml_template(self):
        return "vehicle_with_simple_body_colour_remaps_road.pynml"
