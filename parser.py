import ply.yacc as yacc
import os.path
import scanner
tokens = scanner.tokens

# Global variable to store where the syntax error was trigger
error = "'Program declaration'"

def p_programa(p):
	'programa : ciclo_clase clase_main'
	print('Compilation successful!')

def p_ciclo_clase(p):
	'''ciclo_clase 	: empty
					| ciclo_clase clase'''
	print('ciclo_clase')	

def p_clase(p):
	'''clase : CLASS ID herencia LLIZQ ciclo_vars ciclo_func LLDER'''
	print('clase')

def p_ciclo_vars(p):
	'''ciclo_vars 	: empty
					| ciclo_vars acceso vars'''
	print('ciclo_vars')

def p_ciclo_func(p):
	'''ciclo_func 	: empty
					| ciclo_func func'''
	print('ciclo_func')

def p_clase_main(p):
	'''clase_main 	: CLASS MAIN LLIZQ ciclo_vars ciclo_func main LLDER'''
	print('clase_main')

def p_vars(p):
	'''vars : var_op PYC'''
	print('vars')

def p_var_op(p):
	'''var_op 	: tipo ciclo_tipo
				| ID ciclo_id'''
	print('var_op')

def p_ciclo_tipo(p):
	'''ciclo_tipo 	: ID arreglo asignacion_exp
					| ciclo_id COMA ID arreglo asignacion_exp'''
	print('ciclo_tipo')

def p_ciclo_id(p):
	'''ciclo_id 	: ID arreglo asignacion_obj
					| ciclo_id COMA ID arreglo asignacion_obj'''
	print('ciclo_id')

def p_arreglo(p):
	'''arreglo 		: empty
					| CODER exp_arit COIZQ'''
	print('arreglo')

def p_asignacion_exp(p):
	'''asignacion_exp	: empty
						| IGUAL exp'''
	print('asignacion_exp')

def p_asignacion_obj(p):
	'''asignacion_obj	: empty
						| IGUAL exp_objeto'''
	print('asignacion_obj')

# Function to serve as an empty word
def p_empty(p):
	'empty :'
	pass

# Syntax error function
def p_error(p):
	lineNumber = scanner.lexer.lineno
	global error
	if(p is None):
		print("Syntax error at line {0} in {1}").format(lineNumber, error)
	else:
		print("Syntax error, unexpected '{0}' at line {1} in {2}").format(p.value, lineNumber, error)
	exit()

# The parser is built
parser = yacc.yacc()

# A file is asked from the user from input to parse
s = raw_input('file: ')
if(os.path.isfile(s)):
	f = open(s, 'r')
	s = f.read()
	parser.parse(s)
else:
	print("Couldn't open file specified")