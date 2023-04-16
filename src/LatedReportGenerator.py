import os
import sys
import TestEngine
import Common
import Repgrid

from Data import Data
from Num import Num
from Sym import Sym
from Row import Row
from Cols import Cols
from Utils import rnd, canPrint, rand, set_seed, read_csv, cliffs_delta, selects, Rule, show_rule


# discord chat ta said we need to use stats method to show better/equal/worse of sway1 vs sway2

results = {"all": [], "sway1": [], "xpln1": [], "sway2": [], "xpln2": [], "top": []}

for source in os.listdir(os.path.join(os.path.dirname(__file__), '../etc/data')):

    data = None

    # run every dataset for 20 runs
    for x in range(20):

            data = Data('../etc/data/' + source)

            results["all"].append(data)

            rule = None
            while rule == None:
                best, rest, _ = data.sway() #discord question mentions best having multiple returns and need to choose best one but don't  just avg bc pareto frontier

                # get xpln results
                rule, _ = data.xpln({'best': best, 'rest': rest})


            data1 = data.clone(selects(rule, data.rows))
            ##print('sway with ' + str(sway_res['evals']) + ' evals ' + str(sway_res['best'].stats("mid")) + ', ' + str(sway_res['best'].stats("div")))
            ##print('xpln on ' + str(sway_res['evals']) + ' evals   ' + str(data1.stats("mid")) + ', ' + str(data1.stats("div")))



            results["sway1"].append(best)
            results["xpln1"].append(data1)

            top = data.betters(len(best.rows))   #what is top is it just for sway or use both sway1 and sway2
            top_data = data.clone(top[0])

            results["top"].append(top_data)



            # SWAY2 + XPLN2

            rule = None
            while rule == None:
                best, rest, _ = data.sway2()  # discord question mentions best having multiple returns and need to choose best one but don't  just avg bc pareto frontier

                # get xpln results
                rule, _ = data.xpln2({'best': best, 'rest': rest})

            data1 = data.clone(selects(rule, data.rows))
            ##print('sway with ' + str(sway_res['evals']) + ' evals ' + str(sway_res['best'].stats("mid")) + ', ' + str(sway_res['best'].stats("div")))
            ##print('xpln on ' + str(sway_res['evals']) + ' evals   ' + str(data1.stats("mid")) + ', ' + str(data1.stats("div")))

            results["sway2"].append(best)
            results["xpln2"].append(data1)





















