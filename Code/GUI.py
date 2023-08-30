
from PyQt5 import uic, QtWidgets
from PyQt5.QtCore import Qt


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('blinduino.ui', self)
        self.resizeEvent = self.onResize

    def keyPressEvent(self, event):
        # Capturar el evento de teclado para la tecla "1"
        if event.key() == Qt.Key_1:
            self.nameModule.setFocus(Qt.OtherFocusReason)
        elif event.key() == Qt.Key_2:
            self.idModule.setFocus(Qt.OtherFocusReason)
        elif event.key() == Qt.Key_3:
            self.descriptionModule.setFocus(Qt.OtherFocusReason)
        elif event.key() == Qt.Key_4:
            self.pinModule.setFocus(Qt.OtherFocusReason)
        elif event.key() == Qt.Key_5:
            self.pinLabel.setFocus(Qt.OtherFocusReason)
        elif event.key() == Qt.Key_6:
            self.statusLog.setFocus(Qt.OtherFocusReason)
        elif event.key() == Qt.Key_7:
            self.refreshButton.setFocus(Qt.OtherFocusReason)
        elif event.key() == Qt.Key_Space:
            self.detectButton.setFocus(Qt.OtherFocusReason)

    def get_resolution(self):
        size = self.size()
        ancho, alto = size.width(), size.height()
        self.resolucion = int((ancho**2 + alto**2)**(1/2))

    def font_adapter(self, c, pendiente=25):
        return str(int(c+pendiente*((self.resolucion-840)/1320)))     

    def resize_font(self, widget, default_size, pendiente=25):
        current_style = widget.styleSheet()
        new_style = ";".join([f"\nfont:{self.font_adapter(default_size,pendiente)}pt"
                              if "font" in estilo else estilo
                              for estilo in current_style.split(";")])
        return new_style
    
    def module_detected(self, msg):
        self.idModule.setText(msg[0])
        self.nameModule.setText(msg[1])
        self.pinModule.setText(msg[3])
        self.descriptionModule.setText(msg[4])

    def status_log(self, msg):
        self.statusLog.setText(msg)

    def change_pin(self, msg):
        self.pinLabel.setText(msg)         

    def onResize(self, event):
        self.get_resolution()
        self.pinLabel.setStyleSheet(self.resize_font(self.pinLabel, 32))
        self.nameModule.setStyleSheet(self.resize_font(self.nameModule, 28))
        self.idModule.setStyleSheet(self.resize_font(self.idModule, 28))
        self.descriptionModule.setStyleSheet(self.resize_font(self.descriptionModule, 18, pendiente=10))
        self.pinModule.setStyleSheet(self.resize_font(self.pinModule, 20))
        self.detectButton.setStyleSheet(self.resize_font(self.detectButton, 28))
        self.refreshButton.setStyleSheet(self.resize_font(self.refreshButton, 28))
        self.statusLog.setStyleSheet(self.resize_font(self.statusLog, 7, pendiente=15))


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
