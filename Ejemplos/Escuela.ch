class Persona {
    visible string nombre;
    visible numeral edad;
    visible Persona: madre;
    visible Persona: padre;
    visible string getNombre() {
        return this.nombre;
    }
    visible without setNombre(string nom) {
            this.nombre = nom;
    }
    visible numeral getEdad() {
            return this.edad;
    }
    visible without setEdad(numeral ed) {
            this.edad = ed;
    }
    visible real getMadre() {
            return this.madre;
    }
    visible without setMadre(real mad, numeral prof) {
            madre.edad = prof;
    }
    visible string getPadre() {
            return this.padre;
    }
    visible without setPadre(string pad) {
            this.nombre = pad;
    }
}

class Profesor under Persona {
    visible string materia; 
    visible string getMateria() {
        return this.materia;
    }
    visible without setMateria(string mat) {
            this.materia = mat;
    }
}

class Estudiante under Persona {
    visible real calificacion;
    visible Profesor: profe; 
    visible real getCalif() {
            return this.calificacion;
    }
    visible without setCalif(real calif) {
            this.calificacion = calif;
    }
    visible numeral getProfesor() {
            return this.profe;
    }
    visible without setProfesor(char pro) {
            
    }
}

class main {
    hidden numeral cont = 0;
    visible Persona: mama, papa;
    hidden Persona: arrP[2];
    visible Profesor: profe;
    hidden Estudiante: yo;
    hidden string nombreProfe = "no lo se", nombre;
    visible numeral miEdad;

    visible without main() {
        mama.setNombre("Laura");
        mama.setEdad(45);
        papa.setNombre("Pedro");
        papa.setEdad(45);
        arrP[0] = mama;
        arrP[1] = papa;
        profe.setNombre("Elda");
        profe.setMateria("Compiladores");
        yo.setNombre("Manolo");
        yo.setEdad(20);
        yo.setProfesor('c');
        if (nombreProfe == "Ra	ul" && 2 > 2) {
            output("La materia que da mi Profe es:");
        }
        else if (yo.getEdad() >= 30) {
            output("Esta es mi verdadera edad:	5");
            input(miEdad);
            output( (miEdad*8-5)*2 < 0 && true);
        }
        else {
            output( mama.edad );
        }

        while(cont < 15){
            output(papa.edad);
            cont = cont + 1;
        }

    }
}

