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
                      chainburn,
                      windergill,
                      towerhouse,
                      big_rigg,
                      coalhall,
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
                      oylbarral,
                      oxleas,
                      pigstick,
                      powerstock,
                      quickset,
                      reaver,
                      ribble,
                      road_thief,
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
                      twinhills,
                      waterperry,
                      witch_hill,
                      wookey)

roster = Roster(id = 'brit',
                numeric_id = 1,
                truck_speeds = {0: 20, 1900: 25, 1920: 40, 1940: 55, 1960: 70, 1980: 80},
                tram_speeds = {0: 20, 1895: 35, 1940: 50, 1980: 65},
                vehicles = [ladycross,
                            fairlop,
                            newbold,
                            twinhills,
                            leyburn,
                            thunder,
                            highgate,
                            topley,
                            glenmore,
                            oxleas,
                            acton,
                            big_sky,
                            foxley,
                            tallyho,
                            brass_monkey,
                            goldmire,
                            littleduke,
                            amblecote,
                            brightling,
                            jinglepot,
                            easywheal,
                            quickset,
                            speedwell,
                            chainburn,
                            windergill,
                            towerhouse,
                            big_rigg,
                            nettlebridge,
                            honister,
                            wookey,
                            powerstock,
                            oylbarral,
                            greenscoe,
                            meriden,
                            cloud_hill,
                            thurlbear,
                            limebreach,
                            ribble,
                            mcdowell,
                            shotover,
                            pigstick,
                            swineshead,
                            stungun,
                            bottlebrook,
                            beerwoods,
                            waterperry,
                            silvertop,
                            sparkford,
                            merrivale,
                            fortiscue,
                            coldfall,
                            #foreshore, # deprecated, pending decision on container trucks being in or out
                            reaver,
                            crime_rigg,
                            brigand,
                            road_thief,
                            stancliffe,
                            steeraway,
                            buildwas,
                            coalhall,
                            gravelhead,
                            broadrock,
                            witch_hill,
                            griff,
                            trefell,
                            knockdown,
                            buff])
