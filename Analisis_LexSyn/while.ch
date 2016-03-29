class main {
    
    hidden numeral a;
    visible numeral b, c;

    visible without main () {
    
        a = 50;

        while ( a > b || true ) {
            b = a + c;
            while (a + b > 1) {
                b = c;
            }
        }

        output(a - c / 4);



    }

}
