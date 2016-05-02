class main {

	visible numeral fibo (numeral n) {
		if (n < 3) {
			return 1;
		}
		return fibo(n - 1) + fibo(n - 2);
	}

	visible without main () {
		numeral n;

		output("Introduce indice hasta el cual se calculara fibonacci -> ");
		input(n);

		n = fibo(n);

		output(n);
		output('\n');
	} 
}