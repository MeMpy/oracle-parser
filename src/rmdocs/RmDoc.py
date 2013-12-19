# -*- coding: UTF-8 -*-
'''
Created on 01/nov/2013

@author: ross
'''
import importlib

PACKAGE_RMDOC = 'coge.rmdocs.{0}' #TODO get it automatically
NOT_IMPLEMENTED_MSG = 'It must be implemented in the subclass'


#===============================================================================
# Abstract Factory (Entry Point)
#===============================================================================
def load_Rmdoc_by_name(rmdoc_name, source_file_path, reader_args = None, rmdoc_args = None):    
    rmdoc_name = rmdoc_name.strip()
    module = importlib.import_module(PACKAGE_RMDOC.format(rmdoc_name))
    rmdoc = getattr(module, rmdoc_name)
    return rmdoc(source_file_path, reader_args, rmdoc_args)
 

#===============================================================================
# Abstract class
#===============================================================================
class IRmDoc(object):
    '''
    Abstract Class for an RmDoc (Reader Mapping Document)
    '''


    def __init__(self, path, reader_args = None, rmdoc_args = None):
        '''
        Initialize the reader
        Build the document
        '''       
        self.init_reader(path, reader_args)
        self.build_rmdoc(rmdoc_args)
    
    #TODO Write docs
    def init_reader(self, path, reader_args):
        """        
        """        
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)
    
    #TODO Write docs
    def build_rmdoc(self, rmdoc_args):
        """
        """
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)
    
    #TODO Implement
    def print_available_field(self):
        """
        """
        pass 
                
            
            