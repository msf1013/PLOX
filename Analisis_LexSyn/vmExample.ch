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
	visible numeral k;
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
	visible numeral suma(numeral x) {
		tam = 1;
		this.id = tam + k + x;
		return id;
	}
}

class main {
	hidden Sandia: fruta;

	visible without main() {
		numeral a, b, c, x, y;
		real d, e, f;
		bool g, h, i;
		char j, k, l;
		string m, n, o;
		a = 3;
		x = 1;
		b = a % 2;
		input(c);
		e = 3.5 + c;
		fruta.k = 2;
		fruta.id = fruta.id + a * b;
		f = (b * 5 - 3 / 1.2) * 5;
		g = (3 > a) || (4.5 < e) && !(3 == 3);
		a = 10 % 1;
		if(g) {
			output("Verdadero\n");
		}
		else {
			output("Falso\n");
		}
		if(20 >= 19) {
			output("Verdadero 2\n");
		}
		else {
			output("Falso 2\n");
		}
		while(x <= 10) {
			output(x);
			output(' ');
			x = x + 1;
		}
		output('\n');
		x = 1;
		y = 1;
		while(x <= 100) {
			output(y);
			output(' ');
			y = x + y;
			x = y - x;
		}
		output('\n');
		output("Suma: ");
		output(fruta.suma(3));
		output('\n');
		output("Hola\n");
		output('c');
		output('\n');
		output(a);
		output('\n');
		output(b);
		output('\n');
		output(fruta.id);
		output('\n');
		output(g);
		output('\n');
	}
}