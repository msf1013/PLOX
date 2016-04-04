class Animal {
    visible numeral id;
}

class Perro under Animal {
    visible numeral edad;
    visible numeral hijos;
}

class Persona {
    
    hidden string nombre;
    visible numeral edad;
    hidden numeral hijos;
    visible char dia;
    visible bool esEstudiante;
    visible string apellido;
    hidden Perro : puchi;

    hidden numeral auxEdad(numeral edad) {
        this.edad = edad;
        return edad;
    }
    
    visible numeral getEdad(numeral tre, string chefe, numeral due) {
        numeral e;
        Perro : puchi2;
        e = auxEdad(this.edad);
        return edad - this.edad + e;
    }

    visible without setNombre(string nombre, char ch, numeral nume) {
        numeral tre;
        string loco;
        numeral cuatro;
        this.nombre = nombre;
    }

    visible without setEdad(numeral e) {
        edad = e;
    }

}

class Estudiante under Persona {
    visible numeral materias;
    hidden Perro : nicky;
    hidden Persona : maestro;

    visible numeral setMaterias(numeral m) {
        string loca;
        numeral num;
        m = 56 - 45 * 1 + 1;
        this.materias = m;
    }
    visible without getMaterias() {
        return this.edad;
    }
}

class main {
    
    hidden Persona : yo;

    visible without main () {
        numeral edad;

        yo.setEdad(23);
        edad = yo.getEdad() + 1 * 3;
        output(edad);
    }

}
