from astropy.io import fits
import numpy as np
import os

spectral_types = ['A', 'B', 'O', 'F', 'G', 'K', 'M']

label_path = os.path.join("..", "specObj-BOSS-dr12.fits")

labels_file = fits.getdata(label_path)
classes = labels_file['class']
spectral_class = labels_file['subclass']
dec = labels_file['PLUG_DEC']
RA = labels_file['PLUG_RA']

sRA = ["%.6f" % number for number in RA]
sdec = ["%.6f" % number for number in dec]

with open("Spectra Class.txt", 'a') as f:
    for i, cla in enumerate(classes):
        if cla == "STAR":
            subclass = spectral_class[i]

            if subclass[0] == 's':
                star_type = spectral_class[i][3]
            else:
                star_type = subclass[0]

            if star_type in spectral_types:
                ihatepython = sRA[i] + ' ' + sdec[i] + ' ' +  star_type + '\r\n'
                f.write(ihatepython)
