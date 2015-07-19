from roster import Roster

from vehicles import (acton,
                      amblecote,
                      beerwoods,
                      big_sky,
                      bottlebrook,
                      brass_monkey,
                      brigand,
                      brightling,
                      broadrock,
                      buildwas,
                      buff,
                      capo,
                      chainburn,
                      windergill,
                      towerhouse,
                      big_rigg,
                      cloud_hill,
                      coldfall,
                      crime_rigg,
                      easywheal,
                      fairlop,
                      #foreshore, # deprecated, pending decision on container trucks being in or out
                      fortiscue,
                      foxley,
                      glenmore,
                      goldmire,
                      gravelhead,
                      greenscoe,
                      griff,
                      highgate,
                      honister,
                      jinglepot,
                      knockdown,
                      ladycross,
                      leyburn,
                      limebreach,
                      littleduke,
                      mcdowell,
                      meriden,
                      merrivale,
                      nettlebridge,
                      newbold,
                      northbeach,
                      oylbarral,
                      oxleas,
                      pigstick,
                      powerstock,
                      quickset,
                      rattlebrook,
                      reaver,
                      ribble,
                      road_thief,
                      scrag_end,
                      scrooby_top,
                      shotover,
                      silvertop,
                      sparkford,
                      speedwell,
                      stancliffe,
                      steeraway,
                      stungun,
                      swineshead,
                      tallyho,
                      thunder,
                      thurlbear,
                      topley,
                      trefell,
                      trotalong,
                      twinhills,
                      waterperry,
                      witch_hill,
                      wookey,
                      yeoman)

roster = Roster(id = 'brit',
                numeric_id = 1,
                truck_speeds = {0: 20, 1900: 25, 1920: 40, 1940: 55, 1960: 70, 1980: 80},
                tram_speeds = {0: 25, 1900: 35, 1930: 45, 1960: 55, 1990: 65},
                vehicles = [leyburn,
                            thunder,
                            highgate,
                            topley,
                            glenmore,
                            oxleas,
                            acton,
                            big_sky,
                            tallyho,
                            brass_monkey,
                            goldmire,
                            littleduke,
                            jinglepot,
                            rattlebrook,
                            yeoman,
                            capo,
                            easywheal,
                            quickset,
                            speedwell,
                            chainburn,
                            windergill,
                            towerhouse,
                            big_rigg,
                            honister,
                            wookey,
                            powerstock,
                            greenscoe,
                            meriden,
                            cloud_hill,
                            limebreach,
                            ribble,
                            mcdowell,
                            pigstick,
                            swineshead,
                            stungun,
                            beerwoods,
                            waterperry,
                            silvertop,
                            merrivale,
                            fortiscue,
                            coldfall,
                            #foreshore, # deprecated, pending decision on container trucks being in or out
                            reaver,
                            crime_rigg,
                            brigand,
                            road_thief,
                            # trams
                            ladycross,
                            fairlop,
                            newbold,
                            northbeach,
                            twinhills,
                            foxley,
                            buildwas,
                            brightling,
                            amblecote,
                            scrooby_top,
                            nettlebridge,
                            oylbarral,
                            thurlbear,
                            scrag_end,
                            trotalong,
                            shotover,
                            bottlebrook,
                            sparkford,
                            stancliffe,
                            # off-highway
                            gravelhead,
                            broadrock,
                            witch_hill,
                            griff,
                            trefell,
                            knockdown,
                            buff,
                            steeraway])
