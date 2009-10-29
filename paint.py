"""
Paint.py - Paint by numbers solver
"""

import sys, getopt, os

import yaml

DEBUG = False

def main():
    global DEBUG
    try:
        opts, args = getopt.getopt(sys.argv[1:], "dthf:")
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    if len(opts) == 0:
        usage()
        sys.exit(0)
    for o, a in opts:
        if o == '-h':
            usage()
            sys.exit()
        if o == '-d':
            DEBUG = True
        if o == '-f':
            paint = load_paint(a)
            solve_paint(paint)
            print_paint(paint)
        if o == '-t':
            suite = unittest.TestLoader().loadTestsFromTestCase(TestPBN)
            unittest.TextTestRunner(verbosity=2).run(suite)

def usage():
    print "Usage: %s [-h | -t | -f <file>]\n" % os.path.basename(sys.argv[0])
    print "Options\n"
    print "-h\t\t: help"
    print "-f <file>\t: Solve Paint by Numbers in file"
    print "-t\t\t: Run Unit tests"
    print "-d\t\t: Print debug information during solve"
    
def print_paint(paint):
    if 'solution' not in paint:
        paint['solution'] = [[None for column in range(paint['columns'])] for row in range(paint['rows'])]

    i = 0
    for row in paint['solution']:
        i += 1
        print "Row %2d: %s" % (i, row_string(row))
        
def load_paint(sFile):
    f = open(sFile)
    paint = yaml.load(f)
    f.close()
    
    def EnsureListSize(sName, size):
        if type(size) != int:
            raise Exception("'rows' and 'columns' must be integers")
        a = paint[sName]
        if type(a) != list:
            print "'%s' is not a list: %r" % (sName, a)
            a = paint[sName] = []
            
        extra = len(a) - size
        if extra > 0:
            print "Too many items in %s - trimming to %d" % (sName, size)
            a = a[0:size]
        elif extra < 0:
            print "Not enough items in %s - extending to %d" % (sName, size)
            a.extend([[] for i in range(extra)])
                      
        for runs in a:
            for x in runs:
                if type(x) != int:
                    raise Exception("Run %r contains a non-integer: %r" % (runs, x))
    
    EnsureListSize('row_runs', paint['rows'])
    EnsureListSize('column_runs', paint['columns'])

    return paint
        
def row_string(row):
    s = ''
    for val in row:
        if val == None:
            s += '_'
        elif val == 1:
            s += 'X'
        else:
            s += '.'
    return s
            
    
def solve_paint(paint):
    """ Solve a Point by Numbers puzzle.  The paint dictionary must contain:
    
    rows: number of rows in the puzzle
    columns: number of columns in the puzzle
    row_runs: array of sequences (one per row), of runs of consecutive 1's in the solution row
    column_runs: array of sequences (one per column), of runs of consecutive 1's in the solution column
    solution: (optional) partially specified array for the solution - an array of row vectors containing
              0, 1, or None (not specified).
    
    We start with an un-constrained array for the solution (default, all None), and successively apply
    the row and column runs to further constrain the solution until we can find no additional constrained
    values.
    """
    
    if 'solution' not in paint:
        paint['solution'] = [[None for column in range(paint['columns'])] for row in range(paint['rows'])]
    
    countLast = None
    countNone = sum(paint['solution'][i].count(None) for i in range(paint['rows']))
    
    while countNone != 0 and countNone != countLast:
        countLast = countNone
        if DEBUG:
            print "%d squares remaining" % countNone
            print_paint(paint)
            
        for row, runs in zip(paint['solution'], paint['row_runs']):
            solve_row(row, runs)
    
        if DEBUG:
            countNone = sum(paint['solution'][i].count(None) for i in range(paint['rows']))
            if countNone != 0:
                print "%d squares remaining" % countNone
                print_paint(paint)
        
        for i, column, runs in zip(range(paint['columns']),
                                   columns(paint['solution']),
                                   paint['column_runs']):
            solve_row(column, runs)
            set_column(paint['solution'], i, column)
        
        countNone = sum(paint['solution'][i].count(None) for i in range(paint['rows']))
                             
    return paint['solution']

def columns(a):
    """ Return a list for each of the columns on an array (generator function) """
    for column in range(len(a[0])):
        aColumn = []
        for row in range(len(a)):
            aColumn.append(a[row][column])
        yield aColumn
        
def set_column(a, i, column):
    for row in range(len(column)):
        a[row][i] = column[row]
    return a
    
class paint_iter(object):
    """ Iterator for paint by numbers runs.  Returns all combinations
    of starting positions for each run """
    def __init__(self, n, aRuns):
        self.n = n
        self.aRuns = aRuns
        self.size = len(self.aRuns)
        self.fFirst = True
        self.fZero = False
        
        pos = 0
        self.aPos = []
        
        # Special case for all-zero runs
        if self.size == 1 and aRuns[0] == 0:
            self.fZero = True
            return
        
        for r in aRuns:
            self.aPos.append(pos)
            pos += r + 1
        
        pos -= 1    
        if pos > self.n:
            raise Exception("Runs %r won't fit in allotted space of %d squares." % (aRuns, n))
        
    def __iter__(self):
        return self

    def next(self):
        # If no runs are given, don't iterate on any positions
        if self.size == 0:
            raise StopIteration
        
        if self.fFirst:
            self.fFirst = False
            return self.aPos
        
        if self.fZero:
            raise StopIteration

        i = self.size - 1
        while True:
            if i < 0:
                raise StopIteration
            self.aPos[i] += 1
            for j in range(i+1, self.size):
                self.aPos[j] = self.aPos[j-1] + self.aRuns[j-1] + 1
            if self.aPos[self.size-1] + self.aRuns[self.size-1] > self.n:
                i -= 1
                continue
            return self.aPos

class paint_vector_iter(object):
    """ Iterator produces each of the vector representation of a paint by numbers run pattern """
    def __init__(self, n, aRuns):
        self.n = n
        self.aRuns = aRuns
        self.size = len(aRuns)
        self.pi = paint_iter(n, aRuns)
        
    def __iter__(self):
        return self
    
    def next(self):
        aPos = self.pi.next()
        
        # Special case for zero vector
        if aPos == []:
            return [0 for i in range(self.n)]
        
        aVector = [0 for i in range(self.n)]
        for i in range(self.size):
            for j in range(aPos[i], aPos[i]+self.aRuns[i]):
                aVector[j] = 1
        return aVector
    
def solve_row(row, aRuns):
    """ row contains 0,1, or None based on apriori values known to exist
    at each square.  This function fills in any additional values that
    are currently unconstrained but are determined uniquely by the available
    patterns.  Patterns of runs that are not consistent with the current row
    pattern are ignored. """
    
    if len(aRuns) == 0:
        return row
    
    n = len(row)
    pattern = None
    for trial in paint_vector_iter(n, aRuns):
        if consistent_row(row, trial):
            if pattern is None:
                pattern = trial
            else:
                intersect_row(pattern, trial)
                
    if pattern is None:
        raise Exception("Inconsistent run description: %r cannot match row %s" % (aRuns, row_string(row)))

    # Copy the resulting pattern constraints back into the original row             
    for i in range(n):
        if pattern[i] is not None:
            row[i] = pattern[i]
                
    return row
                
def consistent_row(row, trial):
    """ A trial is consistent if for all the 0's and 1's in row, we have
    matching values in the trial. """
    
    for i in range(len(row)):
        if row[i] is not None and trial[i] != row[i]:
            return False
        
    return True

def intersect_row(pattern, trial):
    """ Reduce the pattern by setting non-matching cells in trial to None """
    
    for i in range(len(pattern)):
        if trial[i] != pattern[i]:
            pattern[i] = None
            
    return pattern
    

# --------------------------------------------------------------------
# Unit Tests
# --------------------------------------------------------------------
import unittest

import test_data

class TestPBN(unittest.TestCase):
    def test_iter(self):
        pi = [list(i) for i in paint_iter(10, [1])]
        self.assertEqual(pi[0], [0])
        self.assertEqual(len(pi), 10)
        
        pi = [list(i) for i in paint_iter(10, [2])]
        self.assertEqual(len(pi), 9)
        
        pi = [list(i) for i in paint_iter(4, [1,1])]
        self.assertEqual(pi, [[0,2], [0,3], [1, 3]])
        
        pi = [list(i) for i in paint_iter(3, [3])]
        self.assertEqual(pi, [[0]])
        
        # Empty run list should not return any iterations
        pi = [list(i) for i in paint_iter(3, [])]
        self.assertEqual(pi, [])
        
        pi = [list(i) for i in paint_iter(3, [0])]
        self.assertEqual(pi, [[]])
        
    def test_iter_error(self):
        self.assertRaises(Exception, lambda x: paint_iter(3, [2,2]))
        
    def test_paint_vector(self):
        pi = list(paint_vector_iter(2, [1]))
        self.assertEqual(pi, [[1,0], [0,1]])
        
        pi = list(paint_vector_iter(5, [1, 2]))
        self.assertEqual(pi, [[1,0,1,1,0],[1,0,0,1,1],[0,1,0,1,1]])
        
        pi = list(paint_vector_iter(3, [3]))
        self.assertEqual(pi, [[1,1,1]])
        
        # Distinguish the empty run list (no information) - from one with a single zero
        pi = list(paint_vector_iter(3, [0]))
        self.assertEqual(pi, [[0,0,0]])
        
        pi = list(paint_vector_iter(3, []))
        self.assertEqual(pi, [])
        
    def test_row_util(self):
        self.assert_(consistent_row([1,0,None], [1,0,1]))
        self.assertEqual(consistent_row([1,0,None], [0,0,1]), False)
        
        self.assertEqual(intersect_row([1,0,1], [1,0,0]), [1,0,None])
        
    def test_solve_row(self):
        self.assertEqual(solve_row([None,None,None], [3]), [1, 1, 1])
        self.assertEqual(solve_row([None,None,None], [2]), [None, 1, None])
        self.assertEqual(solve_row([None,None,None], [1,1]), [1,0,1])
        
    def test_columns(self):
        self.assertEqual(list(columns([[1,2],[3,4]])), [[1,3],[2,4]])
        self.assertEqual(set_column([[1,2],[3,4]], 1, [5,6]), [[1,5],[3,6]])
        
    def test_solve_paint(self):
        solution = solve_paint(test_data.simple1)
        self.assertEqual(len(solution), test_data.simple1['rows'])
        self.assertEqual(len(solution[0]), test_data.simple1['columns'])
        self.assertEqual(solution, test_data.simple1['test_solution'])
        
        solution = solve_paint(test_data.simple2)
        self.assertEqual(solution, test_data.simple2['test_solution'])
        
        solution = solve_paint(test_data.simple3)
        self.assertEqual(solution, test_data.simple3['test_solution'])

if __name__ == "__main__":
    main()
