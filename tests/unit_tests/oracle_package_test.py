'''
Created on 01/nov/2013

@author: ross
'''
import unittest
from unit_tests.consts import qry_script_file


class Test(unittest.TestCase):


    def setUp(self):
        unittest.TestCase.setUp(self)
        print '\n------------------------------------------------------------------\n'
        
    def testOraclePackageParser(self):   
        print 'testOraclePackageParser'
        from rmdocs.parsers import OraclePackageParser
        f = open(qry_script_file, 'r')
        parsed_data = None
        with f:        
            parsed_data = OraclePackageParser.parse(f)
        print parsed_data  
        
        
    def testOraclePackage(self):  
        print 'testOraclePackage' 
        from rmdocs.parsers import OraclePackageParser
        from rmdocs.models import OraclePackageModels
        from rmdocs import RmDoc     
        RmDocGeneric = RmDoc.build_doc(OraclePackageModels.OraclePackageDoc, OraclePackageParser.parse, qry_script_file) 
        print RmDocGeneric  


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCoGeRmDoc']
    unittest.main()