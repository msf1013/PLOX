class Persona {
    hidden string nombre;
    hidden numeral edad;
    hidden Persona madre;
    hidden Persona padre;
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
            this.madre = mad;
    }
    visible string getPadre() {
            return this.Padre;
    }
    visible without setPadre(string pad) {
            this.padre = pad;
    }
}

class Estudiante under Persona {
    hidden real calificacion;
    hidden Profesor profe; 
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
            this.profe = pro;
    }
}

class Profesor under Persona {
    hidden string materia; 
    visible string getMateria() {
        return this.materia;
    }
    visible without setMateria(string mat) {
            this.materia = mat;
    }
}

class main {
    hidden numeral cont = 0;
    visible Persona mama, papa;
    hidden Persona arrP[2];
    visible Profesor profe;
    hidden Estudiante yo;
    hidden string nombreProfe = "no lo se", nombre;
    visible numeral miEdad;

    visible without main() {
        mama = new Persona();
        papa = new Persona();
        profe = new Profesor();
        yo = new Estudiante();
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
        yo.setProfe('c');
        if (nombreProfe == "Ra	ul" && 2 > 2) {
            output("La materia que da mi Profe es:");
        }
        else if (yo.getEdad() >= 30 || mmm == exc.ttt()) {
            out_str("Esta es mi verdadera edad:	5");
            in_num(miEdad);
            output( (miEdad*8-5)*2 < 0 && true);
        }
        else {
            out_num( arrP[2].gg() );
        }

        while(cont < nombre.size){
            out_str(nombre[cont]);
            cont = cont + 1;
        }

    }
}

