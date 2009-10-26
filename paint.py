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
    
def solve_problem(problem):
    return None

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

# --------------------------------------------------------------------
# Unit Tests
# --------------------------------------------------------------------
import unittest

import test_data

class TestPBN(unittest.TestCase):
    def test_Basic(self):
        self.assertEqual(2, 2)
        
    def test_iter(self):
        pi = [list(i) for i in paint_iter(10, [1])]
        self.assertEqual(pi[0], [0])
        self.assertEqual(len(pi), 10)
        
        pi = [list(i) for i in paint_iter(10, [2])]
        self.assertEqual(len(pi), 9)
        
        pi = [list(i) for i in paint_iter(4, [1,1])]
        self.assertEqual(pi, [[0,2], [0,3], [1, 3]])
        
    def test_iter_error(self):
        self.assertRaises(Exception, lambda x: paint_iter(3, [2,2]))

if __name__ == "__main__":
    main()
