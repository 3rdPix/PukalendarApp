#ifndef LOGICA_H
#define LOGICA_H

#include <QObject>

class Logica : public QObject {
    Q_OBJECT

public:
    explicit Logica(QObject *parent = nullptr);

public slots:
    void manejarBotonPresionado();
};

#endif
