import numbers
import yaml
import math
import Common
import copy
import functools
import random

from typing import List, Union
from Cols import Cols
from Row import Row
from Sym import Sym
from Num import Num
from Utils import read_csv, rand, cos, many, kap, merges, value, selects, Rule, first_N, show_rule

with open("config.yml", 'r') as config_file:
    cfg = yaml.safe_load(config_file)


# Holds rows and their summaries in Cols.
class Data:
    def __init__(self, src):
        self.rows = []
        self.cols =  None
        self.src = src

        ## if the src is string then
        ## it reads the file and then calls the add method to add each row
        src_type = type(src)
        if src_type == str :
            read_csv(src, self.add)
        elif src_type == list: # else we were passed the columns as a string
            self.add(src)
        else:
            raise Exception("Unsupported type in Data constructor")

    def add(self, xs: list[str]):

        if not self.cols:
            self.cols = Cols(xs)
        else:
            new_row = Row(xs)
            self.rows.append(new_row)
            self.cols.add(new_row)


    def stats(self, what: str = None, cols: Union[Cols, None] = None, places: int = 2):
        def fun(col):
            whatFunc = getattr(col, what if what != None else "mid")
            return col.rnd(whatFunc(), places), col.txt

        res = kap(cols if cols != None else self.cols.y, fun)
        res['N'] = str(len(self.rows))
        return res

    def clone(self, rows: list[str] = None):
        if(rows == None):
            return copy.deepcopy(self)
        
        new_data = Data(self.cols.names)
        for item in rows:
            new_data.add(item.cells)

        return new_data
        

    ##
    # Defines a function "better" determines if row1 dominates row2 based
    # on a comparison method called "Zitzler04". The function takes three
    # arguments: i, row1, and row2.
    #
    # Initialized several variables: s1 and s2 to 0, ys to i.cols
    # y, x and y to undefined.
    ##
    def better(self, row1, row2):
        s1  = 0
        s2  = 0
        ys  = self.cols.y
    
        ##
        # Calculates the values of x and y by calling the norm method on
        # each element of ys and passing the corresponding cell value from
        # row1 and row2 respectively.
        #
        # s1 and s2 are then updated
        #
        # Returns true if row1 dominates row2 based on the comparison by
        # dividing s1 by the number of elements in ys and comparing it to
        # s2 by the number of elements in ys.
        ##
        for col in ys:
            x = col.norm(row1.cells[col.at])
            y = col.norm(row2.cells[col.at])
            s1 = s1 - math.exp(col.w * ((x-y)/len(ys)))
            s2 = s2 - math.exp(col.w * ((y-x)/len(ys)))

        return (s1/len(ys)) < (s2/len(ys))
    
    def betters(self, n = None):
        sorted_rows = sorted(self.rows, key=functools.cmp_to_key(self.better))
        if n  is None:
            return sorted_rows
        return [sorted_rows[0:n], sorted_rows[-n]]

    ##
    # Defines a function "dist" that calculates the distance between two
    # rows row1 and row2.
    #
    # col.dist calculates the distance between two values in a column.
    # row1.cells[col.at] and row2.cells[col.at] are the values in the
    # column col of row1 and row2 respectively.
    ##
    def dist(self, row1: Row, row2: Row, cols: Cols = None, n = 0, d = 0):
        if cols is None:
            cols = self.cols.x

        p =  Common.cfg['the']['p']
        for col in cols:
            n += 1
            d += pow(col.dist(row1.cells[col.at], row2.cells[col.at]), p)

        return pow(d / n, 1 /  p)



    ##
    # Defines a function "dist2" that calculates the distance between two
    # rows row1 and row2.
    #
    # col.dist calculates the distance between two values in a column.
    # row1.cells[col.at] and row2.cells[col.at] are the values in the
    # column col of row1 and row2 respectively.
    ##
    def dist2(self, row1: Row, row2: Row, cols: Cols = None, n = 0, d = 0):
        if cols is None:
            cols = self.cols.x

        p =  Common.cfg['the']['p']
        for col in cols:
            n += 1
            d += pow(col.dist(row1.cells[col.at], row2.cells[col.at]), p) #TODO change dist func, dist func for nums and syms are called as well

        return pow(d / n, 1 /  p)

    def around(self, rowA: Row, rows = None, cols = None):
        selected_rows = rows if rows != None else self.rows
        def distance(rowB):
            return {"row": rowB, "dist": self.dist(rowA, rowB, None)}

        sorted_rows = sorted(list(map(distance, selected_rows)), key=lambda x: x["dist"])

        return [ sub['row'] for sub in sorted_rows]


    def furthest(self, rowA, rows):
        t = self.around(rowA, rows)
        return t[-1]
    
    
    ##
    # Returns a tuple of two lists (left and right), two values (A and B)
    # mid row, mid and a number c.
    #
    # Sets the value of rows to self.rows if rows is not provided.
    # Calculates a sample of rows using the many function, and sets A to
    # the first element of the sample or the value of above if provided. B
    # is set to the row from self.around(A, some) that has the largest
    # distance from A.
    #
    # Calculates the value of c as the distance between A and B, and
    # initializes the lists left and right as empty.
    #
    # Sorts the rows by the result of the project function applied to each
    # row and maps it to a list of dictionaries containing the row and its
    # corresponding distance from A and B. The function then iterates over
    # this sorted list, adds each row to either left or right based on its
    # index, and sets mid to the row in the middle.
    ##
    def half(self, cols: Cols = None, above: Row = None, rows = None):

        def gap(r1, r2):
            return self.dist(r1, r2, cols)
        
        def project(row: Row):
            projection = cos(self.dist(row, A, cols), self.dist(row, B, cols), c)
            row.x = row.x if row.x != None else float(projection['x'])
            row.y = row.y if row.y != None else float(projection['y'])
            projection["row"] = row
            return projection
        
         #sort by distance from row
        def around(row, rows):
            return sorted(rows, key=lambda x: gap(x, row))

        def far(row, rows):
            around_res = around(row, rows)
            return around_res[int((len(rows) * Common.cfg['the']['Far']))]
        
    
        selected_rows = rows if rows != None else self.rows
        some = many(selected_rows, Common.cfg['the']['Halves'])
        
        A = above if (above != None and Common.cfg['the']['Reuse']) else far(selected_rows[int(rand(0, len(selected_rows)))], some)

        B = far(A, some)

        c = gap(A, B)
        

        sorted_projections = sorted(list(map(project, selected_rows)), key=lambda x: x["x"])

        left = []
        right = []
        mid = {}
        for i, item in enumerate(sorted_projections):
            if i < len(selected_rows) / 2:
                left.append(item['row'])
                mid = item['row']
            else:
                right.append(item['row'])

        evals = 1 if above and Common.cfg['the']['Reuse'] else 2
        return {
                'left': left,
                'right': right,
                'A': A,
                'B': B,
                'mid': mid,
                'c': c,
                'evals': evals
                }

    ##
    # Returns a tuple of two lists (left and right), two values (A and B)
    # mid row, mid and a number c.
    #
    # Sets the value of rows to self.rows if rows is not provided.
    # Calculates a sample of rows using the many function, and sets A to
    # the first element of the sample or the value of above if provided. B
    # is set to the row from self.around(A, some) that has the largest
    # distance from A.
    #
    # Calculates the value of c as the distance between A and B, and
    # initializes the lists left and right as empty.
    #
    # Sorts the rows by the result of the project function applied to each
    # row and maps it to a list of dictionaries containing the row and its
    # corresponding distance from A and B. The function then iterates over
    # this sorted list, adds each row to either left or right based on its
    # index, and sets mid to the row in the middle. Uses distance metric dist2.
    ##
    def half2(self, cols: Cols = None, above: Row = None, rows=None):

        def gap(r1, r2):
            return self.dist2(r1, r2, cols)

        def project(row: Row):
            projection = cos(self.dist2(row, A, cols), self.dist2(row, B, cols), c)
            row.x = row.x if row.x != None else float(projection['x'])
            row.y = row.y if row.y != None else float(projection['y'])
            projection["row"] = row
            return projection

        # sort by distance from row
        def around(row, rows):
            return sorted(rows, key=lambda x: gap(x, row))

        def far(row, rows):
            around_res = around(row, rows)
            return around_res[int((len(rows) * Common.cfg['the']['Far']))]

        selected_rows = rows if rows != None else self.rows
        some = many(selected_rows, Common.cfg['the']['Halves'])

        A = above if (above != None and Common.cfg['the']['Reuse']) else far(
            selected_rows[int(rand(0, len(selected_rows)))], some)

        B = far(A, some)

        c = gap(A, B)

        sorted_projections = sorted(list(map(project, selected_rows)), key=lambda x: x["x"])

        left = []
        right = []
        mid = {}
        for i, item in enumerate(sorted_projections):
            if i < len(selected_rows) / 2:
                left.append(item['row'])
                mid = item['row']
            else:
                right.append(item['row'])

        evals = 1 if above and Common.cfg['the']['Reuse'] else 2
        return {
            'left': left,
            'right': right,
            'A': A,
            'B': B,
            'mid': mid,
            'c': c,
            'evals': evals
        }






    
    def cluster(self,rows = None, cols = None, above = None):
        selected_rows = rows if rows != None else self.rows
        selected_cols = cols if cols != None else self.cols.x
        
        node = {'data': self.clone(selected_rows)}
        if len(selected_rows) >= 2:
            half_res = self.half(selected_cols, above, selected_rows)
            node['A'] = half_res['A']
            node['B'] = half_res['B']
            node['mid'] = half_res['mid']
            node['c'] = half_res['c']
            node['left'] = self.cluster(half_res['left'], selected_cols, half_res['A'])
            node['right'] = self.cluster(half_res['right'], selected_cols, half_res['B'])
        
        
        return node

    # Recursively prune the worst half the data. Return the survivors and some sample of the rest.
    def sway(self):

        def worker(rows, worse, evals = 0, above = None):
            if len(rows) <= pow(len(self.rows), Common.cfg['the']['min']):
                return {'best': rows, 'rest': many(worse, Common.cfg['the']['rest'] * len(rows)), 'evals': evals}
            half_res = self.half(None, above, rows)
            l = half_res['left']
            r = half_res['right']
            A = half_res['A']
            B = half_res['B']
            if self.better(half_res['B'], half_res['A']):
                l = half_res['right']
                r = half_res['left']
                A = half_res['B']
                B = half_res['A']
            for row in r:
                worse.append(row)
            return worker(l, worse, half_res['evals'] + evals, A)
        
        worker_res = worker(self.rows, [])
        return {'best': self.clone(worker_res['best']), 'rest': self.clone(worker_res['rest']), 'evals': worker_res['evals']}

    # Recursively prune the worst half the data. Return the survivors and some sample of the rest. Uses diferent dist function dist2.
    def sway2(self):

        def worker(rows, worse, evals=0, above=None):
            if len(rows) <= pow(len(self.rows), Common.cfg['the']['min']):
                return {'best': rows, 'rest': many(worse, Common.cfg['the']['rest'] * len(rows)), 'evals': evals}
            half_res = self.half2(None, above, rows)
            l = half_res['left']
            r = half_res['right']
            A = half_res['A']
            B = half_res['B']
            if self.better(half_res['B'], half_res['A']):
                l = half_res['right']
                r = half_res['left']
                A = half_res['B']
                B = half_res['A']
            for row in r:
                worse.append(row)
            return worker(l, worse, half_res['evals'] + evals, A)

        worker_res = worker(self.rows, [])
        return {'best': self.clone(worker_res['best']), 'rest': self.clone(worker_res['rest']),
                'evals': worker_res['evals']}

    def tree(self, rows = None, cols = None, above = None):
        selected_rows = rows if rows != None else self.rows

        here = {'data': self.clone(selected_rows)}

        if len(selected_rows) >= (2 * pow(len(self.rows), Common.cfg['the']['min'])):
            half_res = self.half(cols, above, selected_rows)
            here['left'] = self.tree(half_res['left'], cols, half_res['A'])
            here['right'] = self.tree(half_res['right'], cols, half_res['B'])
        return here

    def bin(self, col, x):
        if x == '?' or type(col) == Sym:
            return x
        tmp = (col.hi - col.lo) / (Common.cfg['the']['bins'] - 1)
        res = 1 if (col.hi == col.lo) else (math.floor(float(x) / tmp + 0.5) * tmp)
        return res

    def bins(self, cols, rows_set): #rows_set = best, rest result from sway 
          
        out = []
        n = 0
        for col in cols: #Col objects
            ranges = {}
            # ranges_best_rest = {}
            is_sym = type(col) == Sym
            for name, data in rows_set.items(): #this will go over best, rest groups (lists of Rows)
                for row in data.rows:
                    x = row.cells[col.at]
                    if x != '?':
                        n+=1
                        k = self.bin(col, x)
                        if k not in ranges:
                            ranges[k] = Sym(col.at, col.txt) if is_sym else Num(col.at, col.txt)
                        ranges[k].add(x, name)

            ranges = { key: value for key, value in sorted(ranges.items(), key=lambda x: x[1].lo) }
            to_add = list(ranges.values()) if is_sym else merges(list(ranges.values()), n / Common.cfg['the']['bins'], Common.cfg['the']['d'] * col.div())
            out.append(to_add)
            
        return out

    # Contrast Sets
    # Collect all the ranges into one flat list and sort them by their `value`.
    def xpln(self, sway_res):

        tmp = []
        max_sizes = {}

        def v(has):
            return value(has, "best", len(sway_res['best'].rows), len(sway_res['rest'].rows))
        
        def score(ranges):
            rule = Rule(ranges, max_sizes)
            if rule != None:
                print(str(show_rule(rule)))
                bestr = selects(rule, sway_res['best'].rows)
                restr = selects(rule, sway_res['rest'].rows)
                if len(bestr) + len(restr) > 0:
                    return {'value': v({'best': len(bestr), 'rest': len(restr)}), 'rule': rule}
            return None
        


        for bin_res in self.bins(self.cols.x, sway_res):
            max_sizes[bin_res[0].txt] = len(bin_res)
            print('\n')
            for range in bin_res:
                print(range.txt + ', ' + str(range.lo) + ', ' + str(range.hi))
                tmp.append({'range': range, 'max': len(bin_res), 'val': v(range.sources.has)})

        
        tmp.sort(key = lambda x: x['val'], reverse=True)
        first_n_res = first_N(tmp, score)
        return first_n_res
