from Mapa import map

#mapX = map()
#mapX.set("chefe", "a loco")
#print mapX.get("chefe")

# Tabla de variables de METODO main

TablaVarsM = map()
TablaVarsM.set('x', {'type': 'numeral'})
TablaVarsM.set('r', {'type': 'real'})
TablaVarsM.set('per', {'type': 'Persona'})

# Tabla de variables de METODO loco

TablaVarsL = map()
TablaVarsL.set('equis', {'type': 'Persona'})
TablaVarsL.set('olo', {'type': 'bool'})
TablaVarsL.set('chefe', {'type': 'string'})

# Tabla de variables de CLASE main

TablaVars = map()
TablaVars.set('ch', {'type': 'char'})
TablaVars.set('str', {'type': 'string'})
TablaVars.set('b', {'type': 'bool'})

# Directorio de metodos

DirMetodos = map()
DirMetodos.set('main', TablaVarsM)
DirMetodos.set('loco', TablaVarsL)

# Directorio de clases

DirClases = map()
DirClases.set('main', {'variables':TablaVars, 'metodos':DirMetodos})


# DirClases.get('main').get('variables')
print TablaVarsL == DirClases.get('main').get('metodos').get('loco')

print DirClases.get('main').get('metodos').get('loco').get('equis').get('type')