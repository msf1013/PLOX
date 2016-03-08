#!/usr/bin/python

# Humberto Makoto Morimoto Burgos
# Mat. A01280458

# Implementacion de la clase 'map'.
class map:
	# Metodo constructor que inicializa el map vacio.
	def __init__(self):
		self.map = {}

	# Metodo que liga el elemento dado a la llave dada, agregando un nuevo,
	# par al map si no existia previamente.
	def set(self, key, value):
		self.map[key] = value

	# Metodo que borra una llave y su elemento correspondiente del map.
	def delete(self, key):
		del self.map[key]

	# Metodo que regresa el valor ligado a la llave dada.
	def get(self, key):
		return self.map[key]

	# Metodo que borra todas las entradas del map.
	def clear(self):
		self.map.clear()

	# Metodo que regresa si el map esta vacio o no.
	def empty(self):
		return (len(self.map) == 0)

	# Metodo que regresa el tamanio del map (dado por el numero de llaves).
	def size(self):
		return len(self.map)

	# Metodo que regresa si el diccionario tiene o no una llave.
	def hasKey(self, key):
		return self.map.has_key(key)

	# Metodo que despliega en consola los contenidos del diccionario.
	def display(self):
		items = self.map.items()
		for item in items:
			print item[0], ": ", item[1]