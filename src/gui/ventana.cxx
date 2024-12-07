#include "ventana.h"

Ventana::Ventana(QWidget *parent) : QWidget(parent) {
    boton = new QPushButton("Presionar", this);
    boton->setGeometry(50, 50, 100, 30);

    connect(boton, &QPushButton::clicked, this, &Ventana::botonPresionado);
}
