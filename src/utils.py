import argparse
import os.path
import global_constants
from polar_fox import git_info
from polar_fox.utils import (
    echo_message,
    dos_palette_to_rgb,
    unescape_chameleon_output,
    split_nml_string_lines,
    unwrap_nml_string_declaration,
)
# expose properly to prevent pyflakes warnings
__all__ = [
    "echo_message",
    "dos_palette_to_rgb",
    "unescape_chameleon_output",
    "split_nml_string_lines",
    "unwrap_nml_string_declaration",
]


def get_command_line_args():
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "-pw",
        "--pool_workers",
        type=int,
        default=0,
        dest="num_pool_workers",
        help="The number of pool workers to use in multiprocessing pools [default: 0] (multiprocessing disabled unless explicitly enabled)",
    )
    argparser.add_argument(
        "-gn",
        "--grf-name",
        dest="grf_name",
        required=True,
        help="The grf to build",
        # manually extend the list if more rosters are added
        choices=["road-hog", "heqs", "id-report-only"],
    )
    argparser.add_argument(
        "-sc",
        "--suppress-cargo-sprites",
        action=argparse.BooleanOptionalAction,
        dest="suppress_cargo_sprites",
        help="Optionally suppress visible cargo sprites in the grf output, can save substantial compile time",
    )
    argparser.add_argument(
        "-sd",
        "--suppress-docs",
        action=argparse.BooleanOptionalAction,
        dest="suppress_docs",
        help="Optionally suppress docs, can save some compile time",
    )
    return argparser.parse_args()


def get_docs_url():
    # not convinced this belongs in utils, but I can't find anywhere better to put it
    # could be in polar fox - method will be common to all grfs? - pass the project name as a var?
    # not convinced it's big enough to bother centralising TBH, too much close coupling has costs
    result = [global_constants.metadata["docs_url"]]
    if git_info.get_tag_exact_match() != "undefined":
        result.append(git_info.get_monorepo_tag_parts()[1])
    result.append("index.html")
    return "/".join(result)


def parse_base_lang():
    # expose base lang strings to python - for reuse in docs
    base_lang_file = open(
        os.path.join("src", "lang", "english.lng"), "r", encoding="utf-8"
    )
    text = base_lang_file.readlines()
    # this is fragile, playing one line python is silly :)
    strings = dict(
        (line.split(":", 1)[0].strip(), line.split(":", 1)[1].strip())
        for line in text
        if ":" in line
    )
    return strings

# CABBAGE352 step 008a: IH unpack_colour
def unpack_colour(colour_name, cc_to_remap):
    # seems utils is the best place to keep this, but eh
    if "COLOUR_" in colour_name:
        # assume it's a default CC name constant
        if cc_to_remap == 1:
            return "palette_2cc(" + colour_name + ", company_colour2)"
        if cc_to_remap == 2:
            return "palette_2cc(company_colour1, " + colour_name + ")"
    else:
        # assume custom colour
        colour_name_offset = 2 * list(
            global_constants.custom_wagon_recolour_sprite_maps.keys()
        ).index(colour_name)
        remap_index = colour_name_offset + cc_to_remap - 1
        # return an nml fragment: custom_ship_recolour_sprites + index into recolour sprite + [company_colour1 or company_colour2]
        return (
            "custom_wagon_recolour_sprites + "
            + str(16 * remap_index)
            + " + company_colour"
            + str(1 if cc_to_remap == 2 else 2)
        )

def string_format_compile_time_deltas(time_start, time_later):
    return format((time_later - time_start), ".2f") + " s"


# move timing decorator to Polar Fox?
import time
import functools


def timing(func):
    """Decorator that reports the execution time of the wrapped function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result

    return wrapper


