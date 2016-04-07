class Motor {
	visible numeral numValvulas;
	visible string marcaMotor;

	visible real calcularPotencia(real rendimiento, numeral X, numeral Y){
		return rendimiento * numValvulas - X / Y;
	}
}

class Transporte {
	hidden string tipoTransporte;
	hidden string marca;
	hidden Motor: motor;
	visible numeral aniosCompra;
	visible bool enFuncionamiento;
	hidden Motor: motor2;
	hidden char modelo;

	visible real devuelve(numeral x, real y) {
		y = x - motor.numValvulas;
		return y - (y + y * 3);
	}

	visible numeral prueba() {
		return 1;
	}

	hidden without impresionIdentificacion() {
		output("Marca: ");
		output(marca);
		output("\nModelo: ");
		output(modelo);
		output("\n");
	}

	hidden without impresionFuncionamiento() {
		output("En funcionamiento?: ");
		if(enFuncionamiento) {
			output("Si\n");
		}
		else {
			output("No\n");
		}
		output("Anios en compra: ");
		output(aniosCompra);
		output( motor.calcularPotencia( motor.calcularPotencia( 4.5, 3,aniosCompra ), 16, motor.numValvulas ) );
		output("\n");
	}

	visible without imprimir() {
		impresionIdentificacion();
		impresionFuncionamiento();
	}
}

class VehiculoTerrestre under Transporte {
	hidden numeral numLlantas;
	hidden string tipoTraccion;
}

class Coche under VehiculoTerrestre {
	hidden string color;
	visible Motor: motorReserva;
}

class VehiculoAereo under Transporte {
	hidden string numVuelo;
	visible string aerolinea;
	visible numeral horasVuelo;
}

class main {
	
	visible Coche: coche;

	visible bool imprimirTransportes() {
		coche.imprimir();
		return true;
	}

	visible without main() {
		Coche : coche2;
		real r, s;
		VehiculoAereo: avion;

		r = coche2.devuelve(3, 4.5);

		imprimirTransportes();

		s = coche2.devuelve(4, 3.5) - r * 3;

	}
}