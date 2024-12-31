from tensorflow.lite.python.interpreter import Interpreter
import numpy as np

class modules_recognizer:
    def __init__(self):
        self.classes_names = ['HC-SR04',
            'TCS34725',
            'MQ-2',
            'KY-006',
            'DHT-11',
            'KY-006',
            'ldr',
            'ldr',
            'KY-023',
            'KY-012',
            'SG90',
            'KY-038',
            'background'
        ]
        #['HC-SR04', 'DHT-11', 'ldr', 'KY-023', 'KY-012', "background"]
        self.model = Interpreter("AIvidentes.tflite")  # load_model("AIvidentes.h5")
        self.model.allocate_tensors()

        # Obtener los detalles de entrada y salida del modelo
        self.input_details = self.model.get_input_details()[0]["index"]
        self.output_details = self.model.get_output_details()[0]["index"]

    def read(self, frame):
        x = np.expand_dims(frame.astype(np.float32), axis=0)
        image_tensor = np.vstack([x])

        self.model.set_tensor(self.input_details, image_tensor)
        self.model.invoke()  # Ejecutar la inferencia
        classes = self.model.get_tensor(self.output_details)[0]  # Obtener los resultados de la inferencia

        listed_clas = [prediction for prediction in classes]
        prediccion_prob = max(listed_clas)
        prediccion = listed_clas.index(prediccion_prob)
        probabilidades = {}
        for indx in range(len(self.classes_names)):
            probabilidades[self.classes_names[indx]] = listed_clas[indx]
        print(probabilidades)
        if self.classes_names[prediccion] == "background" or prediccion_prob < 0.8:
            raise Exception
        return self.classes_names[prediccion]