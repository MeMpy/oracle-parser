# -*- coding: UTF-8 -*-
'''
Created on 01/nov/2013

@author: ross
'''
from coge.rmdocs.RmDoc import IRmDoc
from coge.rmdocs.readers import OraclePackageReader
import os
import re

class OraclePackage(IRmDoc):
    '''
    classdocs
    '''
    
    class Procedure(object):
        
        class Parameter(object):
            
            def __init__(self, param_name, sqltype, inoutType ):
                self.param_name = param_name
                self.sql_type = sqltype
                self.inout_type = inoutType
                
            def __str__(self):
                return str(
                           str(self.param_name) + ' ' +
                           str(self.inout_type) + ':' + 
                           str(self.sql_type))
                
                                    
        def __init__(self, procName = None, index = None, headerComment = ""):
            '''
            Rapresents a Procedure reader form a oracle body. It contains:
            - The Procedure Name
            - An identifier (or kind) made from the procName
            - The header comments if any
            - The procedure parameters if any, for each parameters will be stored:
                - the name
                - the type of input/output
                - the type of the parameter
            '''
            self.procName = procName
            self.identifier = self.buildIdentifier()
            self.headerComment = headerComment
            #the zero-based line number in which the procedure is written
            self.procStartIndex = index
            #(param name :  param type, in out type)
            self.procParams = []
            
        def buildIdentifier(self):
            identifier = None
            if self.procName:
                startIndex = 0
                if self.procName.startswith("GET_"):
                    startIndex = len("GET_")-1    
                names = self.procName[startIndex+1:].split("_")
                identifier = str()
                for name in names:
                    identifier +=name[:3].title()            
            return identifier       
        
        def addProcParam(self, name, sqltype, inoutType):
            self.procParams.append(OraclePackage.Procedure.Parameter(name, sqltype, inoutType))
            
        def addProcParamFromList(self, paramsList):
            '''
            @param paramsList: must be as follows: [paramName, in out type, type] 
            '''
            for param in paramsList:
                if len(param) == 3:
                    #there is the input output modifier
                    self.addProcParam(param[0], param[2], param[1])
                elif len(param) == 2:
                    #there isn't the input output modifier
                    self.addProcParam(param[0], param[1], str())
                else:
                    raise Exception("{0} Parameters not well-formed".format(self.procName))
                
        def GetParametersNames(self):
            return self.procParams.keys()
        
        def GetInputParametersCount(self):
            inputParams = [x for x in self.procParams.values() if "IN" in x[1].upper()]
            return len(inputParams)
        
        def __str__(self):
            return str(
                       str(self.identifier) + os.linesep +
                       str(self.procStartIndex) + os.linesep + 
                       str(self.procName) + os.linesep 
                       + str(map(str,self.procParams)))
                                
    
    def init_reader(self, path, reader_args):
        self.parser = OraclePackageReader.buildReader(path)
    
    def build_rmdoc(self, rmdoc_args):
        proceduresList = self._build_procedures_list(self.parser.procs)
        self._proceduresMap = self.__buildProceduresMap(proceduresList)        
        self._proceduresSubSet = list()
        
        self.packageName = self.parser.packageName
        self.procedures = self._build_procedures()
    
    
    
    def __buildProceduresMap(self, proceduresList):
        procsMap = dict()
        for proc in proceduresList:
            procsMap[proc.identifier] = proc
        return procsMap
    
    def _build_procedures(self):
        """
        """
        proceduresSubSet = self._proceduresMap.values()
        if self._proceduresSubSet:
            proceduresSubSet = [x for x in self._proceduresMap.values() if x.procName in self._proceduresSubSet]
        return sorted(proceduresSubSet, key = lambda proc: proc.procStartIndex)    
        
    def _build_procedures_list(self, procList):
        """
        @param procList: It is a list of tuple,
        each tuple is defined as follows:
        (procIndex, commentBlock, SignatureBlock, BodyBlock)
        For each tuple will be called:
        _add_comment_to_proc_obj
        _add_signature_to_proc_obj
        _add_body_to_proc_obj
        In order to build a procedure object
        
        """
        proceduresList = list()
        procObj = None
         
        for p in procList:
            procObj = OraclePackage.Procedure()
            self._add_comment_to_proc_obj(p[1], procObj)
            self._add_signature_to_proc_obj(p[0], p[2], procObj)
            self._add_body_to_proc_obj(p[3], procObj)
            procObj.identifier= procObj.buildIdentifier()        
            proceduresList.append(procObj)
        
        return proceduresList    
    
    
    def _add_comment_to_proc_obj(self, commentBlock, proc):
        """
        """
        pass    
    
    def _add_signature_to_proc_obj(self, procIndex, segnatureBlock, proc):
        """        
        From the signatureBlock read:
        - the procedure name
        - the parameters block
        
        Add them to the procedure object
                    
        """
                      
        match = re.search(OraclePackageReader.PTRN_PROCEDURE_NAME, segnatureBlock)
        procName = match.group()[:-1]            
        match = re.search(OraclePackageReader.PTRN_PARAMETERS_BLOCK, segnatureBlock, flags = re.S) #flags = re.DOTALL
        paramsBlock = match.group()[1:-1]
        
        #=======================================================================
        # Parameters Parsing
        #=======================================================================
        rowParamsList = paramsBlock.split(OraclePackageReader.SPLIT_PARAMETER_TOKEN)
        params = list()        
        rowParam = str()
        startIndex = None
        for rowParam in rowParamsList:        
            startIndex = rowParam.upper().find(OraclePackageReader.FIND_START_PARAMETER_DECLARATION)                
            #first three elements of the list obtained splitting rowParam by a n-whitespace token
            params += [rowParam[startIndex:].split()]
        
        proc.procName = procName
        proc.procStartIndex = procIndex
        proc.addProcParamFromList(params)      
        
    
    
    def _add_body_to_proc_obj(self, bodyBlock, proc):
        """
        """
        pass
    
    #TODO capire se servono
    def GetProceduresNames(self):
        return [x.procName for x in self.GetProcedures()]
    
    def GetProceduresKinds(self):
        return [(x.identifier, x.procName) for x in self.GetProcedures()]
    
    def GetPackageName(self):
        return self._packageName
    
    def SetNewIdentifier(self, oldIdentifier, newIdentifier):
        procTemp = self._proceduresMap.pop(oldIdentifier)
        if self._proceduresMap.has_key(newIdentifier):
            raise Exception("Identifier {0} already used".format(newIdentifier))
        else:
            procTemp.identifier = newIdentifier
            self._proceduresMap[newIdentifier] = procTemp
    
    def set_procedures_subset(self, proceduresNames):
        """
        Set the procedures sub set.
        It is used to filter the procedures returned by gets methods.  
        It must be a list of procedure names contained into the package
        Each time a set is added the procedures list into this reader instance will be rebuild      
        """ 
        if type(proceduresNames) is list:
            self._proceduresSubSet = proceduresNames
            self._procedures = self._build_procedures()
        else:
            raise Exception("proceduresNames isn't a list")

#===============================================================================
#                                     TEST
#===============================================================================
if __name__ == '__main__':
    testFilePath = "/home/ross/Project/other_files/pkg/b_APP_GIR_QRY.sql"
    rmdoc = OraclePackage(testFilePath)
    print rmdoc.packageName
    #===========================================================================
    # identifier = reader.GetProcedures()[0].identifier
    # reader.SetNewIdentifier(identifier, "pippo")
    #===========================================================================
    for proc in rmdoc.procedures:
        print proc 
        
    print rmdoc.__dict__.keys()   
    print rmdoc.procedures[0].__dict__.keys()
    