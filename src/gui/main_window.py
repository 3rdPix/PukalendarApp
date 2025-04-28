"""@private"""
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtBoundSignal
from qfluentwidgets import InfoBar
from qfluentwidgets import InfoBarPosition
import inspect
from PyQt6.QtCore import QObject
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import MSFluentWindow
from qfluentwidgets import NavigationItemPosition
from config import PUCalendarAppPaths as pt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtGui import QIcon
from utils.i18n import _
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import TeachingTipTailPosition
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from qfluentwidgets import TeachingTipView
from qfluentwidgets import PushButton
from qfluentwidgets import TeachingTip
from gui.tabs_views import HomeView
from gui.tabs_views import CalendarView
from gui.tabs_views import CoursesView
from gui.tabs_views import AgendaView
from qfluentwidgets import SplashScreen
from PyQt6.QtCore import QEventLoop
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import QRect
from gui import PukalendarWidget
from collections import defaultdict
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QVBoxLayout
from qfluentwidgets import PopUpAniStackedWidget
from PyQt6.QtWidgets import QLayout
from PyQt6.QtWidgets import QScrollArea
from qfluentwidgets.components.widgets.card_widget import CardSeparator
from qfluentwidgets import NavigationBar


log = logging.getLogger("MainWindow")

class MainWindow(QMainWindow):
    SG_MainWindow_closeEvent: pyqtSignal = pyqtSignal(QRect, name="SG_MainWindow_closeEvent")

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("MainWindow")
        self.initialize_user_interface()
        self._init_self()
        self.show()

    def initialize_user_interface(self) -> None:
        blind_widget = QWidget(); self.setCentralWidget(blind_widget)
        self.window_layout = QHBoxLayout(blind_widget)
        self.content_container = PopUpAniStackedWidget(self)
        self.window_layout.addWidget(self.content_container, stretch=1)
        # self.navigation_bar = QFrame(self, Qt.WindowType.Tool)
        self.navigation_bar = NavigationBar(self)
        self.window_layout.addWidget(self.navigation_bar, stretch=0)

        # Setup navigation bar
        # self.navigation_bar.setLayout(QVBoxLayout(self.navigation_bar))
        # self.navigation_bar.first_sector = QVBoxLayout(self.navigation_bar)
        # self.navigation_bar.second_sector = QScrollArea(self.navigation_bar)
        # self.navigation_bar.third_sector = QVBoxLayout(self.navigation_bar)
        # self.navigation_bar.layout().addChildLayout(self.navigation_bar.first_sector)
        # self.navigation_bar.layout().addWidget(CardSeparator())
        # self.navigation_bar.layout().addWidget(self.navigation_bar.second_sector)
        # self.navigation_bar.layout().addWidget(CardSeparator())
        # self.navigation_bar.layout().addChildLayout(self.navigation_bar.third_sector)

    def insert_section(self, content: QWidget|QLayout, name: str,
                       icon: QIcon|None=None, sector: int=1) -> None:
        blind_widget = content
        if isinstance(content, QLayout):
            blind_widget = QWidget(); blind_widget.setLayout(content)
        self.content_container.addWidget(blind_widget)
        match sector:
            case 1: button_position = NavigationItemPosition.TOP
            case 2: button_position = NavigationItemPosition.SCROLL
            case 3: button_position = NavigationItemPosition.BOTTOM
            case _: raise ValueError("Not a valid NavigationItemPosition")
        self.navigation_bar.addItem(
            routeKey=content.objectName(),
            icon=icon,
            text=name,
            position=button_position,
            onClick=lambda: self.content_container.setCurrentWidget(blind_widget))
        
    def RQ_finished_loading(self) -> None:
        pass
    
    def _load_self_variables(self) -> None:
        """
        Inicializa las variables propias de la instancia de la ventana
        """
        self.__pkwdgts__: dict[str, PukalendarWidget] = defaultdict()
        self.__showing_about: bool = False

    def _init_self(self) -> None:
        """
        Carga los contenidos propios de la ventana principal
        """
        self._load_self_variables()
        self.setWindowIcon(QIcon(pt.Resources.APPLICATION_ICON))
        try:
            with open(pt.Qss.MAIN_WINDOW, 'r', encoding='utf-8') as raw_file:
                self.setStyleSheet(raw_file.read())
        except FileNotFoundError:
            log.error(f"Loading of {pt.Qss.MAIN_WINDOW} could not be resolved")
        self.setWindowTitle(_("MainWindow.Title"))
        icon_about_normal: QIcon = QIcon(pt.Resources.ICON_ABOUT_NORMAL)
        self.navigation_bar.addItem(
            routeKey='about_app',
            icon=icon_about_normal,
            text=_("MainWindow.NavigationInterface.About"),
            onClick=self.show_about_bubble,
            selectable=False,
            position=NavigationItemPosition.BOTTOM)
        self._add_subinterfaces()

    def _add_subinterfaces(self) -> None:
        """
        Añade las pestañas a la navegación para su posterior despliegue
        """
        self.home_view = HomeView()
        self.__pkwdgts__.__setitem__(self.home_view.objectName(), self.home_view)
        icon_home_normal: QIcon = QIcon(pt.Resources.ICON_HOME_NORMAL)
        icon_home_selected: QIcon = QIcon(pt.Resources.ICON_HOME_SELECTED)
        self.insert_section(self.home_view,
                            _("MainWindow.NavigationInterface.Home"),
                            icon_home_normal)
        self.agenda_view = AgendaView()
        self.__pkwdgts__.__setitem__(self.agenda_view.objectName(), self.agenda_view)
        icon_todo_normal: QIcon = QIcon(pt.Resources.ICON_TODO_NORMAL)
        icon_todo_selected: QIcon = QIcon(pt.Resources.ICON_TODO_SELECTED)
        self.insert_section(self.agenda_view,
                            _("MainWindow.NavigationInterface.Agenda"),
                            icon_todo_normal)
        self.courses_view = CoursesView(parent=self)
        self.__pkwdgts__.__setitem__(self.courses_view.objectName(), self.courses_view)
        icon_courses_normal: QIcon = QIcon(pt.Resources.ICON_COURSES_NORMAL)
        icon_courses_selected: QIcon = QIcon(pt.Resources.ICON_COURSES_SELECTED)
        self.insert_section(self.courses_view,
                            _("MainWindow.NavigationInterface.Courses"),
                            icon_courses_normal)
        self.calendar_view = CalendarView()
        self.__pkwdgts__.__setitem__(self.calendar_view.objectName(), self.calendar_view)
        icon_calendar_normal: QIcon = QIcon(pt.Resources.ICON_CALENDAR_NORMAL)
        icon_calendar_selected: QIcon = QIcon(pt.Resources.ICON_CALENDAR_SELECTED)
        self.insert_section(self.calendar_view,
                            _("MainWindow.NavigationInterface.Calendar"),
                            icon_calendar_normal)
    
    # Feo pero hace el trabajo por ahora
    def show_about_bubble(self) -> None:
        if self.__showing_about: return
        self.__showing_about = True
        tail_position = TeachingTipTailPosition.LEFT_BOTTOM
        image = QPixmap(pt.Resources.DIALOG_ABOUT_IMAGE)
        bubble = TeachingTipView(
            title=_("MainWindow.About.Title"),
            content=_("MainWindow.About.Description"),
            image=image,
            isClosable=True,
            tailPosition=tail_position,
            parent=self)
        # no creo necesitar otro texto para el botón
        github_button = PushButton(FIF.GITHUB, 'GitHub')
        bubble.addWidget(github_button, align=Qt.AlignmentFlag.AlignRight)
        panel = TeachingTip.make(
            bubble,
            self.navigationInterface,
            duration=-1,
            tailPosition=tail_position,
            parent=self)    
        bubble.closed.connect(
            lambda: self.hide_about_bubble(panel))
        
    def hide_about_bubble(self, panel: TeachingTip) -> bool:
        self.__showing_about = False
        return panel.close()
    
    def RQ_window_setting(self, window_setting: QRect) -> None:
        self.setGeometry(window_setting)
        # QApplication.processEvents()
    
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.SG_MainWindow_closeEvent.emit(self.geometry())
        return super().closeEvent(a0)
    
    def RQ_show_error_bar(self, title: str, content: str = '') -> None:
        InfoBar.error(title=title, content=content,
                      orient=Qt.Orientation.Horizontal, isClosable=True,
                      position=InfoBarPosition.TOP_RIGHT, duration=-1,
                      parent=self)