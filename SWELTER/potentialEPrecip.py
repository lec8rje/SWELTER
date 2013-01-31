import numpy as np
from netCDF4 import Dataset
from usefulFunctions import monthsAsNumbers, yearsAsStrList,\
     printUsual
import matplotlib.pyplot as plt

class pePrecip():
    def __init__(self):

        self.lambd = 2.45E6
        self.mwr=0.622
        self.cp=1004.0
        self.tcrit=373.15
        self.psyco=0.0004

        self.precip = 0.0
        
        self.wfdEIDir = \
                      "/prj/nceo/WFD-EI-Forcing/"
        self.pointsFile = \
                        "euroPoints2839.dat"


        self.years = yearsAsStrList( 2000, 2010)

        self.months = monthsAsNumbers()



        self.nYears = float( len( self.years))

        self.nY = 50
        self.nX = 81


        self.fromScratch = True
        
    def readPoints(self):

        f = open( self.wfdEIDir + self.pointsFile, "r")
        self.points = np.genfromtxt( f, dtype = np.int16)
        f.close()

    def readPrecip(self):
        variables = [ "Rainf", "Snowf"]
        rain = 0
        snow = 0
        for self.year in self.years:

            rainFile = self.wfdEIDir + variables[0] + \
                       "/" + variables[0] + \
                       "_WFDEI_land_" + self.year + self.month + \
                       ".nc"

##            print( rainFile)

            f = Dataset( rainFile, "r")
            rain += f.variables[ variables[0]][:, self.wfdPoint].mean()
            f.close()

            snowFile = self.wfdEIDir + variables[1] + \
                       "/" + variables[1] + \
                       "_WFDEI_land_" + self.year + self.month + \
                       ".nc"
            f = Dataset( snowFile, "r")
            snow += f.variables[ variables[1]][:, self.wfdPoint].mean()
            f.close()

        return ( rain + snow ) / self.nYears
##
##
##
    def readPEVars(self):
        variables = [ "PSurf", "Tair", "SWdown" ]
        pres = 0.0
        tair = 0.0
        sw = 0.0
        for self.year in self.years:
##
##
            presFile = self.wfdEIDir + variables[0] + \
                       "/" + variables[0] + \
                       "_WFDEI_land_" + self.year + self.month + \
                       ".nc"
            f = Dataset( presFile, "r")
            pres += f.variables[ variables[0]][:, self.wfdPoint].mean()
            f.close()

            tairFile = self.wfdEIDir + variables[1] + \
                       "/" + variables[1] + \
                       "_WFDEI_land_" + self.year + self.month + \
                       ".nc"
            f = Dataset( tairFile, "r")
            tair += f.variables[ variables[1]][:, self.wfdPoint].mean()
            f.close()

            swFile = self.wfdEIDir + variables[2] + \
                       "/" + variables[2] + \
                       "_WFDEI_land_" + self.year + self.month + \
                       ".nc"
            f = Dataset( swFile, "r")
            sw += f.variables[ variables[2]][:, self.wfdPoint].mean()
            f.close()
            
        return pres / self.nYears, tair / self.nYears, \
               sw / self.nYears
##
##
##    
    def calcPE(self):

        tr = 1.0 - ( self.tcrit / self.tair )
        qsat = self.mwr * np.exp( 13.3185 * tr - 1.9760 * tr**2) \
               - 0.6445 * tr**3 - 0.1299 * tr**4

        delq = self.tcrit / self.tair**2 * qsat * \
               ( 13.3185 - 2.0 * 1.9760 * tr - 3.0 * 0.6445 * tr**2 \
                 - 4.0 * 0.1299 * tr**3)
        const= delq / ( delq + self.psyco)
        pe = 1.26 * const * self.sw * 0.7
##        print( tr, qsat, delq, const, pe, self.sw, self.tair )
        return pe
##
##
##
    def writeCDF(self):
        f = Dataset( "euroPE2005-2009.nc", "w")
        f.createDimension( "time", len( self.months))
        f.createDimension( "x", len( self.points))
        f.createDimension( "y", 1)        
        f.createVariable( 'pe', np.float32, [ "time", "y", "x"])
        f.variables["pe"][:] = self.pe
        f.createVariable( 'precip', np.float32, [ "time", "y", "x"])
        f.variables["precip"][:] = self.precip
        f.close()
##
##
##    
    def readPdef(self):
        fn = "/prj/nceo/WFD-EI-Forcing/euroSwelterPdefLE.gra"
        f = open( fn, "rb")
        self.pdef = np.fromfile( f, dtype = np.int32, \
                                 count = self.nY * self.nX)\
                    .reshape( ( self.nY, self.nX)).byteswap()
        f.close()
##
##
##
    def readCDF(self):
        f = Dataset( "euroPE.nc", "r")
        self.pe = f.variables["pe"][:]
        self.precip = f.variables["pe"][:]
        f.close()
##
##
##
    def regridVector(self,var):

        varOut = np.zeros( ( self.nY, self.nX)) - 999.0

        for point in xrange( self.pe.shape[1]):

            x = (self.pdef==point + 1).max(axis=0).argmax()
            y = (self.pdef==point + 1).max(axis=1).argmax()

            varOut[ y, x] = var[ point]

        return varOut
##
##
##        
    def doStuff(self):

        self.readPoints()

        if self.fromScratch:

            self.pe = np.zeros( ( len( self.months), 1, len( self.points)))
            self.precip = np.zeros( ( len( self.months), 1, len( self.points)))        
        
            for self.point in xrange( len( self.points)):

                self.wfdPoint = self.points[ self.point]

##            for self.point in xrange( 10):                        
                if np.mod( self.point, 100) == 0:
                    print( self.point)
                m = 0
                for self.month in self.months:
                    
                    self.precip[ m, 0, self.point] = self.readPrecip()
                    self.pres, self.tair, self.sw = \
                               self.readPEVars()

                    self.pe[ m, 0, self.point] = self.calcPE()
                    m += 1

                print( self.pe[:, 0, self.point])
                print( self.precip[:, 0, self.point])

            self.writeCDF()

        else:
            self.readCDF()
##            pass
##        self.readPdef()
##        var2Plot = self.regridVector( \
##            np.squeeze( self.pe[ 5, :]))
##        plt.imshow( np.ma.masked_array(\
##            var2Plot, var2Plot < 0))
##        plt.colorbar()
##        plt.show()
##
##
if __name__ == "__main__":

    p = pePrecip()

    p.doStuff()
