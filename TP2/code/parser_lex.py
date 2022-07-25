
import ply.lex as lex

tokens = ["LEXMARKER","LITERALS", "EQUAL","CHARACTERS","HASHTAG","HASHTAGS", "CONTENTVAR","WORD","NEWLINE",
        "DOUBLENEWLINE", "IGNORE", "TOKENS", "SLEFTBRACKET", "RIGHT","LEFT", "PRECTAG", "CHARS",
        "SRIGHTBRACKET", "COMMA", "SQM", "UPPERWORD","RE","LEFTBRACKET", "RIGHTBRACKET", "EXPRESSION",
        "STRING", "YACCMARKER", "INITYACC", "PRECEDENCE", "CHAR", "LEFTCOTTER", "RIGHTCOTTER"
        ,"PERCENTAGE","FUNCTION","BODYFUNCTIONLINE","BODYFUNCTIONFINAL"]


states = [
    ("newlineReader", "inclusive"),
    ("pythonReader" , "exclusive"),
    ("functionReader","exclusive"),
    ("varsReader","exclusive")
]


#vars reader

def t_varsReader_CONTENTVAR(t):
    r'[^\n]+'
    return(t)

def t_varsReader_DOUBLENEWLINE(t):
    r'\n\n'
    t.lexer.varsReader = False
    t.lexer.begin('INITIAL')
    return(t)


def t_varsReader_NEWLINE(t):
    r'\n'
    return(t)

t_varsReader_ignore = " \t"

def t_varsReader_error(t):
    print(f"Illegal character {t} lexer")
    t.lexer.skip(1)
    return(t)



#python reader

def t_pythonReader_CHARS(t):
    r'[^{}]+'
    return(t)


def t_pythonReader_RIGHTCOTTER(t):
    r'\}'
    t.lexer.begin('INITIAL')
    return(t)


t_pythonReader_ignore = " \t\n"

def t_pythonReader_error(t):
    print(f"Illegal character {t} lexer")
    t.lexer.skip(1)
    return(t)


#NEWLINE READER

def t_newlineReader_NEWLINE(t):
    r'\n'
    if(t.lexer.varsReader):
        t.lexer.begin('varsReader')

    else:
        t.lexer.begin('INITIAL')
    return(t)



t_newlineReader_ignore = " \t"


#function reader

def t_FUNCTION(t):
    r'def '
    t.lexer.begin('functionReader')
    return(t)

def t_functionReader_BODYFUNCTIONFINAL(t):
    r'.*\n\n'
    t.lexer.begin('INITIAL')
    return(t)

def t_functionReader_BODYFUNCTIONLINE(t):
    r'.*\n'
    return(t)

def t_functionReader_error(t):
    print(f"Illegal character {t} lexer")
    t.lexer.skip(1)
    return(t)



t_functionReader_ignore = " \t"

#INITIAL

t_ignore = " \t\n"

def t_INITYACC(t):
    r'yacc\(\)'
    return t

def t_PARSEYACC(t):
    r'parse'
    return t

def t_STRING(t):
    r'f".*"'
    return(t)


def t_RE(t):
    r'(?:.* return)|.* error'
    return(t)


def t_EXPRESSION(t):
    r'(?:[a-zA-Z.]+\([a-zA-Z.0-9]*\))'
    return(t)

def t_LEXMARKER(t):
    r'\%\%LEX'
    return(t)
    
def t_LITERALS(t):
    r'\%literals'
    return(t)
    
def t_EQUAL(t):
    r'='
    return(t)

def t_CHARACTERS(t):
    r'"[^"]+"'
    return(t)

def t_HASHTAGS(t):
    r'\#\#'
    t.lexer.begin('newlineReader')
    return(t)

def t_HASHTAG(t):
    r'\#'
    t.lexer.begin('newlineReader')
    t.lexer.varsReader = True
    return(t)


def t_UPPERWORD(t):
    r'[A-Z_]+'
    return(t)

def t_RIGHT(t):
    r'right'
    return(t)

def t_LEFT(t):
    r'left'
    return(t)     

def t_WORD(t):
    r'[a-zA-Z.:_]+'
    return(t)
    
def t_IGNORE(t):
    r'\%ignore'
    return(t)


def t_TOKENS(t):
    r'\%tokens'
    return(t)

def t_SLEFTBRACKET(t):
    r'\['
    return(t)
    
def t_SRIGHTBRACKET(t):
    r'\]'
    return(t)
    
def t_COMMA(t):
    r'\,'
    return(t)

def t_SQM(t):
    r'\''
    return(t)
      
def t_LEFTBRACKET(t):
    r'\('
    return(t)
    
def t_RIGHTBRACKET(t):
    r'\)'
    return(t)

def t_LEFTCOTTER(t):
    r'\{'
    t.lexer.begin('pythonReader')
    return(t)
        
def t_RIGHTCOTTER(t):
    r'\}'
    return(t)


# yacc 
def t_YACCMARKER(t):
    r'\%\%YACC'
    return(t)


def t_PRECEDENCE(t):
    r'\%precedence'
    return(t)

def t_PRECTAG(t):
    r'%prec'
    return(t)


def t_PERCENTAGE(t):
    r'%%'
    # t.lexer.begin('functionsReader')
    return(t)

def t_CHAR(t):
    r'.'
    return(t)


def t_error(t):
    print(f"Illegal character {t} lexer")
    t.lexer.skip(1)
    return(t)


lexer = lex.lex()
lexer.varsReader = False
