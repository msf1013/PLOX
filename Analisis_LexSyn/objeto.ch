class Persona {
	visible numeral n;
	visible string str;
	visible numeral arr[5];
}

class Estudiante under Persona {
	visible char ch;
	visible numeral arro[10];
	visible numeral x;
	visible Persona : pp;
}

class Loco under Estudiante {
	visible numeral r;
	visible char cheche;
	visible string strong;
	visible without chofo () {
		numeral x, y, xk;
		string strong;
		Persona : papa;
		pp = papa;
		strong = this.strong;
		this.strong = strong;

	}
}

class main {
	visible Persona : papu, googles;
	visible Estudiante : e;
	visible Loco : l;
	visible numeral a;

	visible without main () {
	} 
}