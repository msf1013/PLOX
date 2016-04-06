class Animal {
    visible numeral id;
}

class Perro under Animal {
    visible numeral edad;
    hidden numeral hijos;

    hidden char chefe() {
        char c;
        c = 'c';
        return c;
    }

}

class Persona {
    
    hidden string nombre;
    visible numeral edad;
    hidden numeral hijos;
    visible char dia;
    visible bool esEstudiante;
    visible string apellido;
    hidden Perro : puchi;

    hidden numeral auxEdad(numeral ee) {
        this.edad = ee;
        edad = ee;
        return edad;
    }
    
    visible numeral getEdad(numeral tre, string chefe, numeral due) {
        numeral e;
        Perro : puchi2;
        e = auxEdad(this.edad);
        return edad - this.edad + puchi.edad;
    }

    visible without setNombre(string nombre, char ch, numeral nume) {
        numeral tre;
        string loco;
        numeral cuatro;
        this.nombre = nombre;
        return;
        this.nombre = nombre;
    }

    visible bool setEdad(numeral e) {
        edad = e;
    }

}

class Estudiante under Persona {
    visible numeral materias;
    hidden Perro : nicky;
    hidden Persona : maestro;

    visible real setMaterias(numeral m) {
        string loca;
        numeral num;
        m = 56 - 45 * 1 + 1;
        this.materias = m;
    }
    visible string getMaterias() {
        string wow = "chefe";

    }
}

class Amigo under Estudiante {
    visible numeral ido;
    
}

class main {
    
    hidden Persona : yo;
    hidden Persona : pucho;

    visible without main () {
        numeral edad;

        yo.setEdad(23);
        edad = yo.getEdad() + 1 * 3 + pucho.edad;
        output(edad);
    }

}
