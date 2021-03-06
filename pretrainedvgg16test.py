import numpy as np
import matplotlib.pyplot as plt
import os
from keras import models
from keras import layers
from keras.optimizers import SGD
from keras.applications.vgg16 import VGG16
from keras.preprocessing.image import ImageDataGenerator
from shutil import copy
from shutil import rmtree

path = 'PokemonData'
if os.path.exists('train'):
    rmtree('train')
if os.path.exists('validate'):
    rmtree('validate')
if os.path.exists('test'):
    rmtree('test')

os.mkdir('train')
os.mkdir('validate')
os.mkdir('test')

image_count = 0
class_count = 0
classes = []
for i in os.listdir(path):
    classes.append(i)
    class_path = os.path.join(path, i)
    if not os.path.exists(os.path.join('train', i)):
        os.mkdir(os.path.join('train', i))
    if not os.path.exists(os.path.join('validate', i)):
        os.mkdir(os.path.join('validate', i))
    if not os.path.exists(os.path.join('test', i)):
        os.mkdir(os.path.join('test', i))
    image_paths = []
    for j in os.listdir(class_path):
        image_paths.append(os.path.join(class_path, j))
        image_count += 1
    np.random.shuffle(image_paths)
    training_path = image_paths[:int(len(image_paths) * .80)]
    test_path = image_paths[int(len(image_paths) * .80):]
    valid_path = training_path[int(len(training_path) * .80):]
    training_path = training_path[:int(len(training_path) * .80)]
    for j in training_path:
        copy(j, os.path.join('train', i))
    for j in valid_path:
        copy(j, os.path.join('validate', i))
    for j in test_path:
        copy(j, os.path.join('test', i))
    class_count += 1
print(image_count)
print(class_count)

train_data_generator = ImageDataGenerator()
train_data = train_data_generator.flow_from_directory(directory='train', target_size=(224,224))

validate_data_generator = ImageDataGenerator()
validate_data = validate_data_generator.flow_from_directory(directory='validate', target_size=(224,224))

test_data_generator = ImageDataGenerator()
test_data = test_data_generator.flow_from_directory(directory='test', target_size=(224,224))

pre_trained_model = VGG16(input_shape=(224,224,3), weights='imagenet', include_top=False, pooling='avg')
pre_trained_model.trainable = False
print(pre_trained_model.summary())

prediction_layer = layers.Dense(150)

total_model = models.Sequential([pre_trained_model, prediction_layer])
total_model.compile(loss='categorical_crossentropy', optimizer = SGD(lr=0.01, momentum=0.9), metrics = ['accuracy'])
print(total_model.summary())

history = total_model.fit(train_data, validation_data=validate_data, epochs=5, verbose=0)

accuracy = total_model.evaluate(test_data, verbose=0)

print("Accuracy: %.4f" % accuracy)

plt.subplot(211)
plt.title('Loss')
plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()

plt.subplot(212)
plt.title('Accuracy')
plt.plot(history.history['accuracy'], label='train')
plt.plot(history.history['val_accuracy'], label='test')
plt.legend()
plt.show()