class main {
	visible without printMain(numeral arr[5]) {
		numeral i;
		i = 0;
		while(i < 5) {
			output(arr[i]);
			output(' ');
			i = i + 1;
		}
		output('\n');
	}

	visible without main() {
		numeral arr[5];
		numeral i;
		i = 0;

		arr[0] = 0;
		arr[1] = 2;
		arr[2] = 4;
		arr[3] = 6;
		arr[4] = 8;

		printMain(arr);

		output('\n');
		while(i < 5) {
			output(arr[i]);
			output(' ');
			i = i + 1;
		}
		output('\n');
	}
}