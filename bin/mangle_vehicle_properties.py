import os.path
currentdir = os.curdir

import sys
sys.path.append(os.path.join('src')) # add to the module search path

property_to_delete = 'buy_menu_width'
property_to_move = 'sea_capable'
property_to_insert_after = 'vehicle_life'
line_to_insert = "            gen=4,"

filenames = ['acton_pax_express.py', 'amblecote_box.py', 'applethwaite_fruit_veg.py', 'beerwoods_edibles_tanker.py', 'big_rigg_flat.py', 'big_sky_pax_express.py', 'boilingwell_tanker.py', 'bottlebrook_edibles_tanker.py', 'brass_monkey_mail.py', 'brigand_supplies.py', 'brightling_open.py', 'broadrock_dump.py', 'buff_log.py', 'buildwas_open.py', 'capo_open.py', 'catchcan_tanker.py', 'chainburn_flat.py', 'cloud_hill_tanker.py', 'colbiggan_box.py', 'coldfall_refrigerated.py', 'coleman_dump.py', 'cowsleigh_livestock.py', 'crime_rigg_supplies.py', 'drumbreck_tanker.py', 'easywheal_box.py', 'fairlop_pax.py', 'flow_edge_edibles_tanker.py', 'foreshore_intermodal.py', 'fortiscue_refrigerated.py', 'foxley_mail.py', 'glenmore_pax_express.py', 'goldmire_mail.py', 'gravelhead_dump.py', 'greenscoe_tanker.py', 'griff_log.py', 'hake_lake_dump.py', 'hawkmoor_dump.py', 'highgate_pax.py', 'honister_dump.py', 'jinglepot_open.py', 'knockdown_log.py', 'ladycross_pax.py', 'leyburn_pax.py', 'limebreach_covered_hopper.py', 'littleduke_mail.py', 'mcdowell_covered_hopper.py', 'meriden_tanker.py', 'merrivale_refrigerated.py', 'nettlebridge_dump.py', 'newbold_pax.py', 'northbeach_pax.py', 'nutbrook_fruit_veg.py', 'oxleas_pax_express.py', 'oylbarral_tanker.py', 'pigstick_livestock.py', 'plumley_fruit_veg.py', 'polangrain_covered_hopper.py', 'poptop_edibles_tanker.py', 'portland_open.py', 'powerstock_dump.py', 'quickset_box.py', 'rackwood_flat.py', 'rakeway_box.py', 'rattlebrook_open.py', 'reaver_supplies.py', 'ribble_covered_hopper.py', 'road_thief_supplies.py', 'runwell_box.py', 'scrag_end_livestock.py', 'scrooby_top_dump.py', 'shotover_livestock.py', 'silvertop_edibles_tanker.py', 'singing_river_mail.py', 'sparkford_refrigerated.py', 'speedwell_box.py', 'stagrun_mail.py', 'stakebeck_flat.py', 'stancliffe_flat.py', 'steeraway_metal.py', 'strongbox_mail.py', 'stungun_livestock.py', 'swineshead_livestock.py', 'tallyho_mail.py', 'thunder_pax.py', 'thurlbear_covered_hopper.py', 'tin_hatch_mail.py', 'topley_pax.py', 'towerhouse_flat.py', 'trefell_log.py', 'trotalong_livestock.py', 'twinhills_pax.py', 'wastelander_open.py', 'waterperry_edibles_tanker.py', 'windergill_flat.py', 'winterfold_refrigerated.py', 'witch_hill_dump.py', 'wookey_dump.py', 'yeoman_open.py']


def delete_property(filename):
    file = open(os.path.join('src','vehicles',filename),'r')
    content = file.readlines()

    for line in content:
        if property_to_delete in line:
            content.remove(line)

    file = open(os.path.join('src','vehicles',filename),'w')
    file.write(''.join(content))
    file.close


def move_property(filename):
    file = open(os.path.join('src','vehicles',filename),'r')
    content = file.readlines()

    for line in content:
        if property_to_move in line:
            cut_line = line
    content.remove(cut_line)
    for line in content:
        if property_to_insert_after in line:
            line_to_insert_after = line
    insert_position = content.index(line_to_insert_after)
    content.insert(insert_position+1, cut_line)

    file = open(os.path.join('src','vehicles',filename),'w')
    file.write(''.join(content))
    file.close

def insert_property(filename):
    file = open(os.path.join('src','vehicles',filename),'r')
    content = file.readlines()

    for line in content:
        if property_to_insert_after in line:
            line_to_insert_after = line
    insert_position = content.index(line_to_insert_after)
    content.insert(insert_position+1, line_to_insert)

    file = open(os.path.join('src','vehicles',filename),'w')
    file.write(''.join(content))
    file.close


for filename in filenames:
    #delete_property(filename)
    #move_property(filename)
    insert_property(filename)
