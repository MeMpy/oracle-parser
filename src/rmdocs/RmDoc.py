# -*- coding: UTF-8 -*-
'''
Created on 01/nov/2013
Modified on 05/01/2014
@author: ross
'''

import os

NOT_IMPLEMENTED_MSG = 'It must be implemented in the subclass'

#############################
OPEN_FILE_MODE = "r"

#TODO Improve
def _check_file(source_file_path):
    if not os.path.exists(source_file_path):
        raise Exception('file not found')

def build_doc(doc_class, parser, source_file_path, *args, **kwargs):
    """
    Main method to build the Doc, it check the file, read it and invoke the parser on it
    and call the doc constructor passing the data parsed.
    Eventually pass to the parser and constructor the args and the kwargs
    """
    _check_file(source_file_path)
    f = open(source_file_path, OPEN_FILE_MODE)
    parsed_data = None
    with f:
        parsed_data = parser(f, *args, **kwargs)
    
    return doc_class(parsed_data, *args, **kwargs)
    

#===============================================================================
# Abstract class, FOR NOW IT'S ONLY A MARKER
#===============================================================================
class IRmDoc(object):
    '''
    Abstract Class for an RmDoc (Reader Mapping Document)
    '''
    
    #TODO Implement
    def print_available_field(self):
        """
        """
        raise Exception(NOT_IMPLEMENTED_MSG)             
            