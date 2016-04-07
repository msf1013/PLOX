class Animal {
    visible numeral id;
}

class Perro under Animal {
    visible numeral edad;
    hidden numeral hijos;
    visible numeral edadPerro() {
    	numeral x;
    	x = 190 - x;
    	return x - (34 / 56 + 2);
    }
}

class Persona {
    
    hidden string nombre;
    hidden numeral edad;
    visible numeral numo;
    visible numeral dias;
    hidden Perro : puchi, puchi2;

    visible numeral auxEdad(numeral ee, numeral x) {
        this.edad = ee;
        return edad;
    }
    
    visible numeral getEdad(numeral tre, numeral chefe, numeral due) {
        return puchi2.edadPerro() - this.edad + puchi.edadPerro();
    }

}

class Estudiante under Persona {
    visible numeral materias;
    visible Animal : nicky;

    visible numeral setMaterias(numeral m) {
        m = puchi.id + getEdad(edad, auxEdad(materias, this.edad) * getEdad(puchi.id, 5, auxEdad(1,3) ),3 ) * materias;
    	m = m + puchi.edadPerro();
    }
}

class main {
    hidden string lol;
    visible numeral a, b, c, d;
    hidden Persona : pucho;
    hidden Estudiante : yo;

    visible without main () {
        numeral edad;
        edad = (3 + 4 / yo.getEdad(3, 4, 5)) * pucho.auxEdad(yo.setMaterias(4), 5);
        output(edad);
    }

}
