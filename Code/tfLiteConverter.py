import tensorflow as tf

# Carga el modelo Keras
model = tf.keras.models.load_model('AIvidentes.h5')

# Convierte el modelo a TensorFlow Lite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Guarda el modelo TensorFlow Lite en un archivo
with open('AIvidentes.tflite', 'wb') as f:
    f.write(tflite_model)
