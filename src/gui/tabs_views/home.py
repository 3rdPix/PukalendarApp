from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QLabel
from qfluentwidgets import CaptionLabel
from qfluentwidgets import DisplayLabel
from PyQt6.QtWidgets import QStackedLayout
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QWidget
from gui.widgets import HomeViewInfoBox
from qfluentwidgets import ScrollArea
from qfluentwidgets import FlowLayout
from PyQt6.QtCore import QEasingCurve
from config import PUCalendarAppPaths as pt
from utils.i18n import _
from gui.widgets import TimePieChart
from PyQt6.QtGui import QColor
from gui import PukalendarWidget
import logging


log = logging.getLogger("HomeView")




class HomeView(QFrame, PukalendarWidget):
    
    def __init__(self, parent: QWidget | None=None) -> None:
        super().__init__(parent)
        self.setObjectName('home_view')
        self._scroll_area: ScrollArea = ScrollArea(self)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self._scroll_area.setObjectName('homescrollarea')
        self._widget_object: QWidget = QWidget()
        self._widget_object.setObjectName('homewidgetobject')
        self._widget_flow_layout: FlowLayout = FlowLayout(
            parent=self._widget_object, needAni=True)
        self._widget_flow_layout.ease = QEasingCurve.Type.InOutExpo
        self._scroll_area.setWidget(self._widget_object)
        self._load_cards()
        try:
            with open(pt.Qss.HOME_VIEW, 'r') as raw_file:
                self.setStyleSheet(raw_file.read())
        except FileNotFoundError:
            log.error(f"Couldn't load Qss file")

    def _load_cards(self) -> None:
        self._widget_flow_layout.addWidget(self._create_agenda_infobox())
        self._widget_flow_layout.addWidget(self._create_courses_infobox())
        self._widget_flow_layout.addWidget(self._create_settings_infobox())
        self._widget_flow_layout.addWidget(self._create_dangers_infobox())
        self._widget_flow_layout.addWidget(self._create_external_infobox())
        self._widget_flow_layout.addWidget(self._create_time_infobox())
        
    def _create_agenda_infobox(self) -> HomeViewInfoBox:
        self.agenda_infobox: HomeViewInfoBox = HomeViewInfoBox()
        self.agenda_infobox.setTitle(_("MainWindow.Home.InfoBoxAgenda.Title"))
        return self.agenda_infobox

    def _create_courses_infobox(self) -> HomeViewInfoBox:
        self.courses_infobox: HomeViewInfoBox = HomeViewInfoBox()
        self.courses_infobox.setTitle(_("MainWindow.Home.InfoBoxCourses.Title"))
        return self.courses_infobox

    def _create_settings_infobox(self) -> HomeViewInfoBox:
        self.settings_infobox: HomeViewInfoBox = HomeViewInfoBox()
        self.settings_infobox.setTitle(_("MainWindow.Home.InfoBoxSettings.Title"))
        return self.settings_infobox

    def _create_dangers_infobox(self) -> HomeViewInfoBox:
        self.dangers_infobox: HomeViewInfoBox = HomeViewInfoBox()
        self.dangers_infobox.setTitle(_("MainWindow.Home.InfoBoxDangers.Title"))
        return self.dangers_infobox

    def _create_external_infobox(self) -> HomeViewInfoBox:
        self.external_infobox: HomeViewInfoBox = HomeViewInfoBox()
        self.external_infobox.setTitle(_("MainWindow.Home.InfoBoxExternal.Title"))
        return self.external_infobox

    def _create_time_infobox(self) -> HomeViewInfoBox:
        self.time_infobox: HomeViewInfoBox = HomeViewInfoBox()
        self.time_infobox.setTitle(_("MainWindow.Home.InfoBoxTime.Title"))
        stacked_form = QStackedLayout()
        # Capa 0 es vacía
        widget_layer_0 = QWidget()
        icon = QLabel()
        icon.setPixmap(QPixmap(pt.Resources.IMAGE_EMPTY_BOX))
        dim = round(self.time_infobox.width() * 0.2)
        icon.setFixedSize(dim, dim)
        icon.setScaledContents(True)
        subtitle = QLabel(_("MainWindow.Home.InfoBoxTime.NoClass"))
        layout_0 = QVBoxLayout(widget_layer_0)
        layout_0.addStretch()
        layout_0.addWidget(icon, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_0.addWidget(subtitle, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_0.addStretch()
        stacked_form.addWidget(widget_layer_0)
        # Capa 1 es completa
        widget_layer_1 = QWidget()
        layout_1 = QGridLayout(widget_layer_1)
        stacked_form.addWidget(widget_layer_1)
        # summary_indicator = QLabel(
        #     _("MainWindow.Home.InfoBoxTime.SummaryIndicator"))
        # layout_1.addWidget(summary_indicator, 0, 0, 1, 3,
        #                    alignment=Qt.AlignmentFlag.AlignCenter)
        pie_chart = TimePieChart(list(), list())
        pie_chart.setMinimumSize(pie_chart._pie_radius, pie_chart._pie_radius)
        layout_1.addWidget(pie_chart, 0, 0, 3, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        
        widget_layer_1.setLayout(layout_1)
        # Capa 2 es singular
        widget_layer_2 = QWidget()
        widget_layer_2.setObjectName("widget_single")
        layout_2 = QGridLayout(widget_layer_2)
        on_session_indicator = QLabel(
            _("MainWindow.Home.InfoBoxTime.OnSessionIndicator"))
        course_indicator = CaptionLabel(
            _("MainWindow.Home.InfoBoxTime.CourseIndicator"))
        course_label = QLabel()
        started_at_indicator = CaptionLabel(
            _("MainWindow.Home.InfoBoxTime.StartedAtIndicator"))
        started_time = QLabel()
        layout_2.addWidget(on_session_indicator, 0, 0, 1, 2,
                           alignment=Qt.AlignmentFlag.AlignCenter)
        layout_2.addWidget(course_indicator, 1, 0, 1, 1,
                           alignment=Qt.AlignmentFlag.AlignLeft)
        layout_2.addWidget(course_label, 1, 1, 1, 1, 
                           alignment=Qt.AlignmentFlag.AlignRight)
        layout_2.addWidget(started_at_indicator, 2, 0, 1, 1,
                           alignment=Qt.AlignmentFlag.AlignLeft)
        layout_2.addWidget(started_time, 2, 1, 1, 1,
                           alignment=Qt.AlignmentFlag.AlignRight)
        stacked_form.addWidget(widget_layer_2)
        stacked_form.setCurrentIndex(0)
        self.time_infobox.insert_layout(stacked_form)
        return self.time_infobox

    def RQ_update_dedication_piechart(self, percentages: list[int], colors: list) -> None:
        stack: QStackedLayout = self.time_infobox.layout().itemAt(2).layout()
        widget_layer_1 = stack.itemAt(1).widget()
        layout_1: QGridLayout = widget_layer_1.layout()
        pie_chart: TimePieChart = layout_1.itemAtPosition(1, 0).widget()
        colors_list = [QColor(str(each)) for each in colors]
        pie_chart.update_proportions(percentages, colors_list)

    def RQ_update_time_infobox(self, layer: int, data: list) -> None:
        stack: QStackedLayout = self.time_infobox.layout().itemAt(2).layout()
        match layer:
            case 0:
                # data = []
                stack.setCurrentIndex(0)
            case 1:
                # data = list[list[alias, timedelta, color]]
                widget_layer_1 = stack.itemAt(1).widget()
                layout_1: QGridLayout = widget_layer_1.layout()
                courses = data
                row_count = 3
                for each in courses:
                    item_1 = layout_1.itemAtPosition(row_count, 1)
                    item_2 = layout_1.itemAtPosition(row_count, 2)
                    if item_1 is not None and item_2 is not None:
                        item_1.widget().setText(str(each[0]))
                        item_2.widget().setText(str(each[1]))
                    else:
                        color = each[2]
                        label_color = QLabel()
                        label_color.setFixedWidth(4)
                        label_color.setStyleSheet(f'QLabel {{background: {color};}}')
                        label_alias = QLabel(str(each[0]))
                        label_time = QLabel(str(each[1]))
                        layout_1.addWidget(label_color, row_count, 0, 1, 1,
                                           alignment=Qt.AlignmentFlag.AlignLeft)
                        layout_1.addWidget(label_alias, row_count, 1, 1, 1,
                                    alignment=Qt.AlignmentFlag.AlignLeft)
                        layout_1.addWidget(label_time, row_count, 2, 1, 1,
                                    alignment=Qt.AlignmentFlag.AlignRight)
                    row_count += 1
                stack.setCurrentIndex(1)
            case 2:
                # data = list[alias, color, timestamp]
                layer_widget = stack.itemAt(2).widget()
                layer_widget.setStyleSheet(
                    f"#widget_single {{border-color: {data[1]};border-width"
                    f": 2px;border-style: dot-dot-dash;border-radius:10px;}}")
                grid: QGridLayout = layer_widget.layout()
                course_alias: QLabel = grid.itemAtPosition(1, 1).widget()
                course_alias.setText(data[0])
                started_time: QLabel = grid.itemAtPosition(2, 1).widget()
                started_time.setText(str(data[2]))
                stack.setCurrentIndex(2)
        stack.update()

    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        self._scroll_area.resize(self.size())
        return super().resizeEvent(a0)