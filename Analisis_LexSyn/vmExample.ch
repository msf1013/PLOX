class Fruta {
	visible numeral id;
	visible string nombre;
	visible numeral dim[4];

	visible without copia(string lele, numeral r, numeral s, numeral arr[4]) {
		numeral i;
		i = 0;
		while (i < 4) {
			dim[i] = arr[i];
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
	hidden Fruta: fruta;

	visible without main() {
		numeral a, b, c;
		real d, e, f;
		bool g, h, i;
		char j, k, l;
		string m, n, o;
		a = 3;
		b = a % 2;
		input(c);
		e = 3.5 + c;
		fruta.id = fruta.id + a * b;
		f = (b * 5 - 3 / 1.2) * 5;
		g = (3 > a) || (4.5 < e) && !(3 == 3);
		output("Hola");
		output('c');
		output(a);
		output(b);
		output(fruta.id);
		output(g);
	}
}