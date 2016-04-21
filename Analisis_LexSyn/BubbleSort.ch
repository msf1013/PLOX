class main {

	visible without main () {
		numeral a, n, i, j, tmp;
		numeral arr[10];

		n = 0;

		output("Introduce los diez numeros del arreglo, cada uno en una línea:\n");

		while(n < 10) {
			input(a);
			arr[n] = a;
			n = n + 1;
		}

		n = 0;
		while(n < 10) {
			output(arr[n]);
			output(' ');
			n = n + 1;
		}
		output('\n');

		i = 0;
		while(i < 9) {
			j = i + 1;
			while(j < 10) {
				if(arr[j] < arr[i]) {
					tmp = arr[i];
					arr[i] = arr[j];
					arr[j] = tmp;
				}
				j = j + 1;
			}
			i = i + 1;
		}

		n = 0;
		while(n < 10) {
			output(arr[n]);
			output(' ');
			n = n + 1;
		}
		output('\n');
	} 
}