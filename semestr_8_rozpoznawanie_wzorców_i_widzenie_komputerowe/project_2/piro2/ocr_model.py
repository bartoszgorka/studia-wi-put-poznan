# Larger CNN for the MNIST Dataset
import numpy
from keras.datasets import mnist
from keras.models import Sequential, model_from_json
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
import os.path
K.set_image_dim_ordering('th')

def save_model(model):
    if not os.path.exists('Data/Model/'):
        os.makedirs('Data/Model/')
    model.save_weights("Data/Model/weights.h5")
    print('Model and weights saved')

def get_model(num_classes = 10):
	model = Sequential()
	model.add(Conv2D(30, (5, 5), input_shape=(1, 28, 28), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Conv2D(15, (3, 3), activation='relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))
	model.add(Dropout(0.2))
	model.add(Flatten())
	model.add(Dense(128, activation='relu'))
	model.add(Dense(50, activation='relu'))
	model.add(Dense(num_classes, activation='softmax'))

	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

def get_trained_model():
    model_dir = os.path.join(os.path.dirname(__file__), 'Data', 'Model')
    weights_file = os.path.join(model_dir, 'weights-2.h5')
    model = get_model()
    model.load_weights(weights_file)
    return model
