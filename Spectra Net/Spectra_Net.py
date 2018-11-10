from astropy.io import fits
import numpy as np
from os import path
from glob import glob
from class_Star import *

img_rows, img_cols = 275, 275
stars = []
images = []
labels = []
label_path = path.join("..", "Spectra Class.txt")
ras, decs = np.genfromtxt(label_path, unpack=True, usecols=[0, 1])
types = np.genfromtxt(label_path, unpack=True, usecols=[2], dtype='unicode')

for file_name in glob(path.join("..", "data", "*.fits")):
     Make_Stars(file_name, stars, ras, decs, types)
     
for star in stars:
    img = [(255 - x) * 1.0 / 255.0 for x in star.make_img()]
    images.append(np.reshape(img, (img_rows, img_cols)))
    labels.append(star.type_label)
images = np.array(images)
images = images.reshape(len(stars), 75625)

from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.1, random_state=4)


from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.normalization import BatchNormalization
from keras.optimizers import adadelta, Adam, adam
from keras.utils import np_utils
from keras import losses

Y_train = np_utils.to_categorical(y_train, 7)
Y_test = np_utils.to_categorical(y_test, 7)

model = Sequential()
model.add(Dense(500, input_dim=img_rows*img_cols, activation="relu", kernel_initializer="normal"))
model.add(Dense(250, activation="hard_sigmoid"))
model.add(Dropout(0.2))
model.add(Dense(7, activation="softmax", kernel_initializer="normal"))

Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
model.compile(loss="categorical_crossentropy", optimizer="Adam", metrics=["accuracy"])

#print(model.summary())

model.fit(X_train, Y_train, batch_size=45, epochs=50, validation_split=0.1, verbose=2)

scores = model.evaluate(X_test, Y_test, verbose=0)
print("Точность работы на тестовых данных: %.2f%%" % (scores[1]*100))

model_json = model.to_json()

# Записываем модель в файлы
json_file = open("spectra_net.json", "w")
json_file.write(model_json)
json_file.close()
model.save_weights("spectra_net.h5")
