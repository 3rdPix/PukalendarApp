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
from PyQt6.QtGui import QPaintEvent, QPainter
from PyQt6.QtGui import QBrush
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtGui import QPalette
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtWidgets import QGraphicsEllipseItem
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtGui import QPen
from random import randint


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


class TimePieChart(QWidget):
    """
    Un gráfico de torta que se construye a partir de la lista de porcentajes
    y la lista de colores asociados.
    """

    def __init__(self, values: list[int], colors: list[QColor],
                 parent: QWidget|None=None,
                 flags: Qt.WindowType=Qt.WindowType.Widget) -> None:
        super().__init__(parent, flags)
        self._values = values
        self._colors = colors
        self._scene = QGraphicsScene()
        # self._scene.setBackgroundBrush(QBrush(QColor(0, 0, 0, 0)))
        self._view = QGraphicsView(self._scene)
        # self._view.setBackgroundBrush(QBrush(QColor(0, 0, 0, 0)))
        self._view.setStyleSheet("background: transparent; border: none;")
        self._view.setRenderHint(QPainter.RenderHint.Antialiasing, on=True)
        self._view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._pie_radius: int = 100
        self._randomize_view = randint(0, 360 * 16)
        layout = QGridLayout(self)
        layout.addWidget(self._view)
        layout.setContentsMargins(0, 0, 0, 0)

    def set_pie_radius(self, radius: int) -> None:
        self._pie_radius = radius

    def __draw__(self) -> None:
        for each in self._scene.items():
            self._scene.removeItem(each)
        total_angle: int = int(self._randomize_view)
        the_pen = QPen(QColor(0, 0, 0, 0))
        the_pen.setWidth(1)
        for percentage, color in zip(self._values, self._colors):
            current_angle: int = round((percentage / 100) * 360 * 16)
            size = self._pie_radius
            current_ellipsis: QGraphicsEllipseItem = QGraphicsEllipseItem(
                0, 0, size, size)
            current_ellipsis.setStartAngle(total_angle)
            current_ellipsis.setSpanAngle(current_angle)
            current_ellipsis.setBrush(QColor(color))
            current_ellipsis.setPen(the_pen)
            total_angle += current_angle
            self._scene.addItem(current_ellipsis)

    def update_proportions(self, values: list[int], colors: list[QColor]) -> None:
        """
        Recibe los nuevos valores a ser desplegados y actualiza la escena
        con las proporciones correspondientes. Este método elimina todos
        los elementos que existían anteriormente para construir nuevos en
        lugar de actualizar los valores de los elementos gráficos.
        """
        self._values = values
        self._colors = colors
        self.repaint()

    def paintEvent(self, event: QPaintEvent|None) -> None:
        self.__draw__()
        return super().paintEvent(event)

if __name__ == "__main__":
    # showcase
    from PyQt6.QtWidgets import QApplication
    app = QApplication([])
    just_close_this = QWidget()
    elm = TimePieChart(list(), list())
    elm.update_proportions([0, 62, 20, 18], ["#e215b9", "#23d2e2", "#10aaa2", "#358b15"])
    elm.show()
    just_close_this.show()
    exit(app.exec())