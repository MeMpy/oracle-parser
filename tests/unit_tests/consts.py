'''
Created on 19/dic/2013

@author: eroreng
'''
#win
import os

template_folder_path = r'C:\Users\ERORENG.ERICSSON\Documents\RRENGA\Dropbox\Portatile\Test_files\CoGePy\template_tests'
pkg_folder_path = r'C:\Users\ERORENG.ERICSSON\Documents\RRENGA\Dropbox\Portatile\Test_files\CoGePy\eco_test\pkg'
#linux
#template_folder_path = '/home/ross/Project/other_files/template_tests/'
#pkg_folder_path = r'/home/ross/Project/other_files/pkg/'

ENSEMBLEECO_TEMPLATE_PATH = os.path.join(template_folder_path, 'EnsembleEcoTemplate.txt')
PROCEDURE_TEMPLATE_PATH = os.path.join(template_folder_path,'ProceduresTemplate.txt')

qry_script_file = os.path.join(pkg_folder_path,'b_APP_GIR_QRY.sql')


