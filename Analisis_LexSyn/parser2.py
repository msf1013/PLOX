#############################################################################
#							       IMPORTS									#
#############################################################################

import ply.yacc as yacc
import os.path
import scanner
import copy

#############################################################################
#							  VARIABLES GLOBALES							#
#############################################################################

# Global utilizada por PLY para recuperar tokens desde el scanner
tokens = scanner.tokens

# Implementacion de pila, basada en lista nativa de Python
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

# Reglas semanticas para operaciones entre tipos numeral (int)
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

# Reglas semanticas para operaciones entre tipos real (float)
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

# Reglas semanticas para operaciones entre tipos bool
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

# Reglas semanticas para operaciones entre tipos char
CuboSemantico['char'] = {}

CuboSemantico['char']['=='] = {}
CuboSemantico['char']['==']['char'] = 'bool'

CuboSemantico['char']['!='] = {}
CuboSemantico['char']['!=']['char'] = 'bool'

CuboSemantico['char']['='] = {}
CuboSemantico['char']['=']['char'] = 'char'

# Reglas semanticas para operaciones entre tipos string
CuboSemantico['string'] = {}

CuboSemantico['string']['=='] = {}
CuboSemantico['string']['==']['string'] = 'bool'

CuboSemantico['string']['!='] = {}
CuboSemantico['string']['!=']['string'] = 'bool'

CuboSemantico['string']['='] = {}
CuboSemantico['string']['=']['string'] = 'string'

CuboSemantico['without'] = {}

# Tabla semantica de clases a utilizar
DirClases = {}

# Pila de saltos
PSaltos = stack()

# Pila de llamadas a metodo
PilaLlamadas = stack()

# Global que almacena nombre de Clase que actualmente se esta parseando
ClaseActual = ''

# Global que almacena nombre de Metodo que actualmente se esta parseando
MetodoActual = ''

# Global que almacena nombre de Invocador de atributo o metodo
Invocador = ''

# Global que almacena Clase de Invocador de atributo o metodo
InvocadorTipo = ''

# Global que almacena nombre de atributo invocado
AtributoAtom = ''

# Global que almacena Clase/tipo de atributo invocado
AtributoTipo = ''

# Global que almacena nombre de Metodo invocado
MetodoNombre = ''

# Global que almacena tipo de retorno de Metodo invocado
MetodoTipo = ''

# Arreglo de cuadruplos
Cuad = [['GOTO', '-', '-', '-']]
Line = 1 # Linea del siguiente cuadruplo, inicia en 1 porque el cuadruplo 0 es GOTO main

# Dictionario global usado para capturar la ultima expresion evaluada,
# para poder realizar validaciones de tipo en IFs y WHILEs
ResExp = {}

# Arreglo para almacenar posiciones del codigo intermedio pendientes de rellenar,
# para implementacion de IFs
Falsos = []

# Numero de cuadruplo final de un bloque de IF
Mark = 0

# Arreglo que almacena tipos de dato primitivos
TiposVar = ['numeral', 'real', 'string', 'bool', 'char']

# Diccionarios que almacenan las direcciones base para cada tipo en:
DirBaseClase = {}		# Clase
DirBaseMetodo = {}		# Metodo
DirBaseMetodoTemp = {}	# Temporales de metodo

DirBaseClase['numeral'] = 1001
DirBaseClase['real'] = 4001
DirBaseClase['string'] = 7001
DirBaseClase['bool'] = 10001
DirBaseClase['char'] = 13001

DirBaseMetodo['numeral'] = 16001
DirBaseMetodo['real'] = 19001
DirBaseMetodo['string'] = 22001
DirBaseMetodo['bool'] = 25001
DirBaseMetodo['char'] = 28001

DirBaseMetodoTemp['numeral'] = 31001
DirBaseMetodoTemp['real'] = 36001
DirBaseMetodoTemp['string'] = 41001
DirBaseMetodoTemp['bool'] = 46001
DirBaseMetodoTemp['char'] = 51001

# Diccionarios que almacenan la siguiente direccion disponible para:
DirsClase = {}			# Clase
DirsMetodo = {}			# Metodo
DirsMetodoTemp = {}		# Temporales de metodo
DirsConst = {}			# Constantes

# Metodos para inicializacion de direcciones disponibles
def initDirsClase ():
	global DirsClase
	DirsClase['numeral'] 	= DirBaseClase['numeral']
	DirsClase['real'] 		= DirBaseClase['real']
	DirsClase['string'] 	= DirBaseClase['string']
	DirsClase['bool'] 		= DirBaseClase['bool']
	DirsClase['char'] 		= DirBaseClase['char']

def initDirsMetodo ():
	global DirsMetodo
	DirsMetodo['numeral'] 	= DirBaseMetodo['numeral']
	DirsMetodo['real'] 		= DirBaseMetodo['real']
	DirsMetodo['string'] 	= DirBaseMetodo['string']
	DirsMetodo['bool'] 		= DirBaseMetodo['bool']
	DirsMetodo['char'] 		= DirBaseMetodo['char']

def initDirsMetodoTemp ():
	global DirsMetodoTemp
	DirsMetodoTemp['numeral'] 	= DirBaseMetodoTemp['numeral']
	DirsMetodoTemp['real'] 		= DirBaseMetodoTemp['real']
	DirsMetodoTemp['string'] 	= DirBaseMetodoTemp['string']
	DirsMetodoTemp['bool'] 		= DirBaseMetodoTemp['bool']
	DirsMetodoTemp['char'] 		= DirBaseMetodoTemp['char']

DirsConst['numeral'] 	= 56002
DirsConst['real'] 		= 61002
DirsConst['string'] 	= 66002
DirsConst['bool'] 		= 71002
DirsConst['char'] 		= 76002

# Diccionario a manera de mapa para identificar a las constantes encontradas
DirsConstMap = {}

DirsConstMap['numeral'] = {}
DirsConstMap['real'] = {}
DirsConstMap['string'] = {}
DirsConstMap['bool'] = {}
DirsConstMap['char'] = {}

# Inicializacion de constantes basicas
DirsConstMap['numeral']['0'] 	= 56001
DirsConstMap['real']['0'] 		= 61001
DirsConstMap['string']['""']	= 66001
DirsConstMap['bool']['false'] 	= 71001
DirsConstMap['char']['0'] 		= 76001

# Global que almacena el error de sintaxis
error = "'Program declaration'"

# Lista de precedencia de operaciones
precedence = (
	('left','OR'),
	('left','AND'),
	('right','NOT'),
	('nonassoc', 'MAYOR', 'MAYORIGUAL', 'MENOR', 'MENORIGUAL', 'IGUALC', 'NOTIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR','ENTRE','MOD'),
    ('right','UMINUS'),
    )

# RESIDUALES
arch = open('codigo.txt', 'w')

#############################################################################
#							METODOS AUXILIARES								#
#############################################################################

# Metodo que devuelve un BOOLEANO indicando si el parametro es un tipo de dato primitivo
def esTipoBasico(tipo):
	global TiposVar 
	return (tipo in TiposVar)

# Metodo que devuelve un BOOLEANO indicando si VAR es un atributo que forme parte de los ancestros de una clase
def checarAtributoAncestros(ancestros, var, lineNumber):
	listaAn = ancestros.items()
	for item in listaAn:
		print(item[1])
		if (item[1]['variables'].has_key(var)):
			return True
	return False

# Metodo que devuelve un BOOLEANO indicando si VAR (que forma parte del arreglo ANCESTROS) es una variable dimensionada
def checarAtributoAncestrosDim(ancestros, var, lineNumber):
	listaAn = ancestros.items()
	for item in listaAn:
		if (item[1]['variables'].has_key(var)):
			if (item[1]['variables'][var].has_key('dim')):
				return True
			else:
				return False

# Metodo que devuelve el tipo (STRING) de la variable VAR (que forma parte del arreglo ANCESTROS)
def valorAtributoAncestros(ancestros, var, lineNumber):
	listaAn = ancestros.items()
	for item in listaAn:
		if (item[1]['variables'].has_key(var)):
			return item[1]['variables'][var]['tipo']

# Metodo que devuelve un BOOLEANO indicando si VAR (que forma parte del arreglo ANCESTROS) es una variable visible (publica)
def esVisibleAtributoAncestros(ancestros, var, lineNumber):
	listaAn = ancestros.items()
	for item in listaAn:
		if (item[1]['variables'].has_key(var)):
			return (item[1]['variables'][var]['acceso'] == 'visible')

# Metodo que devuelve un BOOLEANO indicando si MET es un metodo que forme parte de los ancestros de una clase
def checarMetodoAncestros(ancestros, met, lineNumber):
	listaAn = ancestros.items()
	for item in listaAn:
		if (item[1]['metodos'].has_key(met)):
			return True
	return False

# Metodo que devuelve el tipo de retorno (STRING) del metodo MET (que forma parte del arreglo ANCESTROS)
def valorMetodoAncestros(ancestros, met, lineNumber):
	listaAn = ancestros.items()
	for item in listaAn:
		if (item[1]['metodos'].has_key(met)):
			return item[1]['metodos'][met]['retorno']

# Metodo que devuelve un BOOLEANO indicando si MET es un metodo visible (publico)
def esVisibleMetodoAncestros(ancestros, met, lineNumber):
	listaAn = ancestros.items()
	for item in listaAn:
		if (item[1]['metodos'].has_key(met)):
			return (item[1]['metodos'][met]['acceso'] == 'visible')

# Metodo que devuelve la referencia a METODO en la jerarquia de la clase CLASE
def devuelveMetodo(clase, metodo):
	if (DirClases[clase]['metodos'].has_key(metodo)):
		return DirClases[clase]['metodos'][metodo]
	else:
		return devuelveMetodo(DirClases[clase]['padre'],metodo)

# Metodo que devuelve la clase a la cual pertenece METODO en la jerarquia de la clase CLASE
def devuelveClaseMetodo(clase, metodo):
	if (DirClases[clase]['metodos'].has_key(metodo)):
		return clase
	else:
		return devuelveClaseMetodo(DirClases[clase]['padre'],metodo)

# Metodo que devuelve la referencia a PARAMETROS del metodo METODO en la jerarquia de la clase CLASE
def devuelveParametros(clase, metodo):
	if (DirClases[clase]['metodos'].has_key(metodo)):
		return DirClases[clase]['metodos'][metodo]['parametros']
	else:
		return devuelveParametros(DirClases[clase]['padre'],metodo)

# Metodo que devuelve la referencia a VARS del metodo METODO en la jerarquia de la clase CLASE
def devuelveVars(clase, metodo):
	if (DirClases[clase]['metodos'].has_key(metodo)):
		return DirClases[clase]['metodos'][metodo]['vars']
	else:
		return devuelveVars(DirClases[clase]['padre'],metodo)

#############################################################################
#							REGLAS DE PRODUCCION							#
#############################################################################

# Produccion de programa
def p_programa(p):
	'''programa : ciclo_clase clase_main
				| clase_main'''
	print('Compilation successful!')

# Produccion de ciclo de clases que conforman al programa
def p_ciclo_clase(p):
	'''ciclo_clase 	: clase
					| ciclo_clase clase'''
	print('ciclo_clase')	

# Produccion de declaracion de clase
def p_clase(p):
	'''clase : CLASS ID declararClase herencia LLIZQ ciclo_vars ciclo_func LLDER limpiarMetodoActual
			 | CLASS ID declararClase herencia LLIZQ ciclo_vars LLDER limpiarMetodoActual
			 | CLASS ID declararClase herencia LLIZQ ciclo_func LLDER limpiarMetodoActual
			 | CLASS ID declararClase herencia LLIZQ LLDER limpiarMetodoActual'''
	global ClaseActual
	# Se indica que el parsing de la clase se ha completado
	DirClases[ClaseActual]['estatus'] = 'completa'
	print('clase')

# Acciones semanticas de declaracion de clase
def p_declararClase(p):
	'''declararClase : '''
	global ClaseActual
	global DirClases
	ClaseActual = scanner.ultimoId

	# Validacion de valor unico de nombre de Clase
	if(DirClases.has_key(ClaseActual)):
		lineNumber = scanner.lexer.lineno
		print('Semantic error at line {0}, multiple declaration of Class {1}.').format(lineNumber, ClaseActual)
		exit()
	else:
		# Dar de alta operacion de asignacion para instancias de la nueva Clase
		CuboSemantico[ClaseActual] = {}
		CuboSemantico[ClaseActual]['='] = {}
		CuboSemantico[ClaseActual]['='][ClaseActual] = ClaseActual

		# Inicializion de direcciones validas de clase
		initDirsClase()

		# Dar de alta Clase en Directorio de clases
		DirClases[ClaseActual] = {}

		# Diccionario de variables, que indexa por nombre las variables declaradas en una Clase,
		# almacenando informacion como tipo/Clase y acceso
		# USO: Validaciones de existencia y unicidad de nombres de variables
		DirClases[ClaseActual]['variables'] = { 'this' : {'tipo': ClaseActual, 'acceso' : 'hidden'} }

		# Diccionario de variables, que indexa por tipo las variables declaradas en una Clase,
		# almacenando su direccion y nombre normalizado (en caso de tratarse de atributos de objetos)
		# USO: Direccionamiento en generacion de cuadruplos
		DirClases[ClaseActual]['vars'] = { 'numeral' : {}, 'real' : {}, 'string' : {}, 'char' : {}, 'bool' : {} }

		# Diccionario que almacena metodos asociados a Clase
		DirClases[ClaseActual]['metodos'] = {}

		# Diccionario de almacena referencias a ancestros de una Clase
		DirClases[ClaseActual]['ancestros'] = {}

		# Bandera que indica si la Clase esta siendo parseada
		DirClases[ClaseActual]['estatus'] = 'procesando'

		# Diccionario que indexa por tipo las variables dimensionadas declaradas en una Clase,
		# almacenando su tamanio
		DirClases[ClaseActual]['varsTam'] = { 'numeral' : {}, 'real' : {}, 'string' : {}, 'char' : {}, 'bool' : {} }

		# Diccionario que indexa por nombre los objetos de una Clase, y almacena para cada uno de ellos
		# la direccion de su primer variable/atributo para cada tipo de dato atomico
		DirClases[ClaseActual]['obj'] = {}

		# Diccionario que almacena el total de variables de Clase, por tipo de dato atomico 
		DirClases[ClaseActual]['tam'] = {'numeral' : 0, 'real' : 0, 'bool' : 0, 'string' : 0, 'char' : 0}

# Accion semantica de sanitizacion
def p_limpiarMetodoActual(p):
	'''limpiarMetodoActual : '''
	global MetodoActual
	MetodoActual = ''

# Accion semantica de sanitizacion
def p_limpiarInvocador(p):
	'''limpiarInvocador : '''
	global Invocador
	global InvocadorTipo
	Invocador = ''
	InvocadorTipo = ''

# Produccion para verificar herencia
def p_herencia(p):
	'''herencia : empty
				| UNDER ID agregaAncestro'''
	print('herencia')

# Acciones semanticas para representacion de herencia de Clase
def p_agregaAncestro(p):
	'''agregaAncestro : '''
	global ClaseActual
	global DirClases
	ancestro = scanner.ultimoId
	lineNumber = scanner.lexer.lineno

	# Validar existencia de ancestro
	if(not DirClases.has_key(ancestro)):
		print('Semantic error at line {0}, Class {1} not declared and used in inheritance.').format(lineNumber, ancestro)
		exit()
	# Validar que el nombre de la nueva Clase no sea atributo de ancestros
	elif ( checarAtributoAncestros(DirClases[ancestro]['ancestros'], ClaseActual, lineNumber) or DirClases[ancestro]['variables'].has_key(ClaseActual) ):
		print('Semantic error at line {0}, attribute {1} already declared in Class Hierarchy.').format(lineNumber, ClaseActual)
		exit()
	# Validar que el nombre de la nueva Clase no sea metodo de ancestros
	elif ( checarMetodoAncestros(DirClases[ancestro]['ancestros'], ClaseActual, lineNumber) or DirClases[ancestro]['metodos'].has_key(ClaseActual) ):
		print('Semantic error at line {0}, method {1} already declared in Class Hierarchy.').format(lineNumber, ClaseActual)
		exit()
	else:
		# Copiar informacion de variables de jerarquia de clases
		for tipo in TiposVar:
			DirClases[ClaseActual]['vars'][tipo] = copy.deepcopy(DirClases[ancestro]['vars'][tipo])
			DirClases[ClaseActual]['varsTam'][tipo] = copy.deepcopy(DirClases[ancestro]['varsTam'][tipo])

		# Agregar ancestro y ancestros de ancestro
		DirClases[ClaseActual]['ancestros'] = DirClases[ancestro]['ancestros']
		DirClases[ClaseActual]['ancestros'][ancestro] = DirClases[ancestro]

		# Definir ancestro inmediato / padre
		DirClases[ClaseActual]['padre'] = ancestro

		# Copiar informacion de objetos de jerarquia de clases
		DirClases[ClaseActual]['obj'] = copy.deepcopy(DirClases[ancestro]['obj'])

		# Copiar informacion de cantidad de variables de jerarquia de clases
		DirClases[ClaseActual]['tam'] = copy.deepcopy(DirClases[ancestro]['tam'])

		# Actualizar direcciones disponibles a partir de cantidad de variables en jerarquia de clases
		for tipo in TiposVar:
			DirsClase[tipo] = DirsClase[tipo] + DirClases[ClaseActual]['tam'][tipo]

# Produccion de ciclo de declaracion de variables
def p_ciclo_vars(p):
	'''ciclo_vars 	: acceso vars
					| ciclo_vars acceso vars'''
	print('ciclo_vars')

# Produccion de ciclo de declaracion de metodos
def p_ciclo_func(p):
	'''ciclo_func 	: func
					| ciclo_func func'''
	print('ciclo_func')

# Produccion de ciclo de declaracion de clase MAIN
def p_clase_main(p):
	'''clase_main 	: CLASS MAIN declararClase LLIZQ ciclo_vars ciclo_func main LLDER
					| CLASS MAIN declararClase LLIZQ ciclo_vars main LLDER
					| CLASS MAIN declararClase LLIZQ ciclo_func main LLDER
					| CLASS MAIN declararClase LLIZQ main LLDER'''
	print('clase_main')

# Produccion auxiliar para declaracion de variables
def p_vars(p):
	'''vars : var_op PYC'''
	print('vars')

# Produccion de ciclo de declaracion de variables
def p_var_op(p):
	'''var_op 	: tipo ciclo_tipo
				| ID revisarExistenciaClase DOSP ciclo_id'''
	print('var_op')

# Acciones semanticas de validacion de declaracion de instancia de Clase
def p_revisarExistenciaClase(p):
	'''revisarExistenciaClase : '''
	global ClaseActual
	global DirClases
	tipo = scanner.ultimoId
	lineNumber = scanner.lexer.lineno

	# Validar que la clase forme parte del Directorio de clases
	if(not DirClases.has_key(tipo)):
		print('Semantic error at line {0}, Class {1} not declared but being instanced.').format(lineNumber, tipo)
		exit()
	# Validar que la clase haya terminado de ser procesada
	elif (DirClases[tipo]['estatus'] == 'procesando'):
		print('Semantic error at line {0}, trying to instantiate Class {1} but its Class definition is incomplete.').format(lineNumber, tipo)
		exit()
	else:
		# Guardar Clase
		scanner.ultimoTipo = tipo

# Produccion de ciclo de declaracion de variables atomicas
def p_ciclo_tipo(p):
	'''ciclo_tipo 	: ID declararVariable
					| ID COIZQ cte_numeral CODER declararVariableDim
					| ciclo_tipo COMA ID declararVariable
					| ciclo_tipo COMA ID COIZQ cte_numeral CODER declararVariableDim'''
	print('ciclo_tipo')

# Produccion de ciclo de declaracion de objetos
def p_ciclo_id(p):
	'''ciclo_id 	: ID declararVariable
					| ciclo_id COMA ID declararVariable'''
	print('ciclo_id')

# Acciones semanticas de declaracion de variables dimensionadas
def p_declararVariableDim(p):
	'''declararVariableDim : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	global DirsClase 
	global DirsMetodo

	lineNumber = scanner.lexer.lineno
	var = scanner.ultimoId # Nombre de variable
	tam = int(scanner.ultimoNumeral) # Tamanio

	# Validar que la variable no tenga nombre de Clase
	if(DirClases.has_key(var)):
		print('Semantic error at line {0}, variable {1} declared but Class {1} already exists.').format(lineNumber, var)
		exit()
	# Validar que la variable no haya sido declarada previamente como atributo en la jerarquia de clases
	elif( (DirClases[ClaseActual]['variables'].has_key(var) or checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], var, lineNumber)) and MetodoActual == ''):
		print('Semantic error at line {0}, variable {1} already declared.').format(lineNumber, var)
		exit()
	# Validar que la variable no haya sido declarada previamente como metodo en la jerarquia de clases
	elif(DirClases[ClaseActual]['metodos'].has_key(var) or checarMetodoAncestros(DirClases[ClaseActual]['ancestros'], var, lineNumber)):
		print('Semantic error at line {0}, variable {1} declared but function {1} already declared.').format(lineNumber, var)
		exit()
	# Validar que la variable no haya sido declarada previamente como variable en el metodo actual
	elif(MetodoActual != '' and DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(var)):
		print('Semantic error at line {0}, variable {1} already declared.').format(lineNumber, var)
		exit()
	else:
		tipo = scanner.ultimoTipo

		# Dar de alta variable dimensionada de Clase
		if(MetodoActual == ''):
			DirClases[ClaseActual]['variables'][var] = {'tipo': scanner.ultimoTipo, 'acceso' : scanner.ultimoAcceso, 'dim' : tam}
			DirClases[ClaseActual]['vars'][tipo][var] = DirsClase[tipo]
			DirClases[ClaseActual]['tam'][tipo] = DirClases[ClaseActual]['tam'][tipo] + tam
			DirsClase[tipo] = DirsClase[tipo] + tam
			DirClases[ClaseActual]['varsTam'][tipo][var] = tam
		# Dar de alta variable dimensionada de Metodo
		else:
			DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][var] = {'tipo': scanner.ultimoTipo, 'acceso' : 'hidden', 'dim' : tam}
			DirClases[ClaseActual]['metodos'][MetodoActual]['vars'][tipo][var] = DirsMetodo[tipo]
			DirsMetodo[tipo] = DirsMetodo[tipo] + tam

# Acciones semanticas de declaracion de variables dimensionadas
def p_declararVariable(p):
	'''declararVariable : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	global DirsClase 
	global DirsMetodo

	lineNumber = scanner.lexer.lineno
	var = scanner.ultimoId # Nombre de variable

	# Validar que la variable no tenga nombre de Clase
	if(DirClases.has_key(var)):
		print('Semantic error at line {0}, variable {1} declared but Class {1} already exists.').format(lineNumber, var)
		exit()
	# Validar que la variable no haya sido declarada previamente como atributo en la jerarquia de clases
	elif( (DirClases[ClaseActual]['variables'].has_key(var) or checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], var, lineNumber)) and MetodoActual == ''):
		print('Semantic error at line {0}, variable {1} already declared.').format(lineNumber, var)
		exit()
	# Validar que la variable no haya sido declarada previamente como metodo en la jerarquia de clases
	elif(DirClases[ClaseActual]['metodos'].has_key(var) or checarMetodoAncestros(DirClases[ClaseActual]['ancestros'], var, lineNumber)):
		print('Semantic error at line {0}, variable {1} declared but function {1} already declared.').format(lineNumber, var)
		exit()
	# Validar que la variable no haya sido declarada previamente como variable en el metodo actual
	elif(MetodoActual != '' and DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(var)):
		print('Semantic error at line {0}, variable {1} already declared.').format(lineNumber, var)
		exit()
	else:
		tipo = scanner.ultimoTipo
		# Dar de alta variable de Clase
		if(MetodoActual == ''):
			DirClases[ClaseActual]['variables'][var] = {'tipo': scanner.ultimoTipo, 'acceso' : scanner.ultimoAcceso}
			# Dar de alta variable de tipo primitivo
			if (esTipoBasico(tipo)):
				DirClases[ClaseActual]['vars'][tipo][var] = DirsClase[tipo]
				DirClases[ClaseActual]['tam'][tipo] = DirClases[ClaseActual]['tam'][tipo] + 1 
				DirsClase[tipo] = DirsClase[tipo] + 1
			# Dar de alta objeto
			else:
				DirClases[ClaseActual]['obj'][var] = { 'numeral' : -1, 'real' : -1, 'string' : -1, 'char' : -1, 'bool' : -1, 'tipo' : tipo  }
				# Normalizacion de atributos de objeto
				for tipoVariable in TiposVar:
					esPrimero = True
					# Ordenar atributos de objeto en funcion de su orden de declaracion
					for variable in sorted(DirClases[tipo]['vars'][tipoVariable], key = DirClases[tipo]['vars'][tipoVariable].get):
						# Dar de alta cada atributo del objeto como variable de la clase
						DirClases[ClaseActual]['vars'][tipoVariable][var + '.' + variable] = DirsClase[tipoVariable]
						# Almacenar direccion del primer atributo de tipo 'tipoVariable' que forma parte del objeto
						if (esPrimero):
							DirClases[ClaseActual]['obj'][var][tipoVariable] = DirsClase[tipoVariable]
							esPrimero = False
						# En caso de que el atributo sea dimensionado, memorizar su longitud,
						# actualizar la siguiente direccion disponible dependiendo de su longitud y
						# actualizar el contador de atributos del tipo dado dependiendo de su longitud
						if (DirClases[tipo]['varsTam'][tipoVariable].has_key(variable)):
							DirClases[ClaseActual]['varsTam'][tipoVariable][var + '.' + variable] = DirClases[tipo]['varsTam'][tipoVariable][variable]
							DirsClase[tipoVariable] = DirsClase[tipoVariable] + DirClases[tipo]['varsTam'][tipoVariable][variable]
							DirClases[ClaseActual]['tam'][tipoVariable] = DirClases[ClaseActual]['tam'][tipoVariable] + DirClases[tipo]['varsTam'][tipoVariable][variable]
						# Si el atributo no es dimensionado, solamente aumentar en uno el contador de direcciones y
						# el contador de atributos del tipo dado
						else:
							DirsClase[tipoVariable] = DirsClase[tipoVariable] + 1
							DirClases[ClaseActual]['tam'][tipoVariable] = DirClases[ClaseActual]['tam'][tipoVariable] + 1
		# Dar de alta variable de Metodo
		else:
			DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][var] = {'tipo': scanner.ultimoTipo, 'acceso' : 'hidden'}
			# Dar de alta variable de tipo primitivo
			if (esTipoBasico(tipo)):
				DirClases[ClaseActual]['metodos'][MetodoActual]['vars'][tipo][var] = DirsMetodo[tipo]
				DirsMetodo[tipo] = DirsMetodo[tipo] + 1
			# Dar de alta objeto
			else:
				DirClases[ClaseActual]['metodos'][MetodoActual]['obj'][var] = { 'numeral' : -1, 'real' : -1, 'string' : -1, 'char' : -1, 'bool' : -1, 'tipo' : tipo  }
				# Normalizacion de atributos de objeto
				for tipoVariable in TiposVar:
					esPrimero = True
					# Ordenar atributos de objeto en funcion de su orden de declaracion
					for variable in sorted(DirClases[tipo]['vars'][tipoVariable], key = DirClases[tipo]['vars'][tipoVariable].get):
						# Dar de alta cada atributo del objeto como variable de la clase
						DirClases[ClaseActual]['metodos'][MetodoActual]['vars'][tipoVariable][var + '.' + variable] = DirsMetodo[tipoVariable]
						# Almacenar direccion del primer atributo de tipo 'tipoVariable' que forma parte del objeto
						if (esPrimero):
							DirClases[ClaseActual]['metodos'][MetodoActual]['obj'][var][tipoVariable] = DirsMetodo[tipoVariable]
							esPrimero = False
						# En caso de que el atributo sea dimensionado, actualizar la siguiente direccion disponible dependiendo de su longitud
						if (DirClases[tipo]['varsTam'][tipoVariable].has_key(variable)):
							DirsMetodo[tipoVariable] = DirsMetodo[tipoVariable] + DirClases[tipo]['varsTam'][tipoVariable][variable]
						# Si el atributo no es dimensionado, solamente aumentar en uno el contador de direcciones
						else:
							DirsMetodo[tipoVariable] = DirsMetodo[tipoVariable] + 1

# Produccion de nombres de tipos primitivos
def p_tipo(p):
	'''tipo 	: NUMERAL
				| REAL
				| BOOL
				| CHAR
				| STRING'''
	print('tipo')

# Produccion de tipos de acceso
def p_acceso(p):
	'''acceso 	: HIDDEN
				| VISIBLE'''
	print('acceso')

# Produccion de declaracion de metodo
def p_func(p):
	'''func 	: acceso tipo ID declararMetodo params cuerpo_func
				| acceso WITHOUT ID declararMetodo params cuerpo_func'''
	initDirsMetodoTemp()
	print('func')

# Acciones semanticas para declaracion de metodo
def p_declararMetodo(p):
	'''declararMetodo : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	lineNumber = scanner.lexer.lineno
	retorno = scanner.ultimoTipo # Tipo de retorno del metodo
	MetodoActual = scanner.ultimoId # Nombre de metodo
	# Inicializacion de direcciones de metodo
	initDirsMetodo()
	initDirsMetodoTemp()
	
	# Validar que metodo no se llame como una Clase
	if(DirClases.has_key(MetodoActual) and MetodoActual != 'main'):
		print('Semantic error at line {0}, method {1} declared but Class {1} already exists.').format(lineNumber, MetodoActual)
		exit()
	# Verificar que metodo no se llame como algun atributo declarado en la jerarquia de clases
	elif( DirClases[ClaseActual]['variables'].has_key(MetodoActual) or checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], MetodoActual, lineNumber) ):
		print('Semantic error at line {0}, method {1} declared but variable {1} already declared.').format(lineNumber, MetodoActual)
		exit()
	# Verificar que metodo no se llame como algun metodo declarado en la jerarquia de clases
	elif(DirClases[ClaseActual]['metodos'].has_key(MetodoActual) or checarMetodoAncestros(DirClases[ClaseActual]['ancestros'], MetodoActual, lineNumber) ):
		print('Semantic error at line {0}, method {1} already declared.').format(lineNumber, MetodoActual)
		exit()
	else:
		# Dar de alta metodo en Clase actual
		DirClases[ClaseActual]['metodos'][MetodoActual] = {}

		# Diccionario de variables, que indexa por nombre las variables declaradas en el metodo,
		# almacenando informacion como tipo/Clase y acceso
		# USO: Validaciones de existencia y unicidad de nombres de variables
		DirClases[ClaseActual]['metodos'][MetodoActual]['variables'] = {}

		# Diccionario de variables, que indexa por tipo las variables declaradas en el metodo,
		# almacenando su direccion y nombre normalizado (en caso de tratarse de atributos de objetos)
		# USO: Direccionamiento en generacion de cuadruplos
		DirClases[ClaseActual]['metodos'][MetodoActual]['vars'] = { 'numeral' : {}, 'real' : {}, 'string' : {}, 'char' : {}, 'bool' : {} }

		# Diccionario que almacena parametros asociados a Clase
		DirClases[ClaseActual]['metodos'][MetodoActual]['parametros'] = []

		# Tipo de retorno del metodo
		DirClases[ClaseActual]['metodos'][MetodoActual]['retorno'] = retorno

		# Tipo de acceso al metodo
		DirClases[ClaseActual]['metodos'][MetodoActual]['acceso'] = scanner.ultimoAcceso

		# Diccionario que indexa por nombre los objetos declarados en un metodo, y almacena para cada uno de ellos
		# la direccion de su primer variable/atributo para cada tipo de dato atomico
		DirClases[ClaseActual]['metodos'][MetodoActual]['obj'] = {}

# Produccion de declaracion de metodo main
def p_main(p):
	'''main 	: acceso WITHOUT MAIN rellenaCuadInicial declararMetodo PIZQ PDER cuerpo_func'''
	print('main')

# Accion semantica para indicar cuadruplo en que comienza metodo main
def p_rellenaCuadInicial(p):
    '''rellenaCuadInicial : '''
    global Line
    Cuad[0][2] = Line

# Produccion de declaracion de parametros
def p_params(p):
	'''params 	: PIZQ params_ciclo PDER
				| PIZQ PDER'''
	print('params')

# Produccion de ciclo de parametros
def p_params_ciclo(p):
	'''params_ciclo 	: tipo ID meterParametros
						| tipo ID COIZQ cte_numeral CODER meterParametrosDim
						| params_ciclo COMA tipo ID meterParametros
						| params_ciclo COMA tipo ID COIZQ cte_numeral CODER meterParametrosDim'''
	print('params_ciclo')

# Acciones semanticas para declarar parametros dimensionados
def p_meterParametrosDim(p):
	'''meterParametrosDim : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	lineNumber = scanner.lexer.lineno
	parametro = scanner.ultimoId # Nombre de parametro
	tipo = scanner.ultimoTipo # Tipo de parametro
	tam = int(scanner.ultimoNumeral) # Tamanio

	# Dar de alta en variables de metodo
	DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][parametro] = {'tipo':tipo, 'acceso':'hidden', 'dim' : tam}
	DirClases[ClaseActual]['metodos'][MetodoActual]['vars'][tipo][parametro] = DirsMetodo[tipo]

	# Dar de alta en parametros de metodo
	DirClases[ClaseActual]['metodos'][MetodoActual]['parametros'].append([tipo, parametro, tam])

	# Actualizar direcciones disponibles a partir de tamanio de arreglo
	DirsMetodo[tipo] = DirsMetodo[tipo] + tam

	print('+++DIRNUMERAL')
	print(DirsMetodo['numeral'])

# Acciones semanticas para declarar parametros
def p_meterParametros(p):
	'''meterParametros : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	lineNumber = scanner.lexer.lineno
	parametro = scanner.ultimoId # Nombre de parametro
	tipo = scanner.ultimoTipo # Tipo de parametro

	# Dar de alta en variables de metodo
	DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][parametro] = {'tipo':tipo, 'acceso':'hidden'}
	DirClases[ClaseActual]['metodos'][MetodoActual]['vars'][tipo][parametro] = DirsMetodo[tipo]

	# Dar de alta en parametros de metodo
	DirClases[ClaseActual]['metodos'][MetodoActual]['parametros'].append([tipo, parametro])

	# Actualizar direcciones disponibles
	DirsMetodo[tipo] = DirsMetodo[tipo] + 1

# Acciones semanticas para contabilizar cantidad de variables declaradas en metodo
def p_tamMetodo(p):
	'''tamMetodo : '''
	global ClaseActual
	global MetodoActual
	global Line
	
	DirClases[ClaseActual]['metodos'][MetodoActual]['tam'] = {}
	DirClases[ClaseActual]['metodos'][MetodoActual]['tamTemp'] = {}

	DirClases[ClaseActual]['metodos'][MetodoActual]['tam']['numeral']	= DirsMetodo['numeral'] - DirBaseMetodo['numeral']
	DirClases[ClaseActual]['metodos'][MetodoActual]['tam']['real'] 		= DirsMetodo['real'] - DirBaseMetodo['real']
	DirClases[ClaseActual]['metodos'][MetodoActual]['tam']['char'] 		= DirsMetodo['char'] - DirBaseMetodo['char']
	DirClases[ClaseActual]['metodos'][MetodoActual]['tam']['string'] 	= DirsMetodo['string'] - DirBaseMetodo['string']
	DirClases[ClaseActual]['metodos'][MetodoActual]['tam']['bool'] 		= DirsMetodo['bool'] - DirBaseMetodo['bool']

	DirClases[ClaseActual]['metodos'][MetodoActual]['tamTemp']['numeral'] 	= DirsMetodoTemp['numeral'] - DirBaseMetodoTemp['numeral']
	DirClases[ClaseActual]['metodos'][MetodoActual]['tamTemp']['real'] 		= DirsMetodoTemp['real'] - DirBaseMetodoTemp['real']
	DirClases[ClaseActual]['metodos'][MetodoActual]['tamTemp']['char'] 		= DirsMetodoTemp['char'] - DirBaseMetodoTemp['char']
	DirClases[ClaseActual]['metodos'][MetodoActual]['tamTemp']['string'] 	= DirsMetodoTemp['string'] - DirBaseMetodoTemp['string']
	DirClases[ClaseActual]['metodos'][MetodoActual]['tamTemp']['bool'] 		= DirsMetodoTemp['bool'] - DirBaseMetodoTemp['bool'] 

# Produccion de cuerpo de funcion
def p_cuerpo_func(p):
	'''cuerpo_func 	: inicioFunc LLIZQ ciclo_vars_func ciclo_estatuto LLDER tamMetodo
					| inicioFunc LLIZQ ciclo_vars_func LLDER tamMetodo
					| inicioFunc LLIZQ ciclo_estatuto LLDER tamMetodo
					| inicioFunc LLIZQ LLDER tamMetodo'''
	global ClaseActual
	global MetodoActual
	global Line
	lineNumber = scanner.lexer.lineno
	# Tipo de retorno de metodo actual
	refTipo = DirClases[ClaseActual]['metodos'][MetodoActual]['retorno']

	# Generar cuadruplo de retorno default para cada tipo de metodo
	if (refTipo == 'numeral'):
		Cuad.append(['RETURN', DirsConstMap['numeral']['0'], '-', '-'])
	elif (refTipo == 'real'):
		Cuad.append(['RETURN', DirsConstMap['real']['0'], '-', '-'])
	elif (refTipo == 'bool'):
		Cuad.append(['RETURN', DirsConstMap['bool']['false'], '-', '-'])
	elif (refTipo == 'char'):
		Cuad.append(['RETURN', DirsConstMap['char']['0'], '-', '-'])
	elif (refTipo == 'string'):
		Cuad.append(['RETURN', DirsConstMap['string']['""'], '-', '-'])
	else:
		Cuad.append(['RETURN', '-',  '-', '-'])
	Line = Line + 1
	print('cuerpo_func')

# Accion semantica para indicar numero de cuadruplo en que inica el metodo
def p_inicioFunc(p):
	'''inicioFunc : '''
	global ClaseActual
	global MetodoActual
	DirClases[ClaseActual]['metodos'][MetodoActual]['inicio'] = len(Cuad)

# Produccion de ciclo de variables de funcion
def p_ciclo_vars_func(p):
	'''ciclo_vars_func 	: vars
						| ciclo_vars_func vars'''
	print('ciclo_vars_func')

# Produccion de ciclo de estatutos
def p_ciclo_estatuto(p):
	'''ciclo_estatuto 	: estatuto
						| ciclo_estatuto estatuto'''
	print('ciclo_estatuto')

# Produccion de opciones de estatutos
def p_estatuto(p):
	'''estatuto 	: while
					| asignacion
					| condicion
					| escritura
					| lectura
					| llamada_func limpiarInvocador PYC
					| return'''
	print('estatuto')

# Produccion de llamada a metodo con invocador
def p_llamada_func_invocador(p):
	'''llamada_func : ID PUNTO definirInvocador ID checarFuncion generaEra PIZQ limpiarInvocador exp_ciclo PDER generarGosub
					| ID PUNTO definirInvocador ID checarFuncion generaEra PIZQ limpiarInvocador PDER generarGosub'''
	pos = len(p) - 1
	p[0] = { 'tipo': p[pos]['tipo'], 'id': p[pos]['id'], 'esFuncion' : True }
	print('llamada_func')

# Produccion de llamada a metodo en cotexto de clase actual
def p_llamada_func_sin_invocador(p):
	'''llamada_func : ID checarFuncion generaEra PIZQ limpiarInvocador exp_ciclo PDER generarGosub
					| ID checarFuncion generaEra PIZQ limpiarInvocador PDER generarGosub'''
	pos = len(p) - 1
	p[0] = { 'tipo': p[pos]['tipo'], 'id': p[pos]['id'], 'esFuncion' : True }
	print('llamada_func')

# Acciones semanticas para cuadruplo GOSUB al momento de entrar el contexto de un nuevo metodo invocado
def p_generaGosub(p):
	'''generarGosub : '''
	lineNumber = scanner.lexer.lineno
	global PilaLlamadas
	global Line
	actual = PilaLlamadas.top() # Referencia a metodo que ha sido invocado 
	clase = ''	# Clase a la cual pertenece el metodo
	metodo = actual['id'] # Nombre de metodo
	invocador = '' #Invocador del metodo
	
	# Verificar si el metodo tiene invocador
	if ( actual.has_key('invocador') ):
		clase = actual['invocadorTipo']
		invocador = actual['invocador']
	else:
		clase = ClaseActual

	# Obtener direccion de inicio de metodo
	dirInicio = devuelveMetodo(clase, metodo)['inicio']

	# Verificar coincidencia de numero de parametros
	if ( len( devuelveMetodo(clase, metodo)['parametros'] ) > actual['numP'] ):
		print('Semantic error at line {0}, less parameters than expected passed to \'{1}\' method of Class \'{2}\'.').format(lineNumber, metodo, clase)
		exit()
	
	# Obtener tipo de retorno de metodo
	tipo = devuelveMetodo(clase, metodo)['retorno']
	# Obtener clase a la cual pertenece el metodo
	claseMet = devuelveClaseMetodo(clase,metodo)

	# Si no hay invocador, se pasa la clase actual
	if (invocador == ''):
		# Se pasa al nuevo contexto de la llamada de funcion, todos los atributos
		# que pertenecen a la clase actual
		for tipoVariable in TiposVar:
			if (DirClases[claseMet]['tam'][tipoVariable] > 0):
				total = DirClases[claseMet]['tam'][tipoVariable]
				dirClase = DirBaseClase[tipoVariable]
				for i in range(0, total):
					Cuad.append(['ATTR_GO', dirClase, dirClase, '-'])
					Line = Line + 1
					dirClase = dirClase + 1
	# Si existe invocador, se pasa la clase del invocador
	else:
		# Busca instancia en metodo
		if ( DirClases[ClaseActual]['metodos'][MetodoActual]['obj'].has_key(invocador) ):
			# Se pasa al nuevo contexto de la llamada de funcion, todos los atributos
			# que pertenecen a la clase del invocador
			for tipoVariable in TiposVar:
				dirInstancia = DirClases[ClaseActual]['metodos'][MetodoActual]['obj'][invocador][tipoVariable]
				if (dirInicio != -1):
					total = DirClases[clase]['tam'][tipoVariable]
					dirClase = DirBaseClase[tipoVariable]
					for i in range(0, total):
						Cuad.append(['ATTR_GO', dirInstancia, dirClase, '-'])
						Line = Line + 1
						dirInstancia = dirInstancia + 1
						dirClase = dirClase + 1
		# Busca instancia en clase
		else:
			# Se pasa al nuevo contexto de la llamada de funcion, todos los atributos
			# que pertenecen a la clase del invocador
			for tipoVariable in TiposVar:
				dirInstancia = DirClases[ClaseActual]['obj'][invocador][tipoVariable]
				if (dirInicio != -1):
					total = DirClases[clase]['tam'][tipoVariable]
					dirClase = DirBaseClase[tipoVariable]
					for i in range(0, total):
						Cuad.append(['ATTR_GO', dirInstancia, dirClase, '-'])
						Line = Line + 1
						dirInstancia = dirInstancia + 1
						dirClase = dirClase + 1

	# Si el metodo no es de tipo without/void, entonces se almacena
	# su valor de retorno en una variable temporal
	id = -1
	if (tipo != 'without'):
		id = DirsMetodoTemp[tipo]
		DirsMetodoTemp[tipo] = DirsMetodoTemp[tipo] + 1
		Cuad.append(['GOSUB', metodo, dirInicio, id])
	else:
		Cuad.append(['GOSUB', metodo, dirInicio, '-'])
	
	Line = Line + 1

	# Proceso inverso de paso de variables, ahora en sentido inverso:
	# ahora es el contexto del metodo quien devuelve los valores (posiblemente alterados)
	# a la clase actual, o al invocador del metodo

	# Pasa clase actual
	if (invocador == ''):
		for tipoVariable in TiposVar:
			print('====')
			print(claseMet)
			print(DirClases[claseMet])
			if (DirClases[claseMet]['tam'][tipoVariable] > 0):
				total = DirClases[claseMet]['tam'][tipoVariable]
				dirClase = DirBaseClase[tipoVariable]
				for i in range(0, total):
					Cuad.append(['ATTR_RET', dirClase, dirClase, '-'])
					Line = Line + 1
					dirClase = dirClase + 1
	# Pasa la clase del invocador
	else:
		# Busca instancia en metodo
		if ( DirClases[ClaseActual]['metodos'][MetodoActual]['obj'].has_key(invocador) ):
			for tipoVariable in TiposVar:
				print('---')
				print(invocador)
				print()
				print(DirClases[ClaseActual]['metodos'][MetodoActual]['obj'])
				dirInstancia = DirClases[ClaseActual]['metodos'][MetodoActual]['obj'][invocador][tipoVariable]
				if (dirInicio != -1):
					total = DirClases[clase]['tam'][tipoVariable]
					dirClase = DirBaseClase[tipoVariable]
					for i in range(0, total):
						Cuad.append(['ATTR_RET', dirClase, dirInstancia, '-'])
						Line = Line + 1
						dirInstancia = dirInstancia + 1
						dirClase = dirClase + 1
		# Busca instancia en clase
		else:
			for tipoVariable in TiposVar:
				dirInstancia = DirClases[ClaseActual]['obj'][invocador][tipoVariable]
				if (dirInicio != -1):
					total = DirClases[clase]['tam'][tipoVariable]
					dirClase = DirBaseClase[tipoVariable]
					for i in range(0, total):
						Cuad.append(['ATTR_RET', dirClase, dirInstancia, '-'])
						Line = Line + 1
						dirInstancia = dirInstancia + 1
						dirClase = dirClase + 1

	# Devolver el valor de retorno de la ejecucion del metodo, en caso de tenerlo
	if (actual.has_key('invocador')):
		p[0] = {'tipo' : tipo, 'id' : id, 'invocador' : actual['invocador'] }
	else:
		p[0] = {'tipo' : tipo, 'id' : id}
	
	PilaLlamadas.pop()
	print('generarGosub')

# Acciones semanticas para cuadruplo ERA al momento de crear el contexto de un nuevo metodo invocado
def p_generaEra(p):
	'''generaEra : '''
	global Line
	global PilaLlamadas
	global ClaseActual
	claseAux = ''
	# Meter a pila de llamadas, junto con invocador
	if (Invocador != ''):
		PilaLlamadas.push( {'id': MetodoNombre, "invocador": Invocador, "invocadorTipo": InvocadorTipo, 'numP': 0} )
		claseAux = devuelveClaseMetodo(InvocadorTipo, MetodoNombre)
	# Meter a pila de llamadas, junto sin invocador
	else:
		PilaLlamadas.push( {'id': MetodoNombre, 'numP': 0} )
		claseAux = devuelveClaseMetodo(ClaseActual, MetodoNombre)

	# Generar cuadruplos ERA para cada tipo de dato primitivo
	for tipo in TiposVar:
		Cuad.append(['ERA', MetodoNombre, tipo, DirClases[claseAux]['metodos'][MetodoNombre]['tam'][tipo] ])
	
	# Generar cuadruplos ERA para cada tipo de dato temporal primitivo
	for tipo in TiposVar:
		Cuad.append(['ERA', MetodoNombre, str(tipo)+'-temp', DirClases[claseAux]['metodos'][MetodoNombre]['tamTemp'][tipo] ])

	Line = Line + 10
	print('generaEra')

# Acciones semanticas para validar una invocacion valida a metodo
def p_checarFuncion(p):
	'''checarFuncion : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	global Invocador
	global InvocadorTipo
	global MetodoNombre
	global MetodoTipo
	lineNumber = scanner.lexer.lineno
	func = scanner.ultimoId # Nombre de Metodo

	# Metodo sin invocador
	if (Invocador == ''):
		# Buscar metodo en clase actual
		if ( DirClases[ClaseActual]['metodos'].has_key(func) ):
			MetodoTipo = DirClases[ClaseActual]['metodos'][func]['retorno']
		# Buscar metodo en ancestros de clase actual
		elif ( checarMetodoAncestros(DirClases[ClaseActual]['ancestros'], func, lineNumber)):
			MetodoTipo = valorMetodoAncestros(DirClases[ClaseActual]['ancestros'], func, lineNumber)
		else:
			print('Semantic error at line {0}, method {1} not found in Class Hierarchy.').format(lineNumber, func)
			exit()
	# Metodo con invocador
	else:
		claseAux = ''
		# Buscar invocador en metodo actual
		if (MetodoActual != ''):
			# Invocador pertenece a metodo actual
			if ( DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(Invocador) ):
				claseAux = DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][Invocador]['tipo']
			# Invocador pertenece a clase actual
			elif ( DirClases[ClaseActual]['variables'].has_key(Invocador) ):
				claseAux = DirClases[ClaseActual]['variables'][Invocador]['tipo']
			# Invocador pertenece a ancestros de clase actual
			elif ( checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], Invocador, lineNumber)):
				claseAux = valorAtributoAncestros(DirClases[ClaseActual]['ancestros'], Invocador, lineNumber)
		# Buscar invocador en clase actual
		else:
			# Invocador pertenece a clase actual
			if ( DirClases[ClaseActual]['variables'].has_key(Invocador) ):
				claseAux = DirClases[ClaseActual]['variables'][Invocador]['tipo']
			# Invocador pertenece a ancestros de clase actual
			elif ( checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], Invocador, lineNumber)):
				claseAux = valorAtributoAncestros(DirClases[ClaseActual]['ancestros'], Invocador, lineNumber)

		# Verificar que metodo sea de tipo public / visible
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
		InvocadorTipo = claseAux
	MetodoNombre = func			

# Acciones semanticas para almacenar informacion del invocador de un metodo o atributo
def p_definirInvocador(p):
	'''definirInvocador : '''
	global ClaseActual
	global MetodoActual
	global DirClases
	global Invocador
	lineNumber = scanner.lexer.lineno
	Invocador = scanner.ultimoId # Nombre de invocador
	# Invocador es atributo de la jerarquia actual de clases
	if ( DirClases[ClaseActual]['variables'].has_key(Invocador) or checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], Invocador, lineNumber)):
		pass
	# Invocador es atributo del metodo actual
	elif (MetodoActual != '' and DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(Invocador) ):
		pass
	else:
		print('Semantic error at line {0}, Class instance {1} not found.').format(lineNumber, Invocador)
		exit()

# Produccion de expresiones en parametros de llamada a funcion
def p_exp_ciclo_1(p):
	'''exp_ciclo 	: exp'''
	global PilaLlamadas
	global Line
	actual = PilaLlamadas.top()
	lineNumber = scanner.lexer.lineno

	# Si la llamada a funcion es invocada desde un objeto
	if(actual.has_key('invocadorTipo')):
		# Se verifica que el numero de parametros leidos no sea mayor al numero de parametros esperados 
		if(actual['numP'] >= len(devuelveParametros(actual['invocadorTipo'], actual['id']))):
			print('Semantic error at line {0}, more parameters given than the {1} specified for function {2} of Class {3}.').format(lineNumber, len(devuelveParametros(actual['invocadorTipo'], actual['id'])), actual['id'], actual['invocadorTipo'])
			exit()
		else:
			# Obtener la lista de tipos de los parametros de la funcion
			listaTipos = copy.deepcopy(devuelveParametros(actual['invocadorTipo'], actual['id']))
			# Checar que los tipos coincidan (se permite el casteo de numeral a real)
			if(p[1]['tipo'] != listaTipos[actual['numP']][0] and not (p[1]['tipo'] == 'numeral' and listaTipos[actual['numP']][0] == 'real') ):
				print('Semantic error at line {0}, parameter #{1} of type \'{2}\' given when type \'{3}\' was expected.').format(lineNumber, actual['numP']+1, p[1]['tipo'], listaTipos[actual['numP']][0])
				exit()
			# Checar que el parametro recibido y el esperado coincidan en dimension
			elif (p[1].has_key('dim') and len(listaTipos[actual['numP']]) == 2):
				print('Semantic error at line {0}, expected array reference but got {1}.').format(lineNumber, listaTipos[actual['numP']][0])
				exit()
			# Checar que el parametro recibido y el esperado coincidan en dimension
			elif (not p[1].has_key('dim') and len(listaTipos[actual['numP']]) > 2):
				print('Semantic error at line {0}, expected {1} but got array reference.').format(lineNumber, p[1]['tipo'])
				exit()
			# Parametro recibido y el esperado no son dimensionados
			elif (not p[1].has_key('dim') and len(listaTipos[actual['numP']]) == 2):
				tipo = devuelveParametros(actual['invocadorTipo'], actual['id'])[actual['numP']][0]
				nombreVar = devuelveParametros(actual['invocadorTipo'], actual['id'])[actual['numP']][1]
				Cuad.append(['PARAM', p[1]['id'], '-', devuelveVars(actual['invocadorTipo'], actual['id'])[tipo][nombreVar]])
				Line = Line + 1
			# Checar que el parametro recibido y el esperado sean dimensionados y tengan igual tamanio
			elif ( p[1]['dim'] != listaTipos[actual['numP']][2] ):
				print('Semantic error at line {0}, array received as parameter differs in length from formal argument.').format(lineNumber)
				exit()
			# Parametro recibido y el esperado son dimensionados
			else:
				tipo = devuelveParametros(actual['invocadorTipo'], actual['id'])[actual['numP']][0]
				nombreVar = devuelveParametros(actual['invocadorTipo'], actual['id'])[actual['numP']][1]
				base = devuelveVars(actual['invocadorTipo'], actual['id'])[tipo][nombreVar]
				for x in range(0, p[1]['dim']):	
					Cuad.append(['PARAM', p[1]['id'] + x, '-', base + x])
					Line = Line + 1
	else:
		# Se verifica que el numero de parametros leidos no sea mayor al numero de parametros esperados
		if(actual['numP'] >= len( devuelveParametros(ClaseActual, actual['id']) )):
			print('Semantic error at line {0}, more parameters given than the {1} specified for function {2} of Class {3}.').format(lineNumber, len(devuelveParametros(ClaseActual, actual['id'])), actual['id'], ClaseActual)
			exit()
		else:
			# Obtener la lista de tipos de los parametros de la funcion
			listaTipos = copy.deepcopy(devuelveParametros(ClaseActual, actual['id']))
			# Checar que los tipos coincidan (se permite el casteo de numeral a real)
			if(p[1]['tipo'] != listaTipos[actual['numP']][0] and not (p[1]['tipo'] == 'numeral' and listaTipos[actual['numP']][0] == 'real') ):
				print('Semantic error at line {0}, parameter #{1} of type \'{2}\' given when type \'{3}\' was expected.').format(lineNumber, actual['numP']+1, p[1]['tipo'], listaTipos[actual['numP']][0])
				exit()
			# Checar que el parametro recibido y el esperado coincidan en dimension
			elif (p[1].has_key('dim') and len(listaTipos[actual['numP']]) == 2):
				print('Semantic error at line {0}, expected array reference but got {1}.').format(lineNumber, listaTipos[actual['numP']][0])
				exit()
			# Checar que el parametro recibido y el esperado coincidan en dimension
			elif (not p[1].has_key('dim') and len(listaTipos[actual['numP']]) > 2):
				print('Semantic error at line {0}, expected {1} but got array reference.').format(lineNumber, p[1]['tipo'])
				exit()
			# Parametro recibido y el esperado no son dimensionados
			elif (not p[1].has_key('dim') and len(listaTipos[actual['numP']]) == 2):
				tipo = devuelveParametros(ClaseActual, actual['id'])[actual['numP']][0]
				nombreVar = devuelveParametros(ClaseActual, actual['id'])[actual['numP']][1]
				Cuad.append(['PARAM', p[1]['id'], '-', devuelveVars(ClaseActual, actual['id'])[tipo][nombreVar]])
				Line = Line + 1
			# Checar que el parametro recibido y el esperado sean dimensionados y tengan igual tamanio
			elif ( p[1]['dim'] != listaTipos[actual['numP']][2] ):
				print('Semantic error at line {0}, array received as parameter differs in length from formal argument.').format(lineNumber)
				exit()
			# Parametro recibido y el esperado son dimensionados
			else:
				tipo = devuelveParametros(ClaseActual, actual['id'])[actual['numP']][0]
				nombreVar = devuelveParametros(ClaseActual, actual['id'])[actual['numP']][1]
				base = devuelveVars(ClaseActual, actual['id'])[tipo][nombreVar]
				for x in range(0, p[1]['dim']):	
					Cuad.append(['PARAM', p[1]['id'] + x, '-', base + x])
					Line = Line + 1
	actual['numP'] = actual['numP'] + 1
	PilaLlamadas.pop()
	PilaLlamadas.push(actual)
	print('exp_ciclo')

# Produccion de expresiones en parametros de llamada a funcion
def p_exp_ciclo_2(p):
	'''exp_ciclo 	: exp_ciclo COMA exp'''
	lineNumber = scanner.lexer.lineno
	global PilaLlamadas
	global Line
	actual = PilaLlamadas.top()

	# Si la llamada a funcion es invocada desde un objeto
	if(actual.has_key('invocadorTipo')):
		# Se verifica que el numero de parametros leidos no sea mayor al numero de parametros esperados
		if(actual['numP'] >= len(devuelveParametros(actual['invocadorTipo'], actual['id']))):
			print('Semantic error at line {0}, more parameters given than the {1} specified for function {2} of Class {3}.').format(lineNumber, len(devuelveParametros(actual['invocadorTipo'], actual['id'])), actual['id'], actual['invocadorTipo'])
			exit()
		else:
			# Obtener la lista de tipos de los parametros de la funcion
			listaTipos = copy.deepcopy(devuelveParametros(actual['invocadorTipo'], actual['id']))
			# Checar que los tipos coincidan (se permite el casteo de numeral a real)
			if(p[3]['tipo'] != listaTipos[actual['numP']][0] and not (p[3]['tipo'] == 'numeral' and listaTipos[actual['numP']][0] == 'real') ):
				print('Semantic error at line {0}, parameter #{1} of type \'{2}\' given when type \'{3}\' was expected.').format(lineNumber, actual['numP']+1, p[1]['tipo'], listaTipos[actual['numP']][0])
				exit()
			# Checar que el parametro recibido y el esperado coincidan en dimension
			elif (p[3].has_key('dim') and len(listaTipos[actual['numP']]) == 2):
				print('Semantic error at line {0}, expected array reference but got {1}.').format(lineNumber, listaTipos[actual['numP']][0])
				exit()
			# Checar que el parametro recibido y el esperado coincidan en dimension
			elif (not p[3].has_key('dim') and len(listaTipos[actual['numP']]) > 2):
				print('Semantic error at line {0}, expected {1} but got array reference.').format(lineNumber, p[3]['tipo'])
				exit()
			# Parametro recibido y el esperado no son dimensionados
			elif (not p[3].has_key('dim') and len(listaTipos[actual['numP']]) == 2):
				tipo = devuelveParametros(actual['invocadorTipo'], actual['id'])[actual['numP']][0]
				nombreVar = devuelveParametros(actual['invocadorTipo'], actual['id'])[actual['numP']][1]
				Cuad.append(['PARAM', p[3]['id'], '-', devuelveVars(actual['invocadorTipo'], actual['id'])[tipo][nombreVar]])
				Line = Line + 1
			# Checar que el parametro recibido y el esperado sean dimensionados y tengan igual tamanio
			elif ( p[3]['dim'] != listaTipos[actual['numP']][2] ):
				print('Semantic error at line {0}, array received as parameter differs in length from formal argument.').format(lineNumber)
				exit()
			# Parametro recibido y el esperado son dimensionados
			else:
				tipo = devuelveParametros(actual['invocadorTipo'], actual['id'])[actual['numP']][0]
				nombreVar = devuelveParametros(actual['invocadorTipo'], actual['id'])[actual['numP']][1]
				base = devuelveVars(actual['invocadorTipo'], actual['id'])[tipo][nombreVar]
				for x in range(0, p[3]['dim']):	
					Cuad.append(['PARAM', p[3]['id'] + x, '-', base + x])
					Line = Line + 1
	else:
		# Se verifica que el numero de parametros leidos no sea mayor al numero de parametros esperados
		if(actual['numP'] >= len(devuelveParametros(ClaseActual, actual['id']))):
			print('Semantic error at line {0}, more parameters given than the {1} specified for function {2} of Class {3}.').format(lineNumber, len(devuelveParametros(ClaseActual, actual['id'])), actual['id'], ClaseActual)
			exit()
		else:
			# Obtener la lista de tipos de los parametros de la funcion
			listaTipos = copy.deepcopy(devuelveParametros(ClaseActual, actual['id']))
			# Checar que los tipos coincidan (se permite el casteo de numeral a real)
			if(p[3]['tipo'] != listaTipos[actual['numP']][0] and not (p[3]['tipo'] == 'numeral' and listaTipos[actual['numP']][0] == 'real') ):
				print('Semantic error at line {0}, parameter #{1} of type \'{2}\' given when type \'{3}\' was expected.').format(lineNumber, actual['numP']+1, p[1]['tipo'], listaTipos[actual['numP']][0])
				exit()
			# Checar que el parametro recibido y el esperado coincidan en dimension
			elif (p[3].has_key('dim') and len(listaTipos[actual['numP']]) == 2):
				print('Semantic error at line {0}, expected array reference but got {1}.').format(lineNumber, listaTipos[actual['numP']][0])
				exit()
			# Checar que el parametro recibido y el esperado coincidan en dimension
			elif (not p[3].has_key('dim') and len(listaTipos[actual['numP']]) > 2):
				print('Semantic error at line {0}, expected {1} but got array reference.').format(lineNumber, p[3]['tipo'])
				exit()
			# Parametro recibido y el esperado no son dimensionados
			elif (not p[3].has_key('dim') and len(listaTipos[actual['numP']]) == 2):
				tipo = devuelveParametros(ClaseActual, actual['id'])[actual['numP']][0]
				nombreVar = devuelveParametros(ClaseActual, actual['id'])[actual['numP']][1]
				Cuad.append(['PARAM', p[3]['id'], '-', devuelveVars(ClaseActual, actual['id'])[tipo][nombreVar]])
				Line = Line + 1
			# Checar que el parametro recibido y el esperado sean dimensionados y tengan igual tamanio
			elif ( p[3]['dim'] != listaTipos[actual['numP']][2] ):
				print('Semantic error at line {0}, array received as parameter differs in length from formal argument.').format(lineNumber)
				exit()
			# Parametro recibido y el esperado son dimensionados
			else:
				tipo = devuelveParametros(ClaseActual, actual['id'])[actual['numP']][0]
				nombreVar = devuelveParametros(ClaseActual, actual['id'])[actual['numP']][1]
				base = devuelveVars(ClaseActual, actual['id'])[tipo][nombreVar]
				for x in range(0, p[3]['dim']):	
					Cuad.append(['PARAM', p[3]['id'] + x, '-', base + x])
					Line = Line + 1
	actual['numP'] = actual['numP'] + 1
	PilaLlamadas.pop()
	PilaLlamadas.push(actual)
	print('exp_ciclo')

# Producciones de expresiones binarias
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
	global Line
	global DirsMetodoTemp
	lineNumber = scanner.lexer.lineno

	# Verificar que las expresiones no hagan referencia a arreglos
	if ( p[1].has_key('dim') or p[3].has_key('dim') ):
		print('Semantic error at line {0}, can\'t perform operations over array references').format(lineNumber)
		exit()

	# Generacion de suma
	if (p[2] == '+'):
		# Verificar compatibilidad de tipos
		if (CuboSemantico[ p[1]['tipo'] ].has_key('+') and CuboSemantico[ p[1]['tipo'] ]['+'].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['+'][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['+'][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['+'][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['+'][ p[3]['tipo'] ]] + 1
			Cuad.append(['MAS', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'+\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
	# Generacion de resta
	elif (p[2] == '-'):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('-') and CuboSemantico[ p[1]['tipo'] ]['-'].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['-'][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['-'][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['-'][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['-'][ p[3]['tipo'] ]] + 1
			Cuad.append(['MENOS', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'-\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
	# Generacion de multiplicacion
	elif (p[2] == '*'):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('*') and CuboSemantico[ p[1]['tipo'] ]['*'].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['*'][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['*'][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['*'][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['*'][ p[3]['tipo'] ]] + 1
			Cuad.append(['POR', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'*\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
	# Generacion de division
	elif (p[2] == '/'):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('/') and CuboSemantico[ p[1]['tipo'] ]['/'].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['/'][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['/'][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['/'][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['/'][ p[3]['tipo'] ]] + 1
			Cuad.append(['ENTRE', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'/\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
	# Generacion de modulo
	elif (p[2] == '%'):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('%') and CuboSemantico[ p[1]['tipo'] ]['%'].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['%'][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['%'][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['%'][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['%'][ p[3]['tipo'] ]] + 1
			Cuad.append(['MOD', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'%\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
	# Generacion de comparacion de igualdad
	elif (p[2] == '=='):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('==') and CuboSemantico[ p[1]['tipo'] ]['=='].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['=='][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['=='][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['=='][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['=='][ p[3]['tipo'] ]] + 1
			Cuad.append(['IGUALC', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'==\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
	# Generacion de comparacion de diferencia
	elif (p[2] == '!='):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('!=') and CuboSemantico[ p[1]['tipo'] ]['!='].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['!='][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['!='][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['!='][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['!='][ p[3]['tipo'] ]] + 1
			Cuad.append(['NOTIGUAL', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'!=\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
	# Generacion de mayor que
	elif (p[2] == '>'):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('>') and CuboSemantico[ p[1]['tipo'] ]['>'].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['>'][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['>'][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['>'][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['>'][ p[3]['tipo'] ]] + 1
			Cuad.append(['MAYOR', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'>\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
	# Generacion de mayor o igual que
	elif (p[2] == '>='):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('>=') and CuboSemantico[ p[1]['tipo'] ]['>='].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['>='][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['>='][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['>='][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['>='][ p[3]['tipo'] ]] + 1
			Cuad.append(['MAYORIGUAL', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'>=\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
	# Generacion de menor que
	elif (p[2] == '<'):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('<') and CuboSemantico[ p[1]['tipo'] ]['<'].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['<'][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['<'][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['<'][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['<'][ p[3]['tipo'] ]] + 1
			Cuad.append(['MENOR', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'<\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
	# Generacion de menor o igual que
	elif (p[2] == '<='):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('<=') and CuboSemantico[ p[1]['tipo'] ]['<='].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['<='][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['<='][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['<='][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['<='][ p[3]['tipo'] ]] + 1
			Cuad.append(['MENORIGUAL', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'<=\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
	# Generacion de OR
	elif (p[2] == '||'):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('||') and CuboSemantico[ p[1]['tipo'] ]['||'].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['||'][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['||'][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['||'][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['||'][ p[3]['tipo'] ]] + 1
			Cuad.append(['OR', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'||\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
	# Generacion de AND
	elif (p[2] == '&&'):
		if (CuboSemantico[ p[1]['tipo'] ].has_key('&&') and CuboSemantico[ p[1]['tipo'] ]['&&'].has_key( p[3]['tipo'] )):
			p[0] = {'tipo': CuboSemantico[ p[1]['tipo'] ]['&&'][ p[3]['tipo'] ], 'id': DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['&&'][ p[3]['tipo'] ]] }
			DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['&&'][ p[3]['tipo'] ]] = DirsMetodoTemp[CuboSemantico[ p[1]['tipo'] ]['&&'][ p[3]['tipo'] ]] + 1
			Cuad.append(['AND', (p[1]['invocador']+'.'+p[1]['id'] if p[1].has_key('invocador') else p[1]['id']), (p[3]['invocador']+'.'+p[3]['id'] if p[3].has_key('invocador') else p[3]['id']), p[0]['id']])
			Line = Line + 1;
		else:
			print('Semantic error at line {0}, incompatible types {1} and {2} with operator \'&&\'.').format(lineNumber, p[1]['tipo'], p[3]['tipo'])
			exit()
	# Se salva el valor de la expresion generada para, posiblemente, ser usada en validacion de parametros de llamada a funcion
	ResExp = p[0]
	print('exp_binaria')

# Producciones de expresiones unarias
def p_exp_unaria(p):	
	'''exp 	: NOT exp
			| MENOS exp %prec UMINUS
			| PIZQ exp PDER'''
	global ResExp
	global Line
	lineNumber = scanner.lexer.lineno

	# Verificar que la expresion de entrada no haga referencia a un arreeglo
	if ( p[2].has_key('dim') ):
		print('Semantic error at line {0}, can\'t perform operations over array references').format(lineNumber)
		exit()

	# Genercion de NOT
	if (p[1] == '!'):
		# Validar compatibilidad de tipos
		if (CuboSemantico[ p[2]['tipo'] ].has_key('!')):
			p[0] = {'tipo': CuboSemantico[ p[2]['tipo'] ]['!'], 'id': DirsMetodoTemp[CuboSemantico[ p[2]['tipo'] ]['!']] }
			DirsMetodoTemp[CuboSemantico[ p[2]['tipo'] ]['!']] = DirsMetodoTemp[CuboSemantico[ p[2]['tipo'] ]['!']] + 1
			Cuad.append(['NOT', (p[2]['invocador']+'.'+p[2]['id'] if p[2].has_key('invocador') else p[2]['id']), '-', p[0]['id']])
			Line = Line + 1;
		else:
			print('Semantic error at line {0}, incompatible type {1} with preceding operator \'!\'.').format(lineNumber, p[2]['tipo'])
			exit()
	# Genercion de negacion aritmetica
	elif (p[1] == '-'):
		if (CuboSemantico[ p[2]['tipo'] ].has_key('-') and CuboSemantico[ p[2]['tipo'] ]['-'].has_key('-')):
			p[0] = {'tipo': CuboSemantico[ p[2]['tipo'] ]['-']['-'], 'id': DirsMetodoTemp[CuboSemantico[ p[2]['tipo'] ]['-']['-']] }
			DirsMetodoTemp[CuboSemantico[ p[2]['tipo'] ]['-']['-']] = DirsMetodoTemp[CuboSemantico[ p[2]['tipo'] ]['-']['-']] + 1
			Cuad.append(['UMENOS', (p[2]['invocador']+'.'+p[2]['id'] if p[2].has_key('invocador') else p[2]['id']), '-', p[0]['id']])
			Line = Line + 1;
		else:
			print('Semantic error at line {0}, incompatible type {1} with preceding operator \'-\'.').format(lineNumber, p[2]['tipo'])
			exit()
	# Genercion de parentesis alrededor de expresion
	elif (p[1] == '('):
		p[0] = p[2]
		
	# Se salva el valor de la expresion generada para, posiblemente, ser usada en validacion de parametros de llamada a funcion
	ResExp = p[0]
	print('exp_unaria')

# Produccion de expresion a partir de valores dados
def p_opciones(p):
	'''exp 	: cte_str
			| cte_char
			| cte_numeral
			| cte_real
			| cte_bool
			| atom limpiarInvocador
			| llamada_func limpiarInvocador'''
	global ResExp
	p[0] = p[1]
	# Se salva el valor de la expresion generada para, posiblemente, ser usada en validacion de parametros de llamada a funcion
	ResExp = p[0]
	print('opciones')

# Produccion de constante string
def p_cte_str(p):
	'''cte_str : CTE_STR'''
	print('cte_str')
	global DirsConst
	global DirsConstMap
	# Verificar si la constante ya se ha leido
	if p[1] in DirsConstMap['string']:
		p[0] = { 'tipo': 'string', 'id': DirsConstMap['string'][ p[1] ] }
	else:
		# Dar de alta la constante
		p[0] = { 'tipo': 'string', 'id': DirsConst['string'] }
		DirsConstMap['string'][p[1]] = DirsConst['string']
		DirsConst['string'] = DirsConst['string'] + 1 

# Produccion de constante char
def p_cte_char(p):
	'''cte_char : CTE_CHAR'''
	print('cte_char')
	global DirsConst
	global DirsConstMap
	# Verificar si la constante ya se ha leido
	if p[1] in DirsConstMap['char']:
		p[0] = { 'tipo': 'char', 'id': DirsConstMap['char'][ p[1] ] }
	else:
		# Dar de alta la constante
		p[0] = { 'tipo': 'char', 'id': DirsConst['char'] }
		DirsConstMap['char'][p[1]] = DirsConst['char']
		DirsConst['char'] = DirsConst['char'] + 1

# Produccion de constante numeral
def p_cte_numeral(p):
	'''cte_numeral : CTE_NUMERAL'''
	print('cte_numeral')
	global DirsConst
	global DirsConstMap
	# Verificar si la constante ya se ha leido
	if p[1] in DirsConstMap['numeral']:
		p[0] = { 'tipo': 'numeral', 'id': DirsConstMap['numeral'][ p[1] ] }
	else:
		# Dar de alta la constante
		p[0] = { 'tipo': 'numeral', 'id': DirsConst['numeral'] }
		DirsConstMap['numeral'][p[1]] = DirsConst['numeral']
		DirsConst['numeral'] = DirsConst['numeral'] + 1

# Produccion de constante real
def p_cte_real(p):
	'''cte_real : CTE_REAL'''
	print('cte_real')
	global DirsConst
	global DirsConstMap
	# Verificar si la constante ya se ha leido
	if p[1] in DirsConstMap['real']:
		p[0] = { 'tipo': 'real', 'id': DirsConstMap['real'][ p[1] ] }
	else:
		# Dar de alta la constante
		p[0] = { 'tipo': 'real', 'id': DirsConst['real'] }
		DirsConstMap['real'][p[1]] = DirsConst['real']
		DirsConst['real'] = DirsConst['real'] + 1

# Produccion de constante bool
def p_cte_bool(p):
	'''cte_bool 	: TRUE
					| FALSE'''
	print('cte_bool')
	global DirsConst
	global DirsConstMap
	# Verificar si la constante ya se ha leido
	if p[1] in DirsConstMap['bool']:
		p[0] = { 'tipo': 'bool', 'id': DirsConstMap['bool'][ p[1] ] }
	else:
		# Dar de alta la constante
		p[0] = { 'tipo': 'bool', 'id': DirsConst['bool'] }
		DirsConstMap['bool'][p[1]] = DirsConst['bool']
		DirsConst['bool'] = DirsConst['bool'] + 1

# Produccion de return con valor de retorno
def p_return_exp(p):
	'''return 	: RETURN exp PYC'''
	global ClaseActual
	global MetodoActual
	global Line
	lineNumber = scanner.lexer.lineno

	# Verificar que no se intente regresar una referencia a arreglo
	if ( p[2].has_key('dim') ):
		print('Semantic error at line {0}, can\'t return array reference').format(lineNumber)
		exit()

	# Verificar que el tipo de la expresion coincida con el tipo de retorno del metodo
	if (p[2]['tipo'] != DirClases[ClaseActual]['metodos'][MetodoActual]['retorno'] ):
		print('Semantic error at line {0}, expected "{1}" return, but got "{2}" expression.').format(lineNumber - 1, DirClases[ClaseActual]['metodos'][MetodoActual]['retorno'], p[2]['tipo'])
		exit()
	Cuad.append(['RETURN', p[2]['id'],  '-', '-'])
	Line = Line + 1
	print('return')

# Produccion de return con valor de retorno
def p_return_null(p):
	'''return 	: RETURN PYC'''
	global ClaseActual
	global MetodoActual
	global Line
	lineNumber = scanner.lexer.lineno

	# Verificar que el metodo sea de tipo void/without
	if (not DirClases[ClaseActual]['metodos'][MetodoActual]['retorno'] == 'without'):
		print('Semantic error at line {0}, expected "{1}" return expression, but got "without" return.').format(lineNumber - 1, DirClases[ClaseActual]['metodos'][MetodoActual]['retorno'])
		exit()
	Cuad.append(['RETURN', '-',  '-', '-'])
	Line = Line + 1
	print('return')

# Produccion de ciclo while
def p_while(p):
	'''while 	: WHILE while_1 PIZQ exp PDER while_2 LLIZQ ciclo_estatuto while_3 LLDER
				| WHILE while_1 PIZQ exp PDER while_2 LLIZQ while_3 LLDER'''
	print('while')

# Accion semantica de while
def p_while_1(p):
	'''while_1 : '''
	global PSaltos
	global Line
	# Se mete a la pila de saltos la posicion de inicio de la expresion de condicion del while
	PSaltos.push(Line)

# Accion semantica de while
def p_while_2(p):
	'''while_2 : '''
	global PSaltos
	global Line
	global ResExp
	lineNumber = scanner.lexer.lineno
	# Checar que la expresion devuelta no sea una referencia a arreglo
	if (ResExp.has_key('dim')):
		print('Semantic error at line {0}, expected "bool" expression, but got array reference.').format(lineNumber - 1)
		exit()
	# Checar que la expresion devuelta sea de tipo bool
	if (ResExp['tipo'] != 'bool'):
		print('Semantic error at line {0}, expected "bool" expression, but "{1}" expression given in while loop condition.').format(lineNumber - 1, ResExp['tipo'])
		exit()
	Cuad.append(['GOTOF', ResExp['id'],  'missing', '-'])
	Line = Line + 1;
	# Meter a la pila de saltos la posicion pendiente del goto en falso
	PSaltos.push(Line - 1)

# Accion semantica de while
def p_while_3(p):
	'''while_3 : '''
	global PSaltos
	global Line
	falso = PSaltos.pop()
	retorno = PSaltos.pop()
	# Se genera salto hacia el inicio del while
	Cuad.append(['GOTO', '-', retorno, '-'])
	Line = Line + 1;
	# Se rellena el cuadruplo pendiente del goto en falso
	Cuad[falso][2] = Line

# Produccion de asignacion
def p_asignacion(p):
	'''asignacion 	: atom limpiarInvocador IGUAL exp PYC'''
	global Line
	lineNumber = scanner.lexer.lineno
	
	# Verificar que no se intente hacer una asignacion que involucre referencias a arreglo
	if ( p[1].has_key('dim') or p[4].has_key('dim') ):
		print('Semantic error at line {0}, can\'t perform assignments over array references').format(lineNumber)
		exit()

	# Verificar compatibilidad de tipos en la asignacion
	if (CuboSemantico[ p[1]['tipo'] ].has_key('=') and CuboSemantico[ p[1]['tipo'] ]['='].has_key( p[4]['tipo'] )):
		# Asignacion de tipos primitivos
		if (p[1]['tipo'] in TiposVar): 
			Cuad.append(['IGUAL', p[4]['id'], '-', p[1]['id']])
		# Asignacion de tipos primitivos
		#else:

		Line = Line + 1;
	else:
		print('Semantic error at line {0}, incompatible type assignation of type {1} into type {2}.').format(lineNumber - 1, p[4]['tipo'], p[1]['tipo'])
		exit()
	print('asignacion')

def p_atom_dim(p):
	'''atom : ID PUNTO definirInvocador ID checarAtributoDim COIZQ exp CODER
			| ID checarAtributoDim COIZQ exp CODER
			| THIS PUNTO definirInvocador ID checarAtributoDim COIZQ exp CODER'''
	global ClaseActual
	global MetodoActual
	global Line
	dirBase = -1
	offset = -1

	# Arreglo de THIS 
	if (p[1] == 'this'):

		if ( p[7].has_key('dim') or p[7]['tipo'] != 'numeral' ):
			print('Semantic error at line {0}, array index must be a numeral expression').format(lineNumber)
			exit()

		for tipo in TiposVar:
			if ( DirClases[ClaseActual]['vars'][tipo].has_key( p[4] ) ):
				dirBase = DirClases[ClaseActual]['vars'][tipo][ p[4] ]
		offset = p[7]['id']
	# Arreglo de instancia
	elif (p[2] == '.'):

		if ( p[7].has_key('dim') or p[7]['tipo'] != 'numeral' ):
			print('Semantic error at line {0}, array index must be a numeral expression').format(lineNumber)
			exit()

		# Checar en metodo
		if ( DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key( p[1] ) ):
			for tipo in TiposVar:
				if ( DirClases[ClaseActual]['metodos'][MetodoActual]['vars'][tipo].has_key( p[1] + '.' + p[4] ) ):
					dirBase = DirClases[ClaseActual]['metodos'][MetodoActual]['vars'][tipo][ p[1] + '.' + p[4] ]
		# Checar en clase
		else:
			for tipo in TiposVar:
				if ( DirClases[ClaseActual]['vars'][tipo].has_key( p[1] + '.' + p[4] ) ):
					dirBase = DirClases[ClaseActual]['vars'][tipo][ p[1] + '.' + p[4] ]


		offset = p[7]['id']
	# Arreglo de contexto
	else:

		if ( p[4].has_key('dim') or p[4]['tipo'] != 'numeral' ):
			print('Semantic error at line {0}, array index must be a numeral expression').format(lineNumber)
			exit()

		# Checar en metodo
		if ( DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key( p[1] ) ):
			for tipo in TiposVar:
				if ( DirClases[ClaseActual]['metodos'][MetodoActual]['vars'][tipo].has_key( p[1] ) ):
					dirBase = DirClases[ClaseActual]['metodos'][MetodoActual]['vars'][tipo][ p[1] ]
		# Checar en clase
		else:
			for tipo in TiposVar:
				if ( DirClases[ClaseActual]['vars'][tipo].has_key( p[1] ) ):
					dirBase = DirClases[ClaseActual]['vars'][tipo][ p[1] ]
		offset = p[4]['id']

	Cuad.append(['MAS', ( '|' + str(dirBase) + '|' ), offset, DirsMetodoTemp['numeral'] ])
	p[0] = {'tipo': 'numeral', 'id': ( '(' + str(DirsMetodoTemp['numeral']) + ')' ) }
	DirsMetodoTemp['numeral'] = DirsMetodoTemp['numeral'] + 1
	Line = Line + 1

def p_atom(p):
	'''atom : ID PUNTO definirInvocador ID checarAtributo
			| ID checarAtributo
			| THIS PUNTO definirInvocador ID checarAtributo'''
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
				# Checar si es dimensionada
				if (DirClases[ClaseActual]['varsTam'][AtributoTipo].has_key(AtributoAtom)):
					p[0]['dim'] = DirClases[ClaseActual]['varsTam'][AtributoTipo][AtributoAtom]
			else:
				print("Semantic error at line {0}, THIS -> X can't refer to instances of Class {1}").format(lineNumber, AtributoTipo)
				exit()
		# Buscar en instancia : metodo
		elif (DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(Invocador)):
			p[0] = { 'tipo': AtributoTipo, 'id': DirClases[ClaseActual]['metodos'][MetodoActual]['vars'][AtributoTipo][Invocador + '.' + AtributoAtom] }
			# Checar si es dimensionada
			if (DirClases[ DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][Invocador]['tipo'] ]['variables'][AtributoAtom].has_key('dim')):
				p[0]['dim'] = DirClases[ DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][Invocador]['tipo'] ]['variables'][AtributoAtom]['dim']
		# Buscar en instancia : clase
		else:
			p[0] = { 'tipo': AtributoTipo, 'id': DirClases[ClaseActual]['vars'][AtributoTipo][Invocador + '.' + AtributoAtom] }
			# Checar si es dimensionada
			if (DirClases[ClaseActual]['varsTam'][AtributoTipo].has_key(Invocador + '.' + AtributoAtom)):
				p[0]['dim'] = DirClases[ClaseActual]['varsTam'][AtributoTipo][Invocador + '.' + AtributoAtom]
	else:
		# Buscar en metodo actual
		
		if (DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(AtributoAtom)):
			p[0] = { 'tipo': AtributoTipo, 'id': DirClases[ClaseActual]['metodos'][MetodoActual]['vars'][AtributoTipo][AtributoAtom] }
			# Checar si es dimensionada
			if (DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][AtributoAtom].has_key('dim')):
				p[0]['dim'] = DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][AtributoAtom]['dim']
		# Buscar en clase actual
		else:
			p[0] = { 'tipo': AtributoTipo, 'id': DirClases[ClaseActual]['vars'][AtributoTipo][AtributoAtom] }
			# Checar si es dimensionada
			if (DirClases[ClaseActual]['varsTam'][AtributoTipo].has_key(AtributoAtom)):
				p[0]['dim'] = DirClases[ClaseActual]['varsTam'][AtributoTipo][AtributoAtom]
	print('atom')

def p_checarAtributoDim(p):
	'''checarAtributoDim : '''
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
				if ( DirClases[ClaseActual]['variables'][atributo].has_key('dim') ):
					AtributoTipo = DirClases[ClaseActual]['variables'][atributo]['tipo']
				else:
					print('Semantic error at line {0}, variable {1} is not an array').format(lineNumber, atributo)
					exit()
			elif ( checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber) ):
				if ( checarAtributoAncestrosDim(DirClases[ClaseActual]['ancestros'], atributo, lineNumber) ):
					AtributoTipo = valorAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber)
				else:
					print('Semantic error at line {0}, variable {1} is not an array').format(lineNumber, atributo)
					exit()
			else:
				print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 111').format(lineNumber, atributo)
				exit()
		else:
			if ( DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(atributo) ):
				if ( DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][atributo].has_key('dim') ):
					AtributoTipo = DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][atributo]['tipo']
				else:
					print('Semantic error at line {0}, variable {1} is not an array').format(lineNumber, atributo)
					exit()
			elif ( DirClases[ClaseActual]['variables'].has_key(atributo) ):
				if ( DirClases[ClaseActual]['variables'][atributo].has_key('dim') ):
					AtributoTipo = DirClases[ClaseActual]['variables'][atributo]['tipo']
				else:
					print('Semantic error at line {0}, variable {1} is not an array').format(lineNumber, atributo)
					exit()
			elif ( checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber)):
				if ( checarAtributoAncestrosDim(DirClases[ClaseActual]['ancestros'], atributo, lineNumber) ):
					AtributoTipo = valorAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber)
				else:
					print('Semantic error at line {0}, variable {1} is not an array').format(lineNumber, atributo)
					exit()
			else:
				print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 222').format(lineNumber, atributo)
				exit()
	elif (Invocador == 'this'):
		if ( DirClases[ClaseActual]['variables'].has_key(atributo) ):
			if ( DirClases[ClaseActual]['variables'][atributo].has_key('dim') ):
				AtributoTipo = DirClases[ClaseActual]['variables'][atributo]['tipo']
			else:
				print('Semantic error at line {0}, variable {1} is not an array').format(lineNumber, atributo)
				exit()
		elif( checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber) ):
			if ( checarAtributoAncestrosDim(DirClases[ClaseActual]['ancestros'], atributo, lineNumber) ):
				AtributoTipo = valorAtributoAncestros(DirClases[ClaseActual]['ancestros'], atributo, lineNumber)
			else:
				print('Semantic error at line {0}, variable {1} is not an array').format(lineNumber, atributo)
				exit()
		else:
			print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 333').format(lineNumber, atributo)
			exit()
	else:

		claseAux = ''

		if (MetodoActual != ''):
			if ( DirClases[ClaseActual]['metodos'][MetodoActual]['variables'].has_key(Invocador) ):
				claseAux = DirClases[ClaseActual]['metodos'][MetodoActual]['variables'][Invocador]['tipo']
			elif ( DirClases[ClaseActual]['variables'].has_key(Invocador) ):
				claseAux = DirClases[ClaseActual]['variables'][Invocador]['tipo']
			elif ( checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], Invocador, lineNumber)):
				claseAux = valorAtributoAncestros(DirClases[ClaseActual]['ancestros'], Invocador, lineNumber)
		else:
			if ( DirClases[ClaseActual]['variables'].has_key(Invocador) ):
				claseAux = DirClases[ClaseActual]['variables'][Invocador]['tipo']
			elif ( checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], Invocador, lineNumber)):
				claseAux = valorAtributoAncestros(DirClases[ClaseActual]['ancestros'], Invocador, lineNumber)


		if ( DirClases[claseAux]['variables'].has_key(atributo) ):
			if ( not (DirClases[claseAux]['variables'][atributo]['acceso'] == 'visible') ):
				print('Semantic error at line {0}, variable {1} is hidden').format(lineNumber, atributo)
				exit()
			if ( DirClases[claseAux]['variables'][atributo].has_key('dim') ):
				AtributoTipo = DirClases[claseAux]['variables'][atributo]['tipo']
			else:
				print('Semantic error at line {0}, variable {1} is not an array').format(lineNumber, atributo)
				exit()
		elif ( checarAtributoAncestros(DirClases[claseAux]['ancestros'], atributo, lineNumber) ):
			if ( not esVisibleAtributoAncestros(DirClases[claseAux]['ancestros'], atributo, lineNumber) ):
				print('Semantic error at line {0}, variable {1} is hidden').format(lineNumber, atributo)
				exit()
			if ( checarAtributoAncestrosDim(DirClases[claseAux]['ancestros'], atributo, lineNumber) ):
				AtributoTipo = valorAtributoAncestros(DirClases[claseAux]['ancestros'], atributo, lineNumber)
			else:
				print('Semantic error at line {0}, variable {1} is not an array').format(lineNumber, atributo)
				exit()
		else:
			print('Semantic error at line {0}, variable {1} not found in Class Hierarchy. 444').format(lineNumber, atributo)
			exit()
		InvocadorTipo = claseAux
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

	print('----')
	print(Invocador)
	print(ClaseActual)
	print(atributo)
	
	if (Invocador == ''):
		print( DirClases[ClaseActual]['variables'] )
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
			elif ( DirClases[ClaseActual]['variables'].has_key(Invocador) ):
				claseAux = DirClases[ClaseActual]['variables'][Invocador]['tipo']
			elif ( checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], Invocador, lineNumber)):
				claseAux = valorAtributoAncestros(DirClases[ClaseActual]['ancestros'], Invocador, lineNumber)
		else:
			if ( DirClases[ClaseActual]['variables'].has_key(Invocador) ):
				claseAux = DirClases[ClaseActual]['variables'][Invocador]['tipo']
			elif ( checarAtributoAncestros(DirClases[ClaseActual]['ancestros'], Invocador, lineNumber)):
				claseAux = valorAtributoAncestros(DirClases[ClaseActual]['ancestros'], Invocador, lineNumber)


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
	if (ResExp.has_key('dim')):
		print('Semantic error at line {0}, expected "bool" expression, but got array reference.').format(lineNumber - 1)
		exit()
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
	lineNumber = scanner.lexer.lineno
	if ( p[3].has_key('dim') ):
		print('Semantic error at line {0}, can\'t print array references.').format(lineNumber)
		exit()
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

for i in range(0, len(Cuad)):
	arch2.write(str(i) + '\t' + str(Cuad[i][0]) + '\t' + '\t' + str(Cuad[i][1]) + '\t' + '\t' + str(Cuad[i][2]) + '\t' + str(Cuad[i][3]) + '\n')