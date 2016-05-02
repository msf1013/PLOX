class Arreglo {
	hidden numeral arr[7];

	visible without setI(numeral i, numeral x) {
		arr[i] = x;
	}

	visible numeral getI(numeral i) {
		return arr[i];
	}

	visible numeral find(numeral val) {

		numeral i, pos;
		bool existe;

		pos = -1;
		i = 0;
		existe = false;

		while (i < 7 && !existe) {

			if (arr[i] == val) {
				existe = true;
				pos = i;
			}

			i = i + 1;

		} 

		if (existe) {
			return pos;
		} else {
			return -1;
		}

	}

}

class main {

	visible Arreglo : Arr;

	visible without main () {


		numeral i, aux, res, val;
		i = 0;

		while (i < 7) {
			output("Ingrese el valor del indice "); output(i); output(":\n");
			input(aux);
			Arr.setI(i, aux);
			i = i + 1;
		}

		output("Ingrese el valor a buscar:\n");
		input(val);

		res = Arr.find(val);		

		if (res > -1) {
			output("El numero "); output(val); output(" fue encontrado en la posicion "); output(res); output("\n");
		} else {
			output("El numero "); output(val); output(" no fue encontrado en el arreglo\n");
		}

	}

}
