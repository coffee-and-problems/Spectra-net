from astropy.io import fits
import numpy as np
from os import path
from glob import glob

minimum = []
maximum = []

def  Add_wl(file_name, minimum, maximum):
    file = fits.open(file_name)
    wavelength = file[1].data['loglam']
    wavelength = np.power(10, wavelength)
    
    minimum.append(wavelength[0])
    maximum.append(wavelength[-1])

for file_name in glob(path.join("..", "data", "*.fits")):
     Add_wl(file_name, minimum, maximum)

print("min = ", max(minimum))
print("max = ", min(maximum))

#min =  3614.0994
#max =  10301.486
