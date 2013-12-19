'''
Created on 01/nov/2013

@author: ross
'''
import unittest
from rmdocs.OraclePackage import OraclePackage
from unit_tests.consts import qry_script_file


class Test(unittest.TestCase):


    def testOraclePackageReader(self):        
        rmdoc = OraclePackage(qry_script_file)
        print rmdoc    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCoGeRmDoc']
    unittest.main()