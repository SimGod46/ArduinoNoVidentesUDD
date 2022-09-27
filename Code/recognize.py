import numpy as np
from keras.preprocessing import image
import keras
class modules_recognizer:
    def __init__(self):
        self.classes_names = ['PIR', 'DHT11', 'CO']
        self.model = keras.models.load_model('AIvidentes.h5')
    def read(self,path):
        img = image.load_img(path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        image_tensor = np.vstack([x])
        classes = self.model.predict(image_tensor)
        listed_clas = []
        for i in classes[0]:
            listed_clas.append(i)
        prediccion = max(listed_clas)
        prediccion = listed_clas.index(prediccion)
        print(listed_clas) #Lista de probabilidades
        #print(self.classes_names[prediccion]) 
        return self.classes_names[prediccion]