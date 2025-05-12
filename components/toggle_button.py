from PySide6.QtWidgets import QAbstractButton
from PySide6.QtCore import Qt, QRectF, QPropertyAnimation, QSize, Property
from PySide6.QtGui import QPainter, QColor, QBrush


class ToggleButton(QAbstractButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self._thumb_radius = 12
        self._track_margin = 3
        self._track_color = QColor("#ccc")
        self._thumb_color = QColor("#fff")
        self._on_color = QColor("#2ecc71")

        self._anim = QPropertyAnimation(self, b"offset", self)
        self._anim.setDuration(200)
        self._offset = 0

        self.toggled.connect(self.start_transition)

    def sizeHint(self):
        return QSize(50, 25)

    def start_transition(self, checked):
        self._anim.stop()
        start = self._offset
        end = self.width() - self._thumb_radius * 2 - self._track_margin * 2 if checked else 0
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)
        self._anim.start()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        track_rect = QRectF(0, 0, self.width(), self.height())
        p.setBrush(QBrush(self._on_color if self.isChecked() else self._track_color))
        p.setPen(Qt.NoPen)
        p.drawRoundedRect(track_rect, self.height()/2, self.height()/2)

        thumb_rect = QRectF(self._track_margin + self._offset,
                            self._track_margin,
                            self._thumb_radius * 2,
                            self._thumb_radius * 2)
        p.setBrush(QBrush(self._thumb_color))
        p.drawEllipse(thumb_rect)

    def setOffset(self, value):
        self._offset = value
        self.update()

    def getOffset(self):
        if hasattr(self, "_offset"):
            return self._offset

    offset = Property(float, getOffset, setOffset)
