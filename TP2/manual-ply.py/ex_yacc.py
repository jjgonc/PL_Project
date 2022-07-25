
import ply.yacc as yacc
from ex_lex import tokens
 
precedence = (
    ('left','+','-'),
    ('left','*','/'),
    ('right','UMINUS')
)


# symboltable : dictionary of variables
def p_stat(t):
    "stat : VAR '=' exp"
    parser.ts[t[1]] = t[3]

def p_stat_2(t):
    "stat : exp"
    print(t[1])

def p_exp(t):
    "exp : exp '+' exp"
    t[0] = t[1] + t[3]

def p_exp_1(t):
    "exp : exp '-' exp"
    t[0] = t[1] - t[3]

def p_exp_2(t):
    "exp : exp '*' exp"
    t[0] = t[1] * t[3]

def p_exp_4(t):
    "exp : exp '/' exp"
    t[0] = t[1] / t[3]

def p_exp_6(t):
    "exp : '-' exp %prec UMINUS"
    t[0] = -t[2]

def p_exp_7(t):
    "exp : '(' exp ')'"
    t[0] = t[2]

def p_exp_8(t):
    "exp : NUMBER"
    t[0] = t[1]
  

def p_exp_9(t):
    "exp : VAR"
    t[0] = getval(t[1])

def p_error(t):
    print(f"Syntax error at '{t.value}', [{t.lexer.lineno}]")
    

def getval(n):
    if n not in parser.ts: print(f"Undefined name '{n}'")
    return parser.ts.get(n,0)





# Build the parser
parser = yacc.yacc()

parser.ts = {}

# Read line from input and parse it
import sys
for linha in sys.stdin:
    parser.success = True
    parser.parse(linha)
    if parser.success:
        print("Frase válida!")
    else:
        print("Frase inválida... Corrija e tente novamente!")