import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
from PIL import Image
import numpy as np
from astropy.io import fits

img_rows, img_cols = 275, 275
spectral_types = ['A', 'B', 'O', 'F', 'G', 'K', 'M']

def  Make_Stars(file_name, stars, ras, decs, types):
    file = fits.open(file_name)
    wavelength = file[1].data['loglam']
    wavelength = np.power(10, wavelength)
    flux = file[1].data['flux']

    ra = (str)("%.6f" % file[0].header['PLUG_RA'])
    dec = (str)("%.6f" % file[0].header['PLUG_DEC'])

    found_count = 0
    coordinate_found = -1
    for i, x in enumerate(decs):
        if (dec == (str)(x)) and (ra == (str)(ras[i])):
                found_count += 1
                coordinate_found = i
    if (found_count == 1):
        if types[coordinate_found] in spectral_types:
            stars.append(Star(ra, dec, types[coordinate_found], wavelength, flux)) 

def fig2data(fig):
    fig.canvas.draw ( )
    w,h = fig.canvas.get_width_height()
    buf = np.fromstring ( fig.canvas.tostring_argb(), dtype=np.uint8 )
    buf.shape = ( w, h,4 )
    buf = np.roll ( buf, 3, axis = 2 )
    return buf

def convert_to_L(im):
    im_L = np.empty([im.shape[0], im.shape[1]])
    for i, row in enumerate(im):
        for j, pix in enumerate(row):
            im_L[i,j] = pix[0]* 299/1000 + pix[1]* 587/1000 + pix[2]* 114/1000
    return im_L

def cut_window(wavelength, flux):
    min_idx = 0
    max_idx = 0
    for i, wl in enumerate(wavelength):
        if wl > 3600:
            min_idx = i
            break
    for j, wl in enumerate(wavelength):
        if wl > 10300:
            max_idx = j-1
            break
    return (wavelength[min_idx:max_idx], flux[min_idx:max_idx])

class Star(object):
    def __init__(self, ra, dec, type, wl, flux):
        self.RA = ra
        self.DEC = dec
        self.spectral_type = type
        self.type_label = spectral_types.index(type)
        self.wavelength, self.flux = cut_window(wl, flux)

    def make_img(self):
        figure = matplotlib.pyplot.figure(figsize=(7/2.54, 7/2.54))
        plot = figure.add_subplot(111)
        plot.plot (self.wavelength, self.flux)
        plt.axis('off')
        im = fig2data(figure)
        im_L = convert_to_L(im)
        return im_L.reshape(img_rows*img_cols)
