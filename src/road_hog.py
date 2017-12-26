#!/usr/bin/env python

import os.path
currentdir = os.curdir

import sys
sys.path.append(os.path.join('src')) # add to the module search path

import global_constants
import utils
# get args passed by makefile
makefile_args = utils.get_makefile_args(sys)

# setting up a cache for compiled chameleon templates can significantly speed up template rendering
chameleon_cache_path = os.path.join(currentdir, global_constants.chameleon_cache_dir)
if not os.path.exists(chameleon_cache_path):
    os.mkdir(chameleon_cache_path)
os.environ['CHAMELEON_CACHE'] = chameleon_cache_path

generated_files_path = os.path.join(currentdir, global_constants.generated_files_dir)
if not os.path.exists(generated_files_path):
    os.mkdir(generated_files_path)

from rosters import registered_rosters

from rosters import brit
brit.roster.register()

#from rosters import test
#test.roster.register()

#from rosters import wasteland
#wasteland.roster.register()

def get_consists_in_buy_menu_order():
    consists = []
    # first compose the buy menu order list
    buy_menu_sort_order = []
    if makefile_args.get('roster', '*') == '*':
        active_rosters = [roster.id for roster in registered_rosters]
    else:
        active_rosters = [makefile_args['roster']] # make sure it's iterable
    for roster in registered_rosters:
        if roster.id in active_rosters:
            buy_menu_sort_order.extend(roster.buy_menu_sort_order)
            consists.extend(roster.consists_in_buy_menu_order)

    # now guard against any consists missing from buy menu order or vice versa, as that wastes time asking 'wtf?' when they don't appear in game
    consist_id_defender = set([consist.id for consist in consists])
    buy_menu_defender = set(buy_menu_sort_order)
    for id in buy_menu_defender.difference(consist_id_defender):
        utils.echo_message("Warning: consist " + id + " in buy_menu_sort_order, but not found in registered_consists")
    for id in consist_id_defender.difference(buy_menu_defender):
        utils.echo_message("Warning: consist " + id + " in consists, but not in buy_menu_sort_order - won't show in game")
    return consists
