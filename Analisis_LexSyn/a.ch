class Persona {
hidden string hola;
	visible without main21(numeral chefe, char loco, char chacha, string wow){
	
	}
}

class Estudiante under Persona {
    hidden real calificacion;
    visible Persona : persona, chavo = persona;
	visible real getCalif() {
	        return this.calificacion;
	}
	visible without setCalif(real calif) {
			this.calificacion = calif;
	}
	visible numeral getProfesor() {
	        return this.persona;
	}
	visible without setProfesor(real pro) {
	        this.calificacion = pro;
	}
}

class main {
	hidden real chofo, a;
	
	visible without main() {
		real lol, chu, chossfos;
		string l;
		Estudiante : g, loca;
		l = loca;

	}
}