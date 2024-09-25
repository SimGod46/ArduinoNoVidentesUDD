from recognize import modules_recognizer
from PyQt5.QtWidgets import QMessageBox, QApplication
from dbms import DataManager
from GUI import MainWindow
from cameras import CameraBlinduino
import sys

class Controller:
    def __init__(self):
        args = sys.argv[1:]  # Ignorar el primer elemento, que es el nombre del archivo .py
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        self.camera_state = False

        if "-d" in args:
            self.debug_mode = True
        else:
            self.debug_mode = False

        try:
            self.gui = MainWindow()
            self.gui.refreshButton.clicked.connect(self.refresh_status)
            self.reconocedor_img = modules_recognizer()
            self.refresh_status()

        except Exception as error:
            msg.setWindowTitle("ERROR")
            msg.setText(error)
            x = msg.exec_()

    def refresh_status(self):
        self.gui.module_detected(("ID", "NOMBRE", "", "PINES", "DESCRIPCIÓN"))    

        try:
            self.base_datos = DataManager().query_all()
            self.error_datos = DataManager().query_status(404)
        except Exception as e:
            self.gui.status_log("ERROR: No hay conexión a internet. No será posible identificar los módulos de Arduino")
            print(e)
            return False

        try:
            if not self.camera_state:
                self.camera = CameraBlinduino()
                self.camera_state = True
        except Exception as e:
            self.camera_state = False
            self.gui.status_log("ERROR: Camara no encontrada. No será posible identificar los módulos de Arduino")
            print(e)
            return False

        self.gui.detectButton.clicked.connect(self.take_photo)
        self.gui.status_log("Todo se ha realizado correctamente en la aplicación")
        return True

    def take_photo(self):
        try:
            rgb_frame = self.camera.capture(debug=self.debug_mode)
            module = self.reconocedor_img.read(rgb_frame)
            self.gui.module_detected(self.base_datos[module])
        except Exception as e:
            print(e)
            self.gui.module_detected(self.error_datos)


if __name__ == '__main__':
    app = QApplication([])
    controller = Controller()
    window = controller.gui
    window.setWindowTitle('Blinduino')
    window.showMaximized()
    app.exec()