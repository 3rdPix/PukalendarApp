#include "logic.h"
#include <QDebug>

Logica::Logica(QObject *parent) : QObject(parent) {}

void Logica::manejarBotonPresionado() {
    qDebug() << "Presionado";
}
