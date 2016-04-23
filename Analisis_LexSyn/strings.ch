class Persona {
	visible string compania;
	visible string nombres[4];

	visible char primerLetraApellido() {
		return charAt(nombres[2], 0);
	}

	visible without imprime(string aux) {
		numeral i;
		i = 0;

		while ( i < len(aux) ) {
			output(charAt(compania, i));
			output("hola" + "\n");
			output(charAt(aux, i));
			output("\n");
			i = i + 1;
		}

	}

}

class Estudiante under Persona {
	visible string salon;	

	visible string getSalonCompania() {
		numeral pos;
		pos = len(nombres[len(salon)]);

		while ( pos < len(compania) ) {
			output(charAt(salon, pos));
			output(charAt(nombres[pos], pos));
			output(charAt(compania, pos));
			pos = pos + 1;
		}
		return salon + '*' + "chefe";
	}

}

class main{
	
	visible Estudiante : e, f;
	visible Persona : o, p;

	visible without main () {

		Estudiante : e, k;
		string str1, str2, str3;
		char ch1, ch2, ch3;

		ch1 = o.primerLetraApellido();
		k = this.e;
		ch2 = k.primerLetraApellido();

		p.imprime('a' + str2);

		str2 = f.getSalonCompania();

		str1 = "hola";
		str2 = "ggggg";

		output('1' + " hola " + '\n' + "gg " + '\n');
		output('1' + " hola " + '\n' + "gg " + '\n');
		output(charAt("hola", 0));
		output('\n');
		output(charAt("hola", 1));
		output('\n');
		output(charAt("hola", 2));
		output('\n');
		output(charAt(str1, 3));
		output('\n');
		output(charAt("adios", 0));
		output('\n');
		output(charAt("adios", 2));
		output('\n');
		output(charAt("adios", 4));
		output('\n');
		output(len("a"));
		output('\n');
		output(len("ab"));
		output('\n');
		output(len("abcdefghij"));
		output('\n');
		output(len(str2));
		output('\n');
		output('');
		output("");

	}

}
