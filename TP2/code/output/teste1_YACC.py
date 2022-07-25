import ply.yacc as yacc
from teste1_LEXER import tokens

precedence=[
	('left','+','-'),
	('left','*','/'),
	('right','UMINUS'),
]

def p_stat0(p):
	"stat :  VAR '=' exp"
	ya.ts[p[1]] = p[3] 


def p_stat1(p):
	"stat :  exp"
	print(p[1]) 


def p_exp2(p):
	"exp :  exp '+' exp"
	p[0] = p[1] + p[3] 


def p_exp3(p):
	"exp :  exp '-' exp"
	p[0] = p[1] - p[3] 


def p_exp4(p):
	"exp :  exp '*' exp"
	p[0] = p[1] * p[3] 


def p_exp5(p):
	"exp :  exp '/' exp"
	p[0] = p[1] / p[3] 


def p_exp6(p):
	"exp :  '-' exp %prec UMINUS"
	p[0] = -p[2] 


def p_exp7(p):
	"exp :  '(' exp ')'"
	p[0] = p[2] 


def p_exp8(p):
	"exp :  NUMBER"
	p[0] = p[1] 


def p_exp9(p):
	"exp :  VAR"
	p[0] = getval(p[1]) 


def p_error(t):
	print(f"Syntax error at '{t.value}', [{t.lexer.lineno}]")

def getval(n):
	if n not in ts: print(f"Undefined name '{n}'")
	return ts.get(n,0)


ya = yacc.yacc()

#symboltable : dictionary of variables
ya.ts = { }

ya.parse("3+4*7")