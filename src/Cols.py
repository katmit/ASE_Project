from Num import Num
from Sym import Sym

import Row

import re
from enum import Enum


# Holds summaries of columns
class Cols:
    ##
    # A NUM or SYM is generated based on whether s starts with an uppercase
    # letter or not.
    #
    # The generated NUM or SYM is appended to the all attribute.
    #
    # If s does not end with the character 'X', it is either appended to
    # the y or x attribute based on whether it ends with [!+-] or not. If
    # it ends with !, it sets the klass attribute to this NUM or SYM.
    #
    # names:    A list of all column names in the dataset.
    # all:      A list of all columns, including the skipped ones.
    # klass:    A single dependent class column (if it exists).
    # x:        A list of independent columns.
    # y:        A list of dependent columns.
    ##
    def __init__(self, t: list[str]):
        self.names = t
        self.all = []
        self.x = []
        self.y = []

        for n, s in enumerate(t):
            s = s.strip()
            col = Num(n, s) if s[0].isupper() else Sym(n, s)
            self.all.append(col)
            if(s[-1].lower() != 'x'):
                if s[-1] == '-' or s[-1] == '+':
                    self.y.append(col)
                else:
                    self.x.append(col)
            

    ##
    # The add method updates the dependent and independent columns with
    # details from a given row. It does this by iterating over the x and y
    # lists and calling the add method for each column, passing in the
    # relevant cell from the row.cells list.
    ##
    def add(self, row: Row):
        for col in self.all:
            col.add(row.cells[col.at])
        self.all = sorted(self.all, key=lambda x: x.lo)
