import os
import re
import copy
import math

from Row import Row
from Cols import Cols
from Data import Data

##
# Takes a string line as input and returns a list of parsed cells. Extract any text enclosed in single
# quotes in each comma-separated item in the input line and store it in a list called headers
#
# Finally, the function joins the headers list with a colon separator and appends it to the cells list
# which is returned. The resulting cells list contains all the numbers in the input line, as well as a
# string made up of any header strings found, separated by colons. This string of headers is typically
# used to label the columns of a table or spreadsheet.
##
def parse_line(line: str):

    # Splits the input line on commas and iterates over the resulting items.
    split_line = line.split(',')

    headers = []
    cells = []

    ##
    # Checks if the length of each item in the split_line list is 0 (an empty string). It skips to the
    # next item using the continue statement. The purpose is to remove any empty items in the
    # split_line list.
    #
    # item_stripped = item.strip():         remove any leading or trailing white spaces.
    # is_number = item_stripped.isdigit():  isdigit() method is called on the stripped item to check if
    #                                       it contains only digits.
    #
    # If the item does not contain only digits, findall() method from the re module is called to find
    # all occurrences of text enclosed in single quotes in the unstripped item. If the item is a
    # string, it checks if it contains any single quotes and extracts the text between them as headers
    # The extracted headers are added to a list called headers.
    #
    # If the item is a number, it is stripped of any leading or trailing white space, and added to a
    # list called cells.
    ##
    for item in split_line:
        if len(item) == 0:
            continue

        item_stripped = item.strip()
        is_number = item_stripped.isdigit()
        if not is_number:
            for match in re.findall('\'(.*?)\'', item):
                headers.append(match.replace('\'', ''))
        else:
            cells.append(item_stripped)

    ##
    # Joins all the headers found in the input line into a single string separated by colons and
    # appends it to the list of cell values.
    ##
    cells.append(':'.join(headers))
    return cells

##
# Reads the contents of a file located at the given source path and returns a list of strings where
# each string corresponds to a line in the file.
#
# First checks if the source path is a relative path and if it is, it converts it to an absolute path
# by joining it with the directory of the current script using the os.path module. Then, it opens the
# file using the open() function and reads its contents using the readlines() method, which returns a
# list of strings where each string corresponds to a line in the file. Finally, it returns this list of
# strings.
##
def get_file_contents(src: str):

    ##
    # Try to catch relative paths
    #
    # Checks whether the src file path is a file or not. If it's not a file, it assumes that the path
    # is a relative path and uses the os.path.dirname(__file__) method to get the directory of the
    # current Python script and then appends the src path to it using the os.path.join() method to
    # convert the relative path to an absolute path. The __file__ attribute refers to the current
    # Python script's filename. So, os.path.dirname(__file__) returns the directory where the current
    # script is located. The os.path.join() method then combines the directory path and the src path to
    # create an absolute path.
    #
    # Opens the file in read-only mode using open(), reads all the lines of the file using readlines()
    # and stores them in the repgrid_contents list. Then, returns this list containing the lines of the
    # file.
    ##
    if not os.path.isfile(src):
        src = os.path.join(os.path.dirname(__file__), src)

    src = os.path.abspath(src)

    repgrid_contents = []
    with open(src, 'r') as repgrid_file:
        repgrid_contents = repgrid_file.readlines()
    return repgrid_contents

##
# Reads the contents of a file specified by the src parameter using the get_file_contents function and
# stores the contents in the repgrid_contents variable. It then initializes two empty lists: rows and
# names.
#
# col_query and row_query are regular expressions used to match the "cols" and "rows" sections in the
# file. Retrieves the first line of repgrid_contents list and removes it from the list. strip() is used
# to remove any leading or trailing whitespaces from the line. The line is then used to iterate through
# the file.
##
def repcols(src: str):

    repgrid_contents = get_file_contents(src)

    rows = []
    names = []

    ##
    # col_query and row_query pattern matches any sequence of characters that contains the word "cols"
    # and "rows" after some optional whitespace characters and an optional tab character, followed by
    # an equal sign and another optional whitespace and tab characters, and ends with an opening curly
    # brace.
    ##
    col_query = "( )*\t*cols( )*\t*=( )*\t*{"
    row_query = "( )*\t*rows( )*\t*=( )*\t*{"

    row_len = 0

    current_line = repgrid_contents.pop(0).strip()

    ##
    # Continue to execute as long as the regular expression pattern in col_query is not found in
    # current_line. The purpose of this loop is to skip over lines in repgrid_contents until it reaches
    # the "cols" section of the file.
    #
    # Removes and returns the first item (string) of the repgrid_contents list, and then strips any
    # leading or trailing whitespace from it, storing it in the current_line variable.
    ##
    while not re.search(col_query, current_line):
        current_line = repgrid_contents.pop(0).strip()

    ##
    # Continue to execute as long as the regular expression pattern in row_query is not found in
    # current_line. The purpose of this loop is to skip over lines in repgrid_contents until it reaches
    # the "rows" section of the file.
    #
    # Uses the parse_line function to extract the values of the current line, strips any whitespace
    # from the line, and appends the resulting list to rows. Checks if the length of the current row is
    # longer than the current maximum row length (row_len) and updates row_len if necessary. Checks if
    # there are more lines left to read from the file and, if so, pops the next line from
    # repgrid_contents and assigns it to current_line, stripping any whitespace.
    ##
    while not re.search(row_query, current_line):
        row = parse_line(current_line.strip())
        rows.append(row)
        row_len = max(row_len, len(row))
        if len(repgrid_contents) > 0:
            current_line = repgrid_contents.pop(0).strip()

    ##
    # Extracting the names of the rows from the Repertory Grid file
    #
    # re.split(row_query, current_line) is used to split the line at the "rows =" section, so that
    # current_line contains only the contents of the row names. Creates a list called names with
    # row_len empty strings. row_len variable is length of longest row in Repertory Grid. This is
    # because the Repertory Grid is a matrix and all the rows need to have the same length.
    ##
    current_line = re.split(row_query, current_line)[-1]
    names = [""] * row_len

    ##
    # Checks any string that contains a string that starts with zero or more spaces, followed by zero
    # or more tabs, followed by an opening curly brace {, then any characters and finally a closing
    # curly brace "}"
    #
    # Counts number of underscores in current line of repgrid contents. Used to determine index of
    # current row name being read from the rows section
    ##
    while re.search("( )*\t*[{].*[}]", current_line):
        index = current_line.count('_')
        split = current_line.split('}')[0].split(',')
        value = split[-1]
        names[index] = value.strip().replace('\'', '').replace('{', '')
        if len(repgrid_contents) > 0:
            current_line = repgrid_contents.pop(0).strip()
        else:
            break

    names[-1] = "thingX" # End this off with an X so it gets skipped in calculations
    generated_data = Data(names)

    for row in rows:
        generated_data.add(row)
    return generated_data

def reprows(src: str):

    repgrid_contents = get_file_contents(src)

    rows = []
    names = []


    col_query = "( )*\t*cols( )*\t*=( )*\t*{"
    row_query = "( )*\t*rows( )*\t*=( )*\t*{"

    current_line = repgrid_contents.pop(0).strip()
    while not re.search(col_query, current_line): #for now, let's just skip to the cols section
        current_line = repgrid_contents.pop(0).strip()

    # parse the cols section
    # keep trying to read and parse until we reach the rows section
    while not re.search(row_query, current_line):
        cells = parse_line(current_line.strip())
        names.append(cells.pop(-1))
        for i, cell in enumerate(cells):
            if((i + 1) > len(rows)):
                rows.append([cell])
            else:
                rows[i].append(cell)
        if len(repgrid_contents) > 0:
            current_line = repgrid_contents.pop(0).strip()


    #read the rows
    current_line = re.split(row_query, current_line)[-1]

    #keep reading until we read the end
    while re.search("( )*\t*[{].*[}]", current_line):
        index = current_line.count('_')
        split = current_line.split('}')[0].split(',')
        value = split[-1]
        rows[index].append(value.strip().replace('\'', '').replace('{', ''))
        if len(repgrid_contents) > 0:
            current_line = repgrid_contents.pop(0).strip()
        else:
            break

    names.append("thingX") # end this off with an X so it gets skipped in calculations
    generated_data = Data(names)

    for row in rows:
        generated_data.add(row)
    return generated_data

def repplace(data: Data, n = 20):

    res = [["." for _ in range(n + 1)] for i in range(n + 1)]

    maxy = 0
    for i, row in enumerate(data.rows):
        c = chr(i + 65)
        print(c, row.cells[-1])
        x = int(row.x * n // 1)
        y = int(row.y * n // 1)

        maxy = max(maxy, y + 1)
        res[y + 1][x + 1] = c

    for y in range(maxy):
        print(*res[y])
