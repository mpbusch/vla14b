from glob import glob

from calibration import *

visfiles = glob('*.ms')
for vis in visfiles:
    cal_all(vis, apply_cal=True)
