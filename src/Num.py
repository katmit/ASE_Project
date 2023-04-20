import math

import Common

import numpy


import Sym

def random(lo = None, hi = None):
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

    seed = (16807 * Common.cfg['the']['seed']) % 2147483647
    return lo + (hi - lo) * seed / 2147483647

##
# Import the math class
#
# Defines a class "Num" which represents a stream of numbers. The class has
# methods to track mean, standard deviation, lowest, and
# highest numbers in the stream, and the number of items seen.
#
# The "add" method implements the reservoir sampling algorithm which is
# used to update the mean, standard deviation, etc...
# based on a new value "n".
#
# The "mid" method returns the mean of the numbers seen so
# far.
#
# The "div" method returns the standard deviation.
##
class Num():
    ##
    # Num summarizes a stream of numbers
    #
    # Defines the constructor method for the class initializes the instance
    # variables.
    #
    # num_items is set to 0, representing the number of items seen.
    #
    # mu and m2 are both set to 0.
    #
    # lo is set to math.inf, that is positive infinity. It tracks the lowest
    # number seen.
    #
    # hi is set to -math.inf, that is negative infinity. It tracks the
    # highest number seen.
    #
    # is_sorted is set to True, indicating that the data has not been
    # updated since the last sort.
    ##
    def __init__(self, col_position=0, col_name=""):
        self.at = col_position
        self.txt = col_name

        self.has = {}
        self.n = 0

        self.sources = Sym.Sym()

        self.lo = float('inf')
        self.hi = float('-inf')

        self.w = -1 if '-$' in col_name else 1



    ##
    # Reservoir sampler
    #
    # Defines the method named add that adds a float value n to the class.
    # If value is not equal to the placeholder, '?', the method updates the
    # values of the instance variables.
    #
    # num_items is incremented by 1 to represent an additional item seen.
    #
    # d is defined as the difference between the new value n and the mean
    # mu.
    #
    # mu is updated to be the running average of all values seen so
    # far, by adding the value d/num_items.
    #
    # m2 is updated to keep track of the sum of squares of deviations from
    # the mean, by adding the product of d and the difference between n and
    # the updated mean.
    #
    # lo is updated to be the minimum between the current value of lo and
    # the new value n.
    #
    # hi is updated to be the maximum between the current value of hi and
    # the new value n.
    ##
    # NUM's store the value in a finite sized cache. When it
    # fills to more than the.Max, then at probability 
    # the.Max/col.n replace any existing item
    # (selected at random). If anything is added, the list
    # may not longer be sorted so set `col.ok=false`.
    def add(self, value, source = None):
        if value != '?':
            capacity = Common.cfg['the']['Max']
            if self.n >= capacity:
                rand_value = random()
                random_victim = int(random(0, len(self.has.keys()))) if rand_value < capacity / self.n else None
                if random_victim != None: # make room
                    key = list(self.has.keys())[random_victim]
                    
                    self.n-= 1
                    if key == self.lo:
                        sorted_asc = sorted(self.has.keys())
                        self.lo = sorted_asc[0]
                    if key == self.hi:
                        sorted_asc = sorted(self.has.keys(), reverse=True)
                        self.hi = sorted_asc[0]
                    self.has[key]-= 1
                    
                    if self.has[key] <= 0:
                        self.has.pop(key)

                else: # if we didn't make room, just quit here
                    return 

            float_value = float(value)
            if float_value in self.has:
                self.has[float_value] = self.has[float_value] + 1
            else:
                self.has[float_value] = 1

            self.n+= 1
            self.lo = min(float_value, self.lo)
            self.hi = max(float_value, self.hi)

            self.sources.add(source)

    def set_lo(self, x: float):
        self.lo = x

    def set_hi(self, x: float):
        self.hi = x

    ##
    # Central tendency; for Nums, this is mean
    #
    # The mid method returns the current mean (average) of the data that
    # has been processed till now.
    ##
    def mid(self):  
        if self.n == 0:
            return 0
        total_sum = 0
        for key, value in self.has.items():
            total_sum+= key * value
        return total_sum / self.n


    ##
    # Diversity; for Nums, this is standard deviation using Welford's alg
    #
    # Calculates the standard deviation of the data processed so far.
    #
    # To calculate the standard deviation, the method first checks if
    # either self.m2 is negative or self.# num_items is less than 2. If
    # either of these conditions is true, the method returns 0.
    #
    # If both conditions are false, the method calculates the square root
    # of self.m2 (sum of the squares of the deviations from the mean
    # divided by self.num_items - 1 (number of items processed so far
    # - 1) using the math.pow function, and returns the result.
    ##
    def div(self):
        if len(self.has.keys()) < 2:
            return 0
        running_list = []
        for key, value in self.has.items():
            for i in range(value):
                running_list.append(key)
                
        res = (numpy.percentile(running_list, 90) - numpy.percentile(running_list, 10)) / 2.58
        return res
    ##
    # Checks if value is equal to "?". If it is, it returns value as is. If
    # not, it returns the rounded value to n decimal places using the
    # round function.
    ##
    def rnd(self, x, n):
        if x == "?":
            return x
        mult = math.pow(10, n)
        return math.floor(x*mult + 0.5) / mult

    ##
    # To normalize a numerical value "n" based on the "lo" and "hi" values
    # of an instance of the "NUM" class. We add "1E-32" to prevent a
    # division by zero.
    ##
    def norm(self, n):
        if n == "?":
            return n
        else:
            float_n = float(n)
            return (float_n - self.lo) / (self.hi - (self.lo + 1e-32))

    ##
    # Returns 1 if both n1 and n2 are equal to "?"
    #
    # If n1 is equal to "?", n1 is set to 1 if n2 is less than
    # 0.5 else 0
    #
    # If n2 is equal to "?", n2 is set to 1 if n1 is less than
    # 0.5 else 0
    #
    # Returns the absolute difference between the normalized values of n1
    # and n2 using the math.abs function.
    ##
    def dist(self, n1, n2):
        if n1 == "?" and n2 == "?":
            return 1

        n1, n2 = self.norm(n1), self.norm(n2)

        if n1 == "?":
            n1 = 1 if n2 < 0.5 else 0
        if n2 == "?":
            n2 = 1 if n1 < 0.5 else 0

        return abs(n1 - n2)

    def to_string(self) -> str:
        summary = '{NUM, at: ' + str(self.at) + ', hi: ' + str(self.hi) + ', lo: ' + str(self.lo) + ', n: ' + str(self.n) + ', txt: ' + self.txt + '}'
        return summary