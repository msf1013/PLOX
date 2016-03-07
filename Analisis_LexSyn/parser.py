import ply.yacc as yacc
import os.path
import scanner
tokens = scanner.tokens

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
	'''clase : CLASS ID herencia LLIZQ ciclo_vars ciclo_func LLDER
			 | CLASS ID herencia LLIZQ ciclo_vars LLDER
			 | CLASS ID herencia LLIZQ ciclo_func LLDER
			 | CLASS ID herencia LLIZQ LLDER'''
	print('clase')

def p_herencia(p):
	'''herencia : empty
				| UNDER ID'''
	print('herencia')

def p_ciclo_vars(p):
	'''ciclo_vars 	: HIDDEN vars
					| VISIBLE vars
					| vars
					| ciclo_vars HIDDEN vars
					| ciclo_vars VISIBLE vars
					| ciclo_vars vars'''
	print('ciclo_vars')

def p_ciclo_func(p):
	'''ciclo_func 	: func
					| ciclo_func func'''
	print('ciclo_func')

def p_clase_main(p):
	'''clase_main 	: CLASS MAIN LLIZQ ciclo_vars ciclo_func main LLDER
					| CLASS MAIN LLIZQ ciclo_vars main LLDER
					| CLASS MAIN LLIZQ ciclo_func main LLDER
					| CLASS MAIN LLIZQ main LLDER'''
	print('clase_main')

def p_vars(p):
	'''vars : var_op PYC'''
	print('vars')

def p_var_op(p):
	'''var_op 	: numeral_decl arreglo ciclo_arit
				| real_decl arreglo ciclo_arit
				| bool_decl arreglo ciclo_bool
				| char_decl arreglo ciclo_str
				| string_decl arreglo ciclo_str
				| numeral_decl arreglo IGUAL exp_arit ciclo_arit
				| real_decl arreglo IGUAL exp_arit ciclo_arit
				| numeral_decl arreglo IGUAL atom ciclo_arit
				| real_decl arreglo IGUAL atom ciclo_arit
				| numeral_decl arreglo IGUAL llamada_func ciclo_arit
				| real_decl arreglo IGUAL llamada_func ciclo_arit
				| bool_decl arreglo IGUAL exp_bool ciclo_bool
				| bool_decl arreglo IGUAL atom ciclo_bool
				| bool_decl arreglo IGUAL llamada_func ciclo_bool
				| char_decl arreglo IGUAL exp_str ciclo_str
				| string_decl arreglo IGUAL exp_str ciclo_str
				| char_decl arreglo IGUAL atom ciclo_str
				| char_decl arreglo IGUAL llamada_func ciclo_str
				| string_decl arreglo IGUAL atom ciclo_str
				| string_decl arreglo IGUAL llamada_func ciclo_str
				| obj_decl arreglo ciclo_obj
				| obj_decl arreglo IGUAL exp_objeto ciclo_obj
				| obj_decl arreglo IGUAL atom ciclo_obj
				| obj_decl arreglo IGUAL llamada_func ciclo_obj'''
	print('var_op')

def p_ciclo_arit(p):
	'''ciclo_arit 	: empty
					| ciclo_arit COMA ID arreglo
					| ciclo_arit COMA ID arreglo IGUAL exp_arit
					| ciclo_arit COMA ID arreglo IGUAL atom
					| ciclo_arit COMA ID arreglo IGUAL llamada_func'''

def p_ciclo_bool(p):
	'''ciclo_bool 	: empty
					| ciclo_bool COMA ID arreglo
					| ciclo_bool COMA ID arreglo IGUAL exp_bool
					| ciclo_bool COMA ID arreglo IGUAL atom
					| ciclo_bool COMA ID arreglo IGUAL llamada_func'''

def p_ciclo_str(p):
	'''ciclo_str 	: empty
					| ciclo_str COMA ID arreglo
					| ciclo_str COMA ID arreglo IGUAL exp_str
					| ciclo_str COMA ID arreglo IGUAL atom
					| ciclo_str COMA ID arreglo IGUAL llamada_func'''

def p_ciclo_obj(p):
	'''ciclo_obj 	: empty
					| ciclo_obj COMA ID arreglo
					| ciclo_obj COMA ID arreglo IGUAL exp_str
					| ciclo_obj COMA ID arreglo IGUAL atom
					| ciclo_obj COMA ID arreglo IGUAL llamada_func'''

def p_string_decl(p):
	'''string_decl 	: STRING ID'''

def p_numeral_decl(p):
	'''numeral_decl : NUMERAL ID'''

def p_real_decl(p):
	'''real_decl : REAL ID'''

def p_bool_decl(p):
	'''bool_decl : BOOL ID'''

def p_char_decl(p):
	'''char_decl : CHAR ID'''

def p_obj_decl(p):
	'''obj_decl : ID ID'''

def p_arreglo(p):
	'''arreglo 		: empty
					| COIZQ exp_arit CODER
					| COIZQ atom CODER
					| COIZQ llamada_func CODER'''
	print('arreglo')

def p_func(p):
	'''func 	: HIDDEN WITHOUT ID params cuerpo_func
				| HIDDEN numeral_decl params cuerpo_func_arit
				| HIDDEN real_decl params cuerpo_func_arit
				| HIDDEN bool_decl params cuerpo_func_bool
				| HIDDEN char_decl params cuerpo_func_str
				| HIDDEN string_decl params cuerpo_func_str
				| VISIBLE WITHOUT ID params cuerpo_func
				| VISIBLE numeral_decl params cuerpo_func_arit
				| VISIBLE real_decl params cuerpo_func_arit
				| VISIBLE bool_decl params cuerpo_func_bool
				| VISIBLE char_decl params cuerpo_func_str
				| VISIBLE string_decl params cuerpo_func_str'''
	print('func')

def p_main(p):
	'''main 	: VISIBLE WITHOUT MAIN PIZQ PDER cuerpo_func'''
	print('main')

def p_params(p):
	'''params 	: PIZQ params_ciclo PDER
				| PIZQ PDER'''
	print('params')

#def p_params_op(p):
#	'''params_op : empty
#				| params_ciclo'''
#	print('params_op')

def p_params_ciclo(p):
	'''params_ciclo 	: numeral_decl
						| real_decl
						| char_decl
						| string_decl
						| bool_decl
						| obj_decl
						| params_ciclo COMA numeral_decl
						| params_ciclo COMA real_decl
						| params_ciclo COMA char_decl
						| params_ciclo COMA bool_decl
						| params_ciclo COMA string_decl
						| params_ciclo COMA obj_decl'''
	print('params_ciclo')

def p_cuerpo_func(p):
	'''cuerpo_func 	: LLIZQ ciclo_vars ciclo_estatuto LLDER
					| LLIZQ ciclo_vars LLDER
					| LLIZQ ciclo_estatuto LLDER
					| LLIZQ LLDER'''
	print('cuerpo_func')

def p_cuerpo_func_arit(p):
	'''cuerpo_func_arit 	: LLIZQ ciclo_vars ciclo_estatuto_arit LLDER
							| LLIZQ ciclo_vars LLDER
							| LLIZQ ciclo_estatuto_arit LLDER
							| LLIZQ LLDER'''
	print('cuerpo_func_arit')

def p_cuerpo_func_bool(p):
	'''cuerpo_func_bool 	: LLIZQ ciclo_vars ciclo_estatuto_bool LLDER
							| LLIZQ ciclo_vars LLDER
							| LLIZQ ciclo_estatuto_bool LLDER
							| LLIZQ LLDER'''
	print('cuerpo_func_bool')

def p_cuerpo_func_str(p):
	'''cuerpo_func_str 	: LLIZQ ciclo_vars ciclo_estatuto_str LLDER
						| LLIZQ ciclo_vars LLDER
						| LLIZQ ciclo_estatuto_str LLDER
						| LLIZQ LLDER'''
	print('cuerpo_func_str')

def p_ciclo_estatuto(p):
	'''ciclo_estatuto 	: estatuto
						| ciclo_estatuto estatuto'''
	print('ciclo_estatuto')

def p_ciclo_estatuto_arit(p):
	'''ciclo_estatuto_arit 	: estatuto_arit
							| ciclo_estatuto_arit estatuto_arit'''
	print('ciclo_estatuto_arit')

def p_ciclo_estatuto_bool(p):
	'''ciclo_estatuto_bool 	: estatuto_bool
							| ciclo_estatuto_bool estatuto_bool'''
	print('ciclo_estatuto_bool')

def p_ciclo_estatuto_str(p):
	'''ciclo_estatuto_str 	: estatuto_str
							| ciclo_estatuto_str estatuto_str'''
	print('ciclo_estatuto_str')

def p_estatuto(p):
	'''estatuto 	: while
					| asignacion
					| condicion
					| escritura
					| lectura
					| llamada_func PYC
					| RETURN PYC'''
	print('estatuto')

def p_estatuto_arit(p):
	'''estatuto_arit 	: while_arit
						| asignacion
						| condicion_arit
						| escritura
						| lectura
						| llamada_func PYC
						| RETURN exp_arit PYC
						| RETURN atom PYC
						| RETURN llamada_func PYC'''
	print('estatuto_arit')

def p_estatuto_bool(p):
	'''estatuto_bool 	: while_bool
						| asignacion
						| condicion_bool
						| escritura
						| lectura
						| llamada_func PYC
						| RETURN exp_bool PYC
						| RETURN atom PYC
						| RETURN llamada_func PYC'''
	print('estatuto_bool')

def p_estatuto_str(p):
	'''estatuto_str 	: while_str
						| asignacion
						| condicion_str
						| escritura
						| lectura
						| llamada_func PYC
						| RETURN exp_str PYC
						| RETURN atom PYC
						| RETURN llamada_func PYC'''
	print('estatuto_str')

def p_llamada_func(p):
	'''llamada_func : ID PIZQ exp_ciclo PDER
					| THIS PUNTO ID PIZQ exp_ciclo PDER
					| ID arreglo PUNTO ID PIZQ exp_ciclo PDER
					| ID PIZQ PDER
					| THIS PUNTO ID PIZQ PDER
					| ID arreglo PUNTO ID PIZQ PDER'''
	print('llamada_func')

#def p_caller(p):
#	'''caller 	: empty
#				| THIS PUNTO
#				| ID arreglo PUNTO'''
#	print('caller')

#def p_exp_op(p):
#	'''exp_op 	: empty
#				| exp_ciclo'''
#	print('exp_op')

def p_exp_ciclo(p):
	'''exp_ciclo 	: exp_bool
					| exp_str
					| exp_arit
					| exp_objeto
					| atom
					| llamada_func
					| exp_ciclo COMA exp_bool
					| exp_ciclo COMA exp_str
					| exp_ciclo COMA exp_arit
					| exp_ciclo COMA exp_objeto
					| exp_ciclo COMA atom
					| exp_ciclo COMA llamada_func'''
	print('exp_ciclo')

def p_cte_bool(p):
	'''cte_bool 	: TRUE
					| FALSE'''
	print('cte_bool')

def p_exp_objeto(p):
	'''exp_objeto 	: NEW ID PIZQ PDER'''
	print('exp_objeto')

def p_while(p):
	'''while 	: WHILE PIZQ exp_bool PDER LLIZQ ciclo_estatuto LLDER
				| WHILE PIZQ exp_bool PDER LLIZQ LLDER
				| WHILE PIZQ atom PDER LLIZQ ciclo_estatuto LLDER
				| WHILE PIZQ llamada_func PDER LLIZQ ciclo_estatuto LLDER
				| WHILE PIZQ atom PDER LLIZQ LLDER
				| WHILE PIZQ llamada_func PDER LLIZQ LLDER'''
	print('while')

def p_while_arit(p):
	'''while_arit 	: WHILE PIZQ exp_bool PDER LLIZQ ciclo_estatuto_arit LLDER
					| WHILE PIZQ exp_bool PDER LLIZQ LLDER
					| WHILE PIZQ atom PDER LLIZQ ciclo_estatuto_arit LLDER
					| WHILE PIZQ llamada_func PDER LLIZQ ciclo_estatuto_arit LLDER
					| WHILE PIZQ atom PDER LLIZQ LLDER
					| WHILE PIZQ llamada_func PDER LLIZQ LLDER'''
	print('while_arit')

def p_while_bool(p):
	'''while_bool 	: WHILE PIZQ exp_bool PDER LLIZQ ciclo_estatuto_bool LLDER
					| WHILE PIZQ exp_bool PDER LLIZQ LLDER
					| WHILE PIZQ atom PDER LLIZQ ciclo_estatuto_bool LLDER
					| WHILE PIZQ llamada_func PDER LLIZQ ciclo_estatuto_bool LLDER
					| WHILE PIZQ atom PDER LLIZQ LLDER
					| WHILE PIZQ llamada_func PDER LLIZQ LLDER'''
	print('while_bool')

def p_while_str(p):
	'''while_str 	: WHILE PIZQ exp_bool PDER LLIZQ ciclo_estatuto_str LLDER
					| WHILE PIZQ exp_bool PDER LLIZQ LLDER
					| WHILE PIZQ atom PDER LLIZQ ciclo_estatuto_str LLDER
					| WHILE PIZQ llamada_func PDER LLIZQ ciclo_estatuto_str LLDER
					| WHILE PIZQ atom PDER LLIZQ LLDER
					| WHILE PIZQ llamada_func PDER LLIZQ LLDER'''
	print('while_str')

def p_exp_bool(p):
	'''exp_bool : termino_bool
				| exp_bool OR termino_bool
				| exp_bool OR atom
				| exp_bool OR PIZQ atom PDER
				| exp_bool OR NOT atom
				| exp_bool OR PIZQ NOT atom PDER
				| exp_bool OR llamada_func
				| exp_bool OR PIZQ llamada_func PDER
				| exp_bool OR NOT llamada_func
				| exp_bool OR PIZQ NOT llamada_func PDER
				| atom OR termino_bool
				| PIZQ atom PDER OR termino_bool
				| NOT atom OR termino_bool
				| PIZQ NOT atom PDER OR termino_bool
				| llamada_func OR termino_bool
				| PIZQ llamada_func PDER OR termino_bool
				| NOT llamada_func OR termino_bool
				| PIZQ NOT llamada_func PDER OR termino_bool'''
	print('exp_bool')

def p_termino_bool(p):
	'''termino_bool 	: op_exp_b
						| NOT op_exp_b
						| termino_bool AND op_exp_b
						| termino_bool AND atom
						| termino_bool AND PIZQ atom PDER
						| termino_bool AND NOT atom
						| termino_bool AND PIZQ NOT atom PDER
						| termino_bool AND llamada_func
						| termino_bool AND PIZQ llamada_func PDER
						| termino_bool AND NOT llamada_func
						| termino_bool AND PIZQ NOT llamada_func PDER
						| atom AND op_exp_b
						| PIZQ atom PDER AND op_exp_b
						| NOT atom AND op_exp_b
						| PIZQ NOT atom PDER AND op_exp_b
						| llamada_func AND op_exp_b
						| PIZQ llamada_func PDER AND op_exp_b
						| NOT llamada_func AND op_exp_b
						| PIZQ NOT llamada_func PDER AND op_exp_b'''
	print('termino_bool')

def p_op_exp_b(p):
	'''op_exp_b : cte_bool
				| comparacion
				| PIZQ exp_bool PDER'''
	print('op_exp_b')

def p_comparacion(p):
	'''comparacion 	: exp_arit op_comp exp_arit
					| atom op_comp atom
					| llamada_func op_comp llamada_func
					| atom op_comp exp_arit
					| exp_arit op_comp atom
					| atom op_comp llamada_func
					| llamada_func op_comp atom
					| llamada_func op_comp exp_arit
					| exp_arit op_comp llamada_func
					| exp_str IGUALC exp_str
					| exp_str IGUALC atom
					| atom IGUALC exp_str
					| llamada_func IGUALC exp_str
					| exp_str IGUALC llamada_func'''
	print('comparacion')

def p_op_comp(p):
	'''op_comp 	: MAYOR
				| MENOR
				| IGUALC
				| NOTIGUAL
				| MENORIGUAL
				| MAYORIGUAL'''
	print('op_comp')

def p_exp_arit(p):
	'''exp_arit 	: termino
					| exp_arit MAS termino
					| exp_arit MENOS termino
					| exp_arit MAS atom
					| exp_arit MAS MAS atom
					| exp_arit MAS MENOS atom
					| exp_arit MENOS atom
					| exp_arit MENOS MAS atom
					| exp_arit MENOS MENOS atom
					| exp_arit MAS llamada_func
					| exp_arit MAS MENOS llamada_func
					| exp_arit MAS MAS llamada_func
					| exp_arit MENOS llamada_func
					| exp_arit MENOS MENOS llamada_func
					| exp_arit MENOS MAS llamada_func
					| atom MAS termino
					| MAS atom MAS termino
					| MENOS atom MAS termino
					| llamada_func MAS termino
					| MAS llamada_func MAS termino
					| MENOS llamada_func MAS termino
					| atom MENOS termino
					| MAS atom MENOS termino
					| MENOS atom MENOS termino
					| llamada_func MENOS termino
					| MAS llamada_func MENOS termino
					| MENOS llamada_func MENOS termino'''
	print('exp_arit')

def p_termino(p):
	'''termino  : factor
				| termino POR factor
				| termino ENTRE factor
				| termino MOD factor
				| termino POR atom
				| termino POR MAS atom
				| termino POR MENOS atom
				| termino ENTRE atom
				| termino ENTRE MAS atom
				| termino ENTRE MENOS atom
				| termino MOD atom
				| termino MOD MENOS atom
				| termino MOD MAS atom
				| termino POR llamada_func
				| termino POR MAS llamada_func
				| termino POR MENOS llamada_func
				| termino ENTRE llamada_func
				| termino ENTRE MAS llamada_func
				| termino ENTRE MENOS llamada_func
				| termino MOD llamada_func
				| termino MOD MAS llamada_func
				| termino MOD MENOS llamada_func
				| atom POR factor
				| atom ENTRE factor
				| atom MOD factor
				| MAS atom POR factor
				| MAS atom ENTRE factor
				| MAS atom MOD factor
				| MENOS atom POR factor
				| MENOS atom ENTRE factor
				| MENOS atom MOD factor
				| llamada_func POR factor
				| llamada_func ENTRE factor
				| llamada_func MOD factor
				| MAS llamada_func POR factor
				| MAS llamada_func ENTRE factor
				| MAS llamada_func MOD factor
				| MENOS llamada_func POR factor
				| MENOS llamada_func ENTRE factor
				| MENOS llamada_func MOD factor'''
	print('termino')

def p_factor(p):
	'''factor 	: PIZQ exp_arit PDER
				| MENOS PIZQ exp_arit PDER
				| MAS PIZQ exp_arit PDER
				| PIZQ atom PDER
				| PIZQ MAS atom PDER
				| PIZQ MENOS atom PDER
				| PIZQ llamada_func PDER
				| PIZQ MAS llamada_func PDER
				| PIZQ MENOS llamada_func PDER
				| factor_oper_op factor_cte_op'''
	print('factor')

def p_factor_oper_op(p):
	'''factor_oper_op 	: empty
						| MENOS
						| MAS'''
	print('factor_oper_op')

def p_factor_cte_op(p):
	'''factor_cte_op 	: CTE_NUMERAL
						| CTE_REAL'''
	print('factor_cte_op')

def p_exp_str(p):
	'''exp_str 	: CTE_STR
				| CTE_CHAR'''
	print('exp_str')

def p_asignacion(p):
	'''asignacion 	: atom IGUAL exp_arit PYC
					| atom IGUAL exp_str PYC
					| atom IGUAL exp_bool PYC
					| atom IGUAL exp_objeto PYC
					| atom IGUAL atom PYC
					| atom IGUAL llamada_func PYC'''
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
	'''condicion 	: ciclo_cond ELSE LLIZQ ciclo_estatuto LLDER
					| ciclo_cond ELSE LLIZQ LLDER'''
	print('condicion')

def p_condicion_arit(p):
	'''condicion_arit 	: ciclo_cond_arit ELSE LLIZQ ciclo_estatuto_arit LLDER
						| ciclo_cond_arit ELSE LLIZQ LLDER'''
	print('condicion_arit')

def p_condicion_bool(p):
	'''condicion_bool 	: ciclo_cond_bool ELSE LLIZQ ciclo_estatuto_bool LLDER
						| ciclo_cond_bool ELSE LLIZQ LLDER'''
	print('condicion_bool')

def p_condicion_str(p):
	'''condicion_str 	: ciclo_cond_str ELSE LLIZQ ciclo_estatuto_str LLDER
						| ciclo_cond_str ELSE LLIZQ LLDER'''
	print('condicion_str')

def p_ciclo_cond(p):
	'''ciclo_cond 	: IF PIZQ exp_bool PDER LLIZQ ciclo_estatuto LLDER
					| IF PIZQ exp_bool PDER LLIZQ LLDER
					| IF PIZQ atom PDER LLIZQ ciclo_estatuto LLDER
					| IF PIZQ atom PDER LLIZQ LLDER
					| IF PIZQ llamada_func PDER LLIZQ ciclo_estatuto LLDER
					| IF PIZQ llamada_func PDER LLIZQ LLDER
					| ciclo_cond ELSE IF PIZQ exp_bool PDER LLIZQ ciclo_estatuto LLDER
					| ciclo_cond ELSE IF PIZQ exp_bool PDER LLIZQ LLDER
					| ciclo_cond ELSE IF PIZQ atom PDER LLIZQ ciclo_estatuto LLDER
					| ciclo_cond ELSE IF PIZQ atom PDER LLIZQ LLDER
					| ciclo_cond ELSE IF PIZQ llamada_func PDER LLIZQ ciclo_estatuto LLDER
					| ciclo_cond ELSE IF PIZQ llamada_func PDER LLIZQ LLDER'''
	print('ciclo_cond')

def p_ciclo_cond_arit(p):
	'''ciclo_cond_arit 	: IF PIZQ exp_bool PDER LLIZQ ciclo_estatuto_arit LLDER
						| IF PIZQ exp_bool PDER LLIZQ LLDER
						| IF PIZQ atom PDER LLIZQ ciclo_estatuto_arit LLDER
						| IF PIZQ atom PDER LLIZQ LLDER
						| IF PIZQ llamada_func PDER LLIZQ ciclo_estatuto_arit LLDER
						| IF PIZQ llamada_func PDER LLIZQ LLDER
						| ciclo_cond_arit ELSE IF PIZQ exp_bool PDER LLIZQ ciclo_estatuto_arit LLDER
						| ciclo_cond_arit ELSE IF PIZQ exp_bool PDER LLIZQ LLDER
						| ciclo_cond_arit ELSE IF PIZQ atom PDER LLIZQ ciclo_estatuto_arit LLDER
						| ciclo_cond_arit ELSE IF PIZQ atom PDER LLIZQ LLDER
						| ciclo_cond_arit ELSE IF PIZQ llamada_func PDER LLIZQ ciclo_estatuto_arit LLDER
						| ciclo_cond_arit ELSE IF PIZQ llamada_func PDER LLIZQ LLDER'''
	print('ciclo_cond_arit')

def p_ciclo_cond_str(p):
	'''ciclo_cond_str 	: IF PIZQ exp_bool PDER LLIZQ ciclo_estatuto_str LLDER
						| IF PIZQ exp_bool PDER LLIZQ LLDER
						| IF PIZQ atom PDER LLIZQ ciclo_estatuto_str LLDER
						| IF PIZQ atom PDER LLIZQ LLDER
						| IF PIZQ llamada_func PDER LLIZQ ciclo_estatuto_str LLDER
						| IF PIZQ llamada_func PDER LLIZQ LLDER
						| ciclo_cond_str ELSE IF PIZQ exp_bool PDER LLIZQ ciclo_estatuto_str LLDER
						| ciclo_cond_str ELSE IF PIZQ exp_bool PDER LLIZQ LLDER
						| ciclo_cond_str ELSE IF PIZQ atom PDER LLIZQ ciclo_estatuto_str LLDER
						| ciclo_cond_str ELSE IF PIZQ atom PDER LLIZQ LLDER
						| ciclo_cond_str ELSE IF PIZQ llamada_func PDER LLIZQ ciclo_estatuto_str LLDER
						| ciclo_cond_str ELSE IF PIZQ llamada_func PDER LLIZQ LLDER'''
	print('ciclo_cond_str')

def p_ciclo_cond_bool(p):
	'''ciclo_cond_bool 	: IF PIZQ exp_bool PDER LLIZQ ciclo_estatuto_bool LLDER
						| IF PIZQ exp_bool PDER LLIZQ LLDER
						| IF PIZQ atom PDER LLIZQ ciclo_estatuto_bool LLDER
						| IF PIZQ atom PDER LLIZQ LLDER
						| IF PIZQ llamada_func PDER LLIZQ ciclo_estatuto_bool LLDER
						| IF PIZQ llamada_func PDER LLIZQ LLDER
						| ciclo_cond_bool ELSE IF PIZQ exp_bool PDER LLIZQ ciclo_estatuto_bool LLDER
						| ciclo_cond_bool ELSE IF PIZQ exp_bool PDER LLIZQ LLDER
						| ciclo_cond_bool ELSE IF PIZQ atom PDER LLIZQ ciclo_estatuto_bool LLDER
						| ciclo_cond_bool ELSE IF PIZQ atom PDER LLIZQ LLDER
						| ciclo_cond_bool ELSE IF PIZQ llamada_func PDER LLIZQ ciclo_estatuto_bool LLDER
						| ciclo_cond_bool ELSE IF PIZQ llamada_func PDER LLIZQ LLDER'''
	print('ciclo_cond_bool')

def p_lectura(p):
	'''lectura 	: INPUT PIZQ atom PDER PYC'''
	print('lectura')

def p_escritura(p):
	'''escritura 	: OUTPUT PIZQ exp_arit PDER PYC
					| OUTPUT PIZQ exp_bool PDER PYC
					| OUTPUT PIZQ exp_objeto PDER PYC
					| OUTPUT PIZQ exp_str PDER PYC
					| OUTPUT PIZQ atom PDER PYC
					| OUTPUT PIZQ llamada_func PYC'''
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