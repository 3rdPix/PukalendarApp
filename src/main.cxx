#include <QApplication>
#include "gui/ventana.h"
#include "controller/logic.h"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    Ventana ventana;
    Logica logica;

    QObject::connect(&ventana, &Ventana::botonPresionado, &logica, &Logica::manejarBotonPresionado);

    ventana.show();

    return app.exec();
}
