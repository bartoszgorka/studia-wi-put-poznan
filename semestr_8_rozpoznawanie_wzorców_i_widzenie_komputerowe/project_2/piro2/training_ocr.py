from keras.datasets import mnist
from keras.preprocessing.image import ImageDataGenerator
from matplotlib import pyplot
from keras import backend as K
from skimage.draw import line_aa
from ocr_model import get_model, save_model
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint, TensorBoard
import cv2
import os
import numpy as np
import glob, os
import cv2
K.set_image_dim_ordering('th')


shift = 0.25
s = 3
zoom_low=0.8
zoom_high=1.1

def cv2_clipped_zoom(img, zoom_factor):
     img=img[0]

     height, width = img.shape[:2]
     new_height, new_width = int(height * zoom_factor), int(width * zoom_factor)

     y1, x1 = max(0, new_height - height) // 2, max(0, new_width - width) // 2
     y2, x2 = y1 + height, x1 + width
     bbox = np.array([y1,x1,y2,x2])

     bbox = (bbox / zoom_factor).astype(np.int)
     y1, x1, y2, x2 = bbox
     cropped_img = img[y1:y2, x1:x2]

     resize_height, resize_width = min(new_height, height), min(new_width, width)
     pad_height1, pad_width1 = (height - resize_height) // 2, (width - resize_width) //2
     pad_height2, pad_width2 = (height - resize_height) - pad_height1, (width - resize_width) - pad_width1
     pad_spec = [(pad_height1, pad_height2), (pad_width1, pad_width2)] + [(0,0)] * (img.ndim - 2)

     result = cv2.resize(cropped_img, (resize_width, resize_height))
     result = np.pad(result, pad_spec, mode='constant')
     return result

def grid(img, zoom_factor):
     height, width = img.shape
     #interval = int(np.random.uniform(width/2, width/1.9) * zoom_factor)
     interval = int(np.random.normal(width*.7, .05)*zoom_factor)
     axis_shift = int(np.random.uniform(-s, s))
     x_start_point = np.random.randint(0, width)
     #x_start_point = int(np.random.beta(.5,.5)*width)
     #y_start_point = np.random.randint(0, interval)
     y_start_point = int(np.random.beta(.5,.5)*height)
     tmp_img = np.zeros_like(img)

     try:
          for i in range(width//interval):
               #if x_start_point<wid
               rr, cc, val = line_aa(0, x_start_point + interval * i,\
                    height-1, x_start_point + interval * i + axis_shift)
               tmp_img[rr, cc] = val * .8
               rr, cc, val = line_aa(y_start_point + interval * i, 0,\
                    y_start_point + interval * i - axis_shift, width - 1)
               tmp_img[rr, cc] = val * .8
          return np.clip(img+tmp_img, 0., 1.)
     except:
          return img

def preprocessing(img):
     img = img/255.
     zoom_factor = np.random.uniform(zoom_low, zoom_high)
     img = cv2_clipped_zoom(img, zoom_factor)
     img = grid(img, zoom_factor)
     return img.reshape(1, img.shape[0], img.shape[1])

if __name__=='__main__':
     X_train = []
     y_train = []

     for decision_class in range(0, 10):
         for name in glob.glob("/Users/bgorka/Downloads/Studia/Semestr_8/pattern-recognition-computer-vision/project_2/DataML/{}/Image*.png".format(decision_class)):
             image = cv2.imread(name)
             X_train.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
             y_train.append(decision_class)

     X_train = np.array(X_train)
     y_train = np.array(y_train)
     X_test = X_train.copy()
     y_test = y_train.copy()

     # (X_train, y_train), (X_test, y_test) = mnist.load_data()
     X_train = X_train.reshape(X_train.shape[0], 1, 28, 28)
     X_test = X_test.reshape(X_test.shape[0], 1, 28, 28)
     X_train = X_train.astype('float32')
     X_test = X_test.astype('float32')
     y_train = np_utils.to_categorical(y_train)
     y_test = np_utils.to_categorical(y_test)

     datagen = ImageDataGenerator(width_shift_range=shift, height_shift_range=shift,\
     preprocessing_function=preprocessing, data_format='channels_first')
     datagen.fit(X_train)

     checkpoints = []
     if not os.path.exists('Data/Checkpoints/'):
          os.makedirs('Data/Checkpoints/')
     checkpoints.append(ModelCheckpoint('Data/Checkpoints/best_weights.h5', monitor='val_loss', verbose=0, save_best_only=True, save_weights_only=True, mode='auto', period=1))
     checkpoints.append(TensorBoard(log_dir='Data/Checkpoints/./logs', histogram_freq=0, write_graph=True, write_images=False, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None))

     model = get_model(num_classes = 10)
     model.fit_generator(datagen.flow(X_train, y_train, batch_size=200),\
          steps_per_epoch=X_train.shape[0]/6, epochs=10, callbacks=checkpoints)

     save_model(model)
