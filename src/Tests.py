import os
import sys
import TestEngine
import Common
import Repgrid
import random
from Data import Data
from Num import Num
from Sym import Sym
from Row import Row
from Cols import Cols
from Utils import rnd, canPrint, rand, set_seed, read_csv, cliffs_delta, selects, Rule, show_rule, bootstrap

command_line_args = []

##
# Imports sys, TestEngine, Common, Num from Num, Sym from Sym, rnd,
# canPrint, rand, set_seed, csv from Utils
#
# Checks if it's possible to print the value of the "the" field in the
# "cfg" dictionary in the "Common" module.
#
# Call the "canPrint" function with the "Common.cfg['the']" argument and
# the string "Should be able to print the". If the "canPrint" function
# executes without raising an exception, the "eg_the" function returns
# True, which represents that the test passed.
##
#@TestEngine.test
def eg_the():
    canPrint(Common.cfg['the'], 'Should be able to print the')
    return True

##
# Defines a test function named eg_sym using the @TestEngine.test
# decorator.
#
# Returns the result of the comparison between the calculated
# midpoint and 11/7 and the calculated variance and 0.787.
#
# The function creates an instance of the Sym class and adds
# some string values to it.
#
# The function then calculates the mode and entropy of the symbols and
# rounds the entropy value to 3 decimal places. It then prints the mode and
# entropy values in a formatted string.
#
# Returns true if the mode is "a" and the entropy value is 1.379.
##
#@TestEngine.test
def eg_sym():
    s = Sym()

    test_vals = ["a", "a", "a", "a", "b", "b", "c"]

    for x in test_vals:
        s.add(x)

    res = (1.379 == rnd(s.div(), 3))
    return res

##
# Defines a test function named eg_num using the @TestEngine.test
# decorator.
#
# Checks the Num class. It creates an instance of the Num class named n.
#
# It adds the elements of the list test_vals to the instance of Num using
# the add method.
#
# It calculates the midpoint (mean) and the variance of the elements added
# to the Num instance.
#
# It formats the midpoint, div values and the string "Should be
# able to print mid and div" into a single string and passes it to the
# function canPrint.
##
#@TestEngine.test
def eg_num():
    num1 = Num()
    num2 = Num()

    for i in range(10000):
        num1.add(rand())
    for i in range(10000):
        num2.add(pow(rand(), 2))

    mid = num1.mid()
    mid2 = num2.mid()
    return rnd(num1.mid(), 1) == 0.5 and num1.mid() > num2.mid()


def show_cluster(cluster_res, cols, n_places, level):
    if cluster_res != None:
        report_string = ('|.. '*level)

        data = cluster_res['data']

        if 'left' not in cluster_res:
            report_string+=  str(data.rows[-1].cells[-1])
        else:
            print_val = rnd(100 * cluster_res['c'])
            report_string+=  str(rnd(100 * cluster_res['c']))
        print(report_string)

        show_cluster(cluster_res['left'] if 'left' in cluster_res else None, cols, n_places, level + 1)
        show_cluster(cluster_res['right'] if 'right' in cluster_res else None, cols, n_places, level + 1)

def show_tree(tree, level = None):
    if tree != None:
        level = level if level != None else 0
        report_string = ('|.. '*level)
        data = tree['data']
        report_string+= str(len(data.rows))

        if level == 0 or 'left' not in tree:
            report_string+= '   ' + str(data.stats())
            
        print(report_string)
        show_tree(tree['left'] if 'left' in tree else None, level + 1)
        show_tree(tree['right'] if 'right' in tree else None, level + 1)

#@TestEngine.test 
def test_cliffs():
    if cliffs_delta([8,7,6,2,5,8,7,3],[8,7,6,2,5,8,7,3]) or not cliffs_delta([8,7,6,2,5,8,7,3],[9,9,7,8,10,9,6]):
        return False

    t1, t2 = [], []
    for i in range(1000):
        t1.append(rand())
        t2.append(pow(rand(), 0.5))
    
    if cliffs_delta(t1, t1) or not cliffs_delta(t1, t2):
        return False

    diff, j = False, 1.0
    while not diff:
        t3 = list(map(lambda x: x * j, t1))
        diff = cliffs_delta(t1, t3)
        print('> ' + str(rnd(j)) + ' ' + str(diff))
        j*= 1.025

    return True

#@TestEngine.test
def test_half():
    print('-----------------------------TESTING HALF-----------------------------')
    for source in os.listdir(os.path.join(os.path.dirname(__file__), '../etc/data')):
        data = Data('../etc/data/' + source)
        half_res = data.half()

        print('\n-----' + source + '------\n')
        print(str(len(half_res['left'])) + ", " + str(len(half_res['right'])))

        left, right = data.clone(half_res['left']), data.clone(half_res['right'])
        print(left.stats())
        print(right.stats())
        print('\n-----------\n')
    return True

#@TestEngine.test
def test_sway():
    print('-----------------------------TESTING SWAY-----------------------------')
    for source in os.listdir(os.path.join(os.path.dirname(__file__), '../etc/data')):
        data = Data('../etc/data/' + source)
        sway_res = data.sway()
        print('\n-----' + source + '------\n')
        print('all: ' + str(data.stats()))
        print('best: ' + str(sway_res['best'].stats()))
        print('rest: ' + str(sway_res['rest'].stats()))
        print('\n-----------\n')
    return True

#@TestEngine.test
def test_bin():
    print('-----------------------------TESTING BIN-----------------------------')
    for source in os.listdir(os.path.join(os.path.dirname(__file__), '../etc/data')):
        data = Data('../etc/data/' + source)
        sway_res = data.sway()
        print('\n-----' + source + '------\n')
        print('[all] best: ' + str(len(sway_res['best'].rows)) + ', rest: ' + str(len(sway_res['rest'].rows)))
        b4 = None
        for bin_res in data.bins(data.cols.x, {'best': sway_res['best'], 'rest': sway_res['rest']}):
            for range in bin_res:
                if range.txt != b4:
                    print('')
                b4 = range.txt
                has = range.sources.has
                best_ratio = (has['best'] if 'best' in has else 0) / range.sources.n
                print(range.txt + ', ' + str(range.lo) + ', ' + str(range.hi) + ', ' + str(rnd(best_ratio)) + ', ' + str(range.sources.has))
        print('\n-----------\n')

    return True

#@TestEngine.test
def test_resrvoir_sampling():
    current_max = Common.cfg['the']['Max']
    Common.cfg['the']['Max'] = 32

    num1 = Num()
    for i in range(10000):
        num1.add(i)


    Common.cfg['the']['Max'] = current_max #undo that change
    return len(num1.has) == 32


#@TestEngine.test
def test_xpln():
    print('-----------------------------TESTING XPLN-----------------------------')
    for source in os.listdir(os.path.join(os.path.dirname(__file__), '../etc/data')):
        data = Data('../etc/data/' + source)
        sway_res = data.sway()
        xpln_res = data.xpln({'best': sway_res['best'], 'rest': sway_res['rest']})

        print('\n-----' + source + '------\n')
        if xpln_res['rule'] != None:
            rule = xpln_res['rule']
            print('explain=' + str(show_rule(rule)))

            print('all               ' + str(data.stats("mid")) + ', ' + str(data.stats("div")))

            data1 = data.clone(selects(rule, data.rows))
            print('sway with ' + str(sway_res['evals']) + ' evals ' + str(sway_res['best'].stats("mid")) + ', ' + str(sway_res['best'].stats("div")))
            print('xpln on ' + str(sway_res['evals']) + ' evals   ' + str(data1.stats("mid")) + ', ' + str(data1.stats("div")))

            top = data.betters(len(sway_res['best'].rows))
            top_data = data.clone(top[0])
            print('sort with ' + str(len(data.rows)) + ' evals   ' + str(top_data.stats("mid")) + ', ' + str(top_data.stats("div")))

        print('\n-----------\n')
        

    return True

def condense_data(data_list):
    condensed_output = {}

    condensed_data = Data(data_list[0].cols.names)
    for data in data_list:
        for row in data.rows:
            condensed_data.add(row.cells)

    for y in condensed_data.cols.y:
        condensed_output[y.txt] = y.mid()
    
    return condensed_output
        

@TestEngine.test
def compare_methods():

    seeds = [937162211]
    for i in range(19):
        seeds.append(random.randrange(0, 937162211))

    for source in os.listdir(os.path.join(os.path.dirname(__file__), '../etc/data')):
        print('\n=================================' + source + '=================================')
        data = Data('../etc/data/' + source)

        outputs = {
            'all': [],
            'sway1': [],
            'xpln1': [],
            'sway2': [],
            'xpln2': [],
            'top': []
        }

        evals = {
            'all': 0,
            'sway1': 0,
            'xpln1': 0,
            'sway2': 0,
            'xpln2': 0,
            'top': 0
        }

        compare_pairs = [
            ['all', 'all'],
            ['all' ,'sway1'],
            ['all' ,'sway2'],
            ['sway1', 'sway2'],
            ['sway1', 'xpln1'], 
            ['sway2', 'xpln2'],
            ['sway1', 'top']
        ]

        i = 1
        while i <= 20: #do 20 runs, skipping invalid rule generations
            
            set_seed(seeds[i - 1]) #use the next random seed

            #sway1
            sway_res = data.sway()
            best = sway_res['best']
            rest = sway_res['rest']
            random_rest = random.sample(rest.rows, 3 * len(best.rows))

            #expln1
            xpln_res = data.xpln({'best': best, 'rest': rest.clone(random_rest)}, False)
            if(xpln_res['rule'] != None):
                outputs['all'].append(data)

                outputs['sway1'].append(best)
                evals['sway1']+= sway_res['evals']

                outputs['xpln1'].append(data.clone(selects(xpln_res['rule'], data.rows)))
                evals['xpln1']+= sway_res['evals']

                top_n_best = data.betters(len(best.rows))
                outputs['top'].append(data.clone(top_n_best[0]))
                evals['top']+= len(data.rows)
            else:
                continue       
                
   
            #sway2
            sway_res = data.sway2()
            best = sway_res['best']
            rest = sway_res['rest']
            random_rest = random.sample(rest.rows, 3 * len(best.rows))

            #expln2
            xpln_res = data.xpln2({'best': best, 'rest': rest.clone(random_rest)}, False)
            if(xpln_res['rule'] != None):
                outputs['sway2'].append(best)
                evals['sway2']+= sway_res['evals']

                outputs['xpln2'].append(data.clone(selects(xpln_res['rule'], data.rows))) 
                evals['xpln2']+= sway_res['evals']
            else:
                continue       
            
            i+= 1

        # print table 1
        #show the mean results over 20 repeated runs (with different random number seeds)
        header = ''.ljust(40)
        for y in data.cols.y:
            header+= y.txt.ljust(20)
        print(header + 'average eval count'.ljust(20))
        for name, data_list in outputs.items():
            algorithm_output = name.ljust(40)
            condensed_data = condense_data(data_list)
            for _, val in condensed_data.items():
                algorithm_output+= str(rnd(val, 1)).ljust(20)
            print(algorithm_output + str(rnd(evals[name] / 20, 1)))
        
        # print table 2
        # shows the CONJUNCTION of a effect size test and a significance test that compares 20 "all" results to 20 results from some other treatment
        print('\n' + header)
        for compare_pair in compare_pairs:
            compare_output = (compare_pair[0] + ' to ' + compare_pair[1]).ljust(40)
            results = {}
            blacklist = []
            for j in range(20):
                y_index = 0
                for y in outputs[compare_pair[0]][j].cols.y:
                    if y.txt in blacklist:
                        continue
                    to_compare = outputs[compare_pair[1]][j].cols.y[y_index]
                    bsres = bootstrap(y.has, to_compare.has)
                    cdres = cliffs_delta(y.has, to_compare.has)
                    res = bootstrap(y.has, to_compare.has) and cliffs_delta(y.has, to_compare.has)
                    if y.txt in results:
                        results[y.txt] = results[y.txt] and res
                    else:
                        results[y.txt] = res
                    y_index+= 1
                    if not results[y.txt]:
                        blacklist.append(y.txt)
            for key in results:
                compare_output+= '='.ljust(20) if results[key] else '≠'.ljust(20)
            print(compare_output)

    return True

##
# Defines a function ALL using @TestEngine.test. This function calls other
# functions, whose names start with eg_, stored in Common.eg, one by one,
# and prints their results. The function also keeps track of the number of
# failed tests in the Common.fails variable. The function returns True at
# the end.
##
@TestEngine.test
def ALL():
    for k in Common.eg:
        if k != "ALL":
            print('\n' + "---------------------------------------")
            if not TestEngine.runs(k):
                Common.fails += 1
    return Common.fails == 0

##
# Checks if the script is being run as the main program and if so, it calls
# the TestEngine.runs function with the value of the eg key of the
# dictionary of Common.cfg as its argument. After the call to TestEngine
# runs, the program exits with the value of Common.fails as the exit status
# code.
##
if __name__ == "__main__":
    TestEngine.runs(Common.cfg["the"]["eg"])
    sys.exit(Common.fails)