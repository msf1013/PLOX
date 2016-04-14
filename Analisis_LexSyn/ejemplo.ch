class Persona {
	visible numeral a, b, c;
	visible numeral func(numeral x, numeral a){
		return a + b * (c - x);
	}
}

class main {
	visible numeral x, y, z;
	visible Persona : pepe;
	visible numeral func(numeral n, numeral x){
		return x * n;
	}

	visible without main() {
		Persona : angie;
		numeral x;
		x = angie.func( func(3, func(3,4) ), pepe.func(x, y)  );
	}
}