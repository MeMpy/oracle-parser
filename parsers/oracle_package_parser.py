# -*- coding: UTF-8 -*-
'''
Created on Jan 5, 2014

@author: ross
'''
import re

PTRN_SINGLE_LINE_COMMENT = r'\s*--'
PTRN_BEGIN_BLOCK_COMMENT = r'\s*/\*'
PTRN_END_BLOCK_COMMENT = r'\*/'
PTRN_SINGLE_LINE_COMMENT_SUBS = r'\s*--.*'
PTRN_BLOCK_COMMENT_SUBS = r'\s*/\*.*\*/'
PTRN_START_PROCEDURE_BLOCK = r'\s*PROCEDURE'
PTRN_START_FUNCTION_BLOCK = r'\s*FUNCTION'
PTRN_END_PROC_FUNC_BLOCK_BRACKET = r'\)\s*\n'
PTRN_END_PROC_FUNC_BLOCK_IS = r'\bIS\b'
PTRN_END_PROC_FUNC_BLOCK_AS = r'\bAS\b'
PTRN_PACKAGE = r'\s*CREATE OR REPLACE PACKAGE|\s*CREATE PACKAGE'


SINGLE_WHITE_SPACE = ' '

def _clean_line_from_comments(line):
    """
    Clean the line from single line comment using regular expression
    """
    lineNoComment = re.sub(PTRN_SINGLE_LINE_COMMENT_SUBS, SINGLE_WHITE_SPACE, line)
    lineNoComment = re.sub(PTRN_BLOCK_COMMENT_SUBS, SINGLE_WHITE_SPACE, lineNoComment)
    return lineNoComment

def _check_comment(line, isInCommentBlock):
        """
        Check if we are still in a comment block or
        if we are in a comment line
        or if we are entering or leaving a comment bock
        using regular expression (default behavior)
        """
        isComment = False
        isBlockComment = isInCommentBlock
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
    
def _check_is_in_signature(line, isInSignature):
        """
        Check if we are still in a signature block 
        or if we are entering or leaving a signature bock
        using regular expression (default behavior)
        """            
        #Clean the line from the single line comment        
        lineNoComment = _clean_line_from_comments(line)
        if not isInSignature: #We don't come from a signature block         
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
            #else we still are in a signature block
            return True

def _check_is_in_body_block(line, isInBody):
    """
    This isn't implemented in the default behavior
    """
    return False


def _check_for_package_name(line):
    """
    If the line seems to 
    CREATE OR REPLACE PACKAGE BODY <package_name> AS
    returns the package_name,
    else return None
    
    """
    if re.search(PTRN_PACKAGE, line):
        #We are in the correct line. We need to extract the package_name
        words = line.split()
        return words[-2] #The package_name must be the second-last word (before AS/IS)
    

def _build_comment_block(line, index):
    """
    Not Implemented in default behavior
    """
    return ''


def _build_signature_block(line, signatureLineIndex, procSignature, index = None):
    """
    Simply append the new signature line to the buffer 
    NOTE: this also append the last line when isInSignature become false 
    (default behavior)
    @param index: The index of the actual line
    """
    #This check is needed because we can call this method more than once for a single line
    if signatureLineIndex != index:
        procSignature += _clean_line_from_comments(line)
        signatureLineIndex = index
    
    return procSignature, signatureLineIndex

def _build_procedure_body_block(line, index = None):
    """
    This isn't implemented in the default behavior
    """
    return ''



def parse(f, process_body = False):
    """    
    Legge dal body di un package sql oracle tutte le 
    dichiarazioni di procedure e funzioni e le memorizza 
    in una lista come stringhe    
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
    ritorna la lista con i blocchi creati
    
    NOTA: Al momento non sono presi in considerazione il blocco dei commenti in testa alla procedura, 
    il blocco body e il nome del package
    """     
    package_name = None
    
    #Config and params
    isInSignature = None
    signatureLineIndex = None
    
    isInBody = None
    bodyLineIndex = None
    
    isComment = None
    isInCommentBlock = None
    commentLineIndex = None
    
    #=======================================================================
    # Strings which identify a procedure part. They will be requested from the gets to build a procedure record
    #=======================================================================
    procComment = str()
    procSignature = str()
    procBody = str()
    
    
    line = str()
    procs = list()        
    procIndex = None
    procedureParsed = tuple()
    
    for count, line in enumerate(f):
        isComment, isInCommentBlock = _check_comment(line, isInCommentBlock) #value of the previous step
        if isComment or isInCommentBlock:
            #We are in a comment or in a comment block
            procComment = _build_comment_block(line, count)
            isInBody, isInSignature = False, False
        else:
            #check for package name
            if not package_name:
                package_name = _check_for_package_name(line)
            #We aren't in a comment
            if not isInBody:
                #Check and Eventually Process Signature
                if not(isInSignature) and _check_is_in_signature(line, isInSignature): #value of the previous step
                    #We are just entering into procedure signature
                    procIndex = count
                    isInSignature = True
                    procSignature, signatureLineIndex = _build_signature_block(line, signatureLineIndex, procSignature, count)
                elif isInSignature and _check_is_in_signature(line, isInSignature): #value of the previous step
                    #We are still into procedure signature
                    procSignature, signatureLineIndex = _build_signature_block(line, signatureLineIndex, procSignature, count)
                
                #This check must be done always because a signature can begin and terminate on the same line
                if isInSignature and not _check_is_in_signature(line, isInSignature): #value of the previous step
                    #We are just finished to read the signature
                    isInSignature = False
                    #build for the last time the signature block if necessary
                    procSignature, signatureLineIndex = _build_signature_block(line, signatureLineIndex, procSignature, count)
                    if not process_body:
                        procedureParsed = (procIndex, procComment, procSignature, None)
                        procComment = str()
                        procSignature = str()
                        procs.append(procedureParsed)
                                        
            if process_body and not isInSignature:
                #Check and Eventually Process block
                if not(isInBody) and _check_is_in_body_block(line, isInBody): #value of the previous step
                    #We are just entering into procedure block
                    isInBody = True
                    procBody =  _build_procedure_body_block(line, count)
                elif isInBody and _check_is_in_body_block(line, isInBody): #value of the previous step
                    #We are still into procedure body
                    procBody = _build_procedure_body_block(line, count)
                elif isInBody and not _check_is_in_body_block(line, isInBody): #value of the previous step
                    #We are just finished to read the body
                    isInBody = False
                    procedureParsed = (procIndex, procComment, procSignature, procBody)
                    procComment = str()
                    procSignature = str()
                    procBody = str()
                    procs.append(procedureParsed)
    #end for                    
    return package_name, procs