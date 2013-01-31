import matplotlib.pyplot as plt
import numpy as np
from netCDF4 import Dataset
cdfFile = \
        "/prj/SWELTER/data/jules/jules_euro2/weibas.water.01d.nc"
fid = Dataset( cdfFile, "r")

lH = fid.variables["latentHeat"][:]
sH = fid.variables["ftl"][:]

##print( lH.shape,  sH.shape)

fid.close()

fidSH = open( "sonjaRunSH.gra", "w")
np.squeeze(sH).astype( np.float32).byteswap().tofile( fidSH)
fidSH.close()

fidLH = open( "sonjaRunLH.gra", "w")
np.squeeze(lH).astype( np.float32).byteswap().tofile( fidLH)
fidLH.close()
