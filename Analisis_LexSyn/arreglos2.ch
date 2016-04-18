class Persona {
	visible numeral n;
	visible string str;
	visible numeral arr[5];

	visible numeral sumaArr(numeral s, numeral k) {
		numeral i, suma;
		numeral arreglo[5];
		suma = 0;
		i = 0;

		while (i < 5) {
			arreglo[i] = arr[i];
			suma = arr[i] + suma * this.arr[this.n];
		}

		return suma;
	} 

}

class Estudiante under Persona {
	visible char ch;
	visible numeral arro[5];
	visible numeral x;
	visible Persona : pp;
}

class main {
	visible Persona : papu, googles;
	visible Estudiante : e;
	visible numeral x;
	visible numeral arr[5];


	visible numeral suma1(numeral arr[5]) {
		numeral x, y;
		y = 4 * 56 - 3;
		x = arr[y] + this.arr[y];
		return 4;
	} 

	visible numeral suma2() {
		numeral x, y;
		y = 4 * 56 - 3;
		x = arr[y] + this.arr[y];
		return y;
	}

	visible numeral suma(numeral a, numeral b) {
		a = b;
	} 

	visible without main () {
		numeral a, b, c;
		Persona : auxP;

		this.x = auxP.sumaArr( b, googles.sumaArr( suma(papu.arr[ arr[1] ], 8 - this.x * 4), 9 ) ) - e.sumaArr(suma2(), 67) * suma1(arr);

	} 
}