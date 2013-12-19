'''
Created on 01/nov/2013

@author: ross
'''
import unittest
from rmdocs.OraclePackage import OraclePackage
from templates import Procedures, EnsembleECO
from formatter.CoGePyFormatter import


class Test(unittest.TestCase):


    def testCoGeRmDoc_Procedures(self):
        testFilePath = "/home/ross/Project/other_files/pkg/b_APP_GIR_QRY.sql"
        formatter = CoGePyFormatter()
        rmdoc = OraclePackage(testFilePath)
        print formatter.format(Procedures.NEW_proceduresTemplate, rmdoc)
    
    def testCoGeRmDoc_EnsembleECO(self):
        testFilePath = "/home/ross/Project/other_files/pkg/b_APP_GIR_QRY.sql"
        formatter = CoGePyFormatter()
        rmdoc = OraclePackage(testFilePath)
        collectedParam= dict()
        collectedParam["GET_INCIDENT"] = True
        masterProcs = dict()
        masterProcs["GET_INCIDENT_CHRONOLOGIE"] = "GET_INCIDENT"
        print formatter.format(EnsembleECO.New_ensDefTemplate, rmdoc, serviceName = "PippoService",collectedParam=collectedParam, masterProcs = masterProcs)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testCoGeRmDoc']
    unittest.main()