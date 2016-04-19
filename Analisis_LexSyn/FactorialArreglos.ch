class Factorial {
	
	hidden numeral fact[25];

	visible without calcFactorial() {
		numeral n;
		numeral i;
		n = 1;
		i = 1;
		while(n <= 25) {
			i = i * n;
			fact[n - 1] = i;
			n = n + 1;
		}
	}

	visible without imprimirFactorial() {
		numeral n;
		n = 0;
		while(n < 25) {
			output(fact[n]);
			output(' ');
			n = n + 1;
		}
		output('\n');
	}
}

class main {

	visible without main () {
		Factorial: fact;

		fact.calcFactorial();

		fact.imprimirFactorial();
	} 
}