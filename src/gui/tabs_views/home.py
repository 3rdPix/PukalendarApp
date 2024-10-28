from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QWidget
from gui.widgets import HomeViewInfoBox
from qfluentwidgets import ScrollArea
from qfluentwidgets import FlowLayout
from PyQt6.QtCore import QEasingCurve
from config import PUCalendarAppPaths as pt
from utils.i18n import _

class HomeView(QFrame):
    
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
            print(f'[ERROR] Couldn\'t find stylesheet for {self}')

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
        return self.time_infobox
    
    def resizeEvent(self, a0: QResizeEvent | None) -> None:
        self._scroll_area.resize(self.size())
        return super().resizeEvent(a0)