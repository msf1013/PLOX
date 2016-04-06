class Animal {
    visible numeral id;
}

class Perro under Animal {
    visible numeral edad;
    hidden numeral hijos;
}

class Persona {
    
    hidden string nombre;
    hidden numeral edad;
    visible numeral dias;
    hidden Perro : puchi;

    visible numeral auxEdad(numeral ee, numeral x) {
        this.edad = ee;
        return edad;
    }
    
    visible numeral getEdad(numeral tre, numeral chefe, numeral due) {
        return edad - this.edad + puchi.edad;
    }

}

class Estudiante under Persona {
    visible numeral materias;

    visible numeral setMaterias(numeral m) {
        m = puchi.id + getEdad(edad, auxEdad(materias, this.edad) * getEdad(puchi.id, 5, auxEdad(1,3) ),3 ) * materias;
    }
}

class main {
    
    hidden Estudiante : yo;
    hidden Persona : pucho;

    visible without main () {
        numeral edad;
        edad = (3 + 4 / yo.getEdad(3, 4, 5)) * pucho.auxEdad(yo.setMaterias(4), 5);
        output(edad);
    }

}
