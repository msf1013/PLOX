add Persona;
add Profesor;
class Estudiante under Persona {
    hidden real calificacion;
    hidden Profesor profe; 
visible real getCalif() {
        return this.calificacion;
}
visible without setCalif(real calif) {
        this.calificacion = calif;
}
visible Profesor getProfesor() {
        return this.profe;
}
visible without setProfesor(Profesor pro) {
        this.profe = pro;
}
}
