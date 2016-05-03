class Persona {
    hidden string nombre;

    visible string getNombre(){
        return this.nombre;
    }

    visible without setNombre(string nombre) {
        this.nombre = nombre;
    }
}

class Profesor under Persona {
    visible string materias[3];
    hidden numeral aniosServicio; 

    visible numeral getAniosServicio() {
        return this.aniosServicio;
    }

    visible without setAniosServicio(numeral aniosServicio) {
        this.aniosServicio = aniosServicio;
    }

    visible string getMateriaAtIndex(numeral index) {
        return materias[index];
    }

    visible without setMaterias(string mat[3]) {
        numeral i;
        i = 0;
        while(i < 3) {
            this.materias[i] = mat[i];
            i = i + 1;
        }
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
    visible string getNombreProfe() {
        return profe.getNombre();
    }

    visible without imprimeMateriasProfe() {
        numeral i;
        i = 0;
        while(i < 3) {
            output("    Materia "); output(i + 1); output(": "); output(profe.getMateriaAtIndex(i)); output('\n');
            i = i + 1;
        }
    }
}

class main {
    visible Profesor: profe;
    hidden Estudiante: yo;

    visible without main() {
        string nombreProfe, nombreEstudiante;
        string materias[3];
        output("Indica tu nombre -> ");
        input(nombreEstudiante);
        output("\nIndica el nombre de tu profesor -> ");
        input(nombreProfe);
        yo.setNombre(nombreEstudiante);
        profe.setNombre(nombreProfe);
        materias[0] = "Compiladores";
        materias[1] = "Metodos";
        materias[2] = "Algoritmos";
        profe.setMaterias(materias);
        yo.profe = profe;
        yo.calificacion = 100;
        
        output("Tu nombre es: "); output(yo.getNombre()); output("\n");
        output("El nombre de tu profesor es: "); output(yo.getNombreProfe()); output("\n");
        output("Materias:\n"); yo.imprimeMateriasProfe();
    }
}


