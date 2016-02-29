add Persona;
add Profesor;
add Estudiante;
class main {
    numeral cont = 0;
    Persona mama, papa;
    Persona arrP[2];
Profesor profe;
    Estudiante yo;
    string nombreProfe = "no lo se", nombre;
    numeral miEdad;
    visible without main () {
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
yo.setProfe(profe);
nombreProfe = profe.getNombre();
if (nombreProfe == "Ra	ul") {
    out_str("La materia que da mi Profe es:");
    out_str(profe.getMateria());
} else if (yo.getEdad() >= 30) {
    out_str("Esta es mi verdadera edad:	5");
    in_num(miEdad);
    out_num( (miEdad*8-5)*2 );
} else {
    out_num( arrP[1].getEdad() );
}

    foreach(p in arrP) {
        nombre = p.getNombre();
cont = 0;
while(cont < nombre.size){
    out_str(nombre[cont]);
    cont = cont + 1;
}
}

}
}

