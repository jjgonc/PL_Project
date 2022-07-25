import ply.yacc as yacc
from teste2_LEXER import tokens



def p_lista0(p):
	"lista :  DELIM_ABRIR listaa"
	print(ya.soma)


def p_listaa1(p):
	"listaa :  lcont DELIM_FECHAR"
	#nothing 


def p_listaa2(p):
	"listaa :  DELIM_FECHAR"
	#nothing 


def p_lcont3(p):
	"lcont :  NUM lcontt"
	ya.comp += 1 


def p_lcont4(p):
	"lcont :  PAL lcontt"
	ya.comp += 1
	if p[1] == 'start':
		ya.soma += p[2]
	

def p_lcontt5(p):
	"lcontt :  SEPARATOR NUM lcontt"
	ya.comp += 1
	p[0] = int(p[2]) + p[3]


def p_lcontt6(p):
	"lcontt :  SEPARATOR PAL lcontt"
	ya.comp += 1
	p[0] = 0
	if p[2] == "start":
		 ya.soma += p[3]
		 


def p_lcontt7(p):
	"lcontt : "
	p[0] = 0


def p_error(p):
	print ("Error:",p)


ya = yacc.yacc()

#comentario inteligente
ya.comp = 0
ya.soma = 0
ya.counting = False
ya.output = 0
ya.operacao = 1             

ya.parse("[1,2,4,start,1,2,end]")