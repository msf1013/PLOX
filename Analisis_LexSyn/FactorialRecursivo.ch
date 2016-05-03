class main {

	visible numeral fact(numeral n) {
		if(n == 0) {
			return 1;
		}
		return n * fact(n - 1);
	}

	visible without main () {
		numeral a;

		output("Introduce indice de factorial -> ");
		input(a);

		output(fact(a)); output('\n');
	} 
}