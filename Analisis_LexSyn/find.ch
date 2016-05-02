class main {
	
	hidden numeral arr[5];

	visible without main () {

		numeral i, pos, val;
		bool existe;

		pos = -1;
		i = 0;

		while (i < 5) {
			input(arr[i]);
			i = i + 1;
		}

		input(val);

		i = 0;
		existe = false;

		while (i < 5 && !existe) {

			if (arr[i] == val) {
				existe = true;
				pos = i;
			}

			i = i + 1;

		}

		if (existe) {
			output("El numero "); output(val); output(" fue encontrado en la posicion "); output(pos); output("\n");
		} else {
			output("El numero "); output(val); output(" no fue encontrado en el arreglo\n");
		}

	}

}