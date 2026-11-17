from PySide6.QtCore import Qt, QPoint
from PySide6.QtWidgets import (
    QDialog, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLayout
)


class FilterAlertDialog(QDialog):
    def __init__(self, abp_percent_removed, cbfv_percent_removed, target, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        layout = QVBoxLayout(self)
        self.setFixedSize(target.size())
        self.move(target.mapToGlobal(QPoint(0, 0)))
        self.setStyleSheet(
            "background-color: black; "
            "color: rgb(152, 152, 152);; "
            "border: 0.5px solid rgb(152, 152, 152);;"
        )

        message = QLabel(
            "The selected filter will alter:\n\n"
            f"ABP: {abp_percent_removed:.1f}%\n"
            f"CBFV: {cbfv_percent_removed:.1f}%\n\n"
            "Do you want to proceed?"
        )
        message.setWordWrap(True)
        message.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(message)

        self.cancel_button = QPushButton("Cancel")
        self.proceed_button = QPushButton("Proceed")
        self.proceed_button.setStyleSheet("color: rgb(0,255,0);")

        self.cancel_button.setFixedSize(100, 30)
        self.proceed_button.setFixedSize(100, 30)

        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self.cancel_button)
        buttons.addWidget(self.proceed_button)
        layout.addLayout(buttons)

        self.cancel_button.clicked.connect(self.reject)
        self.proceed_button.clicked.connect(self.accept)
