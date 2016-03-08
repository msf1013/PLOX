from Mapa import map

#mapX = map()
#mapX.set("chefe", "a loco")
#print mapX.get("chefe")

# Tabla de variables de METODO main

TablaVarsM = {}
TablaVarsM['x'] = {'type': 'numeral'}
TablaVarsM['r'] = {'type': 'real'}
TablaVarsM['per'] = {'type': 'Persona'}

# Tabla de variables de METODO loco

TablaVarsL = {}
TablaVarsL['equis'] = {'type': 'Persona'}
TablaVarsL['olo'] = {'type': 'bool'}
TablaVarsL['chefe'] = {'type': 'string'}

# Tabla de variables de CLASE main

TablaVars = {}
TablaVars['ch'] = {'type': 'char'}
TablaVars['str'] = {'type': 'string'}
TablaVars['b'] = {'type': 'bool'}

# Directorio de metodos

DirMetodos = {}
DirMetodos['main'] = TablaVarsM
DirMetodos['loco'] = TablaVarsL

# Directorio de clases

DirClases = {}
DirClases['main'] = {'variables':TablaVars, 'metodos':DirMetodos}


# DirClases.get('main').get('variables')
print TablaVarsL == DirClases['main']['metodos']['loco']

print DirClases['main']['metodos']['loco']['equis']['type']