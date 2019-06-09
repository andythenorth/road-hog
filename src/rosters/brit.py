from roster import Roster

from vehicles import (acton_pax_express,
                      amblecote_box,
                      applethwaite_fruit_veg,
                      bahn_face_open,
                      bahn_steam_face_open,
                      beerwoods_edibles_tanker,
                      big_rigg_flat,
                      # big_sky_pax_express, #deprecated
                      boilingwell_tanker,
                      bottlebrook_edibles_tanker,
                      brass_monkey_mail,
                      brigand_supplies,
                      brightling_open,
                      broadrock_dump,
                      buff_log,
                      buildwas_open,
                      capo_open,
                      catchcan_tanker,
                      chainburn_flat,
                      cloud_hill_tanker,
                      colbiggan_box,
                      coldfall_refrigerated,
                      coleman_dump,
                      cowsleigh_livestock,
                      crime_rigg_supplies,
                      drumbreck_tanker,
                      easywheal_box,
                      fairlop_pax,
                      flow_edge_edibles_tanker,
#                      foreshore_intermodal, # deprecated, pending decision on container trucks being in or out
                      fortiscue_refrigerated,
                      foxley_mail,
                      glenmore_pax_express,
                      goldmire_mail,
#                      gravelhead_dump,
                      greenscoe_tanker,
                      hake_lake_dump,
                      hawkmoor_dump,
                      highgate_pax,
                      honister_dump,
                      jinglepot_open,
                      knockdown_log,
                      ladycross_pax,
                      leyburn_pax,
                      limebreach_covered_hopper,
                      littleduke_mail,
                      mcdowell_covered_hopper,
                      meriden_tanker,
                      merrivale_refrigerated,
                      nettlebridge_dump,
                      newbold_pax,
                      northbeach_pax,
                      nutbrook_fruit_veg,
                      oxleas_pax_express,
                      oylbarral_tanker,
                      pigstick_livestock,
                      plumley_fruit_veg,
                      polangrain_covered_hopper,
                      poptop_edibles_tanker,
                      portland_open,
                      powerstock_dump,
                      quickset_box,
                      rackwood_flat,
                      rakeway_box,
                      rattlebrook_open,
                      reaver_supplies,
                      ribble_covered_hopper,
                      road_thief_supplies,
                      runwell_box,
                      scrag_end_livestock,
                      scrooby_top_dump,
                      shotover_livestock,
                      silvertop_edibles_tanker,
                      singing_river_mail,
                      sparkford_refrigerated,
                      speedwell_box,
                      stagrun_mail,
                      stakebeck_flat,
                      stancliffe_flat,
                      steeraway_metal,
                      strongbox_mail,
                      stungun_livestock,
                      swineshead_livestock,
                      tallyho_mail,
                      thunder_pax,
                      thurlbear_covered_hopper,
                      tin_hatch_mail,
                      topley_pax,
                      towerhouse_flat,
                      trefell_log,
                      trotalong_livestock,
                      twinhills_pax,
                      waterperry_edibles_tanker,
                      windergill_flat,
                      winterfold_refrigerated,
                      witch_hill_dump,
                      wookey_dump,
                      yeoman_open)

roster = Roster(id = 'brit',
                numeric_id = 1,
                # default intro dates per generation, can be over-ridden if needed by setting intro_date kw on consist
                intro_dates = {'ROAD': [1860, 1920, 1945, 1970, 1995, 2020], # gen 1 is long, then after 1920, quite aggressive 25 year gaps for trucks / buses
                               'LOLZ': [1860, 1920, 1945, 1970, 1995, 2020], # keep matched to ROAD
                               'HEQS': [1925, 1945, 1965, 1985, 2015, 2035], # very aggressive 20 year gaps to reflect rapid development + overtake feldbahn
                               'RAIL': [1860, 1900, 1930, 1960, 1990, 2020], # 30 year gaps for trams
                               'HAKE': [1860, 1900, 1950, 2000]}, # only a few generations of feldbahn, then replaced by trucks
                speeds = {'ROAD': [25, 40, 55, 70, 80, 80],
                          'LOLZ': [25, 40, 55, 70, 80, 80], # match to ROAD otherwise LOLZ vehicles cause road blocks
                          'HEQS': [25, 30, 40, 50, 60, 60],
                          'RAIL': [25, 35, 45, 55, 65, 65],
                          'HAKE': [20, 30, 40, 40]}, # caps out at 40mph, replaced by HEQS later
                power_bands = {'ROAD': [100, 150, 250, 450, 650, 750],
                               'LOLZ': [100, 150, 250, 450, 650, 750],
                               'HEQS': [100, 150, 250, 450, 650, 750], # more likely to be over-ridden eh?
                               'RAIL': [240, 480, 720, 960, 1200, 1440], # tram power is excessive compare to RL, otherwise the OpenTTD physics model spanks the trams
                               'HAKE': [240, 480, 720, 960]},
                # note that a few of these will only be used by singleton vehicles
                # but it's convenient to have one and only one standard way to do this (excepting local _capacity over-rides for joker cases)
                # !! might be better to do it per consist, and then divide that over vehicles in capacity(), with allocation of remainders
                unit_capacity_per_vehicle_type = {'bus': [1, 44, 50, 60, 72],
                                                  'coach': [1, 2, 30, 40, 40],
                                                  'feldbahn': [1, 2, 3, 4, 5, 6],
                                                  'freight_tram': [16, 30, 36], # num units varies between generations, so eh :x
                                                  'freight_truck': [1, 12, 15, 20, 20, 20],
                                                  'lolz': [1, 2, 3, 4, 5, 6],
                                                  'mail_tram': [24, 15, 18, 36, 36], # num units varies between generations, so eh :x
                                                  'mail_truck': [1, 12, 15, 25, 25],
                                                  'pax_tram': [20, 27, 50, 60, 70]},
                vehicles = [leyburn_pax,
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
                            #foreshore, # deprecated, pending decision on container trucks being in or out
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
                            buildwas_open,
                            portland_open,
                            brightling_open,
                            amblecote_box,
                            rakeway_box,
                            colbiggan_box,
                            stakebeck_flat,
                            rackwood_flat,
                            stancliffe_flat,
                            scrooby_top_dump,
                            hawkmoor_dump,
                            nettlebridge_dump,
                            drumbreck_tanker,
                            catchcan_tanker,
                            oylbarral_tanker,
                            polangrain_covered_hopper,
                            thurlbear_covered_hopper,
                            scrag_end_livestock,
                            trotalong_livestock,
                            shotover_livestock,
                            poptop_edibles_tanker,
                            bottlebrook_edibles_tanker,
                            winterfold_refrigerated,
                            sparkford_refrigerated,
                            plumley_fruit_veg,
                            applethwaite_fruit_veg,
                            nutbrook_fruit_veg,
                            # feldbahn
                            bahn_steam_face_open,
                            bahn_face_open,
                            hake_lake_dump,
                            # off-highway
                            trefell_log,
                            knockdown_log,
                            buff_log,
                            broadrock_dump,
                            witch_hill_dump,
                            steeraway_metal])
