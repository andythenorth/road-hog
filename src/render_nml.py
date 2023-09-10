import codecs  # used for writing files - more unicode friendly than standard open() module

import sys
import os

currentdir = os.curdir
from time import time

import road_hog
import utils
import global_constants
from polar_fox import git_info

# get args passed by makefile
command_line_args = utils.get_command_line_args()

# chameleon used in most template cases
from chameleon import PageTemplateLoader

# setup the places we look for templates
templates = PageTemplateLoader(os.path.join(currentdir, "src", "templates"))

# setting up a cache for compiled chameleon templates can significantly speed up template rendering
chameleon_cache_path = os.path.join(currentdir, global_constants.chameleon_cache_dir)
# exist_ok=True is used for case with parallel make (`make -j 2` or similar), don't fail with error if dir already exists
os.makedirs(chameleon_cache_path, exist_ok=True)
os.environ["CHAMELEON_CACHE"] = chameleon_cache_path

generated_files_path = road_hog.generated_files_path


def render_header_item_nml(header_item, roster, consists, graphics_path):
    template = templates[header_item + ".pynml"]
    return utils.unescape_chameleon_output(
        template(
            roster=roster,
            consists=consists,
            global_constants=global_constants,
            # temp_storage_ids=global_constants.temp_storage_ids,  # convenience measure # !! shimmed out
            utils=utils,
            # railtype_manager=road_hog.railtype_manager,# !! shimmed out
            # roster_manager=road_hog.roster_manager,# !! shimmed out
            graphics_path=graphics_path,
            git_info=git_info,
        )
    )


def render_item_nml(item, graphics_path):
    result = utils.unescape_chameleon_output(item.render(templates, graphics_path))
    # write the nml per item to disk, it aids debugging
    item_nml = codecs.open(
        os.path.join(generated_files_path, "nml", item.id + ".nml"), "w", "utf8"
    )
    item_nml.write(result)
    item_nml.close()
    # also return the nml directly for writing to the concatenated nml, don't faff around opening the generated nml files from disk
    return result


def main():
    print("[RENDER NML]", " ".join(sys.argv))
    start = time()
    road_hog.main()

    roster = road_hog.roster_manager.active_roster
    # expect Exception failures if there is no active roster, don't bother explicitly handling that case

    # we don't need to user os.path.join here, this is an nml path (and we want the explicit trailing slash also)
    graphics_path = "generated/graphics/" + roster.grf_name + "/"
    generated_nml_path = os.path.join(generated_files_path, "nml")
    # exist_ok=True is used for case with parallel make (`make -j 2` or similar), don't fail with error if dir already exists
    os.makedirs(generated_nml_path, exist_ok=True)
    grf_nml = codecs.open(
        os.path.join(generated_files_path, command_line_args.grf_name + ".nml"),
        "w",
        "utf8",
    )

    """
    spritelayer_cargos = road_hog.registered_spritelayer_cargos
    """
    consists = roster.consists_in_buy_menu_order

    header_items = ["header", "cargo_table", "roadtypes_tramtypes"]
    for header_item in header_items:
        grf_nml.write(
            render_header_item_nml(header_item, roster, consists, graphics_path)
        )

    # multiprocessing was tried here and removed as it was empirically slower in testing (due to overhead of starting extra pythons probably)
    """
    for spritelayercargo in spritelayer_cargos:
        grf_nml.write(render_item_nml(spritelayercargo, graphics_path))
    """

    # note to future self - if we introduce randomised vehicle selections, we might run out of action 2 IDs
    # - see Horse consists_in_order_optimised_for_action_2_ids if that happens, but as of September 2023 it's not a concern
    for consist in consists:
        grf_nml.write(render_item_nml(consist, graphics_path))

    grf_nml.close()

    print(
        "[RENDER NML]",
        command_line_args.grf_name,
        "- complete",
        format((time() - start), ".2f") + "s",
    )


if __name__ == "__main__":
    main()
