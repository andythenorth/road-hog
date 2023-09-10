import argparse
import os.path
import codecs  # used for writing files - more unicode friendly than standard open() module
from polar_fox.utils import echo_message as echo_message
from polar_fox.utils import dos_palette_to_rgb as dos_palette_to_rgb
from polar_fox.utils import unescape_chameleon_output as unescape_chameleon_output
from polar_fox.utils import split_nml_string_lines as split_nml_string_lines
from polar_fox.utils import (
    unwrap_nml_string_declaration as unwrap_nml_string_declaration,
)


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


def get_makefile_args(sys):
    print(
        "get_makefile_args called - deprecated, update caller to use get_command_line_args"
    )
    # get args passed by makefile
    if len(sys.argv) > 1:
        makefile_args = {
            "repo_revision": sys.argv[1],
            "repo_version": 999, # ! shim
            "num_pool_workers": 0, # ! shim
            "roster": "*", # ! shim
        }
    else:  # provide some defaults so templates don't explode when testing python script without command line args
        makefile_args = {"repo_revision": 0, "repo_version": 0}
    return makefile_args


def parse_base_lang():
    # expose base lang strings to python - for reuse in docs
    base_lang_file = codecs.open(
        os.path.join("src", "lang", "english.lng"), "r", "utf8"
    )
    text = base_lang_file.readlines()
    # this is fragile, playing one line python is silly :)
    strings = dict(
        (line.split(":", 1)[0].strip(), line.split(":", 1)[1].strip())
        for line in text
        if ":" in line
    )
    return strings
