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
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtGui import QPainter
from PyQt6.QtGui import QColor
from typing import Optional
from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QApplication


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
        self.widget(index).show()

        # Inicia animaciones
        self._opacityUp.finished.connect(
            lambda: self.rst_effects(self.currentWidget(), self.widget(index)))
        self._opacityDown.start(QAbstractAnimation.DeletionPolicy.KeepWhenStopped)
        self._opacityUp.start(QAbstractAnimation.DeletionPolicy.KeepWhenStopped)

    def rst_effects(self, w_hidden: QWidget, w_shown: QWidget) -> None:
        super().setCurrentWidget(w_shown)
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


class SlidingStackedWidget(QStackedWidget):
    """
    *Widget* con animaciones de desliz en la transición
    """

class LineSeparator(QWidget):
    """
    Una línea separadora de color personalizable
    """

    def __init__(self, parent: Optional[QWidget]=None,
                 line_color: Optional[QColor]=QApplication.palette().highlight().color()) -> None:
        super().__init__(parent=parent)
        self._line_color: QColor = line_color
        self.setFixedHeight(4)

    def set_color(self, line_color: QColor) -> None:
        """Ajustar el color de la línea"""
        self._line_color = line_color

    def paintEvent(self, event: QEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(self._line_color)
        painter.drawLine(2, 1, self.width() - 2, 1)


class IconedButton(QWidget):
    """
    Botón que utiliza dos
    """