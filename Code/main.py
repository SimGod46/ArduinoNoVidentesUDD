from PyQt5 import QtWidgets
from GUI import MainWindow
from recognize import modules_recognizer,pin_recognizer
from dbms import data_manager
from cameras import camera
import time,threading,sys

class Controller:
    def __init__(self):
        try:           
            args = sys.argv[1:] # Ignorar el primer elemento, que es el nombre del archivo .py
            if "-d" in args:
                self.debug_mode = True
            else:
                self.debug_mode = False            
            self.camera = camera()             
            self.gui = MainWindow()
            self.gui.detectButton.clicked.connect(self.take_photo)
            self.base_datos = data_manager()
            self.pinsController = pin_recognizer()
            self.reconocedor_img = modules_recognizer()

            self.thread = threading.Thread(target=self.update_pin_label)
            self.thread.start()
        except Exception as e:
            print(e)

    def take_photo(self):
            rgb_frame = self.camera.capture(debug=self.debug_mode)
            module= self.reconocedor_img.read(rgb_frame)
            print('Detectado: ',module)
            query_rcv = self.base_datos.query_module(module)
            self.gui.module_detected(query_rcv)


    def update_pin_label(self):
        if self.pinsController.gamepad:
            available_pins=self.pinsController.nombre_pin.keys()
            last_pin = ""
            while True:
                time.sleep(0.1)
                report = self.pinsController.gamepad.read(64)
                if report and report[1] in available_pins and self.pinsController.nombre_pin[report[1]] != last_pin:
                    last_pin = self.gui.pinLabel.text()
                    self.gui.changePin(self.pinsController.nombre_pin[report[1]])

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    controller = Controller()
    window = controller.gui
    window.setWindowTitle('Blinduino')
    window.showMaximized()
    app.exec()