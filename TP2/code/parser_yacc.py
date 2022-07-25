import os
import ply.yacc as yacc
from parser_lex import tokens
import sys
import re

def p_phrase(p):
    "phrase : lex yacc" #falta yacc

def p_lex(p):
    "lex : LEXMARKER literals ignore tokens functions"

    #write imports

    parser.outPutLexer.write('import ply.lex as lex\n\n')

    #write literals

    literals = p[2][0]
    literalsComment = p[2][1]


    parser.outPutLexer.write('literals = [')

    for index,x in enumerate(literals):
        if(x != '"'):
            parser.outPutLexer.write('\'' + x + '\'')
        if(index != len(literals) -1 and index != 0 and index != len(literals) -2):
            parser.outPutLexer.write(',')

    parser.outPutLexer.write(']\t\t' + '#' + literalsComment + '\n\n')

    # write ignore

    ignore = p[3][0]
    ignoreComment = p[3][1]
    parser.outPutLexer.write('ignore = ' + ignore)
    if(ignoreComment):
        parser.outPutLexer.write('#' +'\t\t' + ignoreComment + '\n\n')
    else:
        parser.outPutLexer.write('\n\n')


    # write tokens

    tokens = p[4][0].split(',')
    tokensComment = p[4][1]

    parser.outPutLexer.write('tokens = [')

    for index,token in enumerate(tokens):
    
        parser.outPutLexer.write('\'' + token + '\'')
        if(index != len(tokens) -1):
            parser.outPutLexer.write(',')
    parser.outPutLexer.write(']')

    if(tokensComment):
        parser.outPutLexer.write('#' +'\t\t' + tokensComment + '\n\n')
    else:
        parser.outPutLexer.write('\n\n\n')


    #write functions

    functions = p[5]

    for function in functions:
        comment = function[2]
        functionName = function[1][0] #no caso de ser uma função de erro functionName vai conter o print
        functionRE = function[0].split(' return')
        functionReturnType = function[1][1] #no caso de ser uma função de erro conterá o tratamento

        if(comment):
            parser.outPutLexer.write(f"#{comment}")

        if(len(functionRE) != 2):
            #error case
            functionRE = function[0].split(' error')
            parser.outPutLexer.write('def t_error(t):\n\t')
            parser.outPutLexer.write(f"print({functionName})\n\t")
            parser.outPutLexer.write(f"{functionReturnType}\n")

        else:
            #function case
            
            parser.outPutLexer.write('def t_' + functionName + '(t):\n\t')
            parser.outPutLexer.write(f"r'{functionRE[0]}'\n\t")
            
            #verify return type

            match = re.search(r'([a-zA-Z]+)\([^\)]*\)(\.[^\)]*\))?', functionReturnType)
            
            #modify the return
            
            if match:
                nameModifyFunction = match.group(1)
                parser.outPutLexer.write(f"t.value = {nameModifyFunction}(t.value)\n\t")
                 
            parser.outPutLexer.write('return(t)\n\n')

    #write build lex

    parser.outPutLexer.write('\n\nlexer = lex.lex()')



def p_literals(p):
    "literals : LITERALS EQUAL CHARACTERS comment"
    p[0] = ((p[3]),p[4])
    parser.literals = p[0][0]
    
def p_literals_empty(p):
    "literals : "
    p[0] = "literals vazio"

def p_comment(p):
    "comment : HASHTAGS words NEWLINE"
    p[0] = p[2]
    

def p_comment_empty(p):
    "comment : "
    p[0] = ""
    

def p_words(p):
    "words : words WORD"
    p[0] = p[1] + ' ' +p[2]

def p_words_stop(p):
    "words : WORD"
    p[0] = p[1]

def p_ignore(p):
    "ignore : IGNORE EQUAL CHARACTERS comment"
    p[0] = (p[3],p[4])

def p_ignore_empty(p):
    "ignore : "

def p_tokens(p):
    "tokens : TOKENS EQUAL SLEFTBRACKET tokenNames SRIGHTBRACKET comment"
    p[0] = (p[4],p[6])
    parser.tokens = p[4]

def p_tokens_empty(p):
    "tokens : "

def p_tokenNames(p):
     "tokenNames : tokenNames COMMA SQM UPPERWORD SQM"
     p[0] = p[1] + ',' + p[4]

def p_tokenNames_stop(p):
    "tokenNames : SQM UPPERWORD SQM"
    p[0] = p[2]

def p_functions(p):
    "functions : functions function"
    p[0] = p[1] + [p[2]]

def p_functions_empty(p):
    "functions : "
    p[0] = []

def p_function(p):
    "function : RE LEFTBRACKET content RIGHTBRACKET comment "
    p[0] = (p[1],p[3],p[5])


def p_content_returned(p):
    "content : SQM UPPERWORD SQM COMMA EXPRESSION"
    p[0] = (p[2],p[5])

def p_content_returnedWord(p):
    "content : SQM UPPERWORD SQM COMMA WORD"
    p[0] = (p[2],p[5])

def p_content_string(p):
    "content : STRING COMMA EXPRESSION"
    p[0] = (p[1],p[3])


def p_content_characters(p):
    "content : CHARACTERS COMMA EXPRESSION"
    p[0] = (p[1],p[3])


#YACC


def p_yacc(p):
    "yacc : YACCMARKER precedence vars prods PERCENTAGE functionsyacc inityacc parse"


    #tokens error

    for token in parser.tokensUsed:
        if not token in parser.tokens.split(','):
            print(f"Token {token} usado sem ser definido")
    


    #write imports

    parser.outPutYacc.write('import ply.yacc as yacc\n')
    lexerName = "from " + filename.replace(".txt","") + "_LEXER" + " import" + " tokens" + '\n\n'

    parser.outPutYacc.write(lexerName)

    # write precedence

    precedence = p[2]
    parser.outPutYacc.write(precedence + '\n\n')


    #prods

    #parsing all vars

    vars = p[3][1]

    for var in vars:
        parser.yaccVars.append(var.split(' =')[0])


    comment_pos_vars = p[3][2]
    if comment_pos_vars:
        parser.outPutYacc.write('#' + '\t' + comment_pos_vars + '\n')
   

    prods = p[4]

    for index,prod in enumerate(prods):
        code = prod[2]
        codeParsed = ""

        for var in parser.yaccVars:
            code = re.sub(var,p[7][0] + '.' + var,code)

        for codeline in code.split(';'):
            if ':' in codeline:
                splited = codeline.split(':')
                codeParsed = codeParsed + '\t' + splited[0] + ':' 
                for i in range(1,len(splited)):
                    codeParsed = codeParsed + '\n\t\t'+ splited[i] +'\n\t'

            else:
                codeParsed = codeParsed + '\t' + codeline + '\n'

      

        func = f'def p_{prod[0]}{index}(p):\n\t"{prod[0]} : {prod[1]}"\n{codeParsed}\n\n'
        parser.outPutYacc.write(func)

    # functionsYacc
    functionsyacc = p[6]

    parser.outPutYacc.write(functionsyacc)

    #INTYACC
    inityacc = p[7][0]
    commentyacc = p[7][1]
    parser.outPutYacc.write('\n' + inityacc + " = yacc.yacc()" + '\n\n')
    
    
    if commentyacc:
        parser.outPutYacc.write("#" + commentyacc + '\n')



    # vars

    
    comment = p[3][0]

    parser.outPutYacc.write("#" + comment + '\n')
    
    for var in vars:
        parser.outPutYacc.write(p[7][0] + '.' + var + "\n")

    parser.outPutYacc.write("\n")


    #parse
    parse = p[8]


    if parse[0].split(".")[0] == inityacc and parse[0].split(".")[1] == "parse" :
        if parse[4]:
            parser.outPutYacc.write(parse[0] + parse[1] + parse[2] + parse[3] + "\n# " + parse[4])
        else: 
            parser.outPutYacc.write(parse[0] + parse[1] + parse[2] + parse[3])
    else:
        print("ERROR! Check your 'parse' function...")



    


def p_precedence(p):
    "precedence : PRECEDENCE EQUAL SLEFTBRACKET precedences SRIGHTBRACKET comment"
    if p[6]:
        p[0] = "precedence" + p[2] + p[3] + p[4] + "\n" + p[5] + "\n# " + p[6]
    else:
        p[0] = "precedence" + p[2] + p[3] + p[4] + "\n" + p[5]
   
def p_precedence_empty(p):
    "precedence : "
    p[0] = ""

def p_precedences_varios(p):
    "precedences : precedences tokenprecedence"
    p[0] = p[1] + "\n\t" + p[2]

def p_precedences_vazio(p):
     "precedences : "
     p[0] = ""

def p_tokenprecedence(p):
    "tokenprecedence : LEFTBRACKET rl COMMA nametokensprec RIGHTBRACKET COMMA" 
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5] + p[6]

def p_rl_r(p):
    "rl : SQM RIGHT SQM"
    p[0] = p[1] + p[2] + p[3]

def p_rl_l(p):
    "rl : SQM LEFT SQM"
    p[0] = p[1] + p[2] + p[3]

def p_nametokensprec(p):
    "nametokensprec :  nametokensprec COMMA SQM UPPERWORD SQM" 
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5]

def p_nametokensprec_char(p):
    "nametokensprec : nametokensprec COMMA SQM CHAR SQM" 
    p[0] = p[1] + p[2] + p[3] + p[4] + p[5]
    if not p[4] in parser.literals:
        print(f"Literal {p[4]} Usado Sem ser definido")


def p_nametokensprec_char_single(p):
    "nametokensprec : SQM CHAR SQM"
    p[0] = p[1] + p[2] + p[3]
    if not p[2] in parser.literals:
        print(f"Literal {p[2]} Usado Sem ser definido")
        


def p_nametokensprec_upperword_single(p):
    "nametokensprec : SQM UPPERWORD SQM"
    p[0] = p[1] + p[2] + p[3]


def p_vars(p):
    "vars : varsdesc varsaux comment"
    p[0] = (p[1],p[2],p[3])

def p_varsdesc(p):
    "varsdesc : HASHTAG words NEWLINE"
    p[0] = p[2]   

def p_varsaux_empy(p):
    "varsaux : "
    p[0] = []

def p_varsaux(p):
    "varsaux : varsaux var "
    p[0] = p[1] + [p[2]]



def p_var(p):
    "var :  CONTENTVAR changeline"         
    p[0] = p[1]

def p_changeline(p):
    "changeline :  NEWLINE"         

def p_changeline2(p):
    "changeline :  DOUBLENEWLINE"         
    



def p_prods(p):
    "prods : prods prod"
    p[0] = p[1] + [p[2]]

def p_prods_empty(p):
    "prods : "
    p[0] = []
    
def p_prod(p):
    "prod : WORD WORD expProd LEFTCOTTER CHARS RIGHTCOTTER"
    p[0] = (p[1],p[3],p[5])


def p_expProd_token(p):
    "expProd : expProd UPPERWORD"
    p[0] = p[1] + ' ' + p[2]
    parser.tokensUsed.append(p[2])
    

def p_expProd_terminal(p):
    "expProd : expProd WORD"
    p[0] = p[1] + ' ' + p[2]

def p_expProd_terminalLiteral(p):
    "expProd : expProd SQM CHAR SQM"
    p[0] = p[1] + ' ' + '\'' + p[3]+ '\''
    if not p[3] in parser.literals:
        print(f"Literal {p[3]} Usado Sem ser definido")

def p_expProd_terminalEqual(p):
    "expProd : expProd SQM EQUAL SQM"
    p[0] = p[1] + ' '+ '\'' + p[3] + '\''
    if not p[3] in parser.literals:
        print(f"Literal {p[3]} Usado Sem ser definido")

def p_expProd_leftbracket(p):
    "expProd : expProd SQM LEFTBRACKET SQM"
    p[0] = p[1] + ' '+ '\'' + p[3] + '\''
    if not p[3] in parser.literals:
        print(f"Literal {p[3]} Usado Sem ser definido")

def p_expProd_rightbracket(p):
    "expProd : expProd SQM RIGHTBRACKET SQM"
    p[0] = p[1] + ' '+ '\'' + p[3] + '\''
    if not p[3] in parser.literals:
        print(f"Literal {p[3]} Usado Sem ser definido")


def p_expProd_markerPrec(p):
    "expProd : expProd markerPrec"
    p[0] = p[1] + ' ' +  p[2]
    

def p_expProd_vazio(p):
    "expProd : "
    p[0] = ""

def p_markerPrec(p):
    "markerPrec : PRECTAG UPPERWORD"
    p[0] = "%prec " + p[2]




def p_functionsyacc(p):
    "functionsyacc : functionsyacc functionyacc comment"
    if p[3]:
        p[0] = p[1] + p[2] + "# " + p[3] + "\n\n"
    else:
        p[0] = p[1] + p[2]

def p_functionsyacc_empty(p):
    "functionsyacc : "
    p[0] = ""

def p_functionyacc(p):
    "functionyacc : FUNCTION BODYFUNCTIONLINE bodyfunction BODYFUNCTIONFINAL " 
    p[0] = p[1] + " " + p[2] + p[3] + "\t" + p[4]

def p_bodyfunction(p):
    "bodyfunction : bodyfunction BODYFUNCTIONLINE"
    p[0] = p[1] + "\t" + p[2]

def p_bodyfunction_empty(p):
    "bodyfunction : "
    p[0] = ""

def p_parse(p):
    "parse : WORD LEFTBRACKET CHARACTERS RIGHTBRACKET comment"
    p[0] = (p[1], p[2], p[3], p[4],p[5])


def p_inityacc(p):
    "inityacc : WORD EQUAL INITYACC comment"
    p[0] = (p[1],p[4])



def p_error(p):
      print(f"Illegal token yacc'{p}'")

      

# Build the parser
parser = yacc.yacc()

#Read Input File

filename = sys.argv[1]
inputDir = os.getcwd() + '/input/' + filename
input = open(inputDir, 'r').read()

#Create Output Files
outputDir = os.getcwd() + '/output/' + filename.replace(".txt","")

parser.outPutLexer = open(outputDir + "_LEXER.py", "w")
parser.outPutYacc = open(outputDir + "_YACC.py", "w")


parser.yaccVars = []
parser.tokensUsed = []





parser.parse(input)
