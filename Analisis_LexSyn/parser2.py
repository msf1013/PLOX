import ply.yacc as yacc
import os.path
import scanner
import copy
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

# Implementacion de Cubo Semantico para revision de tipos de operadores
CuboSemantico = {}

# Reglas semanticas para 
CuboSemantico['numeral'] = {}

CuboSemantico['numeral']['+'] = {}
CuboSemantico['numeral']['+']['numeral'] = 'numeral'
CuboSemantico['numeral']['+']['real'] = 'real'

CuboSemantico['numeral']['-'] = {}
CuboSemantico['numeral']['-']['-'] = 'numeral'
CuboSemantico['numeral']['-']['numeral'] = 'numeral'
CuboSemantico['numeral']['-']['real'] = 'real'

CuboSemantico['numeral']['/'] = {}
CuboSemantico['numeral']['/']['numeral'] = 'numeral'
CuboSemantico['numeral']['/']['real'] = 'real'

CuboSemantico['numeral']['*'] = {}
CuboSemantico['numeral']['*']['numeral'] = 'numeral'
CuboSemantico['numeral']['*']['real'] = 'real'

CuboSemantico['numeral']['%'] = {}
CuboSemantico['numeral']['%']['numeral'] = 'numeral'

CuboSemantico['numeral']['=='] = {}
CuboSemantico['numeral']['==']['numeral'] = 'bool'
CuboSemantico['numeral']['==']['real'] = 'bool'

CuboSemantico['numeral']['!='] = {}
CuboSemantico['numeral']['!=']['numeral'] = 'bool'
CuboSemantico['numeral']['!=']['real'] = 'bool'

CuboSemantico['numeral']['<'] = {}
CuboSemantico['numeral']['<']['numeral'] = 'bool'
CuboSemantico['numeral']['<']['real'] = 'bool'

CuboSemantico['numeral']['>'] = {}
CuboSemantico['numeral']['>']['numeral'] = 'bool'
CuboSemantico['numeral']['>']['real'] = 'bool'

CuboSemantico['numeral']['<='] = {}
CuboSemantico['numeral']['<=']['numeral'] = 'bool'
CuboSemantico['numeral']['<=']['real'] = 'bool'

CuboSemantico['numeral']['>='] = {}
CuboSemantico['numeral']['>=']['numeral'] = 'bool'
CuboSemantico['numeral']['>=']['real'] = 'bool'

CuboSemantico['numeral']['='] = {}
CuboSemantico['numeral']['=']['numeral'] = 'numeral'


CuboSemantico['real'] = {}

CuboSemantico['real']['+'] = {}
CuboSemantico['real']['+']['numeral'] = 'real'
CuboSemantico['real']['+']['real'] = 'real'

CuboSemantico['real']['-'] = {}
CuboSemantico['real']['-']['-'] = 'real'
CuboSemantico['real']['-']['numeral'] = 'real'
CuboSemantico['real']['-']['real'] = 'real'

CuboSemantico['real']['/'] = {}
CuboSemantico['real']['/']['numeral'] = 'real'
CuboSemantico['real']['/']['real'] = 'real'

CuboSemantico['real']['*'] = {}
CuboSemantico['real']['*']['numeral'] = 'real'
CuboSemantico['real']['*']['real'] = 'real'

CuboSemantico['real']['=='] = {}
CuboSemantico['real']['==']['numeral'] = 'bool'
CuboSemantico['real']['==']['real'] = 'bool'

CuboSemantico['real']['!='] = {}
CuboSemantico['real']['!=']['numeral'] = 'bool'
CuboSemantico['real']['!=']['real'] = 'bool'

CuboSemantico['real']['<'] = {}
CuboSemantico['real']['<']['numeral'] = 'bool'
CuboSemantico['real']['<']['real'] = 'bool'

CuboSemantico['real']['>'] = {}
CuboSemantico['real']['>']['numeral'] = 'bool'
CuboSemantico['real']['>']['real'] = 'bool'

CuboSemantico['real']['<='] = {}
CuboSemantico['real']['<=']['numeral'] = 'bool'
CuboSemantico['real']['<=']['real'] = 'bool'

CuboSemantico['real']['>='] = {}
CuboSemantico['real']['>=']['numeral'] = 'bool'
CuboSemantico['real']['>=']['real'] = 'bool'

CuboSemantico['real']['='] = {}
CuboSemantico['real']['=']['numeral'] = 'numeral'
CuboSemantico['real']['=']['real'] = 'real'


CuboSemantico['bool'] = {}

CuboSemantico['bool']['=='] = {}
CuboSemantico['bool']['==']['bool'] = 'bool'

CuboSemantico['bool']['!='] = {}
CuboSemantico['bool']['!=']['bool'] = 'bool'

CuboSemantico['bool']['&&'] = {}
CuboSemantico['bool']['&&']['bool'] = 'bool'

CuboSemantico['bool']['||'] = {}
CuboSemantico['bool']['||']['bool'] = 'bool'

CuboSemantico['bool']['!'] = 'bool'

CuboSemantico['bool']['='] = {}
CuboSemantico['bool']['=']['bool'] = 'bool'


CuboSemantico['char'] = {}

CuboSemantico['char']['=='] = {}
CuboSemantico['char']['==']['char'] = 'bool'

CuboSemantico['char']['!='] = {}
CuboSemantico['char']['!=']['char'] = 'bool'

CuboSemantico['char']['='] = {}
CuboSemantico['char']['=']['char'] = 'char'


CuboSemantico['string'] = {}

CuboSemantico['string']['=='] = {}
CuboSemantico['string']['==']['string'] = 'bool'

CuboSemantico['string']['!='] = {}
CuboSemantico['string']['!=']['string'] = 'bool'

CuboSemantico['string']['='] = {}
CuboSemantico['string']['=']['string'] = 'string'

CuboSemantico['without'] = {}

# Tabla semantica de clases a utilizar
PSaltos = stack()
DirClases = {}
ClaseActual = ''
MetodoActual = ''
Invocador = ''
InvocadorTipo = ''
AtributoAtom = ''
AtributoTipo = ''
MetodoNombre = ''
MetodoTipo = ''
Line = 0
ResExp = {}
Cuad = []
Falsos = []
Mark = 0

TiposVar = ['numeral', 'real', 'string', 'bool', 'char']

DirsClase = {}
DirsMetodo = {}
DirsMetodoTemp = {}
DirsConstMap = {}
DirsConst = {}

def initDirsClase ():
	global DirsClase
	DirsClase['numeral'] = 1001
	DirsClase['real'] = 4001
	DirsClase['string'] = 7001
	DirsClase['bool'] = 10001
	DirsClase['char'] = 13001
	DirsClase['obj'] = {}

def initDirsMetodo ():
	global DirsClase
	DirsMetodo['numeral'] = 16001
	DirsMetodo['real'] = 19001
	DirsMetodo['string'] = 22001
	DirsMetodo['bool'] = 25001
	DirsMetodo['char'] = 28001
	DirsMetodo['obj'] = {}

def initDirsMetodoTemp ():
	global DirsClaseTemp
	DirsMetodoTemp['numeral'] = 31001
	DirsMetodoTemp['real'] = 36001
	DirsMetodoTemp['string'] = 41001
	DirsMetodoTemp['bool'] = 46001
	DirsMetodoTemp['char'] = 51001
	DirsMetodoTemp['obj'] = {}


DirsConst['numeral'] = 56002
DirsConst['real'] = 61002
DirsConst['string'] = 66002
DirsConst['bool'] = 71002
DirsConst['char'] = 76002
#
DirsConstMap['numeral'] = {}
DirsConstMap['real'] = {}
DirsConstMap['string'] = {}
DirsConstMap['bool'] = {}
DirsConstMap['char'] = {}
#
DirsConstMap['numeral']['0'] = 56001
DirsConstMap['real']['0'] = 61001
DirsConstMap['string'][''] = 66001
DirsConstMap['bool']['false'] = 71001
DirsConstMap['char']['0'] = 76001

def esTipoBasico(tipo):
	global TiposVar 
	return (tipo in TiposVar) 

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
	global ClaseActual
	DirClases[ClaseActual]['estatus'] = 'completa'
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
		CuboSemantico[ClaseActual] = {}
		CuboSemantico[ClaseActual]['='] = {}
		CuboSemantico[ClaseActual]['='][ClaseActual] = ClaseActual
		initDirsClase()
		DirClases[ClaseActual] = {'variables': { 'this' : {'tipo': ClaseActual, 'acceso' : 'hidden'} },
		 'vars' : { 'numeral' : {}, 'real' : {}, 'string' : {}, 'char' : {}, 'bool' : {} }, 'metodos': {}, 'ancestros': {}, 'estatus' : 'procesando'}

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
		for tipo in TiposVar:
			DirClases[ClaseActual]['vars'][tipo] = copy.deepcopy(DirClases[ancestro]['vars'][tipo])
			DirsClase[tipo] = DirsClase[tipo] + len(DirClases[ClaseActual]['vars'][tipo])
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
	lineNumber = scanner.lexer.lineno
	if(not DirClases.has_key(tipo)):
		print('Semantic error at line {0}, Class {1} not declared but being instanced.').format(lineNumber, tipo)
		exit()
	elif (DirClases[tipo]['estatus'] == 'procesando'):
		print('Semantic error at line {0}, trying to instantiate Class {1} but its Class definition is incomplete.').format(lineNumber, tipo)
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

	global DirsClase 
	global DirsMetodo

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
		tipo = scanner.ultimoTipo
		# Variable de clase
		if(MetodoActual == ''):
			DirClases[ClaseActual]['variables'][var] = {'tipo': scanner.ultimoTipo, 'acceso' : scanner.ultimoAcceso}
			if (esTipoBasico(tipo)):
				DirClases[ClaseActual]['vars'][tipo][var] = DirsClase[tipo]
				DirsClase[tipo] = DirsClase[tipo] + 1
			else:
				print('TIPO: ' + tipo)
				print(DirClases[tipo]['vars'])
				for tipoVariable in TiposVar:
					for variable in DirClases[tipo]['vars'][tipoVariable]:
						DirClases[ClaseActual]['vars'][tipoVariable][var + '.' + variable] = DirsClase[tipoVariable]
						DirsClase[tipoVariable] = DirsClase[tipoVariable] + 1
		# Variable de metodo
		else:
			DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][var] = {'tipo': scanner.ultimoTipo, 'acceso' : 'hidden'}
			if (esTipoBasico(tipo)):
				DirClases[ClaseActual]['metodos'][MetodoActual]['vars'][tipo][var] = DirsMetodo[tipo]
				DirsMetodo[tipo] = DirsMetodo[tipo] + 1
			else:
				for tipoVariable in TiposVar:
					for variable in DirClases[tipo]['vars'][tipoVariable]:
						DirClases[ClaseActual]['metodos'][MetodoActual]['vars'][tipoVariable][var + '.' + variable] = DirsMetodo[tipoVariable]
						DirsMetodo[tipoVariable] = DirsMetodo[tipoVariable] + 1


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

def esVisibleAtributoAncestros(ancestros, var, lineNumber):
	listaAn = ancestros.items()
	for item in listaAn:
		if (item[1]['variables'].has_key(var)):
			return (item[1]['variables'][var]['acceso'] == 'visible')

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

def esVisibleMetodoAncestros(ancestros, var, lineNumber):
	listaAn = ancestros.items()
	for item in listaAn:
		if (item[1]['metodos'].has_key(var)):
			return (item[1]['metodos'][var]['acceso'] == 'visible')

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
	initDirsMetodoTemp()
	print('func')

def p_declararMetodo(p):
	'''declararMetodo : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	lineNumber = scanner.lexer.lineno
	retorno = scanner.ultimoTipo
	MetodoActual = scanner.ultimoId
	initDirsMetodo()
	initDirsMetodoTemp()
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
		DirClases[ClaseActual]['metodos'][MetodoActual] = {'variables' : {}, 'parametros' : [], 'params' : [],
		'vars' : { 'numeral' : {}, 'real' : {}, 'string' : {}, 'char' : {}, 'bool' : {} }, 'retorno': retorno, 'acceso' : scanner.ultimoAcceso}

def p_main(p):
	'''main 	: acceso WITHOUT MAIN declararMetodo PIZQ PDER cuerpo_func'''
	print('main')

def p_params(p):
	'''params 	: PIZQ params_ciclo PDER
				| PIZQ PDER'''
	print('params')

def p_params_ciclo(p):
	'''params_ciclo 	: tipo ID meterParametros
						| tipo ID CODER COIZQ meterParametros
						| params_ciclo COMA tipo ID meterParametros
						| params_ciclo COMA tipo ID CODER COIZQ meterParametros'''
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

	DirClases[ClaseActual]['metodos'][MetodoActual]['vars'][tipo][parametro] = DirsMetodo[tipo]
	DirsMetodo[tipo] = DirsMetodo[tipo] + 1

	DirClases[ClaseActual]['metodos'][MetodoActual]['params'].append(tipo)

def p_cuerpo_func(p):
	'''cuerpo_func 	: inicioFunc LLIZQ ciclo_vars_func ciclo_estatuto LLDER
					| inicioFunc LLIZQ ciclo_vars_func LLDER
					| inicioFunc LLIZQ ciclo_estatuto LLDER
					| inicioFunc LLIZQ LLDER'''
	global ClaseActual
	global MetodoActual
	lineNumber = scanner.lexer.lineno
	refTipo = DirClases[ClaseActual]['metodos'][MetodoActual]['retorno']
	if (refTipo == 'numeral'):
		Cuad.append(['RETURN', DirsConstMap['numeral']['0'], '-', '-'])
	elif (refTipo == 'real'):
		Cuad.append(['RETURN', DirsConstMap['real']['0'], '-', '-'])
	elif (refTipo == 'bool'):
		Cuad.append(['RETURN', DirsConstMap['bool']['false'], '-', '-'])
	elif (refTipo == 'char'):
		Cuad.append(['RETURN', DirsConstMap['char']['0'], '-', '-'])
	elif (refTipo == 'string'):
		Cuad.append(['RETURN', DirsConstMap['string'][""], '-', '-'])
	else:
		Cuad.append(['RETURN', '-',  '-', '-'])
	print('cuerpo_func')

def p_inicioFunc(p):
	'''inicioFunc : '''
	global ClaseActual
	global MetodoActual
	DirClases[ClaseActual]['metodos'][MetodoActual]['inicio'] = len(Cuad)
	arch.write(MetodoActual + " : " + str(len(Cuad)) + "\n")

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
			if ( not (DirClases[claseAux]['metodos'][func]['acceso'] == 'visible') ):
				print('Semantic error at line {0}, method {1} is hidden').format(lineNumber, func)
				exit()
			MetodoTipo = DirClases[claseAux]['metodos'][func]['retorno']
		elif ( checarMetodoAncestros(DirClases[claseAux]['ancestros'], func, lineNumber) ):
			if ( not esVisibleMetodoAncestros(DirClases[claseAux]['ancestros'], func, lineNumber) ):
				print('Semantic error at line {0}, method {1} is hidden').format(lineNumber, func)
				exit()
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
	global ResExp
	global cont
	global Line
	global DirsMetodoTemp
	lineNumber = scanner.lexer.lineno
	if (p[2] == '+'):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('+') and CuboSemantico[ p[1]['tipo'] ]['+'].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['+'][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['+'][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['+'][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['+'][ p[3]['tipo'] ]] + 1
			#arch.write(str(Line) + '\t' + 'MAS' + '\t' + (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']) + '\t' + (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']) + '\t' + p[0]['id'] + '\n')
			Cuad.append(['MAS', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
			#arch.write('\t' 'MAS' + '\t' + p[1]['tipo'] + '\t' +  p[3]['tipo'] + '\t' + p[0]['tipo'] + '\n')
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'+\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
		cont = cont + 1
	elif (p[2] == '-'):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('-') and CuboSemantico[ p[1]['tipo'] ]['-'].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['-'][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['-'][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['-'][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['-'][ p[3]['tipo'] ]] + 1
			#arch.write(str(Line) + '\t' + 'MENOS' + '\t' + (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']) + '\t' + (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']) + '\t' + p[0]['id'] + '\n')
			Cuad.append(['MENOS', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
			#arch.write('\t' 'MENOS' + '\t' + p[1]['tipo'] + '\t' +  p[3]['tipo'] + '\t' + p[0]['tipo'] + '\n')
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'-\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
		cont = cont + 1
	elif (p[2] == '*'):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('*') and CuboSemantico[ p[1]['tipo'] ]['*'].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['*'][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['*'][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['*'][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['*'][ p[3]['tipo'] ]] + 1
			#arch.write(str(Line) + '\t' + 'POR' + '\t' + (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']) + '\t' + (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']) + '\t' + p[0]['id'] + '\n')
			Cuad.append(['POR', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
			#arch.write('\t' 'POR' + '\t' + p[1]['tipo'] + '\t' +  p[3]['tipo'] + '\t' + p[0]['tipo'] + '\n')
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'*\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
		cont = cont + 1
	elif (p[2] == '/'):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('/') and CuboSemantico[ p[1]['tipo'] ]['/'].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['/'][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['/'][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['/'][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['/'][ p[3]['tipo'] ]] + 1
			#arch.write(str(Line) + '\t' + 'ENTRE' + '\t' + (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']) + '\t' + (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']) + '\t' + p[0]['id'] + '\n')
			Cuad.append(['ENTRE', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
			#arch.write('\t' 'ENTRE' + '\t' + p[1]['tipo'] + '\t' +  p[3]['tipo'] + '\t' + p[0]['tipo'] + '\n')
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'/\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
		cont = cont + 1
	elif (p[2] == '%'):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('%') and CuboSemantico[ p[1]['tipo'] ]['%'].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['%'][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['%'][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['%'][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['%'][ p[3]['tipo'] ]] + 1
			#arch.write(str(Line) + '\t' + 'MOD' + '\t' + (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']) + '\t' + (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']) + '\t' + p[0]['id'] + '\n')
			Cuad.append(['MOD', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
			#arch.write('\t' 'MOD' + '\t' + p[1]['tipo'] + '\t' +  p[3]['tipo'] + '\t' + p[0]['tipo'] + '\n')
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'%\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
		cont = cont + 1

	elif (p[2] == '=='):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('==') and CuboSemantico[ p[1]['tipo'] ]['=='].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['=='][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['=='][ p[3]['tipo'] ]] }
			#arch.write(str(Line) + '\t' + 'IGUALC' + '\t' + (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']) + '\t' + (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']) + '\t' + p[0]['id'] + '\n')
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['=='][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['=='][ p[3]['tipo'] ]] + 1
			Cuad.append(['IGUALC', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
			#arch.write('\t' 'IGUALC' + '\t' + p[1]['tipo'] + '\t' +  p[3]['tipo'] + '\t' + p[0]['tipo'] + '\n')
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'==\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
		cont = cont + 1
	elif (p[2] == '!='):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('!=') and CuboSemantico[ p[1]['tipo'] ]['!='].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['!='][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['!='][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['!='][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['!='][ p[3]['tipo'] ]] + 1
			#arch.write(str(Line) + '\t' + 'NOTIGUAL' + '\t' + (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']) + '\t' + (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']) + '\t' + p[0]['id'] + '\n')
			Cuad.append(['NOTIGUAL', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
			#arch.write('\t' 'NOTIGUAL' + '\t' + p[1]['tipo'] + '\t' +  p[3]['tipo'] + '\t' + p[0]['tipo'] + '\n')
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'!=\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
		cont = cont + 1
	elif (p[2] == '>'):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('>') and CuboSemantico[ p[1]['tipo'] ]['>'].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['>'][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['>'][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['>'][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['>'][ p[3]['tipo'] ]] + 1
			#arch.write(str(Line) + '\t' + 'MAYOR' + '\t' + (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']) + '\t' + (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']) + '\t' + p[0]['id'] + '\n')
			Cuad.append(['MAYOR', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
			#arch.write('\t' 'MAYOR' + '\t' + p[1]['tipo'] + '\t' +  p[3]['tipo'] + '\t' + p[0]['tipo'] + '\n')
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'>\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
		cont = cont + 1
	elif (p[2] == '>='):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('>=') and CuboSemantico[ p[1]['tipo'] ]['>='].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['>='][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['>='][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['>='][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['>='][ p[3]['tipo'] ]] + 1
			#arch.write(str(Line) + '\t' + 'MAYORIGUAL' + '\t' + (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']) + '\t' + (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']) + '\t' + p[0]['id'] + '\n')
			Cuad.append(['MAYORIGUAL', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
			#arch.write('\t' 'MAYORIGUAL' + '\t' + p[1]['tipo'] + '\t' +  p[3]['tipo'] + '\t' + p[0]['tipo'] + '\n')
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'>=\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
		cont = cont + 1
	elif (p[2] == '<'):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('<') and CuboSemantico[ p[1]['tipo'] ]['<'].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['<'][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['<'][ p[3]['tipo'] ]] }
			#arch.write(str(Line) + '\t' + 'MENOR' + '\t' + (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']) + '\t' + (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']) + '\t' + p[0]['id'] + '\n')
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['<'][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['<'][ p[3]['tipo'] ]] + 1
			Cuad.append(['MENOR', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
			#arch.write('\t' 'MENOR' + '\t' + p[1]['tipo'] + '\t' +  p[3]['tipo'] + '\t' + p[0]['tipo'] + '\n')
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'<\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
		cont = cont + 1
	elif (p[2] == '<='):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('<=') and CuboSemantico[ p[1]['tipo'] ]['<='].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['<='][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['<='][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['<='][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['<='][ p[3]['tipo'] ]] + 1
			#arch.write(str(Line) + '\t' + 'MENORIGUAL' + '\t' + (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']) + '\t' + (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']) + '\t' + p[0]['id'] + '\n')
			Cuad.append(['MENORIGUAL', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
			#arch.write('\t' 'MENORIGUAL' + '\t' + p[1]['tipo'] + '\t' +  p[3]['tipo'] + '\t' + p[0]['tipo'] + '\n')
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'<=\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
		cont = cont + 1
	elif (p[2] == '||'):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('||') and CuboSemantico[ p[1]['tipo'] ]['||'].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['||'][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['||'][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['||'][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['||'][ p[3]['tipo'] ]] + 1
			#arch.write(str(Line) + '\t' + 'OR' + '\t' + (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']) + '\t' + (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']) + '\t' + p[0]['id'] + '\n')
			Cuad.append(['OR', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
			#arch.write('\t' 'OR' + '\t' + p[1]['tipo'] + '\t' +  p[3]['tipo'] + '\t' + p[0]['tipo'] + '\n')
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'||\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
		cont = cont + 1
	elif (p[2] == '&&'):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('&&') and CuboSemantico[ p[1]['tipo'] ]['&&'].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['&&'][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['&&'][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['&&'][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['&&'][ p[3]['tipo'] ]] + 1
			#arch.write(str(Line) + '\t' + 'AND' + '\t' + (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']) + '\t' + (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']) + '\t' + p[0]['id'] + '\n')
			Cuad.append(['AND', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
			#arch.write('\t' 'AND' + '\t' + p[1]['tipo'] + '\t' +  p[3]['tipo'] + '\t' + p[0]['tipo'] + '\n')
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'&&\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
		cont = cont + 1
	ResExp = p[0]
	print('exp_binaria')

def p_exp_unaria(p):	
	'''exp 	: NOT exp
			| MENOS exp %prec UMINUS
			| PIZQ exp PDER'''
	global ResExp
	global cont
	global Line
	lineNumber = scanner.lexer.lineno
	if (p[1] == '!'):
		if (CuboSemantico[ p[2]['tipo'] ].has_key('!')):
			p[0] = {'tipo': CuboSemantico[ p[2]['tipo'] ]['!'], 'id': DirsMetodoTemp[CuboSemantico[ p[2]['tipo'] ]['!']] }
			DirsMetodoTemp[CuboSemantico[ p[2]['tipo'] ]['!']] = DirsMetodoTemp[CuboSemantico[ p[2]['tipo'] ]['!']] + 1
			#arch.write(str(Line) + '\t' + 'NOT' + '\t' + (p[2]['invocador']+'.'+p[2]['id'] if p[2].has_key('invocador') else p[2]['id']) + '\t' +  '-' + '\t' + p[0]['id'] + '\n')
			Cuad.append(['NOT', (p[2]['invocador']+'.'+p[2]['id'] if p[2].has_key('invocador') else p[2]['id']), '-', p[0]['id']])
			Line = Line + 1;
			#arch.write('\t' 'NOT' + '\t' + p[2]['tipo'] + '\t' +  '-' + '\t' + p[0]['tipo'] + '\n')
		else:
			print('Semantic error at line {0}, incompatible type {1} with preceding operator \'!\'.').format(lineNumber, p[2]['tipo'])
			exit()
		cont = cont + 1
	elif (p[1] == '-'):
		if (CuboSemantico[ p[2]['tipo'] ].has_key('-') and CuboSemantico[ p[2]['tipo'] ]['-'].has_key('-')):
			p[0] = {'tipo': CuboSemantico[ p[2]['tipo'] ]['-']['-'], 'id': DirsMetodoTemp[CuboSemantico[ p[2]['tipo'] ]['-']['-']] }
			DirsMetodoTemp[CuboSemantico[ p[2]['tipo'] ]['-']['-']] = DirsMetodoTemp[CuboSemantico[ p[2]['tipo'] ]['-']['-']] + 1
			#arch.write(str(Line) + '\t' + 'UMENOS' + '\t' + (p[2]['invocador']+'.'+p[2]['id'] if p[2].has_key('invocador') else p[2]['id']) + '\t' +  '-' + '\t' + p[0]['id'] + '\n')
			Cuad.append(['UMENOS', (p[2]['invocador']+'.'+p[2]['id'] if p[2].has_key('invocador') else p[2]['id']), '-', p[0]['id']])
			Line = Line + 1;
			#arch.write('\t' 'UMENOS' + '\t' + p[2]['tipo'] + '\t' +  '-' + '\t' + p[0]['tipo'] + '\n')
		else:
			print('Semantic error at line {0}, incompatible type {1} with preceding operator \'-\'.').format(lineNumber, p[2]['tipo'])
			exit()
		cont = cont + 1
	elif (p[1] == '('):
		p[0] = p[2]
	ResExp = p[0]
	print('exp_unaria')

def p_opciones(p):
	'''exp 	: cte_str
			| cte_char
			| cte_numeral
			| cte_real
			| cte_bool
			| atom limpiarInvocador
			| llamada_func limpiarInvocador'''
	global ResExp
	print('OPCION')
	print(p[1])
	p[0] = p[1]
	ResExp = p[0]
	print('opciones')

def p_cte_str(p):
	'''cte_str : CTE_STR'''
	print('cte_str')
	global DirsConst
	global DirsConstMap
	if p[1] in DirsConstMap['string']:
		p[0] = { 'tipo': 'string', 'id': DirsConstMap['string'][ p[1] ] }
	else:
		p[0] = { 'tipo': 'string', 'id': DirsConst['string'] }
		DirsConstMap['string'][p[1]] = DirsConst['string']
		DirsConst['string'] = DirsConst['string'] + 1 

def p_cte_char(p):
	'''cte_char : CTE_CHAR'''
	print('cte_char')
	global DirsConst
	global DirsConstMap
	if p[1] in DirsConstMap['char']:
		p[0] = { 'tipo': 'char', 'id': DirsConstMap['char'][ p[1] ] }
	else:
		p[0] = { 'tipo': 'char', 'id': DirsConst['char'] }
		DirsConstMap['char'][p[1]] = DirsConst['char']
		DirsConst['char'] = DirsConst['char'] + 1

def p_cte_numeral(p):
	'''cte_numeral : CTE_NUMERAL'''
	print('cte_numeral')
	global DirsConst
	global DirsConstMap
	if p[1] in DirsConstMap['numeral']:
		p[0] = { 'tipo': 'numeral', 'id': DirsConstMap['numeral'][ p[1] ] }
	else:
		p[0] = { 'tipo': 'numeral', 'id': DirsConst['numeral'] }
		DirsConstMap['numeral'][p[1]] = DirsConst['numeral']
		DirsConst['numeral'] = DirsConst['numeral'] + 1

def p_cte_real(p):
	'''cte_real : CTE_REAL'''
	print('cte_real')
	global DirsConst
	global DirsConstMap
	if p[1] in DirsConstMap['real']:
		p[0] = { 'tipo': 'real', 'id': DirsConstMap['real'][ p[1] ] }
	else:
		p[0] = { 'tipo': 'real', 'id': DirsConst['real'] }
		DirsConstMap['real'][p[1]] = DirsConst['real']
		DirsConst['real'] = DirsConst['real'] + 1

def p_cte_bool(p):
	'''cte_bool 	: TRUE
					| FALSE'''
	print('cte_bool')
	global DirsConst
	global DirsConstMap
	if p[1] in DirsConstMap['bool']:
		p[0] = { 'tipo': 'bool', 'id': DirsConstMap['bool'][ p[1] ] }
	else:
		p[0] = { 'tipo': 'bool', 'id': DirsConst['bool'] }
		DirsConstMap['bool'][p[1]] = DirsConst['bool']
		DirsConst['bool'] = DirsConst['bool'] + 1

def p_return_exp(p):
	'''return 	: RETURN exp PYC'''
	global ClaseActual
	global MetodoActual
	lineNumber = scanner.lexer.lineno
	if (p[2]['tipo'] != DirClases[ClaseActual]['metodos'][MetodoActual]['retorno'] ):
		print('Semantic error at line {0}, expected "{1}" return, but got "{2}" expression.').format(lineNumber - 1, DirClases[ClaseActual]['metodos'][MetodoActual]['retorno'], p[2]['tipo'])
		exit()
	Cuad.append(['RETURN', p[2]['id'],  '-', '-'])
	print('return')

def p_return_null(p):
	'''return 	: RETURN PYC'''
	global ClaseActual
	global MetodoActual
	lineNumber = scanner.lexer.lineno
	if (not DirClases[ClaseActual]['metodos'][MetodoActual]['retorno'] == 'without'):
		print('Semantic error at line {0}, expected "{1}" return expression, but got "without" return.').format(lineNumber - 1, DirClases[ClaseActual]['metodos'][MetodoActual]['retorno'])
		exit()
	Cuad.append(['RETURN', '-',  '-', '-'])
	print('return')

def p_while(p):
	'''while 	: WHILE while_1 PIZQ exp PDER while_2 LLIZQ ciclo_estatuto while_3 LLDER
				| WHILE while_1 PIZQ exp PDER while_2 LLIZQ while_3 LLDER'''
	print('while')

def p_while_1(p):
	'''while_1 : '''
	global PSaltos
	global Line
	PSaltos.push(Line)

def p_while_2(p):
	'''while_2 : '''
	global PSaltos
	global Line
	global ResExp
	lineNumber = scanner.lexer.lineno
	if (ResExp['tipo'] != 'bool'):
		print('Semantic error at line {0}, expected "bool" expression, but "{1}" expression given in while loop condition.').format(lineNumber - 1, ResExp['tipo'])
		exit()
	#arch.write(str(Line) + '\t' + 'GOTOF' + '\t' + ResExp['id'] + '\t' +  'missing' + '\t' + '-' + '\n')
	Cuad.append(['GOTOF', ResExp['id'],  'missing', '-'])
	Line = Line + 1;
	PSaltos.push(Line - 1)

def p_while_3(p):
	'''while_3 : '''
	global PSaltos
	global Line
	falso = PSaltos.pop()
	retorno = PSaltos.pop()
	#arch.write(str(Line) + '\t' + 'GOTO' + '\t' + '-' + '\t' +  str(retorno) + '\t' + '-' + '\n')
	Cuad.append(['GOTO', '-', retorno, '-'])
	Line = Line + 1;
	Cuad[falso][2] = Line
	#arch.write(str(Line) + '\t' + 'RELLENA' + '\t' + str(falso) + '\t' +  str(Line) + '\t' + '-' + '\n')


def p_asignacion(p):
	'''asignacion 	: atom limpiarInvocador IGUAL exp PYC'''
	global cont
	global Line
	lineNumber = scanner.lexer.lineno
	if (CuboSemantico[ p[1]['tipo'] ].has_key('=') and CuboSemantico[ p[1]['tipo'] ]['='].has_key( p[4]['tipo'] )):
		#p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['='][ p[4]['tipo'] ], 'id': ('t' + str(cont)) }
		if (p[1].has_key('invocador')):
			#arch.write(str(Line) + '\t' + 'IGUAL' + '\t' + p[4]['id'] + '\t' +  '-' + '\t' + (p[1]['invocador']+'.'+p[1]['id']) + '\n')
			Cuad.append(['IGUAL', p[4]['id'], '-', (p[1]['invocador']+'.'+p[1]['id'])])
		else:
			#arch.write(str(Line) + '\t' + 'IGUAL' + '\t' + p[4]['id'] + '\t' +  '-' + '\t' + p[1]['id'] + '\n')
			Cuad.append(['IGUAL', p[4]['id'], '-', p[1]['id']])
		Line = Line + 1;
		#arch.write('\t' 'IGUAL' + '\t' + p[4]['tipo'] + '\t' +  '-' + '\t' + p[1]['tipo'] + '\n')
	else:
		print('Semantic error at line {0}, incompatible type assignation of type {1} into type {2}.').format(lineNumber - 1, p[4]['tipo'], p[1]['tipo'])
		exit()
	#cont = cont + 1
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
	global ClaseActual
	global MetodoActual
	global InvocadorTipo
	global Invocador
	global AtributoAtom
	global AtributoTipo
	lineNumber = scanner.lexer.lineno
	if (Invocador != ''):
		# Buscar en clase actual
		if (Invocador == 'this'):
			if (esTipoBasico(AtributoTipo)):
				p[0] = { 'tipo': AtributoTipo, 'id': DirClases[ClaseActual]['vars'][AtributoTipo][AtributoAtom] }
			else:
				print("Semantic error at line {0}, THIS -> X can't refer to instances of Class {1}").format(lineNumber, AtributoTipo)
				exit()
		# Buscar en instancia : metodo
		elif (DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(Invocador)):
			p[0] = { 'tipo': AtributoTipo, 'id': DirClases[ClaseActual]['metodos'][MetodoActual]['vars'][AtributoTipo][Invocador + '.' + AtributoAtom] }
		# Buscar en instancia : clase
		else:
			p[0] = { 'tipo': AtributoTipo, 'id': DirClases[ClaseActual]['vars'][AtributoTipo][Invocador + '.' + AtributoAtom] }
	else:
		# Buscar en metodo actual
		print(ClaseActual)
		print(MetodoActual)
		print(AtributoAtom)
		if (DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(AtributoAtom)):
			p[0] = { 'tipo': AtributoTipo, 'id': DirClases[ClaseActual]['metodos'][MetodoActual]['vars'][AtributoTipo][AtributoAtom] }
		# Buscar en clase actual
		else:
			p[0] = { 'tipo': AtributoTipo, 'id': DirClases[ClaseActual]['vars'][AtributoTipo][AtributoAtom] }
	print('atom')

def p_checarAtributo2(p):
	'''checarAtributo2 : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	global Invocador
	global InvocadorTipo
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
	elif (Invocador == 'this'):
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
			if ( not (DirClases[claseAux]['variables'][atributo]['acceso'] == 'visible') ):
				print('Semantic error at line {0}, variable {1} is hidden').format(lineNumber, atributo)
				exit()
			AtributoTipo = DirClases[claseAux]['variables'][atributo]['tipo']
		elif ( checarAtributoAncestros(DirClases[claseAux]['ancestros'], atributo, lineNumber) ):
			if ( not esVisibleAtributoAncestros(DirClases[claseAux]['ancestros'], atributo, lineNumber) ):
				print('Semantic error at line {0}, variable {1} is hidden').format(lineNumber, atributo)
				exit()
			AtributoTipo = valorAtributoAncestros(DirClases[claseAux]['ancestros'], atributo, lineNumber)
		else:
			print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 444').format(lineNumber, atributo)
			exit()
		InvocadorTipo = DirClases[ClaseActual]['variables'][Invocador]['tipo']
	AtributoAtom = atributo

def p_checarAtributo(p):
	'''checarAtributo : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	global Invocador
	global InvocadorTipo
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
	elif (Invocador == 'this'):
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
			if ( not (DirClases[claseAux]['variables'][atributo]['acceso'] == 'visible') ):
				print('Semantic error at line {0}, variable {1} is hidden').format(lineNumber, atributo)
				exit()
			AtributoTipo = DirClases[claseAux]['variables'][atributo]['tipo']
		elif ( checarAtributoAncestros(DirClases[claseAux]['ancestros'], atributo, lineNumber) ):
			if ( not esVisibleAtributoAncestros(DirClases[claseAux]['ancestros'], atributo, lineNumber) ):
				print('Semantic error at line {0}, variable {1} is hidden').format(lineNumber, atributo)
				exit()
			AtributoTipo = valorAtributoAncestros(DirClases[claseAux]['ancestros'], atributo, lineNumber)
		else:
			print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 444').format(lineNumber, atributo)
			exit()
		InvocadorTipo = claseAux
	AtributoAtom = atributo

def p_condicion(p):
	'''condicion 	: ciclo_cond ELSE if_3 LLIZQ ciclo_estatuto LLDER if_4
					| ciclo_cond ELSE if_3 LLIZQ LLDER if_4
					| ciclo_cond if_4'''
	print('condicion')

def p_ciclo_cond(p):
	'''ciclo_cond 	: IF PIZQ exp PDER if_1 LLIZQ ciclo_estatuto if_2 LLDER
					| IF PIZQ exp PDER if_1 LLIZQ if_2 LLDER
					| ciclo_cond ELSE IF if_3 PIZQ exp PDER if_1 LLIZQ ciclo_estatuto if_2 LLDER
					| ciclo_cond ELSE IF if_3 PIZQ exp PDER if_1 LLIZQ if_2 LLDER'''
	print('ciclo_cond')

def p_if_1(p):
	'''if_1 : '''
	global PSaltos
	global Line
	global ResExp
	lineNumber = scanner.lexer.lineno
	if (ResExp['tipo'] != 'bool'):
		print('Semantic error at line {0}, expected "bool" expression, but "{1}" expression given in if condition.').format(lineNumber - 1, ResExp['tipo'])
		exit()
	#arch.write(str(Line) + '\t' + 'GOTOF' + '\t' + ResExp['id'] + '\t' +  'missing' + '\t' + '-' + '\n')
	Cuad.append(['GOTOF', ResExp['id'],  'missing', '-'])
	Line = Line + 1;
	PSaltos.push(Line - 1)

def p_if_2(p):
	'''if_2 : '''
	global PSaltos
	global Line
	global Mark
	falso = PSaltos.pop()
	Cuad[falso][2] = Line
	Mark = falso

def p_if_3(p):
	'''if_3 : '''
	global PSaltos
	global Line
	global Falsos
	global Mark
	#arch.write(str(Line) + '\t' + 'GOTO' + '\t' + '-'+ '\t' +  'missing' + '\t' + '-' + '\n')
	Cuad.append(['GOTO', '-',  'missing', '-'])
	Line = Line + 1;
	Cuad[Mark][2] = Line
	PSaltos.push(Line - 1)
	Falsos.append(Line - 1)

def p_if_4(p):
	'''if_4 : '''
	global PSaltos
	global Line
	global Falsos
	for falso in Falsos:
		PSaltos.pop()
		Cuad[falso][2] = Line
	Falsos = []

def p_lectura(p):
	'''lectura 	: INPUT PIZQ atom limpiarInvocador PDER PYC'''
	global Line
	if (p[3].has_key('invocador')):
		#arch.write(str(Line) + '\t' + 'INPUT' + '\t' + '-' + '\t' +  '-' + '\t' + (p[3]['invocador']+'.'+p[3]['id']) + '\n')
		Cuad.append(['INPUT','-', '-', (p[3]['invocador']+'.'+p[3]['id'])])
	else:
		#arch.write(str(Line) + '\t' + 'INPUT' + '\t' + '-' + '\t' +  '-' + '\t' + p[3]['id'] + '\n')
		Cuad.append(['INPUT','-', '-', p[3]['id']])
	Line = Line + 1;
	#arch.write('\t' 'INPUT' + '\t' + '-' + '\t' +  '-' + '\t' + p[3]['tipo'] + '\n')
	print('lectura')

def p_escritura(p):
	'''escritura 	: OUTPUT PIZQ exp PDER PYC'''
	global Line
	#arch.write(str(Line) + '\t' + 'OUTPUT' + '\t' + '-' + '\t' +  '-' + '\t' + p[3]['id'] + '\n')
	Cuad.append(['OUTPUT','-', '-', p[3]['id']])
	Line = Line + 1;
	#arch.write('\t' 'OUTPUT' + '\t' + '-' + '\t' +  '-' + '\t' + p[3]['tipo'] + '\n')
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

arch2 = open('codigoArr.txt', 'w')

print('Animal')
print(DirClases['Animal']['vars'])
print('')
print('Perro')
print(DirClases['Perro']['vars'])
print('')
print('Persona')
print(DirClases['Persona']['vars'])
print('')
print('Estudiante')
print(DirClases['Estudiante']['vars'])
print('')
print('main')
print(DirClases['main']['vars'])
print('')
print('')

print('auxEdad')
print(DirClases['Persona']['metodos']['auxEdad']['vars'])
#print(DirClases['Persona']['metodos']['auxEdad'])
print('')
print('getEdad')
print(DirClases['Persona']['metodos']['getEdad']['vars'])
#print(DirClases['Persona']['metodos']['getEdad'])
print('')
print('setNombre')
print(DirClases['Persona']['metodos']['setNombre']['vars'])
#print(DirClases['Persona']['metodos']['setNombre'])
print('')
print('setEdad')
print(DirClases['Persona']['metodos']['setEdad']['vars'])
#print(DirClases['Persona']['metodos']['setEdad'])
print('')
print('')

print('setMaterias')
print(DirClases['Estudiante']['metodos']['setMaterias']['vars'])
#print(DirClases['Estudiante']['metodos']['setMaterias'])
print('')
print('getMaterias')
print(DirClases['Estudiante']['metodos']['getMaterias']['vars'])
#print(DirClases['Estudiante']['metodos']['getMaterias'])
print('')

print('main')
print(DirClases['main']['metodos']['main']['vars'])
#print(DirClases['Estudiante']['metodos']['getMaterias'])
print('')


for i in range(0, len(Cuad)):
	arch2.write(str(i) + '\t' + str(Cuad[i][0]) + '\t' + '\t' + str(Cuad[i][1]) + '\t' + '\t' + str(Cuad[i][2]) + '\t' + str(Cuad[i][3]) + '\n')