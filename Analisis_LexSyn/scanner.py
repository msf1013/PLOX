# Lista con nombres de tokens de palabras reservadas
reserved = {
   'class'   	  : 'CLASS',
   'under'      : 'UNDER',
   'main'       : 'MAIN',
   'new'        : 'NEW',
   'numeral'    : 'NUMERAL',
   'real'       : 'REAL',
   'bool'       : 'BOOL',
   'char'       : 'CHAR',
   'string'     : 'STRING',
   'hidden'     : 'HIDDEN',
   'visible'    : 'VISIBLE',
   'without'    : 'WITHOUT',
   'this'       : 'THIS',
   'true'       : 'TRUE',
   'false'      : 'FALSE',
   'return'     : 'RETURN',
   'if'         : 'IF',
   'else'       : 'ELSE',
   'while'      : 'WHILE',
   'input'      : 'INPUT',
   'output'     : 'OUTPUT',
   '=='         : 'IGUALC',
   '>='         : 'MAYORIGUAL',
   '<='         : 'MENORIGUAL'
}


# Lista con nombres de tokens y palabras reservadas
tokens = ['ID', 'MAS', 'MENOS', 'POR', 'ENTRE', 'MOD', 'AND', 'OR', 'PYC', 'COMA', 'MAYOR', 'MENOR', 'NOTIGUAL', 'NOT', 'PIZQ', 'PDER', 'LLIZQ', 'LLDER', 'COIZQ', 'CODER', 'PUNTO', 'IGUAL', 'CTE_STR', 'CTE_CHAR', 'CTE_NUMERAL', 'CTE_REAL'] + list(reserved.values())

# Ultimo ID obtenido de scanner
ultimoId = ''
ultimoAcceso = ''
ultimoTipo = ''

# Definicion de tokens a traves de expresiones regulares
t_MAS           = r'\+'
t_MENOS         = r'-'
t_POR           = r'\*'
t_ENTRE         = r'\/'
t_MOD			= r'%'
t_AND			= r'\&\&'
t_OR			= r'\|\|'

t_PYC           = r';'
t_COMA          = r','
t_MAYORIGUAL    = r'\>='
t_MENORIGUAL    = r'\<='

t_NOTIGUAL      = r'!='
t_NOT			= r'!'

t_PIZQ          = r'\('
t_PDER          = r'\)'
t_LLIZQ         = r'\{'
t_LLDER         = r'\}'
t_COIZQ			= r'\['
t_CODER			= r'\]'

t_PUNTO			= r'\.'

t_CTE_STR       = r'\"(\\.|[^"])*\"'
t_CTE_CHAR      = r"\'(\\.|[^'])\'"
t_CTE_NUMERAL   = r'[0-9]+'
t_CTE_REAL      = r'[0-9]+\.[0-9]+'

# Caracteres ignorados
t_ignore = " \t\r"

# Definicion de tokens mediante funciones

def t_ID(t):
    r'[a-zA-Z](_?[a-zA-Z0-9])*'
    t.type = reserved.get(t.value,'ID')    # Verificar si es palabra reservada
    global ultimoId
    global ultimoAcceso
    global ultimoTipo
    if(t.type == 'ID' or t.type == 'MAIN' or t.type == 'THIS'):
      ultimoId = t.value
    elif(t.type == 'HIDDEN' or t.type == 'VISIBLE'):
      ultimoAcceso = t.value
    elif(t.type == 'CHAR' or t.type == 'NUMERAL' or t.type == 'REAL' or t.type == 'STRING' or t.type == 'BOOL'):
      ultimoTipo = t.value
    return t

def t_IGUAL(t):
    r'\=(\=)?'
    t.type = reserved.get(t.value,'IGUAL')
    return t

def t_MAYOR(t):
    r'\>(\=)?'
    t.type = reserved.get(t.value,'MAYOR')
    return t

def t_MENOR(t):
    r'\<(\=)?'
    t.type = reserved.get(t.value,'MENOR')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Caracter ilegal: '%s'. Linea #%d" % (t.value[0], t.lexer.lineno))
    t.lexer.skip(1)
    
# Declaracion del scanner, importado desde ply.lex
import sys
import ply.lex as lex
lexer = lex.lex()
