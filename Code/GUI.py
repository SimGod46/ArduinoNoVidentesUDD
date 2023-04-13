
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
        elif event.key() == Qt.Key_Space:   
            self.detectButton.setFocus(Qt.OtherFocusReason)

    def get_resolution(self):
        size = self.size()
        ancho,alto = size.width(),size.height()
        self.resolucion = int((ancho**2 + alto**2)**(1/2))

    def font_adapter(self,c,pendiente=25):
        return str(int(c+pendiente*((self.resolucion-840)/1320)))     

    def resizeFont(self,widget, defaultSize, pendiente=25):
        current_style = widget.styleSheet()
        new_style = ";".join([f"\nfont:{self.font_adapter(defaultSize,pendiente)}pt" if "font" in estilo else estilo for estilo in current_style.split(";")])         
        return new_style
    
    def module_detected(self,msg):
            #self.font_adapter(28)
            self.nameModule.setText(msg[1])
            self.idModule.setText(msg[0])
            self.descriptionModule.setText(msg[4])
            self.pinModule.setText(msg[3])

    def changePin(self,msg):
        self.pinLabel.setText(msg)         

    def onResize(self, event):
        self.get_resolution()
        self.pinLabel.setStyleSheet(self.resizeFont(self.pinLabel,32))
        self.nameModule.setStyleSheet(self.resizeFont(self.nameModule,28))
        self.idModule.setStyleSheet(self.resizeFont(self.idModule,28))
        self.descriptionModule.setStyleSheet(self.resizeFont(self.descriptionModule,18,pendiente=10))
        self.pinModule.setStyleSheet(self.resizeFont(self.pinModule,20))
        self.detectButton.setStyleSheet(self.resizeFont(self.detectButton,28))



if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
