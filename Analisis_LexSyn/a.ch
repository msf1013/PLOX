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

	hidden real chofo;
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

class wuwu under Estudiante {
	
	visible without main22(real pro) {
			numeral jj;
			this.jj = jj;
	        this.calificacion = pro;
	}
}

class chifo {
	visible numeral a;
	visible without main22(real pro) {
			numeral jj;
			this.a = jj;
	        this.a = pro;
	}
}

class main {
	hidden real nel, a;
	
	visible without main() {
		char le;
		real lol, chu, chossfos;
		string l;
		wuwu : g, lel;
		chifo : Delga;
		g = g.main21();
		output(main21());

	}
}