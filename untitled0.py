# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10vaUIKDyw0GagOmsMGy0e9WXV5DzZuOi
"""

!pip install kaggle

#configure the path of Kaggle.json file
!mkdir -p ~/.Kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

from google.colab import drive
drive.mount('/content/gdrive')

!cp /content/gdrive/My\ Drive/kaggle.json ~/.kaggle/kaggle.json

!kaggle competitions download -c dogs-vs-cats

!ls

"""Extracting the compressed dataset"""

from zipfile import ZipFile

dataset = '/content/dogs-vs-cats.zip'

with ZipFile(dataset, 'r') as zip:
  zip.extractall()
  print('The datset is extracted')

from zipfile import ZipFile

dataset = '/content/train.zip'

with ZipFile(dataset, 'r') as zip:
  zip.extractall()
  print('The datset is extracted')

import os
#count the number of files in train folder
path, dirs, files = next(os.walk('/content/train'))
file_count = len(files)
print('Number of Images: ',file_count)

"""Print the name of Image

"""

file_names = os.listdir('/content/train')
print(file_names)

"""Importing the Dependies

"""

import numpy as np
 from PIL import Image
 import matplotlib.pyplot as plt
 import matplotlib.image as mpimg
 from sklearn.model_selection import train_test_split
 from google.colab.patches import cv2_imshow

"""Displaying the images of dogs and cats

"""

#Display dog image
img = mpimg.imread('/content/train/dog.8858.jpg')
imgplot = plt.imshow(img)
plt.show()

#Display catimage

img = mpimg.imread('/content/train/cat.10003.jpg')
imgplot = plt.imshow(img)
plt.show()

"""Resizing all the images

"""

file_names = os.listdir('/content/train')

for i in range(5):

  name = file_names[i]
  print(name[0:3])

file_names = os.listdir('/content/train')

dog_count = 0
cat_count = 0

for img_file in file_names:

  name = img_file[0:3]

  if name == 'dog':
    dog_count +=1

  else:
    cat_count +=1

print('Number of dog images =', dog_count)
print('Number of cat images =', cat_count)

"""Code to delete director and its content"""

#!rm -rf /content/image\ resized/*

#deleting a directory for resized images
#os.rmdir('/content/image resized')

os.mkdir('/content/image resized')

original_folder = '/content/train/'
resized_folder = '/content/image resized/'

for i in range(2000):

  filename = os.listdir(original_folder)[i]
  img_path = original_folder+filename

  img = Image.open(img_path)
  img = img.resize((224, 224))
  img = img.convert('RGB')

  newImgPath = resized_folder+filename
  img.save(newImgPath)

#Display resized cat image

img = mpimg.imread('/content/image resized/cat.10004.jpg')
imgplot = plt.imshow(img)
plt.show()

#Display dog resized image

#img = mpimg.imread('/content/image resized/dog.98765.jpg')
#imgplot = plt.imshow(img)
#plt.show()

"""Creating labels for resized images of dogs and cats

cat --> 0

dog --> 1
"""

#creating a for loop to assign labels
filenames = os.listdir('/content/image resized/')

labels = []

for i in range(2000):
  file_name = filenames[i]
  label = file_name[0:3]

  if label =='dog':
    labels.append(1)

  else:
    labels.append(0)

print(filenames[0:5])
print(len(filenames))

print(labels[0:5])
print(len(labels))

#counting the images of out of __ images

values, counts = np.unique(labels, return_counts=True)
print(values)
print(counts)

"""Converting all the resized images to numpy arrays"""

import cv2
import glob

image_directory = '/content/image resized/'
image_extension = ['png', 'jpg']

files = []

[files.extend(glob.glob(image_directory + '*.' + e)) for e in image_extension]

dof_cat_image = np.asarray([cv2.imread(file) for file in files])

print(dof_cat_image)

type (dof_cat_image)

print(dof_cat_image.shape)

X = dof_cat_image
Y = np.asarray(labels)

"""Train Test Split"""

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2, random_state=2)

print(X.shape, X_train.shape, X_test.shape)

"""1600 --> training images

400 --> test images
"""

#scaling the data
X_train_scaled = X_train/225

X_test_scaled = X_test/225

"""Building the Neural Network"""

import tensorflow as tf
import tensorflow_hub as hub

"""tf2-preview/mobilenet_v2/feature_vector

"""

import tensorflow as tf
import tensorflow_hub as hub

mobilenet_model = 'https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4'

pretrained_model = hub.KerasLayer(mobilenet_model, input_shape =(224,224,3), trainable = False)

num_of_classes = 2

model = tf.keras.Sequential([

    pretrained_model,
    tf.keras.layers.Dense(num_of_classes)

                             ])

model.summary()

model.compile(
    optimizer = 'adam',
    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True),
    metrics = ['acc']
)

model.fit(X_train_scaled, Y_train, epochs =5)

score, acc = model.evaluate(X_test_scaled, Y_test)

print('Test Loss = ', score)
print('Test Accuracy = ', acc)

"""Predictive System

"""

input_image_path = input('Path of the image to be predicted: ')

input_image = cv2.imread(input_image_path)

cv2_imshow(input_image)

input_image_resize = cv2.resize(input_image, (224,224))

input_image_scaled = input_image_resize/225

image_reshaped = np.reshape(input_image_scaled, [1,224,224,3])

input_prediction = model.predict(image_reshaped)

print(input_prediction)

input_pred_label = np.argmax(input_prediction)
print(input_pred_label)
if input_pred_label == 0:
  print('The image represents a Cat')

else:
  print('The image represents a Dog')

