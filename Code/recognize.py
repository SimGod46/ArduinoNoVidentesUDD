import hid
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
class modules_recognizer:
    def __init__(self):
        self.classes_names = ['HC-SR04', 'DHT-11', 'ldr', 'KY-023', 'KY-012']
        self.model = load_model("AIvidentes.h5")
    def read(self,frame):
#        img = image.load_img(path, target_size=(224, 224))
        x = img_to_array(frame)
        x = np.expand_dims(x, axis=0)
        image_tensor = np.vstack([x])
        classes = self.model.predict(image_tensor)
        listed_clas = []
        for i in classes[0]:
            listed_clas.append(i)
        prediccion = max(listed_clas)
        prediccion = listed_clas.index(prediccion)

        probabilidades = {}
        for indx in range(len(self.classes_names)):
            probabilidades[self.classes_names[indx]] = listed_clas[indx]
        print(probabilidades)
        return self.classes_names[prediccion]
class pin_recognizer:
    def __init__(self):
        self.nombre_pin ={1:"Pin 1",2:"Pin 2",4:"Pin 3",8:"Pin 4",16:"Pin 5",32:"Pin 6",64:"Pin 7",128:"Pin 8"}
        self.gamepad = False
        print("_____ HID _____")
        for device in hid.enumerate():
            print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")
            if 'Arduino Leonardo' in device['product_string']:
                dir1,dir2 = device['vendor_id'], device['product_id']
                self.gamepad = hid.device()
                self.gamepad.open(dir1,dir2)
                self.gamepad.set_nonblocking(True)
        if not self.gamepad:
            print('"Joystick" no encontrado')