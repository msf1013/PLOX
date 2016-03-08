import ply.yacc as yacc
import os.path
import scanner
tokens = scanner.tokens

# Tabla semantica de clases a utilizar
DirClases = {}
ClaseActual = ''
MetodoActual = ''

# Global variable to store where the syntax error was trigger
error = "'Program declaration'"

def p_programa(p):
	'''programa : ciclo_clase clase_main
				| clase_main'''
	print('Compilation successful!')

def p_ciclo_clase(p):
	'''ciclo_clase 	: clase
					| ciclo_clase clase'''
	print('ciclo_clase')	

def p_clase(p):
	'''clase : CLASS ID declararClase herencia LLIZQ ciclo_vars ciclo_func LLDER limpiarMetodoActual
			 | CLASS ID declararClase herencia LLIZQ ciclo_vars LLDER limpiarMetodoActual
			 | CLASS ID declararClase herencia LLIZQ ciclo_func LLDER limpiarMetodoActual
			 | CLASS ID declararClase herencia LLIZQ LLDER limpiarMetodoActual'''
	print('clase')

def p_declararClase(p):
	'''declararClase : '''
	global ClaseActual
	global DirClases
	ClaseActual = scanner.ultimoId
	if(DirClases.has_key(ClaseActual)):
		lineNumber = scanner.lexer.lineno
		print('Semantic error at line {0}, multiple declaration of Class {1}.').format(lineNumber, ClaseActual)
		exit()
	else:
		DirClases[ClaseActual] = {'variables': {}, 'metodos': {}, 'ancestros': {}}

def p_limpiarMetodoActual(p):
	'''limpiarMetodoActual : '''
	global MetodoActual
	MetodoActual = ''

def p_herencia(p):
	'''herencia : empty
				| UNDER ID agregaAncestro'''
	print('herencia')

def p_agregaAncestro(p):
	'''agregaAncestro : '''
	global ClaseActual
	global DirClases
	ancestro = scanner.ultimoId
	if(not DirClases.has_key(ancestro)):
		lineNumber = scanner.lexer.lineno
		print('Semantic error at line {0}, Class {1} not declared and used in inheritance.').format(lineNumber, ancestro)
		exit()
	else:
		DirClases[ClaseActual]['ancestros'] = DirClases[ancestro]['ancestros']
		DirClases[ClaseActual]['ancestros'][ancestro] = DirClases[ancestro]

def p_ciclo_vars(p):
	'''ciclo_vars 	: acceso vars
					| ciclo_vars acceso vars'''
	print('ciclo_vars')

def p_ciclo_func(p):
	'''ciclo_func 	: func
					| ciclo_func func'''
	print('ciclo_func')

def p_clase_main(p):
	'''clase_main 	: CLASS MAIN declararClase LLIZQ ciclo_vars ciclo_func main LLDER
					| CLASS MAIN declararClase LLIZQ ciclo_vars main LLDER
					| CLASS MAIN declararClase LLIZQ ciclo_func main LLDER
					| CLASS MAIN declararClase LLIZQ main LLDER'''
	print('clase_main')

def p_vars(p):
	'''vars : var_op PYC'''
	print('vars')

def p_var_op(p):
	'''var_op 	: tipo ciclo_tipo
				| ID revisarExistenciaClase ciclo_id'''
	print('var_op')

def p_revisarExistenciaClase(p):
	'''revisarExistenciaClase : '''
	global ClaseActual
	global DirClases
	tipo = scanner.ultimoId
	if(not DirClases.has_key(tipo)):
		lineNumber = scanner.lexer.lineno
		print('Semantic error at line {0}, Class {1} not declared but being instanced.').format(lineNumber, tipo)
		exit()
	else:
		scanner.ultimoTipo = tipo

def p_ciclo_tipo(p):
	'''ciclo_tipo 	: ID declararVariable
					| ID declararVariable COIZQ exp CODER
					| ciclo_tipo COMA ID declararVariable
					| ciclo_tipo COMA ID declararVariable COIZQ exp CODER
					| ID declararVariable IGUAL exp
					| ID declararVariable COIZQ exp CODER IGUAL exp
					| ciclo_tipo COMA ID declararVariable IGUAL exp
					| ciclo_tipo COMA ID declararVariable COIZQ exp CODER IGUAL exp'''
	print('ciclo_tipo')

def p_ciclo_id(p):
	'''ciclo_id 	: ID declararVariable 
					| ID declararVariable COIZQ exp CODER 
					| ciclo_id COMA ID declararVariable
					| ciclo_id COMA ID declararVariable COIZQ exp CODER 
					| ID declararVariable IGUAL atom
					| ciclo_id COMA ID declararVariable IGUAL atom'''
	print('ciclo_id')

def p_declararVariable(p):
	'''declararVariable : '''
	'''revisarExistenciaClase : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	lineNumber = scanner.lexer.lineno
	var = scanner.ultimoId
	if(DirClases.has_key(var)):
		print('Semantic error at line {0}, variable {1} declared but Class {1} already exists.').format(lineNumber, var)
		exit()
	elif(DirClases[ClaseActual]['variables'].has_key(var)):
		print('Semantic error at line {0}, variable {1} already declared.').format(lineNumber, var)
		exit()
	elif(DirClases[ClaseActual]['metodos'].has_key(var)):
		print('Semantic error at line {0}, variable {1} declared but function {1} already declared.').format(lineNumber, var)
		exit()
	elif(MetodoActual != '' and DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(var)):
		print('Semantic error at line {0}, variable {1} already declared.').format(lineNumber, var)
		exit()
	elif(checarAncestros(DirClases[ClaseActual]['ancestros'], var, lineNumber)):
		exit()
	else:
		if(MetodoActual != ''):
			DirClases[ClaseActual]['variables'][var] = {'type': scanner.ultimoTipo}
		else:
			DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][var] = {'type': scanner.ultimoTipo}


def checarAncestros(ancestros, var, lineNumber):
	listaAn = ancestros.items()
	for item in listaAn:
		if (item['variables'].has_key(var)):
			print('Semantic error at line {0}, variable {1} already declared.').format(lineNumber, var)
			return True
		elif (item['metodos'].has_key(var)):
			print('Semantic error at line {0}, variable {1} declared but Class {1} already exists.').format(lineNumber, var)
			return True
	return False

def p_tipo(p):
	'''tipo 	: NUMERAL
				| REAL
				| BOOL
				| CHAR
				| STRING'''
	print('tipo')

def p_acceso(p):
	'''acceso 	: HIDDEN
				| VISIBLE'''
	print('acceso')

def p_func(p):
	'''func 	: acceso tipo ID params cuerpo_func
				| acceso WITHOUT ID params cuerpo_func'''
	print('func')

def p_main(p):
	'''main 	: acceso WITHOUT MAIN PIZQ PDER cuerpo_func'''
	print('main')

def p_params(p):
	'''params 	: PIZQ params_ciclo PDER
				| PIZQ PDER'''
	print('params')

def p_params_ciclo(p):
	'''params_ciclo 	: tipo ID
						| params_ciclo COMA tipo ID'''
	print('params_ciclo')

def p_cuerpo_func(p):
	'''cuerpo_func 	: LLIZQ ciclo_vars_func ciclo_estatuto LLDER
					| LLIZQ ciclo_vars_func LLDER
					| LLIZQ ciclo_estatuto LLDER
					| LLIZQ LLDER'''
	print('cuerpo_func')

def p_ciclo_vars_func(p):
	'''ciclo_vars_func 	: vars
						| ciclo_vars_func vars'''
	print('ciclo_vars_func')


def p_ciclo_estatuto(p):
	'''ciclo_estatuto 	: estatuto
						| ciclo_estatuto estatuto'''
	print('ciclo_estatuto')

def p_estatuto(p):
	'''estatuto 	: while
					| asignacion
					| condicion
					| escritura
					| lectura
					| llamada_func PYC
					| return'''
	print('estatuto')

def p_llamada_func(p):
	'''llamada_func : ID PIZQ exp_ciclo PDER
					| THIS PUNTO ID PIZQ exp_ciclo PDER
					| ID PUNTO ID PIZQ exp_ciclo PDER
					| ID COIZQ exp CODER PUNTO ID PIZQ exp_ciclo PDER
					| ID PIZQ PDER
					| THIS PUNTO ID PIZQ PDER
					| ID PUNTO ID PIZQ PDER
					| ID COIZQ exp CODER PUNTO ID PIZQ PDER'''
	print('llamada_func')

def p_exp_ciclo(p):
	'''exp_ciclo 	: exp
					| exp_ciclo COMA exp'''
	print('exp_ciclo')

def p_cte_bool(p):
	'''cte_bool 	: TRUE
					| FALSE'''
	print('cte_bool')

def p_exp(p):
	'''exp 	: opciones ope exp
			| opciones
			| PIZQ exp PDER
			| PIZQ exp PDER ope exp	
			| MENOS PIZQ exp PDER ope exp
			| NOT exp
			| MENOS PIZQ exp PDER'''
	print('exp')

def p_opciones(p):
	'''opciones : CTE_STR
				| CTE_CHAR
				| CTE_NUMERAL
				| CTE_REAL
				| cte_bool
				| atom
				| llamada_func
				| MENOS CTE_NUMERAL
				| MENOS CTE_REAL
				| MENOS atom
				| MENOS llamada_func'''
	print('opciones')

def p_ope(p):
	'''ope 	: MAS
			| MENOS
			| MOD
			| ENTRE
			| POR
			| IGUALC
			| MENOR
			| MENORIGUAL
			| MAYOR
			| MAYORIGUAL
			| NOTIGUAL
			| AND
			| OR'''
	print('ope')

def p_return(p):
	'''return 	: RETURN exp PYC
				| RETURN PYC'''
	print('return')

def p_while(p):
	'''while 	: WHILE PIZQ exp PDER LLIZQ ciclo_estatuto LLDER
				| WHILE PIZQ exp PDER LLIZQ LLDER'''
	print('while')

def p_asignacion(p):
	'''asignacion 	: atom IGUAL exp PYC
					| atom IGUAL NEW ID PIZQ PDER PYC'''
	print('asignacion')

def p_atom(p):
	'''atom : ID PUNTO ID COIZQ exp CODER
			| ID PUNTO ID
			| ID COIZQ exp CODER PUNTO ID COIZQ exp CODER
			| ID COIZQ exp CODER PUNTO ID
			| ID
			| ID COIZQ exp CODER
			| THIS PUNTO ID
			| THIS PUNTO ID COIZQ exp CODER'''
	print('atom')

def p_condicion(p):
	'''condicion 	: ciclo_cond ELSE LLIZQ ciclo_estatuto LLDER
					| ciclo_cond ELSE LLIZQ LLDER'''
	print('condicion')

def p_ciclo_cond(p):
	'''ciclo_cond 	: IF PIZQ exp PDER LLIZQ ciclo_estatuto LLDER
					| IF PIZQ exp PDER LLIZQ LLDER
					| ciclo_cond ELSE IF PIZQ exp PDER LLIZQ ciclo_estatuto LLDER
					| ciclo_cond ELSE IF PIZQ exp PDER LLIZQ LLDER'''
	print('ciclo_cond')

def p_lectura(p):
	'''lectura 	: INPUT PIZQ atom PDER PYC'''
	print('lectura')

def p_escritura(p):
	'''escritura 	: OUTPUT PIZQ exp PDER PYC'''
	print('escritura')

# Function to serve as an empty word
def p_empty(p):
	'''empty :'''
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