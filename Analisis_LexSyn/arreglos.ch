class Persona {
	visible numeral n;
	visible string str;
	visible numeral arr[5];

	visible numeral sumaArr() {
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


	visible without calcArr(numeral arr[5]) {
		numeral x, y;
		y = 4 * 56 - 3;
		x = arr[y] + this.arr[y];
		return;
	} 

	visible without main () {
		numeral a, b, c;
		Persona : auxP;

		auxP.arr[ arr[6 * 3] - papu.arr[3] * e.arr[this.x] ] = papu.arr[ e.arro[5] ];

		auxP.sumaArr();

		e.sumaArr();

		a = this.x * b * c - (auxP.arr[5] - this.arr[googles.arr[5]]);

		calcArr(papu.arr);

		calcArr(e.arr);

		calcArr(arr);

		calcArr(auxP.arr);

	} 
}