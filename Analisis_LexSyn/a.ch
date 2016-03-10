class Persona {
visible numeral jj;
visible string hola;
	visible string calificacion;
	visible without main21(numeral chefe, char loco, char chacha, string wow){
		string hola;
	}
}

class Estudiante under Persona {
    visible Persona : persona, chavo = persona;
	visible real getCalif() {
			Persona : calificacion;
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

class Lalio under Estudiante {
	
	visible without main22(real pro) {
			numeral jj;
			this.jj = jj;
	        this.calificacion = pro;
	}
}

class main {
	hidden real chofo, a;
	
	visible without main() {
		char chofo;
		real lol, chu, chossfos;
		string l;
		Lalio : g, loca;
		g = g.hola;

	}
}