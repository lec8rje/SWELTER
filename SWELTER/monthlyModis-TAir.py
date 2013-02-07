from usefulFunctions import monthsAsNumbers
from usefulFunctions import daysAsNumbers
from usefulFunctions import yearsAsStrList
from usefulFunctions import isLeap
from usefulFunctions import printUsual
import sys
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
##
##
##
class modisMonth():


    def __init__(self):
##
## The first time we read the daily / 3 hourly data
##  we mean it and regrid the WFDEI. After this we have
##  the outputs in a file and it is much easier just to
##  read them in
##
        self.fromScratch = True
##
## Parameters defining the input grid and file structure
##
        self.nXIn = 162
        self.x0In = -10.375
##        self.x0In = -9.875        
        self.nYIn = 100
        self.y0In = 35.125

        self.startYear = 2005
##        self.endYear = 2005 + 1
        self.endYear = 2009 + 1        
        self.months = monthsAsNumbers()
        self.years = yearsAsStrList( self.startYear, self.endYear )
        self.nTimesIn = len( self.months) * len( self.years)
        
        self.rootDir =\
                     '/users/global/cmt/SWELTER/lst/SWELTER_terra_025deg_files/'
##                     '/users/global/cmt/SWELTER/lst/SWELTER_aqua_025deg_files/'
        self.nXOut = 162
        self.nYOut = 100
        self.x0Out = -10.375
        self.y0Out = 35.125

        self.undef = np.zeros( ( self.nYOut, self.nXOut ) ) - 999.0

        self.outputArray = np.zeros( (self.nTimesIn, \
                                     self.nYIn/2, self.nXIn/2),\
                                     dtype = np.float32)
        self.outputArrayBig = np.zeros( (self.nTimesIn, \
                                         self.nYIn, self.nXIn),\
                                        dtype = np.float32)
##
## WFD-EI is on a vector so we have to read in the
##  relevant points mean them and regrid them to our
##  output grid
##
        self.wfdEIDir = \
                      "/prj/nceo/WFD-EI-Forcing/"
        self.pointsFile = \
                        "euroPoints2839.dat"
##
##
##
    def readInput(self):
        fileName = self.rootDir + 'lst_025deg_'  + \
                   self.year + self.month + self.day + '.gra'
        
        if ( self.month == '01' ) | ( self.month == '02' ) |\
               ( self.month == '11' ) | ( self.month == '12' ):
            return self.undef, self.undef, self.undef,\
                   self.undef, self.undef, self.undef, \
                   self.undef, self.undef, self.undef,\
                   self.undef
        else:
            try:
                fidIn = open( fileName, 'rb' )
                print( 'Found file ' + fileName)
                inData = np.fromfile( fidIn, count = self.nYIn * self.nXIn, \
                                      dtype = np.float32 ).byteswap()\
                                      .reshape( ( self.nYIn, self.nXIn ) )
                inN = np.fromfile( fidIn, count = self.nYIn * self.nXIn, \
                                   dtype = np.float32 ).byteswap()\
                                   .reshape( ( self.nYIn, self.nXIn ) )
                inData2 = np.fromfile( fidIn, count = self.nYIn * self.nXIn, \
                                       dtype = np.float32 ).byteswap()\
                                       .reshape( ( self.nYIn, self.nXIn ) )
                inN2 = np.fromfile( fidIn, count = self.nYIn * self.nXIn, \
                                    dtype = np.float32 ).byteswap()\
                                    .reshape( ( self.nYIn, self.nXIn ) )
                inData3 = np.fromfile( fidIn, count = self.nYIn * self.nXIn, \
                                       dtype = np.float32 ).byteswap()\
                                       .reshape( ( self.nYIn, self.nXIn ) )
                inN3 = np.fromfile( fidIn, count = self.nYIn * self.nXIn, \
                                    dtype = np.float32 ).byteswap()\
                                    .reshape( ( self.nYIn, self.nXIn ) )
                inData4 = np.fromfile( fidIn, count = self.nYIn * self.nXIn, \
                                       dtype = np.float32 ).byteswap()\
                                       .reshape( ( self.nYIn, self.nXIn ) )
                inN4 = np.fromfile( fidIn, count = self.nYIn * self.nXIn, \
                                    dtype = np.float32 ).byteswap()\
                                    .reshape( ( self.nYIn, self.nXIn ) )
                inData5 = np.fromfile( fidIn, count = self.nYIn * self.nXIn, \
                                       dtype = np.float32 ).byteswap()\
                                       .reshape( ( self.nYIn, self.nXIn ) )
                inN5 = np.fromfile( fidIn, count = self.nYIn * self.nXIn, \
                                    dtype = np.float32 ).byteswap()\
                                    .reshape( ( self.nYIn, self.nXIn ) )
                fidIn.close()

                return np.flipud( inData ), np.flipud( inN ), \
                       np.flipud( inData2 ), np.flipud( inN2 ),\
                       np.flipud( inData3 ), np.flipud( inN3 ),\
                       np.flipud( inData4 ), np.flipud( inN4 ),\
                       np.flipud( inData5 ), np.flipud( inN5 )

            except:
               return self.undef, self.undef, self.undef,\
                      self.undef, self.undef, self.undef, \
                      self.undef, self.undef, self.undef,\
                      self.undef

##
##
##
    def writeModisCDF(self):
##    fidOut = Dataset( 'aquaQuartMonthEurope.nc', 'w', format = \    
        fidOut = Dataset( 'terraQuartMonthEurope.nc', 'w', format = \
                          'NETCDF3_CLASSIC')
        fidOut.createDimension( 'y', self.nYOut )
        fidOut.createDimension( 'x', self.nXOut )
        fidOut.createDimension( 't', self.nTimesIn )
##
        fidOut.createVariable( 'lst', np.float32, ( 't', 'y', 'x' ) )
        fidOut.variables[ 'lst'][:] = self.allLST
##
        fidOut.close()
##
## Stuff for the reading and regridding of WFD
##
    def readPoints(self):
        f = open( self.wfdEIDir + self.pointsFile, "r")
        self.points = [ int( p) for p in f.read().split()]
        f.close()
        fn = "/prj/nceo/WFD-EI-Forcing/EI-Halfdeg-land-elevation.nc"
        fid = Dataset( fn, "r")
##        for point in self.points:
##            print( fid.variables['latitude'][point-1],\
##                   fid.variables['longitude'][point-1])        
##        sys.exit(-1)
##
##
##
    def readPdef(self):

        fn = "/prj/nceo/WFD-EI-Forcing/euroSwelterPdef2839.gra"

        print( "Reading pdef from ", fn)

        f = open( fn, "rb")
        self.pdef = np.fromfile( f, dtype = np.int32, \
                                 count = self.nYIn / 2 * self.nXIn / 2)\
                    .reshape( ( self.nYIn / 2, self.nXIn / 2)).byteswap()
        f.close()
        print( "Closed pdef file")
##
##
##        
    def readTair(self):
        print( self.year, self.month)
        fileName = self.wfdEIDir +  "Tair/Tair" + \
                   "_WFDEI_land_" + self.year + self.month + \
                   ".nc"
        f = Dataset( fileName, "r")
        tAir = f.variables[ "Tair"][:, self.points].mean(axis=0)
        f.close()
        return tAir
##
##
##
    def regridTair(self):
        print( "Regriding Tair")
        for point in xrange( len( self.points)):
            
##            x = (self.pdef==point ).max(axis=0).argmax()
##            y = (self.pdef==point ).max(axis=1).argmax()
            x = (self.pdef==point + 1).max(axis=0).argmax()
            y = (self.pdef==point + 1).max(axis=1).argmax()
            print( x,y, self.pdef.max())
##            self.tAir[ :, y, x] = 1.0
            self.tAir[ :, y, x] = self.tAirVec[ :, point]            
##
##
##            
    def writeTairCDF(self):
        print( "Writing tAir out to file")
        fidOut = Dataset( 'wfdHalfMonthEurope.nc', 'w', format = \
                          'NETCDF3_CLASSIC')
        fidOut.createDimension( 'y', self.nYOut/2 )
        fidOut.createDimension( 'x', self.nXOut/2 )
        fidOut.createDimension( 't', self.nTimesIn )
##
        fidOut.createVariable( 'Tair', np.float32, ( 't', 'y', 'x' ) )
        print( fidOut.variables[ 'Tair'][:].shape,\
               self.tAir.shape)
        fidOut.variables[ 'Tair'][:] = self.tAir
##
        fidOut.close()
##
##
##        
    def doStuff(self):
        if self.fromScratch:
            self.readPoints()
            self.readPdef()
            self.allLST = self.outputArrayBig.copy()
            self.allCount = self.outputArrayBig.copy()
            self.tAirVec = np.zeros( ( self.nTimesIn,\
                                        len( self.points) ))
            self.tAir = self.outputArray.copy()
        
            count = 0
            for self.year in self.years:
            
                leap = isLeap(self.year)
            
                for self.month in self.months:

                    for self.day in daysAsNumbers( self.month, leap ):
## ##
## ##
                        outputGrid, outputCount, \
                                    forestGrid, forestCount,\
                                    urbanGrid, urbanCount,\
                                    cropGrid, cropCount,\
                                    otherGrid, otherCount\
                                    = self.readInput()
                        if  outputGrid.max() > 0.0:
                            self.allLST[count, :, :] += np.where( outputGrid > 0.0,\
                                                                  outputGrid, 0.0)
                            self.allCount[count, :, :] += np.where( outputGrid > 0.0,\
                                                                    1.0, 0.0)
                    
                    self.tAirVec[count, :] = self.readTair()
##                    printUsual( self.tAirVec[count, :])
                    count += 1
        self.regridTair()
        self.writeTairCDF()
        self.allLST = self.allLST / self.allCount
        self.writeModisCDF()
##
##
##
if __name__ == "__main__":


    mm = modisMonth()

    mm.doStuff()
    



