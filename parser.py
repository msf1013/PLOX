import ply.yacc as yacc
import os.path
import scanner
tokens = scanner.tokens

# Global variable to store where the syntax error was trigger
error = "'Program declaration'"

def p_programa(p):
	'programa : ciclo_clase clase_main'
	print('Compilation successful!')

def p_ciclo_clase(p):
	'''ciclo_clase 	: empty
					| ciclo_clase clase'''
	print('ciclo_clase')	

def p_clase(p):
	'''clase : CLASS ID herencia LLIZQ ciclo_vars ciclo_func LLDER'''
	print('clase')

def p_ciclo_vars(p):
	'''ciclo_vars 	: empty
					| ciclo_vars acceso vars'''
	print('ciclo_vars')

def p_ciclo_func(p):
	'''ciclo_func 	: empty
					| ciclo_func func'''
	print('ciclo_func')

def p_clase_main(p):
	'''clase_main 	: CLASS MAIN LLIZQ ciclo_vars ciclo_func main LLDER'''
	print('clase_main')

def p_vars(p):
	'''vars : var_op PYC'''
	print('vars')

def p_var_op(p):
	'''var_op 	: tipo ciclo_tipo
				| ID ciclo_id'''
	print('var_op')

def p_ciclo_tipo(p):
	'''ciclo_tipo 	: ID arreglo asignacion_exp
					| ciclo_id COMA ID arreglo asignacion_exp'''
	print('ciclo_tipo')

def p_ciclo_id(p):
	'''ciclo_id 	: ID arreglo asignacion_obj
					| ciclo_id COMA ID arreglo asignacion_obj'''
	print('ciclo_id')

def p_arreglo(p):
	'''arreglo 		: empty
					| CODER exp_arit COIZQ'''
	print('arreglo')

def p_asignacion_exp(p):
	'''asignacion_exp	: empty
						| IGUAL exp'''
	print('asignacion_exp')

def p_asignacion_obj(p):
	'''asignacion_obj	: empty
						| IGUAL exp_objeto'''
	print('asignacion_obj')

def p_tipo(p):
	'''tipo 	: NUMERAL
				| REAL
				| BOOL
				| CHAR
				| STRING'''
	print('tipo')

def p_acceso(p):
	'''acceso 	: empty
				| HIDDEN
				| VISIBLE'''
	print('acceso')

def p_func(p):
	'''func 	: acceso retorno ID params cuerpo_func'''
	print('func')

def p_retorno(p):
	'''retorno 	: tipo
				| WITHOUT'''
	print('retorno')

def p_main(p):
	'''main 	: VISIBLE WITHOUT MAIN PIZQ PDER cuerpo_func'''
	print('main')

def p_params(p):
	'''params 	: PIZQ params_op PDER'''
	print('params')

def p_params_op(p):
	'''params_op: empty
				| params_ciclo'''
	print('params_op')

def p_params_ciclo(p):
	'''params_ciclo 	: tipo ID
						| params_ciclo COMA tipo id'''
	print('params_ciclo')

def p_cuerpo_func(p):
	'''cuerpo_func 	: LLIZQ vars ciclo_estatuto LLDER'''
	print('cuerpo_func')

def p_ciclo_estatuto(p):
	'''ciclo_estatuto 	: empty
						| ciclo_estatuto estatuto'''
	print('ciclo_estatuto')

def p_estatuto(p):
	'''estatuto 	: while
					| for
					| asignacion
					| condicion
					| escritura
					| lectura
					| llamada_func
					| return'''
	print('estatuto')

def p_llamada_func(p):
	'''llamada_func : caller ID PIZQ exp_op PDER PYC'''
	print('llamada_func')

def p_caller(p):
	'''caller 	: empty
				| THIS PUNTO
				| ID arreglo PUNTO'''
	print('caller')

def p_exp_op(p):
	'''exp_op 	: empty
				| exp_ciclo'''
	print('exp_op')

def p_exp_ciclo(p):
	'''exp_ciclo 	: exp
					| exp_ciclo COMA exp'''
	print('exp_ciclo')

def p_cte_bool(p):
	'''cte_bool 	: TRUE
					| FALSE'''
	print('cte_bool')

def p_exp(p):
	'''exp 	: exp_bool
			| exp_arit
			| exp_str
			| exp_objeto'''
	print('exp')

def p_exp_objeto(p):
	'''exp_objeto 	: atom
					| NEW ID PIZQ PDER'''
	print('exp_objeto')

def p_return(p):
	'''return 	: RETURN exp PYC'''
	print('return')

def p_while(p):
	'''while 	: WHILE PIZQ exp_bool PDER LLIZQ ciclo_estatuto LLDER'''
	print('while')

def p_exp_bool(p):
	'''exp_bool : termino_bool
				| exp_bool OR termino_bool'''
	print('exp_bool')

def p_termino_bool(p):
	'''termino_bool 	: exp_b
						| termino_bool AND exp_b'''
	print('termino_bool')

def p_exp_b(p):
	'''exp_b 	: negacion op_exp_b'''
	print('exp_b')

def p_negacion(p):
	'''negacion : empty
				| NOT'''
	print('negacion')

def p_op_exp_b(p):
	'''op_exp_b : llamada_func
				| PIZQ exp_bool PDER'''
	print('op_exp_b')

def p_comparacion(p):
	'''comparacion 	: exp_arit op_comp exp_arit
					| exp_str IGUALC exp_str'''
	print('comparacion')

def p_exp_arit(p):
	'''exp_arit 	: termino
					| exp_arit MAS termino
					| exp_arit MENOS termino'''
	print('exp_arit')

def p_termino(p):
	'''termino  : factor
				| termino POR factor
				| termino ENTRE factor'''
	print('termino')

def p_factor(p):
	'''factor 	: PIZQ exp_arit PDER
				| factor_oper_op factor_cte_op'''
	print('factor')

def p_factor_oper_op(p):
	'''factor_oper_op 	: empty
						| MENOS
						| MAS'''
	print('factor_oper_op')

def p_factor_cte_op(p):
	'''factor_cte_op 	: CTE_NUMERAL
						| CTE_REAL
						| atom
						| llamada_func'''
	print('factor_cte_op')

def p_for(p):
	'''for 	: FOR PIZQ asignacion exp_bool PYC atom IGUAL exp PDER LLIZQ ciclo_estatuto LLDER'''
	print('for')

def p_exp_str(p):
	'''exp_str 	: CONST_STR
				| CONST_CHAR
				| atom
				| llamada_func'''
	print('exp_str')

def p_asignacion(p):
	'''asignacion 	: atom IGUAL exp PYC'''
	print('asignacion')

def p_atom(p):
	'''atom : ID arreglo atributo_arr
			| ID arreglo
			| THIS atributo_arr'''
	print('atom')

def p_atributo_arr(p):
	'''atributo_arr 	: PUNTO ID arreglo'''
	print('atributo_arr')

def p_condicion(p):
	'''condicion 	: ciclo_cond ELSE LLIZQ ciclo_estatuto LLDER'''
	print('condicion')

def p_ciclo_cond(p):
	'''ciclo_cond 	: IF PIZQ exp_bool PDER LLIZQ ciclo_estatuto LLDER
					| ciclo_cond ELSE IF PIZQ exp_bool PDER LLIZQ ciclo_estatuto LLDER'''
	print('ciclo_cond')

def p_lectura(p):
	'''lectura 	: INPUT PIZQ atom PDER PYC'''
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