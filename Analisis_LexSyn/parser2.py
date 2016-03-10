import ply.yacc as yacc
import os.path
import scanner
tokens = scanner.tokens

# Tabla semantica de clases a utilizar
DirClases = {}
ClaseActual = ''
MetodoActual = ''
Invocador = ''

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
		DirClases[ClaseActual] = {'variables': { 'this' : {'tipo': ClaseActual, 'acceso' : 'hidden'} }, 'metodos': {}, 'ancestros': {}}

def p_limpiarMetodoActual(p):
	'''limpiarMetodoActual : '''
	global MetodoActual
	MetodoActual = ''

def p_limpiarInvocador(p):
	'''limpiarInvocador : '''
	global Invocador
	Invocador = ''

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
				| ID revisarExistenciaClase DOSP ciclo_id'''
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
					| ID declararVariable IGUAL atom limpiarInvocador
					| ciclo_id COMA ID declararVariable IGUAL atom limpiarInvocador'''
	print('ciclo_id')

def p_declararVariable(p):
	'''declararVariable : '''
	#'''revisarExistenciaClase : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	lineNumber = scanner.lexer.lineno
	var = scanner.ultimoId
	if(DirClases.has_key(var)):
		print('Semantic error at line {0}, variable {1} declared but Class {1} already exists.').format(lineNumber, var)
		exit()
	elif( (DirClases[ClaseActual]['variables'].has_key(var) or checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], var, lineNumber)) and MetodoActual == ''):
		print('Semantic error at line {0}, variable {1} already declared.').format(lineNumber, var)
		exit()
	elif(DirClases[ClaseActual]['metodos'].has_key(var) or checarMetodoAncestros(DirClases[ClaseActual]['ancestros'], var, lineNumber)):
		print('Semantic error at line {0}, variable {1} declared but function {1} already declared.').format(lineNumber, var)
		exit()
	elif(MetodoActual != '' and DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(var)):
		print('Semantic error at line {0}, variable {1} already declared.').format(lineNumber, var)
		exit()
	else:
		if(MetodoActual == ''):
			DirClases[ClaseActual]['variables'][var] = {'tipo': scanner.ultimoTipo, 'acceso' : scanner.ultimoAcceso}
		else:
			DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][var] = {'tipo': scanner.ultimoTipo, 'acceso' : 'hidden'}


def checarAncestros(ancestros, var, lineNumber, tipo):
	listaAn = ancestros.items()
	for item in listaAn:
		if (item[1]['variables'].has_key(var)):
			if (tipo == 0):
				print('Semantic error at line {0}, variable {1} already declared.').format(lineNumber, var)
			else:
				print('Semantic error at line {0}, method {1} declared but variable {1} already declared.').format(lineNumber, var)
			return True
		elif (item[1]['metodos'].has_key(var)):
			if (tipo == 0):
				print('Semantic error at line {0}, variable {1} declared but method {1} already exists.').format(lineNumber, var)
			else:
				print('Semantic error at line {0}, method {1} already declared.').format(lineNumber, var)
			return True
	return False

def checarAtributoAncestros(ancestros, var, lineNumber):
	listaAn = ancestros.items()
	for item in listaAn:
		if (item[1]['variables'].has_key(var)):
			return True
	return False

def checarMetodoAncestros(ancestros, var, lineNumber):
	listaAn = ancestros.items()
	for item in listaAn:
		if (item[1]['metodos'].has_key(var)):
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
	'''func 	: acceso tipo ID declararMetodo params cuerpo_func
				| acceso WITHOUT ID declararMetodo params cuerpo_func'''
	print('---1---')
	for par in DirClases[ClaseActual]['metodos'][MetodoActual]['parametros']:
		print(par[0] + " " + par[1])
	print('---2---')
	print('func')

def p_declararMetodo(p):
	'''declararMetodo : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	lineNumber = scanner.lexer.lineno
	retorno = scanner.ultimoTipo
	MetodoActual = scanner.ultimoId
	if(DirClases.has_key(MetodoActual) and MetodoActual != 'main'):
		print('Semantic error at line {0}, method {1} declared but Class {1} already exists.').format(lineNumber, MetodoActual)
		exit()
	elif( DirClases[ClaseActual]['variables'].has_key(MetodoActual) or checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], MetodoActual, lineNumber) ):
		print('Semantic error at line {0}, method {1} declared but variable {1} already declared.').format(lineNumber, MetodoActual)
		exit()
	elif(DirClases[ClaseActual]['metodos'].has_key(MetodoActual) or checarMetodoAncestros(DirClases[ClaseActual]['ancestros'], MetodoActual, lineNumber) ):
		print('Semantic error at line {0}, method {1} already declared.').format(lineNumber, MetodoActual)
		exit()
	else:
		DirClases[ClaseActual]['metodos'][MetodoActual] = {'variables' : {}, 'parametros' : [], 'retorno': retorno, 'acceso' : scanner.ultimoAcceso}

def p_main(p):
	'''main 	: acceso WITHOUT MAIN declararMetodo PIZQ PDER cuerpo_func'''
	print('main')

def p_params(p):
	'''params 	: PIZQ params_ciclo PDER
				| PIZQ PDER'''
	print('params')

def p_params_ciclo(p):
	'''params_ciclo 	: tipo ID meterParametros
						| params_ciclo COMA tipo ID meterParametros'''
	print('params_ciclo')

def p_meterParametros(p):
	'''meterParametros : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	lineNumber = scanner.lexer.lineno
	parametro = scanner.ultimoId
	tipo = scanner.ultimoTipo
	DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][parametro] = {'tipo':tipo, 'acceso':'hidden'}
	DirClases[ClaseActual]['metodos'][MetodoActual]['parametros'].append([tipo, parametro])

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
					| llamada_func limpiarInvocador PYC
					| return'''
	print('estatuto')

def p_llamada_func(p):
	'''llamada_func : ID checarFuncion PIZQ exp_ciclo PDER
					| ID PUNTO definirInvocador ID checarFuncion PIZQ exp_ciclo PDER
					| ID definirInvocador COIZQ exp CODER PUNTO ID checarFuncion PIZQ exp_ciclo PDER
					| ID checarFuncion PIZQ PDER
					| ID PUNTO definirInvocador ID checarFuncion PIZQ PDER
					| ID definirInvocador COIZQ exp CODER PUNTO ID checarFuncion PIZQ PDER'''
	print('llamada_func')

def p_checarFuncion(p):
	'''checarFuncion : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	global Invocador
	lineNumber = scanner.lexer.lineno
	func = scanner.ultimoId
	if (Invocador == ''):
		if (not DirClases[ClaseActual]['metodos'].has_key(func) and not checarMetodoAncestros(DirClases[ClaseActual]['ancestros'], func, lineNumber)):
			print('Semantic error at line {0}, method {1} not found in Class Hierarchy.').format(lineNumber, func)
			exit()
	else:
		claseAux = ''

		if (MetodoActual != ''):
			if ( DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(Invocador) ):
				claseAux = DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][Invocador]['tipo']
			else:
				claseAux = DirClases[ClaseActual]['variables'][Invocador]['tipo']
		else:
			claseAux = DirClases[ClaseActual]['variables'][Invocador]['tipo']

		if (not DirClases[claseAux]['metodos'].has_key(func) and not checarMetodoAncestros(DirClases[claseAux]['ancestros'], func, lineNumber)):
			print('Semantic error at line {0}, method {1} not associated with Object {2}.').format(lineNumber, func, Invocador)
			exit()

def p_definirInvocador(p):
	'''definirInvocador : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	global Invocador
	lineNumber = scanner.lexer.lineno
	Invocador = scanner.ultimoId
	if ( DirClases[ClaseActual]['variables'].has_key(Invocador) or checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], Invocador, lineNumber)):
		pass
	elif (MetodoActual != '' and DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(Invocador) ):
		pass
	else:
		print('Semantic error at line {0}, Class instance {1} not found.').format(lineNumber, Invocador)
		exit()

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
				| atom limpiarInvocador
				| llamada_func limpiarInvocador
				| MENOS CTE_NUMERAL
				| MENOS CTE_REAL
				| MENOS atom limpiarInvocador
				| MENOS llamada_func limpiarInvocador'''
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
	'''asignacion 	: atom limpiarInvocador IGUAL exp PYC'''
	print('asignacion')

def p_atom(p):
	'''atom : ID PUNTO definirInvocador ID checarAtributo COIZQ exp CODER
			| ID PUNTO definirInvocador ID checarAtributo
			| ID definirInvocador COIZQ exp CODER PUNTO ID checarAtributo COIZQ exp CODER 
			| ID definirInvocador COIZQ exp CODER PUNTO ID checarAtributo
			| ID checarAtributo
			| ID definirInvocador COIZQ exp CODER checarAtributo2
			| THIS PUNTO definirInvocador ID checarAtributo
			| THIS PUNTO definirInvocador ID checarAtributo COIZQ exp CODER '''
	print('atom')

def p_checarAtributo2(p):
	'''checarAtributo2 : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	global Invocador
	lineNumber = scanner.lexer.lineno
	atributo = Invocador
	Invocador = ''
	
	if (Invocador == ''):
		if (MetodoActual == ''):
			if (not DirClases[ClaseActual]['variables'].has_key(atributo) and not checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber)):
				print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 111').format(lineNumber, atributo)
				exit()
		else:
			if (not DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(atributo) and not DirClases[ClaseActual]['variables'].has_key(atributo) and not checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber)):
				print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 222').format(lineNumber, atributo)
				exit()
	elif (Invocador == 'THIS'):
		if (not DirClases[ClaseActual]['variables'].has_key(atributo) and not checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber) ):
			print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 333').format(lineNumber, atributo)
			exit()
	else:

		claseAux = ''

		if (MetodoActual != ''):
			if ( DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(Invocador) ):
				claseAux = DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][Invocador]['tipo']
			else:
				claseAux = DirClases[ClaseActual]['variables'][Invocador]['tipo']
		else:
			claseAux = DirClases[ClaseActual]['variables'][Invocador]['tipo']

		if (not DirClases[claseAux]['variables'].has_key(atributo) and not checarAtributoAncestros(DirClases[claseAux]['ancestros'], atributo, lineNumber)):
			print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 444').format(lineNumber, atributo)
			exit()

def p_checarAtributo(p):
	'''checarAtributo : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	global Invocador
	lineNumber = scanner.lexer.lineno
	atributo = scanner.ultimoId
	
	if (Invocador == ''):
		if (MetodoActual == ''):
			if (not DirClases[ClaseActual]['variables'].has_key(atributo) and not checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber)):
				print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 111').format(lineNumber, atributo)
				exit()
		else:
			if (not DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(atributo) and not DirClases[ClaseActual]['variables'].has_key(atributo) and not checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber)):
				print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 222').format(lineNumber, atributo)
				exit()
	elif (Invocador == 'THIS'):
		if (not DirClases[ClaseActual]['variables'].has_key(atributo) and not checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber) ):
			print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 333').format(lineNumber, atributo)
			exit()
	else:
		
		claseAux = ''

		if (MetodoActual != ''):
			if ( DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(Invocador) ):
				claseAux = DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][Invocador]['tipo']
			else:
				claseAux = DirClases[ClaseActual]['variables'][Invocador]['tipo']
		else:
			claseAux = DirClases[ClaseActual]['variables'][Invocador]['tipo']

		if (not DirClases[claseAux]['variables'].has_key(atributo) and not checarAtributoAncestros(DirClases[claseAux]['ancestros'], atributo, lineNumber)):
			print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 444').format(lineNumber, atributo)
			exit()

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
	'''lectura 	: INPUT PIZQ atom limpiarInvocador PDER PYC'''
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