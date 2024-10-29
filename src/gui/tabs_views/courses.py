
from config import PUCalendarAppPaths as pt
from gui.widgets.boxes import SingleClassCategoryBox
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QGridLayout
from qfluentwidgets import FlowLayout
from gui.widgets.boxes import AllClassesClassBox
from qfluentwidgets import SubtitleLabel
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import Action
from qfluentwidgets import CommandBar
from qfluentwidgets import FluentIcon as FIF
from utils.i18n import _
from qfluentwidgets.components.widgets.card_widget import CardSeparator
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from qfluentwidgets import PrimaryToolButton
from gui.widgets.dialogs import NewClassDialog
from gui.widgets.misc import OpacityAniStackedWidget


class CoursesView(QFrame):
    new_class_dialog: NewClassDialog

    def __init__(self, parent: QWidget | None=None) -> None:
        super().__init__(parent)
        self.setObjectName('courses_view')
        self._create_layout()
        self._create_layers()
        self.new_class_dialog = NewClassDialog()

    def _create_layout(self) -> None:
        """
        Preparación de la interfaz de la pestaña
        """
        tab_layout: QVBoxLayout = QVBoxLayout(self)
        command_bar: CommandBar = CommandBar(self)
        command_bar.setToolButtonStyle(
            Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        command_bar.addActions(self._create_command_bar_actions())
        tab_layout.addWidget(command_bar)
        tab_layout.addWidget(CardSeparator())
        self._stacked_area: OpacityAniStackedWidget = \
            OpacityAniStackedWidget()
        tab_layout.addWidget(self._stacked_area)

    def _create_command_bar_actions(self) -> list[Action]:
        actions: list = list()

        add_new = Action(FIF.ADD, _("MainWindow.Courses.CommandBar.AddNew"))
        add_new.triggered.connect(self._CB_add_new)
        actions.append(add_new)

        delete_puclass = Action(FIF.DELETE, _("MainWindow.Courses.CommandBar.Delete"))
        delete_puclass.triggered.connect(self._CB_del)
        actions.append(delete_puclass)

        edit_puclass = Action(FIF.EDIT, _("MainWindow.Courses.CommandBar.Edit"))
        edit_puclass.triggered.connect(self._CB_edit)
        actions.append(edit_puclass)

        set_scale = Action(FIF.IOT, _("MainWindow.Courses.CommandBar.Scale"))
        set_scale.triggered.connect(self._CB_scale)
        actions.append(set_scale)

        return actions
    
    def _CB_add_new(self) -> None:
        # Es mejor que sea una ventana propia
        self.new_class_dialog.show()

    def _CB_del(self) -> None:
        pass

    def _CB_edit(self) -> None:
        pass

    def _CB_scale(self) -> None:
        pass

    def _create_layers(self) -> None:
        """
        Crea las capas del widget apilado
        La primera capa corresponde a información vacía cuando el usuario
        no tiene cursos agregados
        La segunda capa corresponde a la vista de todas las clases
        La tercera capa corresponde a información específica de una clase
        seleccionada
        """

        # Primera capa puede ser creada acá
        no_puclass_layer = QWidget()
        icon = QLabel()
        icon.setPixmap(QPixmap(pt.Resources.VIEW_COURSES_NO_BOOK))
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle = SubtitleLabel(_("MainWindow.Courses.NoClassView.NoClass"))
        subtitle.setWordWrap(True)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout(no_puclass_layer)
        layout.addStretch()
        layout.addWidget(icon)
        layout.addWidget(subtitle)
        layout.addStretch()
        self._stacked_area.addWidget(no_puclass_layer)

        # Capa 2 
        self._all_classes_view: AllClassesView = AllClassesView()
        self._stacked_area.addWidget(self._all_classes_view)

        # Capa 3
        self._single_class_view: SingleClassView = SingleClassView()
        self._stacked_area.addWidget(self._single_class_view)

    def RQ_update_courses(self, courses_list: list[dict]) -> None:
        self._all_classes_view.clear()
        for course in courses_list:
            alias = course.get("user_alias")
            color = course.get("user_color")
            self._all_classes_view.add_class(alias, color, course)
        # ¿? Automáticamente mostrar segunda capa
        self._stacked_area.setCurrentIndex(
            1 if self._all_classes_view.has_items else 0)
        # Al parecer tiene problemas si se pierde el foco
        self.setFocus()

        """
        BORRAR
        """
        # self._stacked_area.setCurrentIndex(2)
        #for i in range(11):
        #    self._all_classes_view.add_class('curso', '#' + str(randint(100000, 999999)))

class AllClassesView(QFrame):

    def __init__(self) -> None:
        super().__init__(flags=Qt.WindowType.FramelessWindowHint)
        self._flow_container: FlowLayout = FlowLayout(self, True)

    def add_class(self, alias: str, color: str, data: dict={}) -> None:
        new_box: AllClassesClassBox = AllClassesClassBox()
        new_box.set_class_alias(alias)
        new_box.set_class_color(color)
        new_box.load_data(data)
        self._flow_container.addWidget(new_box)
    
    def read_container(self) -> bool:
        return bool(self._flow_container._items)
    
    has_items = property(read_container)

    def clear(self) -> None:
        self._flow_container.takeAllWidgets()

class SingleClassView(QFrame):
    """
    Desplegamos las categorías
     - Información general
     - Horario
     - Calificaciones
     - Eventos / Tareas / Pendientes
    """

    def __init__(self) -> None:
        super().__init__(flags=Qt.WindowType.FramelessWindowHint)
        self._load_view()

    def _load_view(self) -> None:
        """
        <- [color] Nombre [color]
        --------------------------
              [general][horario]
              [calificaciones][eventos]
        """
        first_layout: QVBoxLayout = QVBoxLayout(self)
        top_layout: QHBoxLayout = QHBoxLayout()
        self._return_button: PrimaryToolButton = PrimaryToolButton(FIF.RETURN, self)
        self._left_stripe = QLabel()
        self._name_label = SubtitleLabel()
        self._right_stripe = QLabel()
        top_layout.addWidget(self._return_button)
        top_layout.addWidget(self._left_stripe)
        top_layout.addWidget(self._name_label)
        top_layout.addWidget(self._right_stripe)
        first_layout.addLayout(top_layout, 0)
        first_layout.addWidget(CardSeparator(), 0)

        bottom_layout: QGridLayout = QGridLayout()
        self._generic_cat_box: SingleClassCategoryBox = SingleClassCategoryBox()
        self._schedule_cat_box: SingleClassCategoryBox = SingleClassCategoryBox()
        self._grades_cat_box: SingleClassCategoryBox = SingleClassCategoryBox()
        self._events_cat_box: SingleClassCategoryBox = SingleClassCategoryBox()
        bottom_layout.addWidget(self._generic_cat_box, 0, 0)
        bottom_layout.addWidget(self._schedule_cat_box, 0, 1)
        bottom_layout.addWidget(self._grades_cat_box, 1, 0)
        bottom_layout.addWidget(self._events_cat_box, 1, 1)
        first_layout.addLayout(bottom_layout, 1)

    def load_data(self, class_data: object) -> None:
        """
        Recibe @dataclass con toda la información del curso a desplegar
        """
        pass

    def _set_stripe_color(self, color: str) -> None:
        # Usar hexadecimal #xxxxxx
        self._left_stripe.setStyleSheet(f'QLabel {{background: {color};}}')
        self._right_stripe.setStyleSheet(f'QLabel {{background: {color};}}')