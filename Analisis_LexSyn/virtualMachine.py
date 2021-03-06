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

MapaMemoria = { 'main': {} }
DirConstantes = {}
Cuadruplos = []

PContexto = stack()
PMemoria = stack()
PRetornos = stack()
PContexto.push(0)
PMemoria.push('main')

cuadruploActual = 0

def revisarDireccion(Direccion):
	if(str(Direccion)[0] == '|'):
		return 'Base'
	elif(str(Direccion)[0] == '('):
		return 'Indirecto'
	else:
		return 'Directo'

def suma(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes	
	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = 0

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = 0

	if(TipoDireccion2 != 'Base'):
		if(TipoDireccion2 == 'Indirecto'):
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			else:
				Operador2 = 0

		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		else:
			Operador2 = 0

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = 0

	MapaMemoria[contextoActual][Resultado] = Operador1 + Operador2
	return 'suma'

def resta(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = 0

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = 0

	if(TipoDireccion2 != 'Base'):
		if(TipoDireccion2 == 'Indirecto'):
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			else:
				Operador2 = 0

		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		else:
			Operador2 = 0

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = 0

	MapaMemoria[contextoActual][Resultado] = Operador1 - Operador2
	return 'resta'

def multiplicacion(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = 0

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = 0

	if(TipoDireccion2 != 'Base'):
		if(TipoDireccion2 == 'Indirecto'):
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			else:
				Operador2 = 0

		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		else:
			Operador2 = 0

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = 0

	MapaMemoria[contextoActual][Resultado] = Operador1 * Operador2
	return 'multiplicacion'

def division(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = 0

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = 0

	if(TipoDireccion2 != 'Base'):
		if(TipoDireccion2 == 'Indirecto'):
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			else:
				Operador2 = 0

		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		else:
			Operador2 = 0

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = 0

	if(Operador2 == 0):
		print("\nExecution Error: Division by 0")
		exit()

	MapaMemoria[contextoActual][Resultado] = Operador1 / Operador2
	return 'division'

def asignacion(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes

	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = 0

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = 0

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = 0

	MapaMemoria[contextoActual][Resultado] = Operador1
	return 'asignacion'

def condicionOr(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = False

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = False

	if(TipoDireccion2 != 'Base'):
		if(TipoDireccion2 == 'Indirecto'):
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			else:
				Operador2 = False

		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		else:
			Operador2 = False

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = False


	MapaMemoria[contextoActual][Resultado] = Operador1 or Operador2
	return 'condicionOr'

def condicionAnd(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = False

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = False

	if(TipoDireccion2 != 'Base'):
		if(TipoDireccion2 == 'Indirecto'):
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			else:
				Operador2 = False

		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		else:
			Operador2 = False

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = False

	MapaMemoria[contextoActual][Resultado] = Operador1 and Operador2
	return 'condicionAnd'

def condicionNot(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = False

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = False

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = False

	MapaMemoria[contextoActual][Resultado] = not(Operador1)
	return 'condicionNot'

def mayorQue(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = 0

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = 0

	if(TipoDireccion2 != 'Base'):
		if(TipoDireccion2 == 'Indirecto'):
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			else:
				Operador2 = 0

		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		else:
			Operador2 = 0

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = 0

	MapaMemoria[contextoActual][Resultado] = Operador1 > Operador2
	return 'mayorQue'

def menorQue(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = 0

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = 0

	if(TipoDireccion2 != 'Base'):
		if(TipoDireccion2 == 'Indirecto'):
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			else:
				Operador2 = 0

		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		else:
			Operador2 = 0

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = 0

	MapaMemoria[contextoActual][Resultado] = Operador1 < Operador2
	return 'menorQue'

def menorIgualQue(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = 0

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = 0

	if(TipoDireccion2 != 'Base'):
		if(TipoDireccion2 == 'Indirecto'):
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			else:
				Operador2 = 0

		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		else:
			Operador2 = 0

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = 0

	MapaMemoria[contextoActual][Resultado] = Operador1 <= Operador2
	return 'menorIgualQue'

def mayorIgualQue(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = 0

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = 0

	if(TipoDireccion2 != 'Base'):
		if(TipoDireccion2 == 'Indirecto'):
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			else:
				Operador2 = 0

		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		else:
			Operador2 = 0

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = 0

	MapaMemoria[contextoActual][Resultado] = Operador1 >= Operador2
	return 'mayorIgualQue'

def igualQue(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = 0

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = 0

	if(TipoDireccion2 != 'Base'):
		if(TipoDireccion2 == 'Indirecto'):
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			else:
				Operador2 = 0

		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		else:
			Operador2 = 0

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = 0

	MapaMemoria[contextoActual][Resultado] = Operador1 == Operador2
	return 'igualQue'

def noIgualQue(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = 0

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = 0

	if(TipoDireccion2 != 'Base'):
		if(TipoDireccion2 == 'Indirecto'):
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			else:
				Operador2 = 0

		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		else:
			Operador2 = 0

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = 0

	MapaMemoria[contextoActual][Resultado] = Operador1 != Operador2
	return 'noIgualQue'

def modulo(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = 0

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = 0

	if(TipoDireccion2 != 'Base'):
		if(TipoDireccion2 == 'Indirecto'):
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			else:
				Operador2 = 0

		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		else:
			Operador2 = 0

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = 0

	if(Operador2 == 0):
		print("\nExecution Error: Division by 0")
		exit()

	MapaMemoria[contextoActual][Resultado] = Operador1 % Operador2
	return 'modulo'

def negacion(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = 0

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = 0

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = 0

	MapaMemoria[contextoActual][Resultado] = -1 * Operador1
	return 'negacion'

def stdIn(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	global DirBaseClase
	global DirBaseMetodo
	global DirBaseMetodoTemp
	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion = revisarDireccion(Resultado)
	
	if(TipoDireccion != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Resultado = int(Resultado)

	if(TipoDireccion != 'Base'):
		if(TipoDireccion == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = 0

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

	MapaMemoria[contextoActual][Resultado] = valor
	return 'stdIn'

def stdOut(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion = revisarDireccion(Resultado)
	
	if(TipoDireccion != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Resultado = int(Resultado)

	if(TipoDireccion != 'Base'):
		if(TipoDireccion == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = ''
	
		if(DirConstantes.has_key(Resultado)):
			Resultado = DirConstantes[Resultado]
		elif(MapaMemoria[contextoActual].has_key(Resultado)):
			Resultado = MapaMemoria[contextoActual][Resultado]
		else:
			Resultado = ''

	print(str(Resultado).replace('\\n', '\n'), end='')

	return 'stdOut'

def retorno(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global PRetornos
	global MapaMemoria
	global DirConstantes
	global cuadruploActual
	global numCuadruplos
	
	if(cuadruploActual != numCuadruplos - 1):
		contextoActual = PMemoria.top()
		PContexto.pop()
		contextoNuevo = PMemoria.at(PContexto.top())
		PContexto.push(PMemoria.size() - 1)

		if(Operador1 != '-'):
			Direccion = int(Operador1)
		else:
			Direccion = 0

		if(DirConstantes.has_key(Direccion)):
			ValorRetorno = DirConstantes[Direccion]
		elif(MapaMemoria[contextoActual].has_key(Direccion)):
			ValorRetorno = MapaMemoria[contextoActual][Direccion]
		else:
			ValorRetorno = 0

		DireccionRetorno = PRetornos.top()[0]
		if(DireccionRetorno != '-'):
			MapaMemoria[contextoNuevo][DireccionRetorno] = ValorRetorno

		cuadruploActual = PRetornos.top()[1]

		PRetornos.pop()

		if(Cuadruplos[cuadruploActual + 1][0] != "ATTR_RET" and Cuadruplos[cuadruploActual + 1][0] != "REF_RET"):
			del MapaMemoria[contextoActual]
			PContexto.pop()
			PMemoria.pop()

	return 'retorno'

def gotoF(Operador1, Operador2, Resultado):
	global cuadruploActual
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())

	Operador1 = int(Operador1)

	if(DirConstantes.has_key(Operador1)):
		Condicion = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual].has_key(Operador1)):
		Condicion = MapaMemoria[contextoActual][Operador1]
	else:
		Condicion = False

	if(not(Condicion)):
		cuadruploActual = int(Operador2)
		Operacion = Cuadruplos[cuadruploActual][0]
		Operador1 = Cuadruplos[cuadruploActual][1]
		Operador2 = Cuadruplos[cuadruploActual][2]
		Resultado = Cuadruplos[cuadruploActual][3]
		Operaciones[Operacion](Operador1, Operador2, Resultado)

	return 'gotoF'

def goto(Operador1, Operador2, Resultado):
	global cuadruploActual
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes

	cuadruploActual = int(Operador2)

	Operacion = Cuadruplos[cuadruploActual][0]
	Operador1 = Cuadruplos[cuadruploActual][1]
	Operador2 = Cuadruplos[cuadruploActual][2]
	Resultado = Cuadruplos[cuadruploActual][3]
	Operaciones[Operacion](Operador1, Operador2, Resultado)

	return 'goto'

def mandarAtributo(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	contextoNuevo = PMemoria.top()

	Operador1 = int(Operador1)
	
	if(DirConstantes.has_key(Operador1)):
		ValorOriginal = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual].has_key(Operador1)):
		ValorOriginal = MapaMemoria[contextoActual][Operador1]
	else:
		ValorOriginal = 0

	MapaMemoria[contextoNuevo][int(Operador2)] = ValorOriginal
	return 'mandarAtributo'

def mandarReferencia(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	contextoNuevo = PMemoria.top()

	Operador1 = int(Operador1)
	
	if(DirConstantes.has_key(Operador1)):
		ValorOriginal = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual].has_key(Operador1)):
		ValorOriginal = MapaMemoria[contextoActual][Operador1]
	else:
		ValorOriginal = 0

	MapaMemoria[contextoNuevo][int(Resultado)] = ValorOriginal
	return 'mandarReferencia'

def cambiarContexto(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global PRetornos
	global cuadruploActual

	PContexto.push(PMemoria.size() - 1)
	if(Resultado != '-'):
		PRetornos.push([int(Resultado), cuadruploActual])
	else:
		PRetornos.push(['-', cuadruploActual])

	cuadruploActual = int(Operador2)

	Operacion = Cuadruplos[cuadruploActual][0]
	Operador1 = Cuadruplos[cuadruploActual][1]
	Operador2 = Cuadruplos[cuadruploActual][2]
	Resultado = Cuadruplos[cuadruploActual][3]
	Operaciones[Operacion](Operador1, Operador2, Resultado)

	return 'cambiarContexto'

def regresarReferencia(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	global cuadruploActual
	contextoActual = PMemoria.top()
	PContexto.pop()
	contextoNuevo = PMemoria.at(PContexto.top())
	PContexto.push(PMemoria.size() - 1)
	
	Operacion = Cuadruplos[cuadruploActual][0]
	Operador1 = Cuadruplos[cuadruploActual][1]
	Operador2 = Cuadruplos[cuadruploActual][2]
	Resultado = Cuadruplos[cuadruploActual][3]
	
	while(Operacion == 'REF_RET'):
		Operador1 = int(Operador1)

		if(DirConstantes.has_key(Operador1)):
			ValorOriginal = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			ValorOriginal = MapaMemoria[contextoActual][Operador1]
		else:
			ValorOriginal = 0

		MapaMemoria[contextoNuevo][int(Resultado)] = ValorOriginal

		cuadruploActual = cuadruploActual + 1
		Operacion = Cuadruplos[cuadruploActual][0]
		Operador1 = Cuadruplos[cuadruploActual][1]
		Resultado = Cuadruplos[cuadruploActual][3]

	if(Operacion != 'ATTR_RET'):
		del MapaMemoria[contextoActual]
		PContexto.pop()
		PMemoria.pop()

	cuadruploActual = cuadruploActual - 1

	return 'regresarAtributo'

def regresarAtributo(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	global cuadruploActual
	contextoActual = PMemoria.top()
	PContexto.pop()
	contextoNuevo = PMemoria.at(PContexto.top())
	PMemoria.pop()

	Operacion = Cuadruplos[cuadruploActual][0]
	Operador1 = Cuadruplos[cuadruploActual][1]
	Operador2 = Cuadruplos[cuadruploActual][2]
	Resultado = Cuadruplos[cuadruploActual][3]
	
	while(Operacion == 'ATTR_RET'):
		Operador1 = int(Operador1)

		if(DirConstantes.has_key(Operador1)):
			ValorOriginal = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			ValorOriginal = MapaMemoria[contextoActual][Operador1]
		else:
			ValorOriginal = 0

		MapaMemoria[contextoNuevo][int(Operador2)] = ValorOriginal

		cuadruploActual = cuadruploActual + 1
		Operacion = Cuadruplos[cuadruploActual][0]
		Operador1 = Cuadruplos[cuadruploActual][1]
		Operador2 = Cuadruplos[cuadruploActual][2]

	cuadruploActual = cuadruploActual - 1

	del MapaMemoria[contextoActual]

	return 'regresarAtributo'

def generarContextoMetodo(Operador1, Operador2, Resultado):
	global MapaMemoria
	global PMemoria
	global cuadruploActual
	diferenciadorMetodos = 0

	Operador1 = Operador1 + str(diferenciadorMetodos)

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

	MapaMemoria[Operador1] = {}

	PMemoria.push(Operador1)

	return 'generarContextoMetodo'

def enviarParametro(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	contextoNuevo = PMemoria.top()
	
	Operador1 = int(Operador1)

	if(DirConstantes.has_key(Operador1)):
		ValorOriginal = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual].has_key(Operador1)):
		ValorOriginal = MapaMemoria[contextoActual][Operador1]
	else:
		ValorOriginal = 0

	MapaMemoria[contextoNuevo][int(Resultado)] = ValorOriginal
	return 'enviarParametro'

def verificaArreglo(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	global numCuadruplos
	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion1 = revisarDireccion(Operador1)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	Operador1 = int(Operador1)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = 0

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = 0

	Operador2 = int(Operador2)

	if(Operador1 < 0 or Operador1 >= Operador2):
		print('\nExecution Error: Index out of bounds')
		exit()

	return 'verificaArreglo'

def concatenarStrings(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = ''

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = ''

	if(TipoDireccion2 != 'Base'):
		if(TipoDireccion2 == 'Indirecto'):
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			else:
				Operador2 = ''

		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		else:
			Operador2 = ''

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = 0

	MapaMemoria[contextoActual][Resultado] = str(Operador1) + str(Operador2)
	return 'concatenarStrings'

def caracterEnPosicion(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccion2 = revisarDireccion(Operador2)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccion2 != 'Directo'):
		Operador2 = str(Operador2)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Operador2 = int(Operador2)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = ''

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = ''

	if(TipoDireccion2 != 'Base'):
		if(TipoDireccion2 == 'Indirecto'):
			if(DirConstantes.has_key(Operador2)):
				Operador2 = DirConstantes[Operador2]
			elif(MapaMemoria[contextoActual].has_key(Operador2)):
				Operador2 = MapaMemoria[contextoActual][Operador2]
			else:
				Operador2 = 0

		if(DirConstantes.has_key(Operador2)):
			Operador2 = DirConstantes[Operador2]
		elif(MapaMemoria[contextoActual].has_key(Operador2)):
			Operador2 = MapaMemoria[contextoActual][Operador2]
		else:
			Operador2 = 0

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = 0

	MapaMemoria[contextoActual][Resultado] = str(Operador1)[Operador2]
	return 'caracterEnPosicion'

def longitudString(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())

	TipoDireccion1 = revisarDireccion(Operador1)
	TipoDireccionR = revisarDireccion(Resultado)
	
	if(TipoDireccion1 != 'Directo'):
		Operador1 = str(Operador1)[1:-1]

	if(TipoDireccionR != 'Directo'):
		Resultado = str(Resultado)[1:-1]

	Operador1 = int(Operador1)
	Resultado = int(Resultado)

	if(TipoDireccion1 != 'Base'):
		if(TipoDireccion1 == 'Indirecto'):
			if(DirConstantes.has_key(Operador1)):
				Operador1 = DirConstantes[Operador1]
			elif(MapaMemoria[contextoActual].has_key(Operador1)):
				Operador1 = MapaMemoria[contextoActual][Operador1]
			else:
				Operador1 = ''

		if(DirConstantes.has_key(Operador1)):
			Operador1 = DirConstantes[Operador1]
		elif(MapaMemoria[contextoActual].has_key(Operador1)):
			Operador1 = MapaMemoria[contextoActual][Operador1]
		else:
			Operador1 = ''

	if(TipoDireccionR != 'Base'):
		if(TipoDireccionR == 'Indirecto'):
			if(DirConstantes.has_key(Resultado)):
				Resultado = DirConstantes[Resultado]
			elif(MapaMemoria[contextoActual].has_key(Resultado)):
				Resultado = MapaMemoria[contextoActual][Resultado]
			else:
				Resultado = 0

	MapaMemoria[contextoActual][Resultado] = len(str(Operador1))
	return 'longitudString'

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

# A file is asked from the user for the vm to execute
s = raw_input('file: ')
if(os.path.isfile(s)):
	with open(s, 'r') as f:
		lineArr = f.readlines()
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
		numCuadruplos = int(lineArr[actual])
		for i in range(actual + 1, actual + numCuadruplos + 1):
			line = lineArr[i][:-1].split('\t')
			Cuadruplos.append([line[1], line[2], line[3], line[4]])
	
	cuadruploActual = 0
	#print(DirConstantes)
	while(cuadruploActual != numCuadruplos):
		#print(cuadruploActual)
		#print(MapaMemoria)
		Operacion = Cuadruplos[cuadruploActual][0]
		Operador1 = Cuadruplos[cuadruploActual][1]
		Operador2 = Cuadruplos[cuadruploActual][2]
		Resultado = Cuadruplos[cuadruploActual][3]
		Operaciones[Operacion](Operador1, Operador2, Resultado)
		cuadruploActual = cuadruploActual + 1
	print('\nExecution finished')
	print('')
	print(MapaMemoria)
	print('')
	print(DirConstantes)
else:
	print("Couldn't open file specified")

