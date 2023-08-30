from recognize import modules_recognizer, PinRecognizer
from PyQt5.QtWidgets import QMessageBox, QApplication
from dbms import DataManager
from GUI import MainWindow
from cameras import CameraBlinduino
import time, threading, sys


class Controller:
    def __init__(self):
        args = sys.argv[1:]  # Ignorar el primer elemento, que es el nombre del archivo .py
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        internet, camara = True, True
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
        self.pinsController = PinRecognizer()
        if self.pinsController.gamepad:
            self.thread = threading.Thread(target=self.update_pin_label)
            self.thread.start()
        else:
            self.gui.status_log("No será posible identificar los pines de la placa")
            return False

        try:
            self.base_datos = DataManager().query_all()
            self.error_datos = DataManager().query_status(404)
        except Exception:
            self.gui.status_log("ERROR: No hay conexión a internet. No será posible identificar los módulos Arduinos")
            return False

        try:
            self.camera = CameraBlinduino()
        except Exception:
            self.gui.status_log("ERROR: Camara no encontrada. No será posible identificar los módulos Arduinos")
            return False

        self.gui.detectButton.clicked.connect(self.take_photo)
        self.gui.status_log("Todo se ha realizado correctamente en la aplicación")
        return True

    def take_photo(self):
        rgb_frame = self.camera.capture(debug=self.debug_mode)
        try:
            module = self.reconocedor_img.read(rgb_frame)
            self.gui.module_detected(self.base_datos[module])
        except Exception:
            self.gui.module_detected(self.error_datos)

    def update_pin_label(self):
        available_pins = self.pinsController.nombre_pin.keys()
        while True:
            time.sleep(0.01)
            report = self.pinsController.gamepad.read(64)
            if report and report[1] in available_pins:
                self.gui.change_pin(self.pinsController.nombre_pin[report[1]])


if __name__ == '__main__':
    app = QApplication([])
    controller = Controller()
    window = controller.gui
    window.setWindowTitle('Blinduino')
    window.showMaximized()
    app.exec()
