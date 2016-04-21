class main{
	
	visible numeral arr[10];

	visible numeral partition(numeral lo, numeral hi, numeral arr[10]) {
		numeral pivot, i, j, aux;

		pivot = arr[hi];
		i = lo;
		j = lo;

		while (j < hi) {
			if (arr[j] <= pivot) {
				aux = arr[i];
				arr[i] = arr[j];
				arr[j] = aux;
				i = i + 1;
			}
			j = j + 1;
		}
		aux = arr[i];
		arr[i] = arr[hi];
		arr[hi] = aux;

		return i;

	}

	visible without qsort(numeral lo, numeral hi, numeral arr[10]) {

		numeral p;

		if (lo < hi) {
			p = partition(lo, hi, arr);
			qsort(lo, p-1, arr);
			qsort(p+1, hi, arr);
		}

	}

	visible without main () {

		numeral arreglo[10];

		numeral n, i;

		i = 0;

		output("Ingrese el tamanio del arreglo:\n");
		input(n);

		while (i < n) {
			output("Elemento #"); output(i); output(":\n");
			input(arr[i]);
			i = i + 1; 
		}

		qsort(0, n-1, arreglo);

		output("Resultado de qsort:\n");

		i = 0;
		while (i < n) {
			output(arr[i]); output("\n");
			i = i + 1; 
		}

	}

}
