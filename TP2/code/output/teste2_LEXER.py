import ply.lex as lex

literals = ['l']		#i

ignore = " \t\n"

tokens = ['DELIM_ABRIR','SEPARATOR','NUM','PAL','DELIM_FECHAR']


def t_DELIM_ABRIR(t):
	r'\['
	return(t)

def t_SEPARATOR(t):
	r','
	return(t)

def t_NUM(t):
	r'[0-9]+'
	return(t)

def t_PAL(t):
	r'[a-zA-Z]+'
	return(t)

def t_DELIM_FECHAR(t):
	r'\]'
	return(t)

def t_error(t):
	print(f"carater ilegal: ', t.value[0]")
	t.lexer.skip(1)


lexer = lex.lex()