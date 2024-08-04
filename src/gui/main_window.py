from PyQt6.QtCore import QRect
from qfluentwidgets import MSFluentWindow
from qfluentwidgets import NavigationItemPosition
from config.static_paths import ApplicationPaths
from config.static_paths import PathKey
from PyQt6.QtGui import QCloseEvent, QIcon
from utils.i18n import _
from config.text_keys import TextKey
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
from json import dump
from json import load
from json import JSONDecodeError
from PyQt6.QtCore import QSize
from PyQt6.QtCore import QPoint

class MainWindow(MSFluentWindow):
    """
    Clase de la ventana principal de la aplicación sobre la
    que se despliegan todas las vistas y sub-widgets
    """



    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName('MainWindow')
        self.splash_screen = SplashScreen(
            ApplicationPaths.get_path(PathKey.APPLICATION_ICON), self)
        self.show()
        self._init_self()
        
        # Le compraré tiempo intencionalmente al splash para que se aprecie
        # Lo más probable es que una vez la aplicación esté más avanzada no
        # sea necesario comprarle nada, y logre solo
        self.loopear_3_sec()
        self.splash_screen.finish()

    def show(self) -> None:
        try:
            with open(ApplicationPaths.get_path(PathKey.USER_WINDOW_STATUS), 'r') as raw_file:
                status: dict = load(raw_file)
                self.move(status.get('x'), status.get('y'))
                self.resize(status.get('w'), status.get('h'))
        except FileNotFoundError:
            pass
        except JSONDecodeError:
            # Archivo vacío
            pass
        return super().show()

    def loopear_3_sec(self) -> None:
        loop = QEventLoop(self)
        QTimer.singleShot(3000, loop.quit)
        loop.exec()
    
    def _init_self(self) -> None:
        """
        Carga los contenidos propios de la ventana principal
        """
        self._load_self_variables()
        self.setWindowIcon(QIcon(ApplicationPaths.get_path(
            PathKey.APPLICATION_ICON)))
        try:
            with open(ApplicationPaths.get_path(PathKey.QSS_MAIN_WINDOW),
                       'r', encoding='utf-8') as raw_file:
                self.setStyleSheet(raw_file.read())
        except FileNotFoundError:
            print(f'[ERROR] loading {ApplicationPaths.get_path(PathKey.QSS_MAIN_WINDOW)}')
        self.setWindowTitle(_(TextKey.WINDOW_TITLE))
        self.navigationInterface.addItem(
            routeKey='about_app',
            icon=FIF.HELP,
            text=_(TextKey.ABOUT_LABEL),
            onClick=self.show_about_bubble,
            selectable=False,
            position=NavigationItemPosition.BOTTOM)
        self._add_subinterfaces()
        
    def _add_subinterfaces(self) -> None:
        """
        Añade las pestañas a la navegación para su posterior despliegue
        """
        self.addSubInterface(
            HomeView(), FIF.HOME, _(TextKey.HOME_LABEL), FIF.HOME_FILL)
        self.addSubInterface(
            AgendaView(), FIF.TAG, _(TextKey.AGENDA_LABEL), FIF.CHECKBOX)
        self.addSubInterface(
            CoursesView(), FIF.LIBRARY,
            _(TextKey.COURSES_LABEL), FIF.LIBRARY_FILL)
        self.addSubInterface(
            CalendarView(), FIF.CALENDAR, _(TextKey.CALENDAR_LABEL))

    def _load_self_variables(self) -> None:
        """
        Inicializa las variables propias de la instancia de la ventana
        """
        self.__showing_about: bool = False

    # Feo pero hace el trabajo por ahora
    def show_about_bubble(self) -> None:
        if self.__showing_about: return
        self.__showing_about = True
        tail_position = TeachingTipTailPosition.LEFT_BOTTOM
        image = QPixmap(ApplicationPaths.get_path(PathKey.ABOUT_BUBBLE_IMAGE))
        bubble = TeachingTipView(
            title=_(TextKey.ABOUT_LABEL),
            content=_(TextKey.ABOUT_DESCRIPTION),
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
    
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        current_win_size: QSize = self.size()
        current_win_pos: QPoint = self.mapToGlobal(self.pos())
        print(current_win_pos, current_win_pos.x(), current_win_pos.y())
        with open(ApplicationPaths.get_path(PathKey.USER_WINDOW_STATUS), 'w') as raw_file:
            dump({'x': current_win_pos.x(),
                  'y': current_win_pos.y(),
                  'h': current_win_size.height(),
                  'w': current_win_size.width()},
                  raw_file)
        return super().closeEvent(a0)