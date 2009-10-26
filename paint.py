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

# --------------------------------------------------------------------
# Unit Tests
# --------------------------------------------------------------------
import unittest

import test_data

class TestPBN(unittest.TestCase):
    def test_Basic(self):
        self.assertEqual(2, 2)

if __name__ == "__main__":
    main()
