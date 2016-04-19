class main {

	visible without main () {
		numeral a;
		numeral x, y, n;

		output("Introduce indice hasta el cual se calculara fibonacci -> ");
		input(a);

		x = 1;
		y = 1;
		n = 3;

		output("1 1 ");

		while(n <= a) {
			y = x + y;
			x = y - x;
			n = n + 1;
			output(y);
			output(' ');
		}

		output('\n');
	} 
}