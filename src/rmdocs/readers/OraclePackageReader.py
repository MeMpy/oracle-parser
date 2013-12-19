# -*- coding: UTF-8 -*-
'''
Created on 30/ago/2013

Replaced on 1/nov/2013

@author: eroreng

'''

from os import path
import re

#===============================================================================
#                                 MODEL
#===============================================================================


#===============================================================================
#                             READER
# #NOTE: If too slow try using re.compile
#===============================================================================

SCRIPT_EXTENSION = ".sql"

PTRN_SINGLE_LINE_COMMENT = r'\s*--'
PTRN_BEGIN_BLOCK_COMMENT = r'\s*/\*'
PTRN_END_BLOCK_COMMENT = r'\*/'
PTRN_WHITE_SPACE_SUBS = r' +'
PTRN_PROCEDURE_NAME = r'\b\w*\s*\('
PTRN_PARAMETERS_BLOCK = r'\(.*\)' #Works only if there aren't parameters with comments (into which there is a ")")
PTRN_SINGLE_LINE_COMMENT_SUBS = r'\s*--.*'
PTRN_BLOCK_COMMENT_SUBS = r'\s*/\*.*\*/'
PTRN_START_PROCEDURE_BLOCK = r'\s*PROCEDURE'
PTRN_START_FUNCTION_BLOCK = r'\s*FUNCTION'
PTRN_END_PROC_FUNC_BLOCK_BRACKET = r'\)\s*\n'
PTRN_END_PROC_FUNC_BLOCK_IS = r'\bIS\b'
PTRN_END_PROC_FUNC_BLOCK_AS = r'\bAS\b'

SPLIT_PARAMETER_TOKEN = ','

FIND_START_PARAMETER_DECLARATION = "P"

FIND_END_PACKAGE_NAME = "."

SINGLE_WHITE_SPACE = ' '

OPEN_FILE_MODE = "r"


#===============================================================================
#                                         ENTRY POINT
#===============================================================================
def buildReader(filePath):
    """
    """
    return ProcedureParser(filePath)
    
    

class ProcedureParser(object):
    """    
    Legge dal body di un package sql oracle tutte le 
    dichiarazioni di procedure e funzioni e memorizza 
    tutti i rispettivi parametri compreso tipo
    e il modificatore di input/output.
    Inoltre coserva il numero di linea in cui è
    stata trovata la procedura/funzione
    
    Algoritmo:
    Per ogni linea che non sia un comment block o una linea di commento:
        1)Pulisci la linea da eventuali commenti
        2)Se nella linea si trova la dichiarazione di una procedure/funzione allora
            -Inizia a memorizzare le linee che trovi
            fino a quando la linea corrente non contiene un terminatore della dichiarazione
            @see PTRN_END_PROC_FUNC_*
        3)altrimenti ignora la linea
    Ottenuta la lista contenente tutte le dichiarazioni di procedure e funzioni come stringhe
    Per ogni procedure/funzione
        1) Leggi il nome tramite re: @see PTRN_PROCEDURE_NAME
        2) Leggi il blocco tramite re: @see PTRN_PARAMETERS_BLOCK
            Per ogni parametro:
                1)Pulisci tutto ciò che c'è prima dell'inizio del nome del parametro e trimma
                2)Splitta la linea trimmata per ' '
                3)Ritorna solo i primi tre elementi: (paramName, inOutType, type)                    
        3) Costruisci l'oggetto Procedure
        4) Costruisci la lista delle Procedure
    Infine:
        Costruisci l'oggetto ProcedureReader passando la lista sopra creata

    Aggiunta: Lettura package name dal nome del file:
    Il nome del file deve essere per convenzione così fatto:
    b_<nomePackege>.sql
    
    NOTA:
    Per aggiungere funzionalità al parser è possibile estenderlo e sovrascrivere i metodi chiave:
    check_is_in_* = Utilizzato per controllare in che posizione del packege siamo. Valorizza le relative flag che
                permettono al parser di spostarsi in maniera intelligente
    build_*_block = Costruisce linea per linea il blocco di tipo stringa contenente tutto il corpo di una parte 
                    di procedura: (commenti, firma, body). Deve valorizzare gli attributi utilizzati dal builder
                    per costruire l' oggetto procedura
    get_*_block = Semplicemente ritorna il blocco costruito in precedenza
    add_*_to_proc_obj = Dato l'oggetto procedura e dato il blocco stringa relativo ad una parte di procedura codifica
                        tale stringa all'interno dell'oggetto Procedure
    """
    
    def build_package_name(self):
        """
        Build the package name from the file base name
        (default behavior)
        """
        fileBaseName = path.basename(self.file_path)
        self.packageName = fileBaseName[2: fileBaseName.find(FIND_END_PACKAGE_NAME)]
        
    
    def __init__(self, filePath, processBody = False):
        """
        @param filePath: full file path in sql format
        @param processBody: True if the parser must parse the body too else it will parse only the signature 
        """
        if path.splitext(filePath)[1] <> SCRIPT_EXTENSION:
            raise Exception("The file {0} isn't a .sql script".format(filePath))
        
        #public data
        self.file_path = filePath;            
        self.build_package_name()
        self.procs = None
        
        #Config and params
        self._process_body = processBody
        self.isInSignature = None
        self.signatureLineIndex = None
        self.isInBody = None
        self.bodyLineIndex = None
        self.isComment = None
        self.isInCommentBlock = None
        self.commentLineIndex = None
        
        #=======================================================================
        # Strings which identify a procedure part. They will be requested from the gets to build a procedure record
        #=======================================================================
        self._procComment = str()
        self._procSignature = str()
        self._procBody = str()
        
        self._parse()
    
    def check_comment(self, line):
        """
        Check if we are still in a comment block or
        if we are in a comment line
        or if we are entering or leaving a comment bock
        using regular expression (default behavior)
        """
        isComment = False
        isBlockComment = self.isInCommentBlock
        if not isBlockComment: #we don't come from a comment block
            #check if it a line comment or a block comment on a single line
            if (re.match(PTRN_SINGLE_LINE_COMMENT, line) or
                (re.match(PTRN_BEGIN_BLOCK_COMMENT, line) and
                 re.search(PTRN_END_BLOCK_COMMENT, line))):
                isComment = True
            else:
                isComment = False        
                if re.match(PTRN_BEGIN_BLOCK_COMMENT, line):
                    isBlockComment = True #we are entering in a comment block
        elif re.search(PTRN_END_BLOCK_COMMENT, line): #we come from a block comment
            #we are leaving from a block comment
            isBlockComment = False
        return isComment, isBlockComment
        
    
    def build_comment_block(self,line, index):
        """
        Not Implemented in default behavior
        """
        pass
    
    def _clean_line_from_comments(self, line):
        """
        Clean the line from single line comment using regular expression
        """
        lineNoComment = re.sub(PTRN_SINGLE_LINE_COMMENT_SUBS, SINGLE_WHITE_SPACE, line)
        lineNoComment = re.sub(PTRN_BLOCK_COMMENT_SUBS, SINGLE_WHITE_SPACE, lineNoComment)
        return lineNoComment
    
    def check_is_in_signature(self, line):
        """
        Check if we are still in a signature block 
        or if we are entering or leaving a signature bock
        using regular expression (default behavior)
        """
        #Clean the line from the single line comment
        lineNoComment = self._clean_line_from_comments(line)
        if not self.isInSignature: #We don't come from a signature block         
            #Check if the line contains the beginning of a procedure
            if re.match(PTRN_START_PROCEDURE_BLOCK, lineNoComment, re.I) or re.match(PTRN_START_FUNCTION_BLOCK, lineNoComment, re.I):
                return True
            else:
                return False
        #We come from a signature block
        elif (re.search(PTRN_END_PROC_FUNC_BLOCK_BRACKET, lineNoComment) or
              re.search(PTRN_END_PROC_FUNC_BLOCK_IS, lineNoComment) or
              re.search(PTRN_END_PROC_FUNC_BLOCK_AS, lineNoComment)):
            #if the signature block ends
            return False
        else:
            #else we are still in a signature block
            return self.isInSignature
    
    def build_signature_block(self, line, index = None):
        """
        Simply append the new signature line to the buffer 
        NOTE: this also append the last line when self.isInSignature become false 
        (default behavior)
        @param index: The index of the actual line
        """
        if self.signatureLineIndex != index:
            self._procSignature += self._clean_line_from_comments(line)
            self.signatureLineIndex = index
        
    
    def check_is_in_body_block(self, line):
        """
        This isn't implemented in the default behavior
        """
        return False
    
    def build_procedure_body_block(self, line, index = None):
        """
        This isn't implemented in the default behavior
        """
        pass
    
    def get_comment_block(self):
        """
        Return the comment string and clear the buffer
        (default)
        """        
        temp =  self._procComment
        self._procComment = str()
        return temp
    
    def get_signature_block(self):
        """
        Return the signature string and clear the buffer
        (default)
        """
        temp =  self._procSignature
        self._procSignature = str()
        return temp
    
    def get_body_block(self):
        """
        Return the body string and clear the buffer
        (default always an empty string)
        """
        temp =  self._procBody
        self._procBody = str()
        return temp
    
    
    def _parse(self):
        """
        TODO Spiegazione algoritmo
        """
        f = open(self.file_path, OPEN_FILE_MODE)
        line = str()
        procs = list()        
        procIndex = None
        procedureParsed = tuple()
        with f:
            for count, line in enumerate(f):
                self.isComment, self.isInCommentBlock = self.check_comment(line)
                if self.isComment or self.isInCommentBlock:
                    #We are in a comment or in a comment block
                    self.build_comment_block(line, count)
                    self.isInBody, self.isInSignature = False, False
                else:
                    #We aren't in a comment
                    if not self.isInBody:
                        #Check and Eventually Process Signature
                        if not(self.isInSignature) and self.check_is_in_signature(line):
                            #We are just entering into procedure signature
                            procIndex = count
                            self.isInSignature = True
                            self.build_signature_block(line,count)
                        elif self.isInSignature and self.check_is_in_signature(line):
                            #We are still into procedure signature
                            self.build_signature_block(line, count)
                        
                        #This check must be done always because a signature can begin and terminate on the same line
                        if self.isInSignature and not self.check_is_in_signature(line):
                            #We are just finished to read the signature
                            self.isInSignature = False
                            #build for the last time the signature block if necessary
                            self.build_signature_block(line, count)
                            if not self._process_body:
                                procedureParsed = (procIndex, self.get_comment_block(), self.get_signature_block(), None)
                                procs.append(procedureParsed)
                                                
                    if self._process_body and not self.isInSignature:
                        #Check and Eventually Process block
                        if not(self.isInBody) and self.check_is_in_body_block(line):
                            #We are just entering into procedure block
                            self.isInBody = True
                            self.build_procedure_body_block(line, count)
                        elif self.isInBody and self.check_is_in_body_block(line):
                            #We are still into procedure body
                            self.build_procedure_body_block(line, count)
                        elif self.isInBody and not self.check_is_in_body_block(line):
                            #We are just finished to read the body
                            self.isInBody = False
                            procedureParsed = (procIndex, self.get_comment_block(), self.get_signature_block(), self.get_body_block())
                            procs.append(procedureParsed)
                            
            #end with f:
            self.procs = procs                