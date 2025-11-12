from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtCore import QObject
from PyQt6.QtCore import QThread
from PyQt6.QtCore import QTimer
from datetime import timedelta
from datetime import datetime
from common import PukalendarWidget
from common.entities import StudySession


class CollidingSessionError(Exception): ...
class UninitializedSessionError(Exception): ...


class TimerWorker(QObject):
    time_updated = pyqtSignal(timedelta)
    _qtimer: QTimer|None = None
    def __init__(self, parent: QObject|None=None):
      super().__init__(parent)
      self._elapsed_time = timedelta(seconds=0)
      self._one_second = timedelta(seconds=1)

    @pyqtSlot()
    def _update_time(self) -> None:
      self._elapsed_time += self._one_second
      self.time_updated.emit(self._elapsed_time)

    @pyqtSlot()
    def start_timing(self) -> None:
      if self._qtimer is None:
        self._qtimer = QTimer(parent=self)
        self._qtimer.timeout.connect(self._update_time)
      if not self._qtimer.isActive():
        self._qtimer.start(1000)

    @pyqtSlot()
    def stop_timer(self) -> None:
      assert self._qtimer
      self._qtimer.stop()

    @property
    def working(self) -> bool:
      assert self._qtimer
      return self._qtimer.isActive()

class SessionController(QObject, PukalendarWidget):
  SG_active_session_time_changed = pyqtSignal(timedelta)
  __SG_stop_session = pyqtSignal()
  def __init__(self, parent: QObject) -> None:
    super().__init__(parent)
    self._session_is_active = False
    self._course_in_session: int|None = None

  def start_session(self, course_identifier: int) -> None:
    if self.in_session:
      raise CollidingSessionError(
        f"Tried starting session for {course_identifier}"
        f" when {self.course_in_session} is already in one.")
    self._starting_time = datetime.now()
    self._timer_thread = QThread()
    self._worker = TimerWorker()
    self._worker.time_updated.connect(self.SG_active_session_time_changed.emit)
    self._worker.moveToThread(self._timer_thread)
    self._timer_thread.started.connect(self._worker.start_timing)
    self._timer_thread.finished.connect(self._worker.deleteLater)
    self.__SG_stop_session.connect(self._worker.stop_timer)
    self._timer_thread.start()
    self._session_is_active = True
    self._course_in_session = course_identifier

  def stop_session(self) -> StudySession:
    if not self.in_session:
      raise UninitializedSessionError(
        "Tried to end session while no session is running.")
    assert self.course_in_session
    ended_session = StudySession(
      inscripcion_id=self.course_in_session,
      fecha_inicio=self._starting_time,
      fecha_fin=datetime.now())
    self._session_is_active = False
    self._course_in_session = None
    self.__SG_stop_session.emit()
    self._timer_thread.quit()
    self._timer_thread.wait()
    del self._timer_thread
    del self._worker
    del self._starting_time
    return ended_session

  @property
  def in_session(self) -> bool:
    return self._session_is_active and self._worker.working

  @property
  def course_in_session(self) -> int|None:
    return self._course_in_session