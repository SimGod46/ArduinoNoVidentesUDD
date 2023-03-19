import os, re, time, json
import PIL.Image, PIL.ImageFont, PIL.ImageDraw
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50
from matplotlib import pyplot as plt
#import tensorflow_datasets as tfds

print("Tensorflow version " + tf.__version__)

"""## Parameters

- Define the batch size
- Define the class (category) names
"""
classes = ['Pir', 'DHT 11', 'CO']

"""Define some functions that will help you to create some visualizations. (These will be used later)"""

#@title Visualization Utilities[RUN ME]
#Matplotlib config
plt.rc('image', cmap='gray')
plt.rc('grid', linewidth=0)
plt.rc('xtick', top=False, bottom=False, labelsize='large')
plt.rc('ytick', left=False, right=False, labelsize='large')
plt.rc('axes', facecolor='F8F8F8', titlesize="large", edgecolor='white')
plt.rc('text', color='a8151a')
plt.rc('figure', facecolor='F0F0F0')# Matplotlib fonts
MATPLOTLIB_FONT_DIR = os.path.join(os.path.dirname(plt.__file__), "mpl-data/fonts/ttf")
# utility to display a row of digits with their predictions
def display_images(digits, predictions, labels, title):

  n = 10

  indexes = np.random.choice(len(predictions), size=n)
  n_digits = digits[indexes]
  n_predictions = predictions[indexes]
  n_predictions = n_predictions.reshape((n,))
  n_labels = labels[indexes]
 
  fig = plt.figure(figsize=(20, 4))
  plt.title(title)
  plt.yticks([])
  plt.xticks([])

  for i in range(10):
    ax = fig.add_subplot(1, 10, i+1)
    class_index = n_predictions[i]
    
    plt.xlabel(classes[class_index])
    plt.xticks([])
    plt.yticks([])
    plt.imshow(n_digits[i])

# utility to display training and validation curves
def plot_metrics(metric_name, title, ylim=5):
  plt.title(title)
  plt.ylim(0,ylim)
  plt.plot(history.history[metric_name],color='blue',label=metric_name)
  plt.plot(history.history['val_' + metric_name],color='green',label='val_' + metric_name)

"""## Loading and Preprocessing Data
[CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) dataset has 32 x 32 RGB images belonging to 10 classes. You will load the dataset from Keras.
"""
training_images = []
training_labels = []
for file_path in os.listdir('train'):
  for file_name in os.listdir(os.path.join('train',file_path)):
    training_images.append(np.array(PIL.Image.open(os.path.join('train',file_path,file_name))))
    training_labels.append(classes.index(file_path))

validation_images = []
validation_labels = []
for file_path in os.listdir('valid'):
  for file_name in os.listdir(os.path.join('valid',file_path)):
    validation_images.append(np.array(PIL.Image.open(os.path.join('valid',file_path,file_name))))
    validation_labels.append(classes.index(file_path))


training_images   = np.array(training_images)
training_labels   = np.array(training_labels)
validation_images = np.array(validation_images)  
validation_labels = np.array(validation_labels)   
"""### Visualize Dataset

Use the `display_image` to view some of the images and their class labels.
"""

display_images(training_images, training_labels, training_labels, "Training Data" )

display_images(validation_images, validation_labels, validation_labels, "Training Data" )

"""### Preprocess Dataset
Here, you'll perform normalization on images in training and validation set. 
- You'll use the function [preprocess_input](https://github.com/keras-team/keras-applications/blob/master/keras_applications/resnet50.py) from the ResNet50 model in Keras.
"""

def preprocess_image_input(input_images):
  input_images = input_images.astype('float32')
  output_ims = tf.keras.applications.resnet50.preprocess_input(input_images)
  return output_ims

train_X = preprocess_image_input(training_images)
valid_X = preprocess_image_input(validation_images)

"""## Define the Network
You will be performing transfer learning on **ResNet50** available in Keras.
- You'll load pre-trained **imagenet weights** to the model.
- You'll choose to retain all layers of **ResNet50** along with the final classification layers.
"""

'''
Feature Extraction is performed by ResNet50 pretrained on imagenet weights. 
Input size is 224 x 224.
'''
def feature_extractor(inputs):

  feature_extractor = tf.keras.applications.resnet.ResNet50(input_shape=(224, 224, 3),
                                               include_top=False,
                                               weights='imagenet')(inputs)
  return feature_extractor


'''
Defines final dense layers and subsequent softmax layer for classification.
'''
def classifier(inputs):
    x = tf.keras.layers.GlobalAveragePooling2D()(inputs)
    x = tf.keras.layers.Flatten()(x)
    x = tf.keras.layers.Dense(1024, activation="relu")(x)
    x = tf.keras.layers.Dense(512, activation="relu")(x)
    x = tf.keras.layers.Dense(3, activation="softmax", name="classification")(x)
    return x

'''
Since input image size is (32 x 32), first upsample the image by factor of (7x7) to transform it to (224 x 224)
Connect the feature extraction and "classifier" layers to build the model.
'''
def final_model(inputs):

#    resize = tf.keras.layers.UpSampling2D(size=(7,7))(inputs)

    resnet_feature_extractor = feature_extractor(inputs)
    classification_output = classifier(resnet_feature_extractor)

    return classification_output

'''
Define the model and compile it. 
Use Stochastic Gradient Descent as the optimizer.
Use Sparse Categorical CrossEntropy as the loss function.
'''
def define_compile_model():
  inputs = tf.keras.layers.Input(shape=(224,224,3))
  
  classification_output = final_model(inputs) 
  model = tf.keras.Model(inputs=inputs, outputs = classification_output)
 
  model.compile(optimizer='SGD', 
                loss='sparse_categorical_crossentropy',
                metrics = ['accuracy'])
  
  return model


model = define_compile_model()

model.summary()

"""## Train the model"""

# this will take around 20 minutes to complete
EPOCHS = 80
history = model.fit(train_X, training_labels,steps_per_epoch=10 ,epochs=EPOCHS, validation_data = (valid_X, validation_labels), batch_size=64)

"""## Evaluate the Model

Calculate the loss and accuracy metrics using the model's `.evaluate` function.
"""
model.save("AIvidentes.h5")

loss, accuracy = model.evaluate(valid_X, validation_labels, batch_size=64)

"""### Plot Loss and Accuracy Curves

Plot the loss (in blue) and validation loss (in green).
"""

plot_metrics("loss", "Loss")

"""Plot the training accuracy (blue) as well as the validation accuracy (green)."""

plot_metrics("accuracy", "Accuracy")

"""### Visualize predictions
You can take a look at the predictions on the validation set.
"""

probabilities = model.predict(valid_X, batch_size=64)
probabilities = np.argmax(probabilities, axis = 1)

display_images(validation_images, probabilities, validation_labels, "Bad predictions indicated in red.")