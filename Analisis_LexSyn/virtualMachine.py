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



MapaMemoria = { 'main': { 'main' : {} } }
DirConstantes = {}
Cuadruplos = []

PContexto = stack()
PMemoria = stack()
PContexto.push(0)
PMemoria.push(['main', 'main'])

def suma(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	if(DirConstantes.has_key(Operador1)):
		Operador1 = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador1)):
		Operador1 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador1]
	else:
		Operador1 = 0

	if(DirConstantes.has_key(Operador2)):
		Operador2 = DirConstantes[Operador2]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador2)):
		Operador2 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador2]
	else:
		Operador2 = 0

	MapaMemoria[contextoActual[0]][contextoActual[1]][Resultado] = Operador1 + Operador2
	return 'suma'

def resta(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	if(DirConstantes.has_key(Operador1)):
		Operador1 = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador1)):
		Operador1 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador1]
	else:
		Operador1 = 0

	if(DirConstantes.has_key(Operador2)):
		Operador2 = DirConstantes[Operador2]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador2)):
		Operador2 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador2]
	else:
		Operador2 = 0

	MapaMemoria[contextoActual[0]][contextoActual[1]][Resultado] = Operador1 - Operador2
	return 'resta'

def multiplicacion(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	if(DirConstantes.has_key(Operador1)):
		Operador1 = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador1)):
		Operador1 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador1]
	else:
		Operador1 = 0

	if(DirConstantes.has_key(Operador2)):
		Operador2 = DirConstantes[Operador2]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador2)):
		Operador2 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador2]
	else:
		Operador2 = 0

	MapaMemoria[contextoActual[0]][contextoActual[1]][Resultado] = Operador1 * Operador2
	return 'multiplicacion'

def division(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	if(DirConstantes.has_key(Operador1)):
		Operador1 = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador1)):
		Operador1 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador1]
	else:
		Operador1 = 0

	if(DirConstantes.has_key(Operador2)):
		Operador2 = DirConstantes[Operador2]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador2)):
		Operador2 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador2]
	else:
		Operador2 = 0

	MapaMemoria[contextoActual[0]][contextoActual[1]][Resultado] = Operador1 / Operador2
	return 'division'

def asignacion(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	if(DirConstantes.has_key(Operador1)):
		Operador1 = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador1)):
		Operador1 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador1]
	else:
		Operador1 = 0

	MapaMemoria[contextoActual[0]][contextoActual[1]][Resultado] = Operador1
	return 'asignacion'

def condicionOr(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	if(DirConstantes.has_key(Operador1)):
		Operador1 = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador1)):
		Operador1 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador1]
	else:
		Operador1 = 0

	if(DirConstantes.has_key(Operador2)):
		Operador2 = DirConstantes[Operador2]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador2)):
		Operador2 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador2]
	else:
		Operador2 = 0

	MapaMemoria[contextoActual[0]][contextoActual[1]][Resultado] = Operador1 or Operador2
	return 'condicionOr'

def condicionAnd(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	if(DirConstantes.has_key(Operador1)):
		Operador1 = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador1)):
		Operador1 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador1]
	else:
		Operador1 = 0

	if(DirConstantes.has_key(Operador2)):
		Operador2 = DirConstantes[Operador2]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador2)):
		Operador2 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador2]
	else:
		Operador2 = 0

	MapaMemoria[contextoActual[0]][contextoActual[1]][Resultado] = Operador1 and Operador2
	return 'condicionAnd'

def condicionNot(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	if(DirConstantes.has_key(Operador1)):
		Operador1 = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador1)):
		Operador1 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador1]
	else:
		Operador1 = 0

	MapaMemoria[contextoActual[0]][contextoActual[1]][Resultado] = not(Operador1)
	return 'condicionNot'

def mayorQue(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	if(DirConstantes.has_key(Operador1)):
		Operador1 = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador1)):
		Operador1 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador1]
	else:
		Operador1 = 0

	if(DirConstantes.has_key(Operador2)):
		Operador2 = DirConstantes[Operador2]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador2)):
		Operador2 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador2]
	else:
		Operador2 = 0

	MapaMemoria[contextoActual[0]][contextoActual[1]][Resultado] = Operador1 > Operador2
	return 'mayorQue'

def menorQue(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	if(DirConstantes.has_key(Operador1)):
		Operador1 = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador1)):
		Operador1 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador1]
	else:
		Operador1 = 0

	if(DirConstantes.has_key(Operador2)):
		Operador2 = DirConstantes[Operador2]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador2)):
		Operador2 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador2]
	else:
		Operador2 = 0

	MapaMemoria[contextoActual[0]][contextoActual[1]][Resultado] = Operador1 < Operador2
	return 'menorQue'

def menorIgualQue(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	if(DirConstantes.has_key(Operador1)):
		Operador1 = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador1)):
		Operador1 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador1]
	else:
		Operador1 = 0

	if(DirConstantes.has_key(Operador2)):
		Operador2 = DirConstantes[Operador2]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador2)):
		Operador2 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador2]
	else:
		Operador2 = 0

	MapaMemoria[contextoActual[0]][contextoActual[1]][Resultado] = Operador1 <= Operador2
	return 'menorIgualQue'

def mayorIgualQue(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	if(DirConstantes.has_key(Operador1)):
		Operador1 = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador1)):
		Operador1 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador1]
	else:
		Operador1 = 0

	if(DirConstantes.has_key(Operador2)):
		Operador2 = DirConstantes[Operador2]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador2)):
		Operador2 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador2]
	else:
		Operador2 = 0

	MapaMemoria[contextoActual[0]][contextoActual[1]][Resultado] = Operador1 >= Operador2
	return 'mayorIgualQue'

def igualQue(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	if(DirConstantes.has_key(Operador1)):
		Operador1 = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador1)):
		Operador1 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador1]
	else:
		Operador1 = 0

	if(DirConstantes.has_key(Operador2)):
		Operador2 = DirConstantes[Operador2]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador2)):
		Operador2 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador2]
	else:
		Operador2 = 0

	MapaMemoria[contextoActual[0]][contextoActual[1]][Resultado] = Operador1 == Operador2
	return 'igualQue'

def noIgualQue(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	if(DirConstantes.has_key(Operador1)):
		Operador1 = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador1)):
		Operador1 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador1]
	else:
		Operador1 = 0

	if(DirConstantes.has_key(Operador2)):
		Operador2 = DirConstantes[Operador2]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador2)):
		Operador2 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador2]
	else:
		Operador2 = 0

	MapaMemoria[contextoActual[0]][contextoActual[1]][Resultado] = Operador1 != Operador2
	return 'noIgualQue'

def modulo(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	if(DirConstantes.has_key(Operador1)):
		Operador1 = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador1)):
		Operador1 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador1]
	else:
		Operador1 = 0

	if(DirConstantes.has_key(Operador2)):
		Operador2 = DirConstantes[Operador2]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador2)):
		Operador2 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador2]
	else:
		Operador2 = 0

	MapaMemoria[contextoActual[0]][contextoActual[1]][Resultado] = Operador1 % Operador2
	return 'modulo'

def negacion(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())
	
	if(DirConstantes.has_key(Operador1)):
		Operador1 = DirConstantes[Operador1]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Operador1)):
		Operador1 = MapaMemoria[contextoActual[0]][contextoActual[1]][Operador1]
	else:
		Operador1 = 0

	MapaMemoria[contextoActual[0]][contextoActual[1]][Resultado] = -1 * Operador1
	return 'negacion'

def stdIn(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())

	Resultado = int(Resultado)

	if((Resultado >= 1001 and Resultado < 4001) or (Resultado >= 16001 and Resultado < 19001) or (Resultado >= 31001 and Resultado < 36001)):
		valor = int(raw_input())
	elif((Resultado >= 4001 and Resultado < 7001) or (Resultado >= 19001 and Resultado < 22001) or (Resultado >= 36001 and Resultado < 41001)):
		valor = float(raw_input())
	elif((Resultado >= 10001 and Resultado < 13001) or (Resultado >= 25001 and Resultado < 28001) or (Resultado >= 46001 and Resultado < 51001)):
		valor = raw_input()
		if(valor == 'true'):
			valor = True
		else:
			valor = False
	else:
		valor = raw_input()

	MapaMemoria[contextoActual[0]][contextoActual[1]][Resultado] = valor
	return 'stdIn'

def stdOut(Operador1, Operador2, Resultado):
	global PMemoria
	global PContexto
	global MapaMemoria
	global DirConstantes
	contextoActual = PMemoria.at(PContexto.top())

	Direccion = int(Resultado)
	
	if(DirConstantes.has_key(Resultado)):
		Resultado = DirConstantes[Resultado]
	elif(MapaMemoria[contextoActual[0]][contextoActual[1]].has_key(Resultado)):
		Resultado = MapaMemoria[contextoActual[0]][contextoActual[1]][Resultado]
	else:
		Resultado = 0

	print(str(Resultado))
	return 'stdOut'

def retorno(Operador1, Operador2, Resultado):
	return 'retorno'

def gotoF(Operador1, Operador2, Resultado):
	return 'gotoF'

def goto(Operador1, Operador2, Resultado):
	return 'goto'

def igualacionObjetos(Operador1, Operador2, Resultado):
	return 'igualacionObjetos'

def mandarAtributo(Operador1, Operador2, Resultado):
	return 'mandarAtributo'

def cambiarContexto(Operador1, Operador2, Resultado):
	return 'cambiarContexto'

def regresarAtributo(Operador1, Operador2, Resultado):
	return 'regresarAtributo'

def generarContextoClase(Operador1, Operador2, Resultado):
	return 'generarContextoClase'

def generarContextoMetodo(Operador1, Operador2, Resultado):
	return 'generarContextoMetodo'

def enviarParametro(Operador1, Operador2, Resultado):
	return 'enviarParametro'

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
	'IGUAL-OBJ': igualacionObjetos,
	'ATTR_GO': mandarAtributo,
	'GOSUB': cambiarContexto,
	'ATTR_RET': regresarAtributo,
	'CONTEXTO-CLASE': generarContextoClase,
	'ERA': generarContextoMetodo,
	'PARAM': enviarParametro
}

# A file is asked from the user for the vm to execute
s = raw_input('file: ')
if(os.path.isfile(s)):
	with open(s, 'r') as f:
		lineArr = f.readlines()
		numConstantesEnteras = int(lineArr[0])
		for i in range(1, numConstantesEnteras + 1):
			DirConstantes[ lineArr[i][:-1].split('\t')[1] ] = int(lineArr[i][:-1].split('\t')[0])
		numConstantesReales = int(lineArr[numConstantesEnteras + 1])
		for i in range(numConstantesEnteras + 2, numConstantesEnteras + numConstantesReales + 2):
			DirConstantes[ lineArr[i][:-1].split('\t')[1] ] = float(lineArr[i][:-1].split('\t')[0])
		actual = numConstantesEnteras + numConstantesReales + 2
		numConstantesString = int(lineArr[actual])
		for i in range(actual + 1, actual + numConstantesString + 1):
			DirConstantes[ lineArr[i][:-1].split('\t')[1] ] = lineArr[i][:-1].split('\t')[0][1:-1]
		actual = actual + numConstantesString + 1
		numConstantesBool = int(lineArr[actual])
		for i in range(actual + 1, actual + numConstantesBool + 1):
			if(lineArr[i][:-1].split('\t')[0] == 'true'):
				DirConstantes[ lineArr[i][:-1].split('\t')[1] ] = True
			else:
				DirConstantes[ lineArr[i][:-1].split('\t')[1] ] = False
		actual = actual + numConstantesBool + 1
		numConstantesChar = int(lineArr[actual])
		for i in range(actual + 1, actual + numConstantesChar + 1):
			DirConstantes[ lineArr[i][:-1].split('\t')[1] ] = lineArr[i][:-1].split('\t')[0][1:-1]
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
	print
	print(MapaMemoria)
	print
	print(DirConstantes)
else:
	print("Couldn't open file specified")

