import os.path

DirConstantes = {}

# A file is asked from the user for the vm to execute
s = raw_input('file: ')
if(os.path.isfile(s)):
	with open(s, 'r') as f:
		lineArr = f.readlines()
		numConstantes = int(lineArr[0])
		for i in range(1, numConstantes):
			DirConstantes[ lineArr[i][:-1].split(' ')[1] ] = lineArr[i][:-2].split(' ')[0]
		numCuadruplos = int(lineArr[numConstantes + 1])
		for i in range(numConstantes + 2, numConstantes + numCuadruplos + 2):
			line = lineArr[i][:-1].split('\t')
			Operacion = line[1]
			Operador1 = line[2]
			Operador2 = line[3]
			Resultado = line[4]
			print(Operacion + '\t' + Operador1 + '\t' + Operador2 + '\t' + Resultado)
else:
	print("Couldn't open file specified")