from roster import Roster

from vehicles import acton_pax_express
from vehicles import amblecote_box
from vehicles import applethwaite_fruit_veg
from vehicles import beerwoods_edibles_tanker
from vehicles import big_rigg_flat

# from vehicles import big_sky_pax_express, #deprecated
from vehicles import boilingwell_tanker
from vehicles import bottlebrook_edibles_tanker
from vehicles import brass_monkey_mail
from vehicles import brigand_supplies
from vehicles import brightling_open
from vehicles import broadrock_dump
from vehicles import buff_log
from vehicles import buildwas_open
from vehicles import capo_open
from vehicles import catchcan_tanker
from vehicles import cattlegrid_livestock
from vehicles import chainburn_flat
from vehicles import chophouse_livestock
from vehicles import cloud_hill_tanker
from vehicles import colbiggan_box
from vehicles import coldfall_refrigerated
from vehicles import coleman_dump
from vehicles import cowsleigh_livestock
from vehicles import crawshot_livestock
from vehicles import crime_rigg_supplies
from vehicles import dewsnap_fruit_veg
from vehicles import dinkum_open
from vehicles import dora_flat
from vehicles import dreadnought_box
from vehicles import drumbreck_tanker
from vehicles import dry_fork_tanker
from vehicles import dugout_dump
from vehicles import dumpling_dump
from vehicles import easdale_box
from vehicles import easywheal_box
from vehicles import eidsborg_dump
from vehicles import elterwater_box
from vehicles import fairlop_pax
from vehicles import flow_edge_edibles_tanker

# from vehicles import foreshore_intermodal # deprecated, pending decision on container trucks being in or out
from vehicles import fortiscue_refrigerated
from vehicles import foxley_mail
from vehicles import glenmore_pax_express
from vehicles import goldmire_mail

# from vehicles import gravelhead_dump
from vehicles import greenscoe_tanker
from vehicles import greenleaf_fruit_veg
from vehicles import hawkmoor_dump
from vehicles import highgate_pax
from vehicles import hogsback_livestock
from vehicles import honister_dump
from vehicles import hopping_pipe_tanker
from vehicles import imperial_open
from vehicles import ingleby_box
from vehicles import intake_open
from vehicles import irvine_tanker
from vehicles import jinglepot_open
from vehicles import jubilee_open
from vehicles import jumbo_dump
from vehicles import kedge_flat
from vehicles import knockdown_log
from vehicles import ladycross_pax
from vehicles import leyburn_pax
from vehicles import limebreach_covered_hopper
from vehicles import limpet_open
from vehicles import littleduke_mail
from vehicles import loggan_box
from vehicles import magee_dump
from vehicles import mcdowell_covered_hopper
from vehicles import meethball_livestock
from vehicles import meriden_tanker
from vehicles import merrivale_refrigerated
from vehicles import mullion_flat
from vehicles import nettlebridge_dump
from vehicles import newbiggin_flat
from vehicles import newbold_pax
from vehicles import northbeach_pax
from vehicles import nutbrook_fruit_veg
from vehicles import oxleas_pax_express
from vehicles import oylbarral_tanker
from vehicles import pigstick_livestock
from vehicles import pippin_fruit_veg
from vehicles import plumley_fruit_veg
from vehicles import polangrain_covered_hopper
from vehicles import poptop_edibles_tanker
from vehicles import portland_open
from vehicles import powerstock_dump
from vehicles import quickset_box
from vehicles import rackwood_flat
from vehicles import rakeway_box
from vehicles import rattlebrook_open
from vehicles import reaver_supplies
from vehicles import redbeet_fruit_veg
from vehicles import redoil_tanker
from vehicles import ribble_covered_hopper
from vehicles import road_thief_supplies
from vehicles import runwell_box
from vehicles import scrag_end_livestock
from vehicles import scrooby_top_dump
from vehicles import shotover_livestock
from vehicles import silvertop_edibles_tanker
from vehicles import singing_river_mail
from vehicles import sparkford_refrigerated
from vehicles import speedwell_box
from vehicles import spud_fruit_veg
from vehicles import stagrun_mail
from vehicles import stakebeck_flat
from vehicles import stancliffe_flat
from vehicles import stawell_flat
from vehicles import steeraway_metal
from vehicles import strongbox_mail
from vehicles import stungun_livestock
from vehicles import swineshead_livestock
from vehicles import tallyho_mail
from vehicles import tankard_tanker
from vehicles import thunder_pax
from vehicles import thurlbear_covered_hopper
from vehicles import tin_hatch_mail
from vehicles import topley_pax
from vehicles import towerhouse_flat
from vehicles import trefell_log
from vehicles import trotalong_livestock
from vehicles import twinhills_pax
from vehicles import waterperry_edibles_tanker
from vehicles import windergill_flat
from vehicles import winterfold_refrigerated
from vehicles import wookey_dump
from vehicles import yeoman_open


def main():
    return Roster(
        id="landrace",
        numeric_id=1,
        grf_name="road-hog",
        grfid=r"\97\87\EA\FF",
        str_grf_name="Road Hog",
        # note that the grf name is Road Hog, but we're in a multiple-grf compile with Road Hog and other grfs, where the word 'hog' is used in the compile also
        # so to avoid overloading 'hog', we use `landrace` as the id for Road Hog, this is easily find-and-replaced if we need to
        # default intro dates per generation, can be over-ridden if needed by setting intro_date kw on consist
        intro_dates={
            "ROAD": [
                1860,
                1920,
                1945,
                1970,
                1995,
                2020,
            ],  # gen 1 is long, then after 1920, quite aggressive 25 year gaps for trucks / buses
            "LOLZ": [1860, 1920, 1945, 1970, 1995, 2020],  # keep matched to ROAD
            "HEQS": [
                1925,
                1945,
                1965,
                1985,
                2015,
                2035,
            ],  # very aggressive 20 year gaps to reflect rapid development + overtake feldbahn
            "RAIL": [1860, 1900, 1930, 1960, 1990, 2020],
        },  # 30 year gaps for trams
        speeds={
            "ROAD": [25, 40, 55, 70, 80, 80],
            "LOLZ": [
                25,
                40,
                55,
                70,
                80,
                80,
            ],  # match to ROAD otherwise LOLZ vehicles cause road blocks
            "HEQS": [25, 30, 40, 50, 60, 60],
            "RAIL": [25, 35, 45, 55, 65, 65],
        },
        power_bands={
            "ROAD": [100, 150, 250, 450, 650, 750],
            "LOLZ": [100, 150, 250, 450, 650, 750],
            "HEQS": [100, 150, 250, 450, 650, 750],  # more likely to be over-ridden eh?
            "RAIL": [240, 480, 720, 960, 1200, 1440],
        },  # tram power is excessive compare to RL, otherwise the OpenTTD physics model spanks the trams
        # note that a few of these will only be used by singleton vehicles
        # but it's convenient to have one and only one standard way to do this (excepting local _capacity over-rides for joker cases)
        # !! might be better to do it per consist, and then divide that over vehicles in capacity(), with allocation of remainders
        unit_capacity_per_vehicle_type={
            "bus": [1, 44, 50, 60, 72],
            "coach": [1, 2, 30, 40, 40],
            "feldbahn": [16, 20, 20],
            "freight_tram": [
                16,
                30,
                36,
            ],  # num units varies between generations, so eh :x
            "freight_truck": [1, 12, 15, 20, 20, 20],
            "lolz": [1, 2, 3, 4, 5, 6],
            "mail_tram": [
                24,
                15,
                18,
                36,
                36,
            ],  # num units varies between generations, so eh :x
            "mail_truck": [1, 12, 15, 25, 25],
            "pax_tram": [20, 27, 50, 60, 70],
        },
        vehicles=[
            leyburn_pax,
            thunder_pax,
            highgate_pax,
            topley_pax,
            glenmore_pax_express,
            oxleas_pax_express,
            acton_pax_express,
            # big_sky, deprecated
            tallyho_mail,
            brass_monkey_mail,
            goldmire_mail,
            littleduke_mail,
            jinglepot_open,
            rattlebrook_open,
            yeoman_open,
            capo_open,
            runwell_box,
            easywheal_box,
            quickset_box,
            speedwell_box,
            chainburn_flat,
            windergill_flat,
            towerhouse_flat,
            big_rigg_flat,
            coleman_dump,
            honister_dump,
            wookey_dump,
            powerstock_dump,
            boilingwell_tanker,
            greenscoe_tanker,
            meriden_tanker,
            cloud_hill_tanker,
            limebreach_covered_hopper,
            ribble_covered_hopper,
            mcdowell_covered_hopper,
            cowsleigh_livestock,
            pigstick_livestock,
            swineshead_livestock,
            stungun_livestock,
            flow_edge_edibles_tanker,
            beerwoods_edibles_tanker,
            waterperry_edibles_tanker,
            silvertop_edibles_tanker,
            merrivale_refrigerated,
            fortiscue_refrigerated,
            coldfall_refrigerated,
            # foreshore, # deprecated, pending decision on container trucks being in or out
            reaver_supplies,
            crime_rigg_supplies,
            brigand_supplies,
            road_thief_supplies,
            # trams
            ladycross_pax,
            fairlop_pax,
            newbold_pax,
            northbeach_pax,
            twinhills_pax,
            tin_hatch_mail,
            foxley_mail,
            stagrun_mail,
            strongbox_mail,
            singing_river_mail,
            intake_open,
            jubilee_open,
            imperial_open,
            limpet_open,
            dinkum_open,
            buildwas_open,
            portland_open,
            brightling_open,
            easdale_box,
            ingleby_box,
            dreadnought_box,
            elterwater_box,
            loggan_box,
            amblecote_box,
            rakeway_box,
            colbiggan_box,
            mullion_flat,
            stawell_flat,
            newbiggin_flat,
            kedge_flat,
            dora_flat,
            stakebeck_flat,
            rackwood_flat,
            stancliffe_flat,
            dumpling_dump,
            dugout_dump,
            jumbo_dump,
            eidsborg_dump,
            magee_dump,
            scrooby_top_dump,
            hawkmoor_dump,
            nettlebridge_dump,
            tankard_tanker,
            hopping_pipe_tanker,
            irvine_tanker,
            dry_fork_tanker,
            redoil_tanker,
            drumbreck_tanker,
            catchcan_tanker,
            oylbarral_tanker,
            polangrain_covered_hopper,
            thurlbear_covered_hopper,
            crawshot_livestock,
            meethball_livestock,
            chophouse_livestock,
            hogsback_livestock,
            cattlegrid_livestock,
            scrag_end_livestock,
            trotalong_livestock,
            shotover_livestock,
            poptop_edibles_tanker,
            bottlebrook_edibles_tanker,
            winterfold_refrigerated,
            sparkford_refrigerated,
            dewsnap_fruit_veg,
            pippin_fruit_veg,
            spud_fruit_veg,
            redbeet_fruit_veg,
            greenleaf_fruit_veg,
            plumley_fruit_veg,
            applethwaite_fruit_veg,
            nutbrook_fruit_veg,
            # off-highway
            trefell_log,
            knockdown_log,
            buff_log,
            broadrock_dump,
            steeraway_metal,
        ],
    )
