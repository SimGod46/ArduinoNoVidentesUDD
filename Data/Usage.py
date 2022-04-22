import numpy as np
from keras.preprocessing import image
import keras
classes_names = ['Pir', 'DHT 11', 'CO']
model = keras.models.load_model('AIvidentes.h5')
while True:
    path = input('> nombre imagen: ')#'test.jpg'
    img = image.load_img(path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    image_tensor = np.vstack([x])
    classes = model.predict(image_tensor)
    listed_clas = []
    for i in classes[0]:
        listed_clas.append(i)
    prediccion = max(listed_clas)
    prediccion = listed_clas.index(prediccion)
    print(listed_clas)
    print(classes_names[prediccion])