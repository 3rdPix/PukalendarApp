#ifndef VENTANA_H
#define VENTANA_H

#include <QWidget>
#include <QPushButton>

class Ventana : public QWidget {
    Q_OBJECT

public:
    explicit Ventana(QWidget *parent = nullptr);

signals:
    void botonPresionado();

private:
    QPushButton *boton;
};

#endif
