'''
Created on Jan 5, 2014

@author: ross
'''
from rmdocs.RmDoc import IRmDoc
import os
import re

PTRN_WHITE_SPACE_SUBS = r' +'
PTRN_PROCEDURE_NAME = r'\b\w*\s*\('
PTRN_PARAMETERS_BLOCK = r'\(.*\)' #Works only if there aren't parameters with comments (into which there is a ")")

SPLIT_PARAMETER_TOKEN = ','

FIND_START_PARAMETER_DECLARATION = "P"

class OraclePackageDoc(IRmDoc):
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
            self.identifier = self._buildIdentifier()
            self.headerComment = headerComment
            #the zero-based line number in which the procedure is written
            self.procStartIndex = index
            #(param name :  param type, in out type)
            self.procParams = []
            
        def _buildIdentifier(self):
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
        
        def _addProcParam(self, name, sqltype, inoutType):
            self.procParams.append(OraclePackageDoc.Procedure.Parameter(name, sqltype, inoutType))
            
        def addProcParamFromList(self, paramsList):
            '''
            @param paramsList: must be as follows: [paramName, in out type, type] 
            '''
            for param in paramsList:
                if len(param) == 3:
                    #there is the input output modifier
                    self._addProcParam(param[0], param[2], param[1])
                elif len(param) == 2:
                    #there isn't the input output modifier
                    self._addProcParam(param[0], param[1], str())
                else:
                    raise Exception("{0} Parameters not well-formed".format(self.procName))
        
        #Utility   
        def get_parameters_pames(self):
            return self.procParams.keys()
        
        def get_input_parameters_count(self):
            inputParams = [x for x in self.procParams.values() if "IN" in x[1].upper()]
            return len(inputParams)
        
        def __str__(self):
            return str(
                       str(self.identifier) + os.linesep +
                       str(self.procStartIndex) + os.linesep + 
                       str(self.procName) + os.linesep 
                       + str(map(str,self.procParams)))                
                                
    
    def __init__(self, procs_data):
        
        #Build a list of Procedure objects
        proceduresList = self._build_procedures_list(procs_data)
        #Build the internal structure which manage the procedure objects
        self._proceduresMap = self._buildProceduresMap(proceduresList)
        
        #Initialize the procedure names subset to empty list      
        self._proceduresSubSet = list()
        
        self.packageName = "packageName" #TODO package name
        
        #Build the attribute that will be used by the user
        self.procedures = self._build_procedures()
    
    
    def _buildProceduresMap(self, proceduresList):
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
            procObj = OraclePackageDoc.Procedure()
            self._add_comment_to_proc_obj(p[1], procObj)
            self._add_signature_to_proc_obj(p[0], p[2], procObj)
            self._add_body_to_proc_obj(p[3], procObj)
            procObj.identifier= procObj._buildIdentifier()        
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
                      
        match = re.search(PTRN_PROCEDURE_NAME, segnatureBlock)
        procName = match.group()[:-1]            
        match = re.search(PTRN_PARAMETERS_BLOCK, segnatureBlock, flags = re.S) #flags = re.DOTALL
        paramsBlock = match.group()[1:-1]
        
        #=======================================================================
        # Parameters Parsing
        #=======================================================================
        rowParamsList = paramsBlock.split(SPLIT_PARAMETER_TOKEN)
        params = list()        
        rowParam = str()
        startIndex = None
        for rowParam in rowParamsList:        
            startIndex = rowParam.upper().find(FIND_START_PARAMETER_DECLARATION)                
            #first three elements of the list obtained splitting rowParam by a n-whitespace token
            params += [rowParam[startIndex:].split()]
        
        proc.procName = procName
        proc.procStartIndex = procIndex
        proc.addProcParamFromList(params)      
        
    
    
    def _add_body_to_proc_obj(self, bodyBlock, proc):
        """
        """
        pass
    
    #Utility
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
            self.procedures = self._build_procedures()
        else:
            raise Exception("proceduresNames isn't a list")
        
    def __str__(self):
        result = [self.packageName]
        for p in self.procedures:
            result.append(str(p))
        return os.linesep.join(result)    
