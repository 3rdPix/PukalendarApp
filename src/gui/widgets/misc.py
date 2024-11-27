"""
Colección miscelánea
--------------------
Varios widgets que pueden resultar útiles
"""
from PyQt6.QtWidgets import QStackedWidget
from PyQt6.QtCore import QAbstractAnimation
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtCore import QPropertyAnimation


class OpacityAniStackedWidget(QStackedWidget):
    """
    Widget con animaciones de opacidad en la transición
    """

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.__create_animations()

    def setCurrentIndex(self, index: int) -> None:
        if index == self.currentIndex(): return
        if not self.widget(index): return
        
        # Índice actual se esconde, índice objetivo se muestra
        self.currentWidget().setGraphicsEffect(self._opacity1)
        self.widget(index).setGraphicsEffect(self._opacity2)

        # Mostrar widget objetivo
        #tno = self.currentIndex()
        super().setCurrentIndex(index)
        #self.widget(tno).show()

        # Inicia animaciones
        self._opacityUp.finished.connect(
            lambda: self.rst_effects(self.currentWidget(), self.widget(index)))
        self._opacityDown.start(QAbstractAnimation.DeletionPolicy.KeepWhenStopped)
        self._opacityUp.start(QAbstractAnimation.DeletionPolicy.KeepWhenStopped)

    def rst_effects(self, w_hidden: QWidget, w_shown: QWidget) -> None:
        #super().setCurrentWidget(w_shown)
        w_hidden.setGraphicsEffect(None)
        w_shown.setGraphicsEffect(None)
        self.__create_animations()

    def __create_animations(self) -> None:

        self._opacity1 = QGraphicsOpacityEffect(self)
        self._opacity2 = QGraphicsOpacityEffect(self)
        self._opacity2.setOpacity(0.0)

        # Animación para ambas opacidades
        self._opacityDown = QPropertyAnimation(self._opacity1, b'opacity')
        self._opacityDown.setStartValue(1.0)
        self._opacityDown.setEndValue(0.0)

        self._opacityUp = QPropertyAnimation(self._opacity2, b'opacity')
        self._opacityUp.setStartValue(0.0)
        self._opacityUp.setEndValue(1.0)

    def setDuration(self, ms: int) -> None:
        """Sets the duration of the transition between widgets"""
        self._opacityUp.setDuration(ms)
        self._opacityDown.setDuration(ms)

    def setCurrentWidget(self, w: QWidget) -> None:
        self.setCurrentIndex(self.indexOf(w))