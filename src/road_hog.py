#!/usr/bin/env python

import os.path
currentdir = os.curdir

import sys
sys.path.append(os.path.join('src')) # add to the module search path

import global_constants
import utils

# setting up a cache for compiled chameleon templates can significantly speed up template rendering
chameleon_cache_path = os.path.join(currentdir, global_constants.chameleon_cache_dir)
if not os.path.exists(chameleon_cache_path):
    os.mkdir(chameleon_cache_path)
os.environ['CHAMELEON_CACHE'] = chameleon_cache_path

generated_files_path = os.path.join(currentdir, global_constants.generated_files_dir)
if not os.path.exists(generated_files_path):
    os.mkdir(generated_files_path)

# get args passed by makefile
if len(sys.argv) > 1:
    repo_vars = {'repo_title' : sys.argv[1], 'repo_version' : sys.argv[2]}
else: # provide some defaults so templates don't explode when testing python script without command line args
    repo_vars = {'repo_title' : 'FISH - compiled without makefile', 'repo_version' : 1}

print("[IMPORT VEHICLES] iron_horse.py")

from vehicles import registered_consists

from rosters import registered_rosters

# changing the order of rosters breaks savegames (parameter values change), don't do it.
from rosters import brit
#from rosters import wasteland

def get_consists_in_buy_menu_order(show_warnings=False):
    sorted_consists = []
    buy_menu_sort_order = []
    # first compose the buy menu order list
    for roster in registered_rosters:
        buy_menu_sort_order.extend(roster.buy_menu_sort_order)

        for id in buy_menu_sort_order:
            found = False
            for consist in registered_consists:
                if consist.id == id:
                    sorted_consists.append(consist)
                    found = True
            if show_warnings and not found:
                utils.echo_message("Warning: consist " + id + " in buy_menu_sort_order, but not found in registered_consists")

    # now guard against any consists missing from buy menu order, as that wastes time asking 'wtf?' when they don't appear in game
    for consist in registered_consists:
        id = consist.id
        if show_warnings and id not in buy_menu_sort_order:
            utils.echo_message("Warning: consist " + id + " in registered_consists, but not in buy_menu_sort_order - won't show in game")
    return sorted_consists
