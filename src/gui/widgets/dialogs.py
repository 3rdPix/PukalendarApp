from qfluentwidgets import PrimaryPushButton
from PyQt6.QtWidgets import QVBoxLayout
from qfluentwidgets import PushButton
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import MessageBoxBase
from PyQt6.QtGui import QScreen
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout
from qfluentwidgets import CaptionLabel
from qfluentwidgets import LineEdit
from qfluentwidgets import ListWidget
from qfluentwidgets import ColorPickerButton
from PyQt6.QtGui import QColor
from random import randint
from gui import PukalendarWidget
from utils.i18n import _


class NewClassDialog(QWidget, PukalendarWidget):
    SG_NewClassDialog_search = pyqtSignal(str, name="SG_NewClassDialog_search")
    SG_NewClassDialog_create = pyqtSignal(int, str, str, name="SG_NewClassDialog_create")

    def __init__(self) -> None:
        super().__init__()
        self.init_gui()
        self.connect_signals()

    def init_gui(self) -> None:
        self.viewLayout = QVBoxLayout(self)

        # Bloque de búsqueda
        sub_layout1 = QHBoxLayout()
        search_label = CaptionLabel(text=_("Dialogs.NewClass.Search"))
        self.search_linedit = LineEdit(self)
        self.search_linedit.setClearButtonEnabled(True)
        self.search_linedit.setPlaceholderText(_("Dialogs.NewClass.SearchPlaceholder"))
        sub_layout1.addWidget(search_label)
        sub_layout1.addWidget(self.search_linedit)
        self.viewLayout.addLayout(sub_layout1)

        # Bloque de resultados
        self.search_result_view = ListWidget(self)
        self.viewLayout.addWidget(self.search_result_view)

        # Otros parámetros
        sub_layout2 = QHBoxLayout()
        alias_label = CaptionLabel(text=_("Dialogs.NewClass.Alias"))
        self.alias_linedit = LineEdit(self)
        self.alias_linedit.setClearButtonEnabled(True)
        self.alias_linedit.setPlaceholderText(_("Dialogs.NewClass.AliasPlaceholder"))
        self.alias_linedit.setEnabled(False)
        color_label = CaptionLabel(_("Dialogs.NewClass.Color"))
        self.color_selector = ColorPickerButton(
            QColor('#' + str(randint(100000, 999999))), _("Dialogs.NewClass.ColorDialog.Title"))
        self.color_selector.setEnabled(False)
        sub_layout2.addWidget(alias_label)
        sub_layout2.addWidget(self.alias_linedit)
        sub_layout2.addWidget(color_label)
        sub_layout2.addWidget(self.color_selector)
        self.viewLayout.addLayout(sub_layout2)

        # Opciones finales
        self.yesButton = PrimaryPushButton(self)
        self.yesButton.setText(_("Dialogs.NewClass.Confirm"))
        self.yesButton.setEnabled(False)
        self.cancelButton = PushButton(self)
        self.cancelButton.setText(_("Dialogs.NewClass.Cancel"))
        sub_layout3 = QHBoxLayout()
        sub_layout3.addWidget(self.yesButton)
        sub_layout3.addWidget(self.cancelButton)
        self.viewLayout.addLayout(sub_layout3)
        self.setMinimumSize(500, 600)

    def connect_signals(self) -> None:
        self.search_linedit.returnPressed.connect(
            self.search_for_puclass)
        self.search_result_view.itemClicked.connect(
            self._enable_buttons)
        self.alias_linedit.textChanged.connect(
            self._check_selection_completed)
        self.yesButton.pressed.connect(
            self.send_selection)
        self.cancelButton.pressed.connect(
            self._close)

    def _close(self) -> None:
        self.hide()
        self._clearinterface()

    def _enable_buttons(self) -> None:
        self.alias_linedit.setEnabled(True)
        self.color_selector.setEnabled(True)

    def _clearinterface(self) -> None:
        self.search_result_view.clear()
        self.search_linedit.clear()
        self.alias_linedit.clear()
        self.alias_linedit.setEnabled(False)
        self.color_selector.setEnabled(False)
        self.yesButton.setEnabled(False)

    def _check_selection_completed(self) -> None:
        if self.search_result_view.currentRow() == -1: return
        if self.alias_linedit.text() == '':
            self.yesButton.setEnabled(False)
            return
        self.yesButton.setEnabled(True)

    def show(self) -> None:
        self.color_selector.setColor(QColor('#' + str(randint(100000, 999999))))
        return super().show()

    #########################################################
    ###                     Enviar                        ###
    #########################################################

    def send_selection(self) -> None:
        self.SG_NewClassDialog_create.emit(
            self.search_result_view.currentRow(),
            self.alias_linedit.text(),
            self.color_selector.color.name())
        self._close()

    def search_for_puclass(self) -> None:
        self.search_result_view.setCurrentRow(-1)
        self.SG_NewClassDialog_search.emit(self.search_linedit.text())
    
    #########################################################
    ###                     Recibir                       ###
    #########################################################
        
    def RQ_web_search_result(self, course_list: list[dict]) -> None:
        self.search_result_view.clear()
        results: list[str] = list()
        for course_dict in course_list:
            presentation: str = '"'
            presentation += course_dict.get("official_name")
            presentation += "\" -"
            presentation += course_dict.get("official_section")
            presentation += ':'
            presentation += course_dict.get("official_professor")
            presentation += "  ("
            presentation += course_dict.get("official_code")
            presentation += ')'
            results.append(presentation)
        self.search_result_view.addItems(results)