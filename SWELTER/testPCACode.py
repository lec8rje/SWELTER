import matplotlib.pyplot as plt
import numpy as np
from usefulFunctions import printUsual
from netCDF4 import Dataset
from matplotlib.mlab import PCA
import sys
class pcaCode():
    '''
    A class to implement the matplotlib pca code

    Author: RichE
    Insitute: CEH Wallingford
    Email: rjel@ceh.ac.uk
    This code is entirely without warrenty and I accept
    no laibility for any failures or flaws.

    '''
    def __init__(self):

        self.inputFile = "/prj/SWELTER/rjel/cardingtonJULESRuns/OUTPUT/WFDEI-test.tstep.30m.nc"


    def readWFDEIOutput(self):
        fid = Dataset( self.inputFile, "r")

        self.wfdLH = np.squeeze(fid.variables['latentHeat'][:])
        self.wfdSH = np.squeeze(fid.variables['ftl'][:])
        self.wfdSTHU = np.squeeze(fid.variables['sthu'][:,3,0,0])
        self.precip = np.squeeze(fid.variables['precip'][:])
        self.sw = np.squeeze(fid.variables['SWdown'][:])
        self.lw = np.squeeze(fid.variables['LWdown'][:])
        print( "There are  " + str( self.wfdSTHU.shape) + " points in the JULES output")
        fid.close()

    def makeArray(self):
        self.array = np.zeros( ( self.wfdSTHU.shape[0], 6))
        self.array[ :, 0] = self.wfdSTHU
        self.array[ :, 1] = self.wfdLH
        self.array[ :, 2] = self.wfdSH            
        self.array[ :, 3] = self.precip * 1800.0
        self.array[ :, 4] = self.sw
        self.array[ :, 5] = self.lw


    def doStuff(self):

        self.readWFDEIOutput()
        self.makeArray()
            
        pca = PCA( self.array)

        print( pca.mu)

        print( pca.fracs)        

        out = pca.project(self.array,minfrac=0.1)

        print( out.shape)

        plt.subplot(1,3,1)

        plt.plot( out[:,0],out[:,1], 'k+')

        plt.subplot(1,3,2)
        plt.plot( out[:,0],out[:,2], 'k+')

        plt.subplot(1,3,3)
        plt.plot( out[:,1],out[:,2], 'k+')


        plt.show()

if __name__ == "__main__":
##
    p = pcaCode()
    p.doStuff()
