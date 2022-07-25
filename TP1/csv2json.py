import ply.lex as lex
import sys
import re

tokens = ["SEPARATOR", "DATA", "NEWLINE", "LISTSIZE", "AGREGATION"]

states = [
    ("header", "inclusive"),
    ("listReader", "inclusive")
]

#verify if list element is a digit

def is_number_regex(s):
    if re.match("^\d+?\.\d+?$", s) is None:
        return s.isdigit()
    return True


def t_header_LISTSIZE(t):
    r'{(?P<min>\d+)(,(?P<max>\d+))?}'
    minSize = int(t.lexer.lexmatch.group("min"))
    maxSizeStr = t.lexer.lexmatch.group("max")

    if maxSizeStr:
        maxSize = int(t.lexer.lexmatch.group("max"))
    else:
        maxSize = minSize

    lexer.maxSize = maxSize
    lexer.context.pop(lexer.index)
    lexer.context.append("inicioLista")
    for i in range(minSize-2):          # menos 2 é o inicioLista
        lexer.context.append("lista")

    if maxSize > 1:
        for i in range(maxSize-minSize+1):
            lexer.context.append("fimLista")

    for j in range(maxSize-1):
        lexer.headers.append(lexer.headers[lexer.index])
        lexer.agregation.append("no_Agregation")


def t_header_SEPARATOR(t):
    r','
    lexer.index += 1


def t_header_DATA(t):
    r'[^:,\n{]+'
    lexer.context.append("normal")
    lexer.agregation.append("no_Agregation")
    lexer.headers.append(t.value)


def t_header_NEWLINE(t):
    r'\n'

    if(lexer.context[0] == "inicioLista"):
        t.lexer.begin('listReader')
    else:
        t.lexer.begin("INITIAL")

    lexer.jsonFile.write('\t{\n')
    lexer.index = 0

    lexer.line += 1


def t_header_AGREGATION(t):
    r'::(?P<func>\w+),'
    agreg_func = t.lexer.lexmatch.group("func")

    if (agreg_func == 'sum') or (agreg_func == 'media') or (agreg_func == 'max') or (agreg_func == 'min'):
        for i in range(lexer.maxSize):
            lexer.agregation.pop(lexer.index)
            lexer.agregation.append(agreg_func)
            columnName = lexer.headers.pop(lexer.index)
            lexer.headers.append(columnName + "_" + agreg_func)
        # reset the max size variable after filling the agregation array
        lexer.maxSize = 0


def t_listReader_DATA(t):
    r'[^,\n]+'
    lexer.opList.append(t.value)


def writeList(t, separator):
    if(is_number_regex(lexer.opList[0])):
        lexer.jsonFile.write(
            '\t\t"' + lexer.headers[lexer.index] + '" : [' + lexer.opList[0])
    else:
        lexer.jsonFile.write(
            '\t\t"' + lexer.headers[lexer.index] + '" : [' + '"' + lexer.opList[0] + '"')

    # calcular onde começa a lista

    i = lexer.index

    while lexer.context[i] != "inicioLista":
        i -= 1

    if(lexer.context[i + len(lexer.opList) - 1]) != "fimLista":
        print(
            "O ficheiro CSV possui um erro nos limites da lista na linha " + str(lexer.line))

    for j in range(len(lexer.opList)-1):

        if(is_number_regex(lexer.opList[j+1])):
            lexer.jsonFile.write(
                str("," + lexer.opList[j+1]))
        else:
            lexer.jsonFile.write(
                str("," + '"' + lexer.opList[j+1] + '"'))

    if(separator):
        lexer.jsonFile.write(
            str("],\n")
        )
        t.lexer.opList = []

    else:
        lexer.jsonFile.write(str("]\n\t}"))
        t.lexer.opList = []
        lexer.index = 0


def writeAgregation(t, separator):
    opValue = 0
    for i in range(len(lexer.opList)):
        if (lexer.agregation[lexer.index] == "sum"):
            opValue += int(lexer.opList[i])
        elif (lexer.agregation[lexer.index] == "media"):
            opValue += int(lexer.opList[i])

    # caso a operação pretendida seja a media, temos que dividir pelo nº total de elementos
    if lexer.agregation[lexer.index] == "media":
        opValue = opValue/len(lexer.opList)
    elif lexer.agregation[lexer.index] == "max":
        opValue = max(lexer.opList)
    elif lexer.agregation[lexer.index] == "min":
        opValue = min(lexer.opList)
    if(separator):

        lexer.jsonFile.write(
            '\t\t"' + lexer.headers[lexer.index] + '" : ' + str(opValue) + ',\n')

    else:
        lexer.jsonFile.write(
            '\t\t"' + lexer.headers[lexer.index] + '" : ' + str(opValue) + '\n\t}')

    t.lexer.opList = []


def t_listReader_NEWLINE(t):
    r'\n'
    if lexer.context[lexer.index] == "fimLista" and lexer.agregation[lexer.index] == "no_Agregation":
        writeList(t, False)
        lexer.begin('INITIAL')
        lexer.jsonFile.write(',\n\t{\n')

    elif lexer.context[lexer.index] == "fimLista" and lexer.agregation[lexer.index] != "no_Agregation":
        writeAgregation(t, False)
        lexer.begin('INITIAL')
        lexer.jsonFile.write(',\n\t{\n')

    lexer.index = 0

    if(lexer.context[lexer.index] == "inicioLista"):
        lexer.begin('listReader')


def t_listReader_SEPARATOR(t):
    r','

    if lexer.context[lexer.index] == "fimLista" and lexer.context[lexer.index+1] != "fimLista" and lexer.agregation[lexer.index] == "no_Agregation":
        writeList(t, True)
        lexer.begin('INITIAL')

    elif lexer.context[lexer.index] == "fimLista" and lexer.context[lexer.index+1] != "fimLista" and lexer.agregation[lexer.index] != "no_Agregation":
        writeAgregation(t, True)
        lexer.begin('INITIAL')

    if(lexer.context[lexer.index + 1] == "inicioLista"):
        lexer.begin('listReader')

    lexer.index += 1


def t_listReader_eof(t):

    if lexer.context[lexer.index] == "fimLista" and lexer.agregation[lexer.index] == "no_Agregation":
        writeList(t, False)

    elif lexer.context[lexer.index] == "fimLista" and lexer.agregation[lexer.index] != "no_Agregation":
        writeAgregation(t, False)

    return None


def t_SEPARATOR(t):
    r','

    if(lexer.context[lexer.index+1] == "inicioLista"):
        lexer.begin("listReader")

    lexer.index += 1


def t_DATA(t):
    r'[^,\n]+'

    if(lexer.index == len(lexer.headers) - 1):
        lexer.jsonFile.write(
            '\t\t"' + lexer.headers[lexer.index] + '" : "' + str(t.value) + '"\n\t}')

    else:
        lexer.jsonFile.write(
            '\t\t"' + lexer.headers[lexer.index] + '" : "' + str(t.value) + '",\n')


def t_NEWLINE(t):
    r'\n'
    lexer.index = 0

    if(lexer.context[0] == "inicioLista"):
        t.lexer.begin('listReader')
    else:
        t.lexer.begin("INITIAL")
    lexer.jsonFile.write(',\n\t{\n')
    lexer.line += 1


def t_error(t):
    print("Este token nao e reconhecido", t.value)
    t.lexer.skip(1)


# Criar instância de lex
lexer = lex.lex()


# state
# verificar se é necessário
filename = sys.argv[1]
csvFile = open(filename, 'r')
filenameFormatted = re.sub(r'(\w+).csv', r'\1', filename)
final_Filename = filenameFormatted + ".json"


lexer.context = []
lexer.headers = []
lexer.maxSize = 0
# em cada index indica se é para aplicar ou nao uma operacao de agregação
lexer.agregation = []
lexer.opList = []   # lista na qual se vai aplicar os operadores
lexer.jsonFile = open(final_Filename, "w", encoding="utf-8")
lexer.index = 0
lexer.line = 1


lexer.begin("header")


# Alimentar o lexer
lexer.jsonFile.write('[\n')

for line in csvFile:
    lexer.input(line)
    for tok in lexer:
        print(tok)


lexer.jsonFile.write('\n]')
