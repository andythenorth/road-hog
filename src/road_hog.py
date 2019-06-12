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

from vehicles import numeric_id_defender

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

def vacant_numeric_ids_formatted():
    # when adding vehicles it's useful to know what the next free numeric ID is
    # tidy-mind problem, but do we have any vacant numeric ID slots in the currently used range?
    # 'print' eh? - but it's fine echo_message isn't intended for this kind of info, don't bother changing
    max_id = max(numeric_id_defender) -  (max(numeric_id_defender) % 10)
    id_gaps = []
    for i in range(0, int(max_id/10)):
        id = i * 10
        if id not in numeric_id_defender:
            id_gaps.append(str(id))
    return "Vacant numeric ID slots: " + ', '.join(id_gaps) + (" and from " if len(id_gaps) > 0 else '') + str(max_id + 10) + " onwards"
