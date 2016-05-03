from __future__ import print_function
import os.path

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

     def at(self, index):
     	 return self.items[index] 

# Directorios qu indican el rango de direcciones
DirBaseClase = {}
DirBaseMetodo = {}
DirBaseMetodoTemp = {}

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

# Diccionario que representa el mapa de memoria de la maquina virtual
MapaMemoria = { 'main': {} }

# Directorio de constantes que almacenan las constantes que son utilizadas
# durante la ejecucion de la maquina virtual
DirConstantes = {}

# Lista que almacena los cuadruplos del programa compilado
Cuadruplos = []

# Pilas de contexto actual y de memorias instanciadas
PContexto = stack()
PMemoria = stack()

# Pila de direcciones y valores a donde se regresara despues de llamar a
# una funcion
PRetornos = stack()

# Se inicia el programa con el contexto actual como main y esta siendo la
# unica funcion que existe en memoria
PContexto.push(0)
PMemoria.push('main')

# Variables para controlar el cuadruplo actual en el que se esta y el total
# de cuadruplos que se tienen
cuadruploActual = 0
numCuadruplos = 0

# Global que almacena el error de ejecucion correspondiente
error = ''

# Funcion auxiliar que sirve para revisar si una direccion de memoria
# representa un acceso a una variable guardada en esa direccion, un acceso
# a una direccion guardada en dicha direccion o simplemente la direccion
# como tal
def revisarDireccion(Direccion):
	if(str(Direccion)[0] == '|'):
		return 'Base'
	elif(str(Direccion)[0] == '('):
		return 'Indirecto'
	else:
		return 'Directo'

# Funcion que toma dos operadores del cuadruplo, los suma y pone su
# resultado en la direccion del Resultado
def suma(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes

	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion2 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion2 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador2 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador2 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = 0

	# Se almacena el valor de la suma en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = Operador1 + Operador2
	return 'suma'

# Funcion que toma dos operadores del cuadruplo, los resta y pone su
# resultado en la direccion del Resultado
def resta(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes

	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())
	
	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion2 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion2 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador2 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador2 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = 0

	# Se almacena el valor de la resta en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = Operador1 - Operador2
	return 'resta'

# Funcion que toma dos operadores del cuadruplo, los multiplica y pone su
# resultado en la direccion del Resultado
def multiplicacion(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())
	
	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion2 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion2 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador2 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador2 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = 0

	# Se almacena el valor de la multiplicacion en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = Operador1 * Operador2
	return 'multiplicacion'

# Funcion que toma dos operadores del cuadruplo, los divide y pone su
# resultado en la direccion del Resultado
def division(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	global error
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion2 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion2 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador2 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador2 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = 0

	# Si el operador 2 en la division es 0, entonces se marca error de ejecucion
	# y se detiene el programa
	if(Operador2 == 0):
		error = "Execution Error: Division by 0"
		raise KeyboardInterrupt

	# Se almacena el valor de la division en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = Operador1 / Operador2
	return 'division'

# Funcion que asigna un valor a otro valor y pone su resultado en la direccion del
# Resultado
def asignacion(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes

	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = 0

	# Se almacena el valor de la asignacion en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = Operador1
	return 'asignacion'

# Funcion que toma dos operadores del cuadruplo, aplica la operacion or y
# pone su resultado en la direccion del Resultado
def condicionOr(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = False

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = False

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion2 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion2 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador2 = False

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador2 = False

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = False

	# Se almacena el valor de la operacion or en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = Operador1 or Operador2
	return 'condicionOr'

# Funcion que toma dos operadores del cuadruplo, aplica la operacion and y
# pone su resultado en la direccion del Resultado
def condicionAnd(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = False

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = False

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion2 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion2 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador2 = False

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador2 = False

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = False

	# Se almacena el valor de la operacion and en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = Operador1 and Operador2
	return 'condicionAnd'

# Funcion que toma un valor booleano y le aplica la operacion not, poniendo
# su resultado en la direccion del Resultado
def condicionNot(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = False

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = False

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = False

	# Se almacena el valor de la operacion not en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = not(Operador1)
	return 'condicionNot'

# Funcion que toma dos operadores del cuadruplo, revisa si el primero es mayor
# al segundo, y pone el resultado de la operacion en la direccion del Resultado
def mayorQue(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())
	
	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion2 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion2 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador2 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador2 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = 0

	# Se almacena el valor de la operacion mayor que en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = Operador1 > Operador2
	return 'mayorQue'

# Funcion que toma dos operadores del cuadruplo, revisa si el primero es menor
# al segundo, y pone el resultado de la operacion en la direccion del Resultado
def menorQue(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion2 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion2 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador2 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador2 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = 0

	# Se almacena el valor de la operacion menor que en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = Operador1 < Operador2
	return 'menorQue'

# Funcion que toma dos operadores del cuadruplo, revisa si el primero es menor o igual
# al segundo, y pone el resultado de la operacion en la direccion del Resultado
def menorIgualQue(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion2 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion2 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador2 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador2 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = 0

	# Se almacena el valor de la operacion menor o igual que en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = Operador1 <= Operador2
	return 'menorIgualQue'

# Funcion que toma dos operadores del cuadruplo, revisa si el primero es mayor o igual
# al segundo, y pone el resultado de la operacion en la direccion del Resultado
def mayorIgualQue(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion2 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion2 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador2 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador2 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = 0

	# Se almacena el valor de la operacion mayor o igual que en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = Operador1 >= Operador2
	return 'mayorIgualQue'

# Funcion que toma dos operadores del cuadruplo, revisa si el primero es igual
# al segundo, y pone el resultado de la operacion en la direccion del Resultado
def igualQue(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion2 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion2 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador2 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador2 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = 0

	# Se almacena el valor de la operacion igual que en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = Operador1 == Operador2
	return 'igualQue'

# Funcion que toma dos operadores del cuadruplo, revisa si el primero es diferente
# al segundo, y pone el resultado de la operacion en la direccion del Resultado
def noIgualQue(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion2 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion2 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador2 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador2 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = 0

	# Se almacena el valor de la operacion diferente a en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = Operador1 != Operador2
	return 'noIgualQue'

# Funcion que toma dos operadores del cuadruplo, los divide y pone su
# resultado en la direccion del Resultado
def modulo(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	global error
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion2 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion2 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador2 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador2 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = 0

	# Si el operador 2 en la division es 0, entonces se marca error de ejecucion
	# y se detiene el programa
	if(Operador2 == 0):
		error = "Execution Error: Division by 0"
		raise KeyboardInterrupt

	# Se almacena el valor de la division en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = Operador1 % Operador2
	return 'modulo'

# Funcion que toma un valor numerico y lo multiplica por -1, poniendo
# su resultado en la direccion del Resultado
def negacion(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = 0

	# Se almacena el valor de la operacion negacion en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = -1 * Operador1
	return 'negacion'

# Funcion que obtiene un valor como input del teclado y lo almacena en una variable
def stdIn(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	global DirBaseClase
	global DirBaseMetodo
	global DirBaseMetodoTemp
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = 0

	# Se revisa de qué tipo es la dirección de la variable donde se va a almacenar
	# el resultado y se parsea al tipo especifico
	if((Resultado >= DirBaseClase['numeral'] and Resultado < DirBaseClase['real']) or (Resultado >= DirBaseMetodo['numeral'] and Resultado < DirBaseMetodo['real']) or (Resultado >= DirBaseMetodoTemp['numeral'] and Resultado < DirBaseMetodoTemp['real'])):
		valor = int(raw_input())
	elif((Resultado >= DirBaseClase['real'] and Resultado < DirBaseClase['string']) or (Resultado >= DirBaseMetodo['real'] and Resultado < DirBaseMetodo['string']) or (Resultado >= DirBaseMetodoTemp['real'] and Resultado < DirBaseMetodoTemp['string'])):
		valor = float(raw_input())
	elif((Resultado >= DirBaseClase['bool'] and Resultado < DirBaseClase['char']) or (Resultado >= DirBaseMetodo['bool'] and Resultado < DirBaseMetodo['char']) or (Resultado >= DirBaseMetodoTemp['bool'] and Resultado < DirBaseMetodoTemp['char'])):
		valor = raw_input()
		if(valor == 'true'):
			valor = True
		else:
			valor = False
	else:
		valor = raw_input()

	# Se almacena el valor qu se obtiene del teclado en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = valor
	return 'stdIn'

# Funcion que arroja un valor como output a la consola
def stdOut(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = ''
	
		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Resultado)):
			Resultado = DirConstantes[Resultado]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Resultado)):
			Resultado = MapaMemoria[contextoActual][Resultado]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Resultado = ''

	# Se imprime el resultado en consola, reemplazando los \n
	print(str(Resultado).replace('\\n', '\n'), end='')

	return 'stdOut'

# Funcion que sirve para retornar los valores de una funcion a su contexto anterior
def retorno(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global PRetornos
	global MapaMemoria
	global DirConstantes
	global cuadruploActual
	global numCuadruplos
	
	# Si no es el retorno de la funcion main
	if(cuadruploActual != numCuadruplos - 1):
		# Se obtiene el contexto actual
		contextoActual = PMemoria.top()
		PContexto.pop()

		# Se obtiene el contexto al que se va a regresar
		contextoNuevo = PMemoria.at(PContexto.top())
		PContexto.push(PMemoria.size() - 1)

		# Si si se retorna un valor
		if(Operador1 != '-'):
			# Se revisa que tipo de direcciones representan las direcciones de los
			# operadores y la direccion del resultado
			TipoDireccion = revisarDireccion(Operador1)
	
			# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
			# al principio y al final de la direccion)
			if(TipoDireccion != 'Directo'):
				Operador1 = str(Operador1)[1:-1]

			# Se parsea el valor de las direcciones a valores enteros
			Direccion = int(Operador1)
		
		# Si no se retorna un valor
		else:
			TipoDireccion = 'Base'
			Direccion = 0

		# Si el tipo de direccionamiento no es una direccion tal cual
		if(TipoDireccion != 'Base'):
			# Si el direccionamiento es de tipo indirecto
			if(TipoDireccion == 'Indirecto'):
				# Se revisa en el directorio de constantes si ahi se encuentra la
				# nueva direccion, y si es asi, se almacena su valor
				if(DirConstantes.has_key(Direccion)):
					Direccion = DirConstantes[Direccion]
				# Se revisa en el mapa de memoria si ahi se encuentra la nueva
				# direccion, y si es asi, se almacena su valor
				elif(MapaMemoria[contextoActual].has_key(Direccion)):
					Direccion = MapaMemoria[contextoActual][Direccion]
				# Si no se encontro el valor de la nueva direccion, se obtiene
				# entonces el valor default que es 0
				else:
					Direccion = ''

			# Se revisa en el directorio de constantes si ahi se encuentra el valor
			# de la direccion del operador, y si es asi, se almacena este valor
			if(DirConstantes.has_key(Direccion)):
				ValorRetorno = DirConstantes[Direccion]
			# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
			# direccion del operador, y si es asi, se almacena este valor
			elif(MapaMemoria[contextoActual].has_key(Direccion)):
				ValorRetorno = MapaMemoria[contextoActual][Direccion]
			# Si no se encontro el valor al que apuntaba la direccion, se obtiene
			# entonces el valor default que es 0
			else:
				ValorRetorno = 0

		# Se obtiene la direccion en la que se guardara valor de retorno
		DireccionRetorno = PRetornos.top()[0]
		
		# Si la direccion si tiene valor de retorno, este se guarda
		if(DireccionRetorno != '-'):
			MapaMemoria[contextoNuevo][DireccionRetorno] = ValorRetorno

		# Se obtiene el cuadruplo al cual se regresara
		cuadruploActual = PRetornos.top()[1]

		PRetornos.pop()

		# Si no se regresan ni arreglos ni atributos del objeto, se borra el
		# contexto actual del Mapa de Memoria y se saca este contexto de la
		# pila de contextos y la pila de memorias
		if(Cuadruplos[cuadruploActual + 1][0] != "ATTR_RET" and Cuadruplos[cuadruploActual + 1][0] != "REF_RET"):
			del MapaMemoria[contextoActual]
			PContexto.pop()
			PMemoria.pop()

	return 'retorno'

# Funcion que sirve para manejar la ejecucion de saltos en falso en los programas
def gotoF(Operador1, Operador2, Resultado):
	global cuadruploActual
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)

	# Se revisa en el directorio de constantes si ahi se encuentra el valor
	# de la direccion del operador, y si es asi, se almacena este valor
	if(DirConstantes.has_key(Operador1)):
		Condicion = DirConstantes[Operador1]
	# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
	# direccion del operador, y si es asi, se almacena este valor
	elif(MapaMemoria[contextoActual].has_key(Operador1)):
		Condicion = MapaMemoria[contextoActual][Operador1]
	# Si no se encontro el valor al que apuntaba la direccion, se obtiene
	# entonces el valor default que es 0
	else:
		Condicion = False

	# Si la condicion dio falso como resultado.
	if(not(Condicion)):
		# Se mueve el cuadruplo actual al siguiente cuadruplo a ejecutar
		cuadruploActual = int(Operador2)
		Operacion = Cuadruplos[cuadruploActual][0]
		Operador1 = Cuadruplos[cuadruploActual][1]
		Operador2 = Cuadruplos[cuadruploActual][2]
		Resultado = Cuadruplos[cuadruploActual][3]
		Operaciones[Operacion](Operador1, Operador2, Resultado)

	return 'gotoF'

# Funcion que sive para simular realizar saltos en ejecucion.
def goto(Operador1, Operador2, Resultado):
	global cuadruploActual
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes

	# Se obtiene el valor del cuadruplo al que se saltara
	cuadruploActual = int(Operador2)

	# # Se mueve el cuadruplo actual al siguiente cuadruplo a ejecutar
	Operacion = Cuadruplos[cuadruploActual][0]
	Operador1 = Cuadruplos[cuadruploActual][1]
	Operador2 = Cuadruplos[cuadruploActual][2]
	Resultado = Cuadruplos[cuadruploActual][3]
	Operaciones[Operacion](Operador1, Operador2, Resultado)

	return 'goto'

# Funcion para mandar un atributo de un contexto de clase a otro.
def mandarAtributo(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtienen los contextos actual y nuevo.
	contextoActual = PMemoria.at(PContexto.top())
	contextoNuevo = PMemoria.top()

	# Se obtiene la direccion de la que proviene atributo
	Operador1 = int(Operador1)

	# Se revisa en el directorio de constantes si ahi se encuentra el valor
	# de la direccion del operador, y si es asi, se almacena este valor
	if(DirConstantes.has_key(Operador1)):
		ValorOriginal = DirConstantes[Operador1]
	# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
	# direccion del operador, y si es asi, se almacena este valor
	elif(MapaMemoria[contextoActual].has_key(Operador1)):
		ValorOriginal = MapaMemoria[contextoActual][Operador1]
	# Si no se encontro el valor al que apuntaba la direccion, se obtiene
	# entonces el valor default que es 0
	else:
		ValorOriginal = 0

	# Se guarda el valor del atributo en su nueva direccion
	MapaMemoria[contextoNuevo][int(Operador2)] = ValorOriginal
	return 'mandarAtributo'

# Funcion para mandar un atributo como referencia
def mandarReferencia(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtienen los contextos actual y nuevo.
	contextoActual = PMemoria.at(PContexto.top())
	contextoNuevo = PMemoria.top()

	# Se obtiene la direccion de la que proviene atributo
	Operador1 = int(Operador1)
	
	# Se revisa en el directorio de constantes si ahi se encuentra el valor
	# de la direccion del operador, y si es asi, se almacena este valor
	if(DirConstantes.has_key(Operador1)):
		ValorOriginal = DirConstantes[Operador1]
	# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
	# direccion del operador, y si es asi, se almacena este valor
	elif(MapaMemoria[contextoActual].has_key(Operador1)):
		ValorOriginal = MapaMemoria[contextoActual][Operador1]
	# Si no se encontro el valor al que apuntaba la direccion, se obtiene
	# entonces el valor default que es 0
	else:
		ValorOriginal = 0

	# Se guarda el valor del atributo en su nueva direccion
	MapaMemoria[contextoNuevo][int(Resultado)] = ValorOriginal
	return 'mandarReferencia'

# Funcion que se ejecuta cuando se llega al cuadruplo GOSUB y sirve para
# cambiar el contexto de la maquina virtual a la nueva funcion
def cambiarContexto(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global PRetornos
	global cuadruploActual

	# Se mete el nuevo contexto en la pila de contextos
	PContexto.push(PMemoria.size() - 1)

	# Si la funcion retorna algo
	if(Resultado != '-'):
		# Se mete este valor y el cuadruplo al que se regresara a la pila
		# de retornos
		PRetornos.push([int(Resultado), cuadruploActual])
	# Si no
	else:
		# Se mete un valor vacio y el cuadruplo al que se regresara a la
		# pila de retornos
		PRetornos.push(['-', cuadruploActual])

	# Se obtiene el cuadruplo al que se llegara al inicio de la funcion
	cuadruploActual = int(Operador2)

	# Se manda a llamar la siguiente operacion
	Operacion = Cuadruplos[cuadruploActual][0]
	Operador1 = Cuadruplos[cuadruploActual][1]
	Operador2 = Cuadruplos[cuadruploActual][2]
	Resultado = Cuadruplos[cuadruploActual][3]
	Operaciones[Operacion](Operador1, Operador2, Resultado)

	return 'cambiarContexto'

# Funcion para regresar el valor final de un parametro por referencia de
# una funcion
def regresarReferencia(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	global cuadruploActual
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.top()
	PContexto.pop()

	# Se obtiene el contexto nuevo
	contextoNuevo = PMemoria.at(PContexto.top())
	PContexto.push(PMemoria.size() - 1)
	
	# Se obtienen los valores del cuadruplo actual
	Operacion = Cuadruplos[cuadruploActual][0]
	Operador1 = Cuadruplos[cuadruploActual][1]
	Operador2 = Cuadruplos[cuadruploActual][2]
	Resultado = Cuadruplos[cuadruploActual][3]
	
	# Mientras la operacion sea regresar un parametro
	while(Operacion == 'REF_RET'):
		# Se castea el operador 1 a int
		Operador1 = int(Operador1)

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			ValorOriginal = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			ValorOriginal = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			ValorOriginal = 0

		# Se guarda el valor del atributo en su nueva direccion
		MapaMemoria[contextoNuevo][int(Resultado)] = ValorOriginal

		# Se incrementa el cuadruplo y se obtienen los valores de este
		cuadruploActual = cuadruploActual + 1
		Operacion = Cuadruplos[cuadruploActual][0]
		Operador1 = Cuadruplos[cuadruploActual][1]
		Resultado = Cuadruplos[cuadruploActual][3]

	# Si la siguiente operacion no es regresar un atributo
	if(Operacion != 'ATTR_RET'):
		# Se borra el contexto actual del mapa y se saca de las pilas de contexto
		# y de memorias
		del MapaMemoria[contextoActual]
		PContexto.pop()
		PMemoria.pop()

	# Se decrementa el cuadruplo actual en 1
	cuadruploActual = cuadruploActual - 1

	return 'regresarAtributo'

# Funcion para regresar el valor final de un atributo de clase de
# una funcion
def regresarAtributo(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	global cuadruploActual
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.top()
	PContexto.pop()
	
	# Se obtiene el contexto nuevo
	contextoNuevo = PMemoria.at(PContexto.top())
	PMemoria.pop()

	# Se obtienen los valores del cuadruplo actual
	Operacion = Cuadruplos[cuadruploActual][0]
	Operador1 = Cuadruplos[cuadruploActual][1]
	Operador2 = Cuadruplos[cuadruploActual][2]
	Resultado = Cuadruplos[cuadruploActual][3]
	
	# Mientras la operacion sea regresar un atributo
	while(Operacion == 'ATTR_RET'):
		# Se castea el operador 1 a int
		Operador1 = int(Operador1)

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			ValorOriginal = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			ValorOriginal = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			ValorOriginal = 0

		# Se guarda el valor del atributo en su nueva direccion
		MapaMemoria[contextoNuevo][int(Operador2)] = ValorOriginal

		# Se incrementa el cuadruplo y se obtienen los valores de este
		cuadruploActual = cuadruploActual + 1
		Operacion = Cuadruplos[cuadruploActual][0]
		Operador1 = Cuadruplos[cuadruploActual][1]
		Operador2 = Cuadruplos[cuadruploActual][2]

	# Se decrementa el cuadruplo actual en 1
	cuadruploActual = cuadruploActual - 1

	# Se borra el contexto actual del mapa de memorias
	del MapaMemoria[contextoActual]

	return 'regresarAtributo'

# Metodo que genera el contexto nuevo al llegar un cuadruplo
# de tipo ERA
def generarContextoMetodo(Operador1, Operador2, Resultado):
	global MapaMemoria
	global PMemoria
	global cuadruploActual

	# Se establece un numero para identificar llamadas recursivas
	# o de metodos con mismo nombre en diferentes clases
	diferenciadorMetodos = 0

	# Se obtiene el nombre del metodo y se le hace append el diferenciador
	Operador1 = Operador1 + str(diferenciadorMetodos)

	# Mientras el metodo ya exista en el mapa de memoria, el numero del
	# identificador sigue aumentando
	while(MapaMemoria.has_key(Operador1)):
		n = diferenciadorMetodos - 1
		if(n <= 0):
			x = 1
		else:
			x = 0
		while(n > 0):
			n = n // 10
			x = x + 1
		while(x > 0):
			Operador1 = str(Operador1)[:-1]
			x = x - 1
		Operador1 = Operador1 + str(diferenciadorMetodos)
		diferenciadorMetodos = diferenciadorMetodos + 1

	# Se mete el nuevo metodo al mapa de memorias
	MapaMemoria[Operador1] = {}

	# Se mete el nuevo metodo a la pila de memorias
	PMemoria.push(Operador1)

	return 'generarContextoMetodo'

# Funcion para enviar un parametro por valor a una funcion
def enviarParametro(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtienen los contextos actual y nuevo
	contextoActual = PMemoria.at(PContexto.top())
	contextoNuevo = PMemoria.top()
	
	# Se castea el operador 1 a int
	Operador1 = int(Operador1)

	# Se revisa en el directorio de constantes si ahi se encuentra el valor
	# de la direccion del operador, y si es asi, se almacena este valor
	if(DirConstantes.has_key(Operador1)):
		ValorOriginal = DirConstantes[Operador1]
	# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
	# direccion del operador, y si es asi, se almacena este valor
	elif(MapaMemoria[contextoActual].has_key(Operador1)):
		ValorOriginal = MapaMemoria[contextoActual][Operador1]
	# Si no se encontro el valor al que apuntaba la direccion, se obtiene
	# entonces el valor default que es 0
	else:
		ValorOriginal = 0

	# Se guarda el valor del atributo en su nueva direccion
	MapaMemoria[contextoNuevo][int(Resultado)] = ValorOriginal
	return 'enviarParametro'

# Funcion para verificar que en el acceso a un arreglo, el indice especificado
# se encuentre dentro del rango de dimensiones del mismo
def verificaArreglo(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	global numCuadruplos
	global error

	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = 0

	# Se parsea el valor de las direcciones a valores enteros
	Operador2 = int(Operador2)

	# Si el indice no esta dentro de las direcciones, se marca error de ejecucion
	# y se detiene la ejecucion del programa
	if(Operador1 < 0 or Operador1 >= Operador2):
		error = 'Execution Error: Index out of bounds'
		raise KeyboardInterrupt

	return 'verificaArreglo'

# Funcion que toma dos strings del cuadruplo, los concatena y pone su
# resultado en la direccion del Resultado
def concatenarStrings(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = ''

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = ''

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion2 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion2 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador2 = ''

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador2 = ''

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = 0

	# Se almacena el valor de la operacion de concatenacion en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = str(Operador1) + str(Operador2)
	return 'concatenarStrings'

# Funcion que toma un string y un indice del cuadruplo, obtiene el caracter
# en tal posicion en el string y pone su resultado en la direccion del Resultado
def caracterEnPosicion(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = ''

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = ''

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion2 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion2 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador2 = 0

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador2 = 0

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = 0

	# Se almacena el valor de la operacion de charAt en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = str(Operador1)[Operador2]
	return 'caracterEnPosicion'

# Funcion que toma un string y obtiene su longitud en cuanto a numero de caracteres
# en tal posicion en el string y pone su resultado en la direccion del Resultado
def longitudString(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	
	# Se obtiene el contexto actual
	contextoActual = PMemoria.at(PContexto.top())

	# Se revisa que tipo de direcciones representan las direcciones de los
	# operadores y la direccion del resultado
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccionR = revisarDireccion(Resultado)
	
	# Se obtiene el valor numerico de las direcciones (eliminando '||' y '()'
	# al principio y al final de la direccion)
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	# Se parsea el valor de las direcciones a valores enteros
	Operador1 = int(Operador1)
	Resultado = int(Resultado)

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccion1 != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccion1 == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Operador1 = ''

		# Se revisa en el directorio de constantes si ahi se encuentra el valor
		# de la direccion del operador, y si es asi, se almacena este valor
		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		# Se revisa en el mapa de memoria si ahi se encuentra el valor de la
		# direccion del operador, y si es asi, se almacena este valor
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		# Si no se encontro el valor al que apuntaba la direccion, se obtiene
		# entonces el valor default que es 0
		else:
			Operador1 = ''

	# Si el tipo de direccionamiento no es una direccion tal cual
	if(TipoDireccionR != 'Base'):
		# Si el direccionamiento es de tipo indirecto
		if(TipoDireccionR == 'Indirecto'):
			# Se revisa en el directorio de constantes si ahi se encuentra la
			# nueva direccion, y si es asi, se almacena su valor
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			# Se revisa en el mapa de memoria si ahi se encuentra la nueva
			# direccion, y si es asi, se almacena su valor
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			# Si no se encontro el valor de la nueva direccion, se obtiene
			# entonces el valor default que es 0
			else:
				Resultado = 0

	# Se almacena el valor de la operacion de longitud de string en la direccion del resultado
	MapaMemoria[contextoActual][Resultado] = len(str(Operador1))
	return 'longitudString'

# Diccionario de operaciones que mapea las operaciones en los cuadruplos
# con funciones que previamente se han definido
Operaciones = {
	'MAS': suma,
	'MENOS': resta,
	'POR': multiplicacion,
	'ENTRE': division,
	'IGUAL': asignacion,
	'OR': condicionOr,
	'AND': condicionAnd,
	'NOT': condicionNot,
	'MAYOR': mayorQue,
	'MENOR': menorQue,
	'MENORIGUAL': menorIgualQue,
	'MAYORIGUAL': mayorIgualQue,
	'IGUALC': igualQue,
	'NOTIGUAL': noIgualQue,
	'MOD': modulo,
	'UMENOS': negacion,
	'INPUT': stdIn,
	'OUTPUT': stdOut,
	'RETURN': retorno,
	'GOTOF': gotoF,
	'GOTO': goto,
	'ATTR_GO': mandarAtributo,
	'GOSUB': cambiarContexto,
	'ATTR_RET': regresarAtributo,
	'ERA': generarContextoMetodo,
	'PARAM': enviarParametro,
	'VER': verificaArreglo,
	'REF_GO': mandarReferencia,
	'REF_RET': regresarReferencia,
	'CONCAT': concatenarStrings,
	'CHARAT': caracterEnPosicion,
	'LEN': longitudString
}

# Metodo que se llama al iniciar la ejecucion de la maquina virtual
def execute():
	global DirConstantes
	global numCuadruplos
	global cuadruploActual
	global Cuadruplos
	global MapaMemoria
	global error
	global PContexto
	global PMemoria
	global PRetornos

	# Se inicializan controladores globales de la maquina virtual
	MapaMemoria = { 'main': {} }
	DirConstantes = {}
	Cuadruplos = []

	PContexto = stack()
	PMemoria = stack()
	PRetornos = stack()
	PContexto.push(0)
	PMemoria.push('main')

	error = ''

	cuadruploActual = 0
	numCuadruplos = 0

	# Se lee el codigo intermedio del archivo codigoArr.txt
	s = 'codigoArr.txt'
	if(os.path.isfile(s)):
		with open(s, 'r') as f:
			# Se almacena cada linea del archivo en un arreglo
			lineArr = f.readlines()

			# Se guardan las constantes utilizadas en el programa en el directorio
			# de constantes, parseando los valores a sus contrapartes correspondientes
			numConstantesEnteras = int(lineArr[0])
			for i in range(1, numConstantesEnteras + 1):
				DirConstantes[ int(lineArr[i][:-1].split('\t')[1]) ] = int(lineArr[i][:-1].split('\t')[0])
			numConstantesReales = int(lineArr[numConstantesEnteras + 1])
			for i in range(numConstantesEnteras + 2, numConstantesEnteras + numConstantesReales + 2):
				DirConstantes[ int(lineArr[i][:-1].split('\t')[1]) ] = float(lineArr[i][:-1].split('\t')[0])
			actual = numConstantesEnteras + numConstantesReales + 2
			numConstantesString = int(lineArr[actual])
			for i in range(actual + 1, actual + numConstantesString + 1):
				DirConstantes[ int(lineArr[i][:-1].split('\t')[1]) ] = lineArr[i][:-1].split('\t')[0][1:-1]
			actual = actual + numConstantesString + 1
			numConstantesBool = int(lineArr[actual])
			for i in range(actual + 1, actual + numConstantesBool + 1):
				if(lineArr[i][:-1].split('\t')[0] == 'true'):
					DirConstantes[ int(lineArr[i][:-1].split('\t')[1]) ] = True
				else:
					DirConstantes[ int(lineArr[i][:-1].split('\t')[1]) ] = False
			actual = actual + numConstantesBool + 1
			numConstantesChar = int(lineArr[actual])
			for i in range(actual + 1, actual + numConstantesChar + 1):
				DirConstantes[ int(lineArr[i][:-1].split('\t')[1]) ] = lineArr[i][:-1].split('\t')[0][1:-1]
			actual = actual + numConstantesChar + 1
			
			# Se guardan los cuadruplos generados en compilacion en un arreglo
			numCuadruplos = int(lineArr[actual])
			for i in range(actual + 1, actual + numCuadruplos + 1):
				line = lineArr[i][:-1].split('\t')
				Cuadruplos.append([line[1], line[2], line[3], line[4]])
		
		# Se inicializa en el cuadruplo actual
		cuadruploActual = 0
		
		# Si el cuadruplo actual no es el ultimo cuadruplo
		while(cuadruploActual != numCuadruplos):
			# Se realiza la operacion de dicho cuadruplo
			Operacion = Cuadruplos[cuadruploActual][0]
			Operador1 = Cuadruplos[cuadruploActual][1]
			Operador2 = Cuadruplos[cuadruploActual][2]
			Resultado = Cuadruplos[cuadruploActual][3]
			Operaciones[Operacion](Operador1, Operador2, Resultado)
			
			# Se aumenta el numero del cuadruplo actual
			cuadruploActual = cuadruploActual + 1
		
		# Se imprime mensaje de ejecucion finalizada
		print('\nExecution finished')

		# Se cierra archivo de codigo intermedio
		f.close()
	
	# Si no se pudo leer el archivo, se indica con un mensaje.
	else:
		print("Couldn't open file specified")

