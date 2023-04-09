from PyQt5 import QtWidgets
from GUI import MainWindow
from recognize import modules_recognizer,pin_recognizer
from dbms import data_manager
from cameras import camera
import time,threading
def text_format(text,text_size):
    return f'<html><head/><body><p align="center"><span style=" font-size:{text_size}pt;">{text}</span></p></body></html>'

class Controller:
    def __init__(self):
        try:             
            self.gui = MainWindow()
            self.gui.detectButton.clicked.connect(self.take_photo)
            self.camera = camera("GENERAL WEBCAM")            
            self.base_datos = data_manager()
            self.pinsController = pin_recognizer()
            self.reconocedor_img = modules_recognizer()

            self.thread = threading.Thread(target=self.update_pin_label)
            self.thread.start()
        except Exception as e:
            print(e)

    def take_photo(self):
            rgb_frame = self.camera.capture()
            module_detected= self.reconocedor_img.read(rgb_frame)
            print('Detectado: ',module_detected)
            query_rcv = self.base_datos.query_module(module_detected) #
            self.gui.nameModule.setText(text_format(query_rcv[1],"28"))
            self.gui.idModule.setText(text_format(query_rcv[0],"28"))
            self.gui.descriptionModule.setText(text_format(query_rcv[4],"24"))
            self.gui.pinModule.setText(text_format(query_rcv[3],"26"))

    def update_pin_label(self):
        if self.pinsController.gamepad:
            available_pins=self.pinsController.nombre_pin.keys()
            last_pin = ""
            while True:
                time.sleep(0.1)
                report = self.pinsController.gamepad.read(64)
                if report and report[1] in available_pins and self.pinsController.nombre_pin[report[1]] != last_pin:
                    last_pin = self.gui.pin_label.text()
                    self.gui.pinLabel.setText(self.pinsController.nombre_pin[report[1]])

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    controller = Controller()
    window = controller.gui
    window.show()
    app.exec()