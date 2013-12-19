'''
Created on 12/ott/2013

@author: ross
'''
import unittest
import CoGePy
from unit_tests.consts import ENSEMBLEECO_TEMPLATE_PATH, qry_script_file,\
    PROCEDURE_TEMPLATE_PATH


class Test(unittest.TestCase):
    
    def _print_seprator(self):
        print "-----------------------------------------------------------------------------------"    
        
    def testMainEnsembleEco1(self):        
        argv = str(ENSEMBLEECO_TEMPLATE_PATH +" "+ qry_script_file +"  -kwargs serviceName:Incident collectedParam:{\'GET_DICTIONNAIRE\':False,\'GET_INCIDENT\':True}").split()
        
        self.assertEqual(CoGePy.main(argv), 0, "No Code Generated")
        
        self._print_seprator()
    
    def testMainProcedures(self):
        argv = str(PROCEDURE_TEMPLATE_PATH+" "+qry_script_file).split()
         
        self.assertEqual(CoGePy.main(argv), 0, "No Code Generated")
         
        self._print_seprator()
     
    #===========================================================================
    # def testExecuteGenerationGlade(self):
    #     templateName = "Glade"
    #     readerArgs = [test_Glade_file_path]
    #     processArgs = ["GladeCoGeGuiHandler", ["GtkButton","GtkFileChooserButton", "GtkEntry", "GtkCheckButton", "GtkTreeView", "GtkListStore", "GtkWindow"], True]
    #     code  = Generate.ExecuteGeneration(templateName, None, readerArgs, None, processArgs)
    #     print code
    #     self.assertNotEqual(code, "", "No Code Generated")
    #      
    #     self._print_seprator()
    #===========================================================================

    


if __name__ == "__main__":
    unittest.main()