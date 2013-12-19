'''
Created on 01/dic/2013

@author: ross
'''
import unittest
import CoGePy
from coge import Generator
from unit_tests.consts import PROCEDURE_TEMPLATE_PATH, qry_script_file

class Test(unittest.TestCase):

    def _print_seprator(self):
        print "-----------------------------------------------------------------------------------"    
    

    def testExecuteGeneration(self):
        
        print 'test ExecuteGeneration'
        
        print Generator.execute(PROCEDURE_TEMPLATE_PATH, qry_script_file)
        
        self._print_seprator()

        
    def testScriptProcedures(self):
        
        print 'test Script Procedures'
                
        argv = str(PROCEDURE_TEMPLATE_PATH+' '+qry_script_file).split()
        
        print CoGePy.main(argv)
        
        self._print_seprator()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testMain']
    unittest.main()