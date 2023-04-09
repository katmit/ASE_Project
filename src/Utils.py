from subprocess import call
import os
import csv
import random
import copy
import sys

import Common
import math
import yaml
from pathlib import Path

from Sym import Sym

##
# Imports call from subprocess, math, yaml and Path from pathlib
#
# Provides several functions and a class for test purposes. Includes
# functions for reading values from a YAML config file, generating
# pseudo-random numbers, type-casting strings to appropriate data types,
# reading CSV files, processing command-line arguments, etc. It also
# defines a custom exception class named "TestError" for raising exceptions
# in case of errors during tests.
##

##
# Retrieves the parent directory path of the current file and appends
# "config.yml" to it to create a config_path variable.
##
my_path = Path(__file__).resolve()  # resolve to get rid of any symlinks
config_path = my_path.parent / 'config.yml'

##
# Opens the file at that path and uses the yaml.safe_load method to parse
# the YAML data in the file into a Python object configs. passer is
# assigned an empty string value.
##
with config_path.open() as config_file:
    configs = yaml.safe_load(config_file)


passer = ""

##
# Defines a custom exception class named "TestError". The class has an
# __init__ method that takes a string argument mess and assigns it to an
# instance variable self.mess. This custom exception can be raised and
# caught in a try-except block to handle specific error conditions in a
# program.
##
class TestError(Exception):
    def __init__(self, mess):
        self.mess = mess

##
# Defines a function "canPrint" which takes two arguments "content" and
# "mess". The function first tries to print the "content". If there is an
# exception raised while trying to print "content", it will raise a custom
# exception "TestError" with the message specified in the argument "mess".
##
def canPrint(content, mess):
    try:
        print(content)
    except:
        raise TestError(mess)

##
# Takes a string as an argument and returns a Boolean indicating whether
# the string can be converted to a floating-point number or not. If the
# string can be converted, the function returns True. If not, the function
# returns False.
##
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

##
# Defines a function "rand" that generates a pseudo-random number within a
# specified range (lo and hi). The number is generated based on a given
# seed value stored in the "configs" dictionary, which is multiplied by
# 16807 and then taken modulo 2147483647 to get the next seed. The
# generated number is then calculated by adding "lo" to the result of (hi -
# lo) multiplied by the seed value divided by 2147483647.
##
def rand(lo = None, hi = None):
    """
    Generates a pseudo-random number using seed.
    :param lo: Lower limit of generated number
    :param hi: Higher limit of generated number
    :return: Pseudo-random number
    """
    if not lo:
        lo = 0

    if not hi:
        hi = 1

    configs['the']['seed'] = (16807 * configs['the']['seed']) % 2147483647
    return lo + (hi - lo) * configs['the']['seed'] / 2147483647

def get_rand_items(list, item_count: int):
    return random.sample(list, item_count)

##
# Defines a function "rnd" that takes a floating point number x and an
# argument places, which sets the number of decimal places for the rounded
# result.
#
# It calculates the rounded value by multiplying x with 10 raised to the
# power of places, adding 0.5 to it. Then, rounding down to the nearest
# integer (floor), and then dividing it by the same value of 10 raised to
# the power of places. The rounded value is returned as the final result.
##
def rnd(x, places=2):
    mult = 10 ** places
    return math.floor(x * mult + 0.5) / mult

##
# Defines a function coerce that takes a string input s and converts it to
# its equivalent data type (either integer, boolean or string).
#
# The function coerce first checks if the input string s is a number by
# calling the function is_number. If s is a number, the function coerce
# returns a float representation of s. If s is not a number, the function
# returns None or the result of function fun with s as the argument.
##
def coerce(s):
    ##
    # Convert input in the form of a string to appropriate data type int
    # bool/str
    #
    # The function fun takes a string s1 as input and returns a
    # boolean value if the string is equal to "true" or "false". If s1 is
    # neither of those values, fun returns s1.
    ##
    def fun(s1):
        # returns boolean for the string
        if s == "true":
            return True
        elif s == "false":
            return False
        return s1

    ##
    # Return integer of the number in the form of string or calls fun to
    # return appropriately
    ##
    if is_number(s):
        return float(s)
    else:
        return None or fun(s)

def kap(list, func):
    res = {}
    for i, item in enumerate(list):
        ret = func(item)
        res[item.txt] = ret[0]
    return res

#find x,y from a line connecting `a` to `b`
def cos(a, b, c):
    denominator = 1 if c == 0 else 2 * c
    x1 = (pow(a, 2) + pow(c, 2) - pow(b, 2)) / denominator
    x2 = max(0, min(1, x1))
    y = pow(abs((pow(a, 2) - pow(x2, 2))), 0.5)
    return {'x': x2, 'y': y}

##
# Call "fun" on each row. Row cells are divided in "the.seperator"
#
# Defines a function csv(fname, fun=None), which reads a CSV (Comma
# Separated Values) file specified by fname, typecasts every cell in each
# row to appropriate data type (int, bool or str) using the coerce()
# function, and applies the function fun to every row of the CSV file, if
# fun is specified.
#
# If fname is None or an empty string, an Exception is raised with message
# "File not found". The separator used to split a row is specified in
# Common.cfg['the']['separator']. The new line (\n) at the end of each row
# is removed before typecasting the cells.
##
def read_csv(fname, fun=None):
    if fname is None or len(fname.strip()) == 0:
        raise Exception("File not found")
    else:

        #try to catch relative paths
        if not os.path.isfile(fname):
            fname = os.path.join(os.path.dirname(__file__), fname)

        fname = os.path.abspath(fname)

        csv_list = []
        with open(fname, 'r') as csv_file:
            csv_list = list(csv.reader(csv_file, delimiter=','))
        
        if fun != None:
            for item in csv_list:
                fun(item)

##
# Function that processes command line arguments passed to the script. The
# function takes two arguments: args: A string of command line arguments
# separated by a space and configs: A dictionary that stores the
# configuration of the script.
#
# The function returns the updated configs dictionary
##
def cli(args, configs):
    arg_arr = args.split(" ")


    if '-e' in arg_arr:
        arg_arr.remove("-e")


    def find_arg_value(args: list[str], optionA: str, optionB: str, defaultValue) -> str:
        if optionA not in args and optionB not in args:
            return defaultValue
        index = args.index(optionA) if optionA in args else args.index(optionB)
        if (index + 1) < len(args):
            return args[index + 1]
        return None

    configs['the']['help'] = '-h' in args or '--help' in args
    configs['the']['go'] = '-g' in args or '--go' in args
    configs['the']['quit'] = '-q' in args or '--quit' in args
    configs['the']['bins'] = float(find_arg_value(arg_arr, '-b', '--bins', 16))
    configs['the']['file'] = find_arg_value(arg_arr, '-f', '--file', '../etc/data/auto93.csv')
    configs['the']['d'] = float(find_arg_value(arg_arr, '-d', '--d', 0.35))
    configs['the']['cliffs'] = float(find_arg_value(arg_arr, '-c', '--cliffs', 0.147))
    configs['the']['Far'] = float(find_arg_value(arg_arr, '-F', '--Far', 0.95))
    configs['the']['Halves'] = float(find_arg_value(arg_arr, '-H', '--Halves', 512))
    configs['the']['min'] = float(find_arg_value(arg_arr, '-m', '--min', 0.5))
    configs['the']['Max'] = int(find_arg_value(arg_arr, '-M', '--Max', 512))
    configs['the']['p'] = int(find_arg_value(arg_arr, '-p', '--p', 2))
    configs['the']['rest'] = int(find_arg_value(arg_arr, '-r', '--rest', 4))
    configs['the']['Reuse'] = bool(find_arg_value(arg_arr, '-R', '--Reuse', True))
    configs['the']['seed'] = float(find_arg_value(arg_arr, '-s', '--seed', 937162211))

    return configs

def many(list, count):
    return random.choices(list, k = int(count))

def cliffs_delta(nsA, nsB):
    if len(nsA) > 256:
        nsA = many(nsA, 256)
    if len(nsB) > 256:
        nsB = many(nsB, 256)
    if len(nsA) > 10 * len(nsB):
        nsA = many(nsA, 10 * len(nsB))
    if len(nsB) > 10 * len(nsA):
        nsB = many(nsB, 10 * len(nsA))

    n, gt, lt = 0, 0, 0
    for itemA in nsA:
        for itemB in nsB:
            n+= 1
            if itemA > itemB:
                gt+= 1
            if itemA < itemB:
                lt+= 1
    
    return (abs(lt - gt) / n) > Common.cfg['the']['cliffs']


def merge(col1, col2):# col is a num or a sym
    col1_copy = copy.deepcopy(col1)
    for item, count in col2.has.items():
        for i in range(count):
            col1_copy.add(item)
            
    for item, count in col2.sources.has.items():
        for i in range(count):
            col1_copy.sources.add(item)
    
    return col1_copy

# If (1) the parts are too small or
# (2) the whole is as good (or simpler) than the parts,
# then return the merge.
def merged(col1, col2, nSmall = None, nFar = None):
    merged = merge(col1, col2)
    
    if nSmall and col1.n < nSmall or col2.n < nSmall:
        return merged
    if nFar and type(col1) != Sym and abs(col1.mid() - col2.mid()) < nFar:
        return merged

    if merged.div() <= (((col1.div() * col1.n) + (col2.div() * col2.n)) / merged.n):
        return merged
    return None

# A representation of a Num or Sym without it's actual values represented. 
class Range():
    def __init__(self, at: int = 0, txt: str = "", lo: float = -math.inf, hi: float = math.inf):
        self.txt = txt
        self.lo = lo
        self.hi = hi
        self.at = at
        self.sources = {}


def merges(ranges0, nSmall, nFar): #ranges0: sorted lists of ranges (nums)

    def get_no_gaps_ranges(t):
        col_count = len(t)
        out_list = [Range() for i in range(col_count)]
        for j in range(col_count): # copy over the txt, high, and lo values
            out_list[j].txt = t[j].txt
            out_list[j].lo = t[j].lo
            out_list[j].hi = t[j].hi
            out_list[j].sources = t[j].sources

        for j in range(1, col_count): # shift things
            out_list[j].lo = t[j - 1].hi

        out_list[0].lo = -math.inf
        out_list[-1].hi = math.inf
        return out_list

    ranges1, j = [], 0
    while j < len(ranges0):
        left = ranges0[j]
        to_add = left
        right = ranges0[j + 1] if (j + 1) < len(ranges0) else None
        if right != None:
            y = merged(left.sources, right.sources, nSmall, nFar)
            if y != None:
                j+= 1
                to_add = merge(left, right)
                

        ranges1.append(to_add)
        j+= 1
    
    return get_no_gaps_ranges(ranges0) if len(ranges0) == len(ranges1) else merges(ranges1, nSmall, nFar)

##
# Function sets the value of seed in the dictionary configs['the'] to x.
# The configs dictionary holds the configuration data and the seed key in
# it holds the value for a seed used for generating random numbers. This
# function sets the value of seed to x.
##
def set_seed(x):
    configs['the']['seed'] = x

# A query that returns the score a distribution of symbols inside a SYM.
# Sorts the ranges (has) by how well the select for <best> using 
# (probability * support) = (b^2) / (b + r)
def value(has, sGoal: str, nB = 1, nR = 1):
    b = 0
    r = 0
    for x in has:
        goal_len = has[x]
        if x == sGoal:
            b+= goal_len
        else:
            r+= goal_len
    b = b / (nB + 1 / sys.float_info.max)
    r = r / (nR + 1 / sys.float_info.max) #handling zero divide errors
    return (b**2) / (b + r)

def selects(rule, rows):
    def disjunction(ranges, row):
        for range in ranges:
            lo = range['lo']
            hi = range['hi']
            at = range['at']
            x = row.cells[at]
            if x == '?':
                return True
            float_x = float(x)
            if(lo == hi and lo == float_x) or (lo <= float_x and float_x < hi):
                return True
        return False
    
    def conjunction(row):
        for i, ranges in rule.items():
            if ranges is None:
                continue
            if not disjunction(ranges, row):
                return False
        return True
    
    output = []
    for row in rows:
        if conjunction(row): #todo i am not sure if this is what his LUA code is doing (is it only returning ones where conjuction returns true?)
            output.append(row)
    return output
    



##
# Create a  RULE that groups `ranges` by their column id.
# Each group is a disjunction of its contents (and sets of groups are conjunctions).
#
# Takes a list of ranges, a maximum size maxSize, and returns a pruned version of the ranges based on
# their column id.
#
# Creates an empty dictionary t. For each range in the input list, checks if there is an existing key
# in the dictionary t corresponding to the column id (range.txt). If the key doesn't exist, a new empty
# list is created for that key. Range is then added to that list as a dictionary with keys 'lo', 'hi'
# and 'at'.
#
# Prune function is called with the dictionary, t and maximum siz, maxSize.
##
def Rule(ranges, maxSizes):
    t = {}
    for range in ranges:
        if range.txt not in t:
            t[range.txt] = []
        t[range.txt].append({'lo': range.lo, 'hi': range.hi, 'at': range.at})
    return prune(t, maxSizes)

##
# Takes a dictionary rule, a dictionary maxSize, and returns a pruned version of rule based on the
# values in maxSize.
#
# Initializes variable n to 0. For each key-value pair txt, ranges in input dictionary rule:
#   increment n by 1
#   length of ranges list = maxSize[txt], increments n by 1 again and set the key-value pair with
#   key txt from rule to nil/none.
#
# After processing all key-value pairs in rule, if:
#   n > 0, pruned rule is returned
#   n = 0, returns None
##
def prune(rule, maxSizes):
    n = 0
    for txt, ranges in rule.items():
        n += 1
        if len(ranges) == maxSizes[txt]:
            n += 1
            rule[txt] = None
    if n > 0:
        return rule
    
def first_N(sortedRangeItems, scoreFunction):
    print('\n')

    first = sortedRangeItems[0]['val']
    def useful(item):
        if item['val'] > 0.05 and item['val'] > (first / 10): 
            return item
        return None
        
    #iterate through sortedRanges, print each and determine which are "useful"
    useful_range_items = []
    for item in sortedRangeItems:
        print(item['range'].txt + ', ' + str(item['range'].lo) + ', ' + str(item['range'].hi) + ', ' +  str(rnd(item['val'])) + ', ' + str(item['range'].sources.has))
        if useful(item):
            useful_range_items.append(item['range'])
    
    most = -1
    out_rule = None

    print('\n')

    for n in range(len(useful_range_items)):
        subset = useful_range_items[0:(n + 1)]
        score_res = scoreFunction(subset)
        if score_res != None:
            if score_res['value'] > most:
                out_rule = score_res['rule']
                most = score_res['value']
    return {'rule': out_rule, 'most': most}

def show_rule(rule: Rule):
    def pretty(range):
        return range['lo'] if range['lo'] == range['hi'] else [range['lo'], range['hi']]
    
    def merge_rule(t0):
        t = []
        j = 0

        while j < len(t0):
            left = t0[j]
            right = t0[j + 1] if (j + 1) < len(t0) else None
            if right != None and left['hi'] == right['lo']:
                left['hi'] = right['hi']
                j+=1
            t.append({'lo': left['lo'], 'hi': left['hi']})
            j+=1
        return t if len(t0) == len(t) else merge_rule(t)

    def merges_rule(attr, ranges):
        merges_rule_out = {}
        if ranges == None:
            merges_rule_out[attr] = []
            return merges_rule_out
       
        sorted_ranges = sorted(ranges, key=lambda x: x['lo'])
        sorted_ranges = merge_rule(sorted_ranges)
        for range in sorted_ranges:
            merges_rule_out[attr] = pretty(range)
        return merges_rule_out
    
    out = []
    for attribute, items in rule.items():
        out.append(merges_rule(attribute, items))
    return out
