class main {
	 
	visible numeral fibo(numeral x) {
		if (x == 0) {
			return 0;
		}
		if (x == 1) {
			return 1;
		}
		return x;
	}

	visible without main () {
		numeral a, b, c, d, e, f, g;

		a = fibo(5);

		output(a);
	} 
}