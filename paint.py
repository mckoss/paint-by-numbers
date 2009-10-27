"""
Paint.py - Paint by numbers solver
"""

import sys, getopt, os

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "thf:")
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
        if o == '-f':
            Puzzazz(a)
        if o == '-b':
            Boggle(a)
        if o == '-t':
            suite = unittest.TestLoader().loadTestsFromTestCase(TestPBN)
            unittest.TextTestRunner(verbosity=2).run(suite)

def usage():
    print "Usage: %s [-h | -t | -f <file>]\n" % os.path.basename(sys.argv[0])
    print "Options\n"
    print "-h\t\t: help"
    print "-f <file>\t: Solve Paint by Numbers in file"
    print "-t\t\t: Run Unit tests"
    
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
                             
    return paint['solution']
    
    
class paint_iter(object):
    """ Iterator for paint by numbers runs.  Returns all combinations
    of starting positions for each run """
    def __init__(self, n, aRuns):
        self.n = n
        self.aRuns = aRuns
        self.size = len(self.aRuns)
        
        pos = 0
        self.aPos = []
        for r in aRuns:
            self.aPos.append(pos)
            pos += r + 1
        
        pos -= 1    
        if pos > self.n:
            raise Exception("Runs %r won't fit in allotted space of %d squares." % (aRuns, n))

        self.fFirst = True
        
    def __iter__(self):
        return self

    def next(self):
        if self.fFirst:
            self.fFirst = False
            return self.aPos
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
    
    n = len(row)
    pattern = None
    for trial in paint_vector_iter(n, aRuns):
        if consistent_row(row, trial):
            if pattern is None:
                pattern = trial
            else:
                intersect_row(pattern, trial)
                
    return pattern
                
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
        
    def test_iter_error(self):
        self.assertRaises(Exception, lambda x: paint_iter(3, [2,2]))
        
    def test_paint_vector(self):
        pi = list(paint_vector_iter(2, [1]))
        self.assertEqual(pi, [[1,0], [0,1]])
        
        pi = list(paint_vector_iter(5, [1, 2]))
        self.assertEqual(pi, [[1,0,1,1,0],[1,0,0,1,1],[0,1,0,1,1]])
        
        pi = list(paint_vector_iter(3, [3]))
        self.assertEqual(pi, [[1,1,1]])
        
    def test_row_util(self):
        self.assert_(consistent_row([1,0,None], [1,0,1]))
        self.assertEqual(consistent_row([1,0,None], [0,0,1]), False)
        
        self.assertEqual(intersect_row([1,0,1], [1,0,0]), [1,0,None])
        
    def test_solve_row(self):
        self.assertEqual(solve_row([None,None,None], [3]), [1, 1, 1])
        self.assertEqual(solve_row([None,None,None], [2]), [None, 1, None])
        self.assertEqual(solve_row([None,None,None], [1,1]), [1,0,1])
        
    def test_solve_paint(self):
        solution = solve_paint(test_data.simple1)
        self.assertEqual(len(solution), test_data.simple1['rows'])
        self.assertEqual(len(solution[0]), test_data.simple1['columns'])

if __name__ == "__main__":
    main()
