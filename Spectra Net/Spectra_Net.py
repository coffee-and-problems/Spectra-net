from astropy.io import fits
import numpy as np
from os import path
from glob import glob
from class_Star import Make_Stars

stars = []
images = []
labels = []
label_path = path.join("..", "Spectra Class.txt")
ras, decs = np.genfromtxt(label_path, unpack=True, usecols=[0, 1])
types = np.genfromtxt(label_path, unpack=True, usecols=[2], dtype='unicode')

for file_name in glob(path.join("..", "data", "*.fits")):
     Make_Stars(file_name, stars, ras, decs, types)

for star in stars:
    images.append(star.make_img)
    labels.append(star.type_label)