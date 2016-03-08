class Persona {
	visible without main21(){
	
	}
}

class Estudiante under Persona {
    hidden real calificacion;
    hidden Persona persona;
	visible real getCalif() {
	        return this.calificacion;
	}
	visible without setCalif(real calif) {
	        this.calificacion = calif;
	}
	visible numeral getProfesor() {
	        return this.profe;
	}
	visible without setProfesor(real pro) {
	        this.profe = pro;
	}
}

class main {
	visible without main(){
	
	}
}