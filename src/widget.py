# This Python file uses the following encoding: utf-8
import sys

from enum import Enum

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication, QWidget

from ui_widget import Ui_Widget
from rsa_lib import generate_keys, encrypt, decrypt


class EncryptionMode(Enum):
    encode = 0
    decode = 1


class Widget(QWidget):
    def __init__(self):
        super(Widget, self).__init__()
        self.ui = Ui_Widget()
        self.ui.setupUi(self)

        self.encryption_mode = EncryptionMode.encode
        self.ui.encodeRadioButton.setChecked(True)
        self.ui.convertButton.setDisabled(True)
        self.setup_connections()

    def setup_connections(self):
        self.ui.encodeRadioButton.clicked.connect(self.set_encode_mode)
        self.ui.decodeRadioButton.clicked.connect(self.set_decode_mode)
        self.ui.input.textChanged.connect(self.toggle_convert_button)
        self.ui.convertButton.clicked.connect(self.convert_button)
        self.ui.generateButton.clicked.connect(self.generate_button)

    @QtCore.Slot()
    def set_encode_mode(self):
        self.encryption_mode = EncryptionMode.encode

    @QtCore.Slot()
    def set_decode_mode(self):
        self.encryption_mode = EncryptionMode.decode

    @QtCore.Slot()
    def toggle_convert_button(self):
        if not self.ui.input.toPlainText():
            self.ui.convertButton.setDisabled(True)
        elif self.ui.eLineEdit.text():
            self.ui.convertButton.setDisabled(False)

    @QtCore.Slot()
    def convert_button(self):
        msg = self.ui.input.toPlainText()
        match self.encryption_mode:
            case EncryptionMode.encode:
                msg = encrypt(self.e, self.n, msg)
                self.ui.output.setPlainText(msg)
            case EncryptionMode.decode:
                msg = decrypt(self.d, self.n, msg)
                self.ui.output.setPlainText(msg)

    @QtCore.Slot()
    def generate_button(self):
        self.e, self.n, self.d = generate_keys(31)

        self.ui.eLineEdit.setText(str(self.e))
        self.ui.nLineEdit.setText(str(self.n))
        self.ui.dLineEdit.setText(str(self.d))
        self.ui.nLineEdit_2.setText(str(self.n))

        if self.ui.input.toPlainText():
            self.ui.convertButton.setDisabled(False)


if __name__ == "__main__":
    app = QApplication([])
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
