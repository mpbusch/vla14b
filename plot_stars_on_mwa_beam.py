import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.wcs.utils import skycoord_to_pixel
from scipy.ndimage import map_coordinates

hdul = fits.open('/data3/piyanat/runs/shared/vis_interp_delta_21cm_l128_0.000h_151.075MHz_Beam_XX.fits')
hdu2 = hdul[0]
wcs2 = WCS(hdu2.header)

#arr = np.empty((360, 180))
x = np.arange(180, -180, -1)
y = np.arange(-90, 90, 1)
gridx, gridy = np.meshgrid(x, y)
coords = SkyCoord(ra=gridx.ravel(), dec=gridy.ravel(), unit='deg', frame='icrs')

pixels = skycoord_to_pixel(coords, wcs2)
arr = map_coordinates(hdu2.data, pixels)
arr.shape = (180, 360)

gal = np.load("GalaxyMap.npy")

fig = plt.figure()
ax = fig.add_subplot(111)
ax.contour(x, y, arr, [0.01])
ax.imshow(np.log10(gal), extent=[-180, 180, -90, 90], cmap=plt.cm.gray,
          origin='lower')
ax.set_xlabel('RA [degree]')
ax.set_ylabel('Dec [degree]')
# ax.set_xlim(100, -10)
# ax.set_ylim(-50, 50)
ax.set_xlim(180, -180)
ax.set_ylim(-90, 90)
plt.grid('on')

# RA, Dec must be in rage [180, -180] and [-90, 90] degree
#star_ra = [10, 35, -20]
#star_dec = [0, -10, 25]

star_ra, star_dec = np.genfromtxt('vla_coords.csv', delimiter=',', unpack=True)

for ra, dec in zip(star_ra, star_dec):
    ax.scatter(ra, dec, marker='*', color='white')

plt.minorticks_on()

plt.show()
