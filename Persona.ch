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
visible Persona getMadre() {
        return this.madre;
}
visible without setMadre(Persona mad) {
        this.madre = mad;
}
visible Persona getPadre() {
        return this.Padre;
}
visible without setPadre(Persona pad) {
        this.padre = pad;
}
}

