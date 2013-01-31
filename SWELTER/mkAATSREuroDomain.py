from usefulFunctions import monthsAsNumbers
from usefulFunctions import yearsAsStrList
from usefulFunctions import printUsual

from netCDF4 import Dataset
import sys
import matplotlib.pyplot as plt
import numpy as np

class aatsr():


    def __init__(self):
##
## Parameters defining the input grid and file structure
##
        self.nXIn = 1440
        self.x0In = -179.75
        self.nYIn = 720
        self.y0In = -89.75
        self.nTimesIn = 1826
##        self.nTimesIn = 365        
        self.startYear = 2007
        self.endYear = 2011 + 1

        self.years = yearsAsStrList(  self.startYear, self.endYear )

        self.months = monthsAsNumbers()
        self.years = yearsAsStrList( self.startYear, self.endYear )
        self.rootDir =\
                     "/prj/nceo/aatsrLstP25Deg/"

##
        self.nXOut = 162
        self.x0Out = -9.875
        self.nYOut = 100
        self.y0Out = 35.125

    def readInput(self, y, m):

        fileName = self.rootDir + 'ATS_LST_3P_UOL'  + y + m + 'XX_0.25CS3_POA2CYEI.nc'
        print( fileName)

##        try:
        fid = Dataset( fileName, "r")
        
        varIn = fid.variables["L3_Day_mu"][:,:]
        
        plt.imshow( np.rot90( varIn))
        plt.show()
        
        fid.close()
        

##        except:
##            print( "No such luck buddy!")
        
    def doStuff(self):

        for year in self.years:
            for month in self.months:
                self.readInput(year,month)
                sys.exit(-10)
if __name__ == "__main__":


    a = aatsr()
    a.doStuff()
