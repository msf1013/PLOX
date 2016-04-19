class Fruta {
	hidden numeral id;
	visible string nombre;
	visible numeral dim[4];

	visible without copia(string lele, numeral r, numeral s, numeral arr[4]) {
		numeral i;
		i = 0;
		while (i < 4) {
			dim[i] = arr[i];
			i = i + 1;
		}
	}

}

class Sandia under Fruta {
	hidden numeral tam;
	visible Fruta : FrutaAmiga;
	visible numeral edades[4];
	hidden numeral k;
	visible numeral arri[5];

	visible numeral getDim(numeral i) {
		numeral aux;
		numeral arro[5];
		aux = dim[i];
		return aux;
	}
	visible numeral getEdades(numeral i) {
		numeral aux;
		aux = edades[i];
		return aux;
	}
}

class main {

	visible numeral lol;
	visible real r;
	visible numeral arr[4]; 	

	visible numeral getArr() {
		return arr[3];
	}

	visible without main() {
		numeral a, b;
		Fruta : f;
		Sandia : s, s2;
		s.edades[3] = 2;
		lol = 34 * s.edades[3];
		s2.copia("g", 5, 6, s.edades);
		a = 5 + 2 *6;
		b = a;
		output( s2.getEdades(a) + s2.getDim(b) );
		output('\n');
		output(lol);
		output('\n');
	}
}