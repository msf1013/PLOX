import ply.yacc as yacc
import os.path
import scanner
tokens = scanner.tokens

# Implementacion de STACK
# Basada en lista nativa de Python
class stack:
     def __init__(self):
         self.items = []

     def isEmpty(self):
         return (len(self.items) == 0)

     def push(self, item):
         self.items.append(item)

     def pop(self):
         return self.items.pop()

     def top(self):
         return self.items[len(self.items)-1]

     def size(self):
         return len(self.items)

# Tabla semantica de clases a utilizar
DirClases = {}
ClaseActual = ''
MetodoActual = ''
Invocador = ''
AtributoAtom = ''
AtributoTipo = ''
MetodoNombre = ''
MetodoTipo = ''

arch = open('codigo.txt', 'w')

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
	lineNumber = scanner.lexer.lineno
	if(not DirClases.has_key(ancestro)):
		print('Semantic error at line {0}, Class {1} not declared and used in inheritance.').format(lineNumber, ancestro)
		exit()
	elif ( checarAtributoAncestros(DirClases[ancestro]['ancestros'], ClaseActual, lineNumber) or DirClases[ancestro]['variables'].has_key(ClaseActual) ):
		print('Semantic error at line {0}, attribute {1} already declared in Class Hierarchy.').format(lineNumber, ClaseActual)
		exit()
	elif ( checarMetodoAncestros(DirClases[ancestro]['ancestros'], ClaseActual, lineNumber) or DirClases[ancestro]['metodos'].has_key(ClaseActual) ):
		print('Semantic error at line {0}, method {1} already declared in Class Hierarchy.').format(lineNumber, ClaseActual)
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

def valorAtributoAncestros(ancestros, var, lineNumber):
	listaAn = ancestros.items()
	for item in listaAn:
		if (item[1]['variables'].has_key(var)):
			return item[1]['variables'][var]['tipo']

def checarMetodoAncestros(ancestros, var, lineNumber):
	listaAn = ancestros.items()
	for item in listaAn:
		if (item[1]['metodos'].has_key(var)):
			return True
	return False

def valorMetodoAncestros(ancestros, var, lineNumber):
	listaAn = ancestros.items()
	for item in listaAn:
		if (item[1]['metodos'].has_key(var)):
			return item[1]['metodos'][var]['retorno']

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
	if (Invocador != ''):
		p[0] = { 'tipo': MetodoTipo, 'id': MetodoNombre, "invocador": Invocador, 'esFuncion' : True }
	else:
		p[0] = { 'tipo': MetodoTipo, 'id': MetodoNombre, 'esFuncion' : True }
	print('llamada_func')

def p_checarFuncion(p):
	'''checarFuncion : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	global Invocador
	global MetodoNombre
	global MetodoTipo
	lineNumber = scanner.lexer.lineno
	func = scanner.ultimoId
	if (Invocador == ''):
		if ( DirClases[ClaseActual]['metodos'].has_key(func) ):
			MetodoTipo = DirClases[ClaseActual]['metodos'][func]['retorno']
		elif ( checarMetodoAncestros(DirClases[ClaseActual]['ancestros'], func, lineNumber)):
			MetodoTipo = valorMetodoAncestros(DirClases[ClaseActual]['ancestros'], func, lineNumber)
		else:
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

		if ( DirClases[claseAux]['metodos'].has_key(func) ):
			MetodoTipo = DirClases[claseAux]['metodos'][func]['retorno']
		elif ( checarMetodoAncestros(DirClases[claseAux]['ancestros'], func, lineNumber) ):
			MetodoTipo = valorMetodoAncestros(DirClases[claseAux]['ancestros'], func, lineNumber)
		else:
			print('Semantic error at line {0}, method {1} not associated with Object {2}.').format(lineNumber, func, Invocador)
			exit()
	MetodoNombre = func			

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

precedence = (
	('left','OR'),
	('left','AND'),
	('right','NOT'),
	('nonassoc', 'MAYOR', 'MAYORIGUAL', 'MENOR', 'MENORIGUAL', 'IGUALC', 'NOTIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR','ENTRE','MOD'),
    ('right','UMINUS'),
    )

cont = 0

def p_exp_binaria(p):	
	'''exp 	: exp MAS exp
			| exp MENOS exp
			| exp POR exp
			| exp ENTRE exp
			| exp MOD exp
			| exp IGUALC exp
			| exp NOTIGUAL exp
			| exp MAYOR exp
			| exp MAYORIGUAL exp
			| exp MENOR exp
			| exp MENORIGUAL exp
			| exp AND exp
			| exp OR exp'''
	global cont
	if (p[2] == '+'):
		p[0] = {'tipo': 'numeral', 'id': ('t' + str(cont)) }
		arch.write('MAS' + '\t' + p[1]['id'] + '\t' +  p[3]['id'] + '\t' + p[0]['id'] + '\n')
		cont = cont + 1
	elif (p[2] == '-'):
		p[0] = {'tipo': 'numeral', 'id': ('t' + str(cont)) }
		arch.write('MENOS' + '\t' + p[1]['id'] + '\t' +  p[3]['id'] + '\t' + p[0]['id'] + '\n')
		cont = cont + 1
	elif (p[2] == '*'):
		p[0] = {'tipo': 'numeral', 'id': ('t' + str(cont)) }
		arch.write('POR' + '\t' + p[1]['id'] + '\t' +  p[3]['id'] + '\t' + p[0]['id'] + '\n')
		cont = cont + 1
	elif (p[2] == '/'):
		p[0] = {'tipo': 'numeral', 'id': ('t' + str(cont)) }
		arch.write('ENTRE' + '\t' + p[1]['id'] + '\t' +  p[3]['id'] + '\t' + p[0]['id'] + '\n')
		cont = cont + 1
	elif (p[2] == '%'):
		p[0] = {'tipo': 'numeral', 'id': ('t' + str(cont)) }
		arch.write('MOD' + '\t' + p[1]['id'] + '\t' +  p[3]['id'] + '\t' + p[0]['id'] + '\n')
		cont = cont + 1

	elif (p[2] == '=='):
		p[0] = {'tipo': 'bool', 'id': ('t' + str(cont)) }
		arch.write('IGUALC' + '\t' + p[1]['id'] + '\t' +  p[3]['id'] + '\t' + p[0]['id'] + '\n')
		cont = cont + 1
	elif (p[2] == '!='):
		p[0] = {'tipo': 'bool', 'id': ('t' + str(cont)) }
		arch.write('NOTIGUAL' + '\t' + p[1]['id'] + '\t' +  p[3]['id'] + '\t' + p[0]['id'] + '\n')
		cont = cont + 1
	elif (p[2] == '>'):
		p[0] = {'tipo': 'bool', 'id': ('t' + str(cont)) }
		arch.write('MAYOR' + '\t' + p[1]['id'] + '\t' +  p[3]['id'] + '\t' + p[0]['id'] + '\n')
		cont = cont + 1
	elif (p[2] == '>='):
		p[0] = {'tipo': 'bool', 'id': ('t' + str(cont)) }
		arch.write('MAYORIGUAL' + '\t' + p[1]['id'] + '\t' +  p[3]['id'] + '\t' + p[0]['id'] + '\n')
		cont = cont + 1
	elif (p[2] == '<'):
		p[0] = {'tipo': 'bool', 'id': ('t' + str(cont)) }
		arch.write('MENOR' + '\t' + p[1]['id'] + '\t' +  p[3]['id'] + '\t' + p[0]['id'] + '\n')
		cont = cont + 1
	elif (p[2] == '<='):
		p[0] = {'tipo': 'bool', 'id': ('t' + str(cont)) }
		arch.write('MENORIGUAL' + '\t' + p[1]['id'] + '\t' +  p[3]['id'] + '\t' + p[0]['id'] + '\n')
		cont = cont + 1
	elif (p[2] == '||'):
		p[0] = {'tipo': 'bool', 'id': ('t' + str(cont)) }
		arch.write('OR' + '\t' + p[1]['id'] + '\t' +  p[3]['id'] + '\t' + p[0]['id'] + '\n')
		cont = cont + 1
	elif (p[2] == '&&'):
		p[0] = {'tipo': 'bool', 'id': ('t' + str(cont)) }
		arch.write('AND' + '\t' + p[1]['id'] + '\t' +  p[3]['id'] + '\t' + p[0]['id'] + '\n')
		cont = cont + 1

	print('exp_binaria')

def p_exp_unaria(p):	
	'''exp 	: NOT exp
			| MENOS exp %prec UMINUS
			| PIZQ exp PDER'''
	global cont
	if (p[1] == '!'):
		p[0] = {'tipo': 'bool', 'id': ('t' + str(cont)) }
		arch.write('NOT' + '\t' + p[2]['id'] + '\t' +  '-' + '\t' + p[0]['id'] + '\n')
		cont = cont + 1
	elif (p[1] == '-'):
		p[0] = {'tipo': 'numeral', 'id': ('t' + str(cont)) }
		arch.write('UMENOS' + '\t' + p[2]['id'] + '\t' +  '-' + '\t' + p[0]['id'] + '\n')
		cont = cont + 1
	elif (p[1] == '('):
		p[0] = p[2]
	print('exp_unaria')

def p_opciones(p):
	'''exp 	: cte_str
			| cte_char
			| cte_numeral
			| cte_real
			| cte_bool
			| atom limpiarInvocador
			| llamada_func limpiarInvocador'''
	print('OPCION')
	print(p[1])
	p[0] = p[1]
	print('opciones')

def p_cte_str(p):
	'''cte_str : CTE_STR'''
	print('cte_str')
	p[0] = { 'tipo': 'cte_string', 'id': p[1] }

def p_cte_char(p):
	'''cte_char : CTE_CHAR'''
	print('cte_char')
	p[0] = { 'tipo': 'cte_char', 'id': p[1] }

def p_cte_numeral(p):
	'''cte_numeral : CTE_NUMERAL'''
	print('cte_numeral')
	p[0] = { 'tipo': 'cte_numeral', 'id': p[1] }

def p_cte_real(p):
	'''cte_real : CTE_REAL'''
	print('cte_real')
	p[0] = { 'tipo': 'cte_real', 'id': p[1] }

def p_cte_bool(p):
	'''cte_bool 	: TRUE
					| FALSE'''
	print('cte_bool')
	p[0] = { 'tipo': 'cte_bool', 'id': p[1] }

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
	#print(PilaO)
	#print(POper)
	#print(PilaO.top())
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
	if (Invocador != ''):
		print(Invocador)
		p[0] = { 'tipo': AtributoTipo, 'id': AtributoAtom, "invocador": Invocador }
	else:
		p[0] = { 'tipo': AtributoTipo, 'id': AtributoAtom }
	print('atom')

def p_checarAtributo2(p):
	'''checarAtributo2 : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	global Invocador
	global AtributoAtom
	global AtributoTipo
	lineNumber = scanner.lexer.lineno
	atributo = Invocador
	Invocador = ''
	
	if (Invocador == ''):
		if (MetodoActual == ''):
			if ( DirClases[ClaseActual]['variables'].has_key(atributo) ):
				AtributoTipo = DirClases[ClaseActual]['variables'][atributo]['tipo']
			elif ( checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber) ):
				AtributoTipo = valorAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber)
			else:
				print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 111').format(lineNumber, atributo)
				exit()
		else:
			if ( DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(atributo) ):
				AtributoTipo = DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][atributo]['tipo']
			elif ( DirClases[ClaseActual]['variables'].has_key(atributo) ):
				AtributoTipo = DirClases[ClaseActual]['variables'][atributo]['tipo']
			elif ( checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber)):
				AtributoTipo = valorAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber)
			else:
				print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 222').format(lineNumber, atributo)
				exit()
	elif (Invocador == 'THIS'):
		if ( DirClases[ClaseActual]['variables'].has_key(atributo) ):
			AtributoTipo = DirClases[ClaseActual]['variables'][atributo]['tipo']
		elif( checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber) ):
			AtributoTipo = valorAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber)
		else:
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

		if ( DirClases[claseAux]['variables'].has_key(atributo) ):
			AtributoTipo = DirClases[claseAux]['variables'][atributo]['tipo']
		elif ( checarAtributoAncestros(DirClases[claseAux]['ancestros'], atributo, lineNumber) ):
			AtributoTipo = valorAtributoAncestros(DirClases[claseAux]['ancestros'], atributo, lineNumber)
		else:
			print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 444').format(lineNumber, atributo)
			exit()
	AtributoAtom = atributo

def p_checarAtributo(p):
	'''checarAtributo : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	global Invocador
	global AtributoAtom
	global AtributoTipo
	lineNumber = scanner.lexer.lineno
	atributo = scanner.ultimoId
	
	if (Invocador == ''):
		if (MetodoActual == ''):
			if ( DirClases[ClaseActual]['variables'].has_key(atributo) ):
				AtributoTipo = DirClases[ClaseActual]['variables'][atributo]['tipo']
			elif ( checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber) ):
				AtributoTipo = valorAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber)
			else:
				print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 111').format(lineNumber, atributo)
				exit()
		else:
			if ( DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(atributo) ):
				AtributoTipo = DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][atributo]['tipo']
			elif ( DirClases[ClaseActual]['variables'].has_key(atributo) ):
				AtributoTipo = DirClases[ClaseActual]['variables'][atributo]['tipo']
			elif ( checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber)):
				AtributoTipo = valorAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber)
			else:
				print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 222').format(lineNumber, atributo)
				exit()
	elif (Invocador == 'THIS'):
		if ( DirClases[ClaseActual]['variables'].has_key(atributo) ):
			AtributoTipo = DirClases[ClaseActual]['variables'][atributo]['tipo']
		elif( checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber) ):
			AtributoTipo = valorAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber)
		else:
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

		if ( DirClases[claseAux]['variables'].has_key(atributo) ):
			AtributoTipo = DirClases[claseAux]['variables'][atributo]['tipo']
		elif ( checarAtributoAncestros(DirClases[claseAux]['ancestros'], atributo, lineNumber) ):
			AtributoTipo = valorAtributoAncestros(DirClases[claseAux]['ancestros'], atributo, lineNumber)
		else:
			print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 444').format(lineNumber, atributo)
			exit()
	AtributoAtom = atributo

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