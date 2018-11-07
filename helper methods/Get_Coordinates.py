from astropy.io import fits
import numpy as np
from os import path
from glob import glob

with open('stars.txt', 'a') as f:
    f.write('name  RA(deg)  DEC(deg)\r\n')
    for file_name in glob(path.join("..", "data", "*.fits")):
        file = fits.open(file_name)
        ra = (str)("%.6f" % file[0].header['PLUG_RA'])
        dec = (str)("%.6f" % file[0].header['PLUG_DEC'])
        names = file_name.split('\\')
        star = (str)(ra + ' ' + dec + '\n')
        f.write(star)
