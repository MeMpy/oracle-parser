'''
Created on 01/nov/2013

@author: ross
'''
import unittest
from consts import qry_script_file


class Test(unittest.TestCase):


    def setUp(self):
        unittest.TestCase.setUp(self)
        print '\n------------------------------------------------------------------\n'
        
    def testOraclePackageParser(self):   
        print 'testOraclePackageParser'
        from parsers import oracle_package_parser
        f = open(qry_script_file, 'r')
        parsed_data = None
        with f:        
            parsed_data = oracle_package_parser.parse(f)
        print parsed_data  
        
        
    def testOraclePackageModels(self):
        print 'testOraclePackage'
        from models.oracle_package_models import OraclePackageDoc

        m = OraclePackageDoc.build_doc(qry_script_file)
        print m


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCoGeRmDoc']
    unittest.main()