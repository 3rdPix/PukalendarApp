from qfluentwidgets import MessageBoxBase
from PyQt6.QtGui import QScreen
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout
from qfluentwidgets import CaptionLabel
from qfluentwidgets import LineEdit
from qfluentwidgets import ListWidget
from qfluentwidgets import ColorPickerButton
from PyQt6.QtGui import QColor
from utils.i18n import _

class NewClassDialog(MessageBoxBase):
    SGsearch_for_puclass = pyqtSignal(str)
    SGselect_puclass = pyqtSignal(int, str, str)

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        pantalla: QScreen = QApplication.instance().primaryScreen()
        geometria = pantalla.geometry()
        dimension_x = round(geometria.width() * 0.6)
        dimension_y = round(geometria.height() * 0.6)
        self.resize(dimension_x, dimension_y)
        self.init_gui()
        self.connect_signals()
    
    def init_gui(self) -> None:
        # Search block
        sub_layout1 = QHBoxLayout()
        search_label = CaptionLabel(text=_("MainWindow.Courses.NewClassDialog.Search"))
        self.search_linedit = LineEdit(self)
        self.search_linedit.setClearButtonEnabled(True)
        self.search_linedit.setPlaceholderText(_("MainWindow.Courses.NewClassDialog.SearchPlaceholder"))
        sub_layout1.addWidget(search_label)
        sub_layout1.addWidget(self.search_linedit)
        self.viewLayout.addLayout(sub_layout1)

        # Results block
        self.search_result_view = ListWidget(self)
        self.viewLayout.addWidget(self.search_result_view)

        # Other parameters
        sub_layout2 = QHBoxLayout()
        alias_label = CaptionLabel(text=_("MainWindow.Courses.NewClassDialog.Alias"))
        self.alias_linedit = LineEdit(self)
        self.alias_linedit.setClearButtonEnabled(True)
        self.alias_linedit.setPlaceholderText(_("MainWindow.Courses.NewClassDialog.AliasPlaceholder"))
        self.alias_linedit.setEnabled(False)
        self.alias_linedit.setMaxLength(10)
        color_label = CaptionLabel(_("MainWindow.Courses.NewClassDialog.Color"))
        self.color_selector = ColorPickerButton(
            QColor('#5010aaa2'), _("MainWindow.Courses.NewClassDialog.ColorDialog.Title"))
        self.color_selector.setEnabled(False)
        sub_layout2.addWidget(alias_label)
        sub_layout2.addWidget(self.alias_linedit)
        sub_layout2.addWidget(color_label)
        sub_layout2.addWidget(self.color_selector)
        self.viewLayout.addLayout(sub_layout2)

        # final text
        self.yesButton.setText(_("MainWindow.Courses.NewClassDialog.Confirm"))
        self.yesButton.setEnabled(False)
        self.cancelButton.setText(_("MainWindow.Courses.NewClassDialog.Cancel"))

    def connect_signals(self) -> None:
        self.search_linedit.returnPressed.connect(
            self.search_for_puclass)
        
        self.search_result_view.itemClicked.connect(
            self._enable_buttons)
        
        self.alias_linedit.textChanged.connect(
            self._check_selection_completed)

        self.accepted.connect(
            self.send_selection)

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

    #########################################################
    ###                     Senders                       ###
    #########################################################

    def send_selection(self) -> None:
        self.SGselect_puclass.emit(
            self.search_result_view.currentRow(),
            self.alias_linedit.text(),
            self.color_selector.color.name())
        self._clearinterface()

    def search_for_puclass(self) -> None:
        self.search_result_view.setCurrentRow(-1)
        self.SGsearch_for_puclass.emit(self.search_linedit.text())
    
    #########################################################
    ###                     Listeners                     ###
    #########################################################
        
    def show_search_result(self, result_list: list[str]) -> None:
        self.search_result_view.clear()
        self.search_result_view.addItems(result_list)