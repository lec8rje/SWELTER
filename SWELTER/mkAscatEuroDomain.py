from usefulFunctions import monthsAsNumbers
from usefulFunctions import daysAsNumbers
from usefulFunctions import yearsAsStrList
from usefulFunctions import isLeap
from usefulFunctions import printUsual
import sys
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

class mkAscat():


    def __init__(self):
##
## Parameters defining the input grid and file structure
##
        self.nXIn = 1440
        self.x0In = -179.875
        self.nYIn = 480
        self.y0In = -59.875
##        self.y0In = 60.125        
        self.dXYIn = 0.25
        self.nTimesIn = 1826
        self.startYear = 2007
##        self.endYear = 2007 + 1
        self.endYear = 20011 + 1        
        self.months = monthsAsNumbers()
        self.years = yearsAsStrList( self.startYear, self.endYear )
        self.rootDir = '/users/global/cmt/ASCAT/archive/global/'
##
## Parameters defining the output grid and netcdf file
##
        self.averageOutput = False
        if self.averageOutput:
            self.nXOut = 81
            self.nYOut = 50
            self.x0Out = -10.25
            self.y0Out = 59.75
            self.dXYOut = 0.5
        else:
            self.nXOut = 162
            self.nYOut = 100
            self.x0Out = -10.375
            self.y0Out = 35.125
##            self.y0Out = 59.825            
            self.dXYOut = 0.25            
##
## This defines the output grid as a portion of the input grid
##
        self.startXPoint = ( self.x0Out - ( self.x0In ) ) / self.dXYIn
        self.endXPoint = self.startXPoint + self.nXOut * self.dXYOut / self.dXYIn

        self.startYPoint = ( self.y0Out - self.y0In) / self.dXYIn
##        self.startYPoint = ( self.y0In - self.y0Out ) / self.dXYIn
        self.endYPoint = self.startYPoint + self.nYOut * self.dXYOut / self.dXYIn

##        print( self.startYPoint, self.endYPoint )
##        print( self.y0In + self.nYIn * 0.25)
##        print( self.y0Out + self.nYOut * 0.25)

##
## Morning or afternoon swath
        self.doAM = True
        if self.doAM:
            self.suffix = '_am.gra'
            self.fidOut = Dataset( 'ascatAm2003Europe.nc', 'w', format = \
                                   'NETCDF3_CLASSIC')
        else:
            self.fidOut = Dataset( 'ascatPmHalfDegEurope.nc', 'w', format = \
                              'NETCDF3_CLASSIC')
            self.suffix = '_pm.gra'
##
##
##

        
    def readInput(self):
        fileName = self.rootDir + self.year + '/' + self.year + self.month + \
                   self.day + self.suffix    
        print( fileName )
        fidIn = open( fileName, 'rb' )
        
        inData = np.fromfile( fidIn, count = self.nYIn * self.nXIn, \
                              dtype = np.uint8 )\
                              .reshape( ( self.nYIn, self.nXIn ) )
        fidIn.close()
        return inData
##
##
##
    def takeASlice(self):
        print( 'Slice ', self.startYPoint, self.startXPoint, \
               self.endYPoint, self.endXPoint)
        
        localData = np.flipud( self.inputGrid)[ self.startYPoint: self.endYPoint, \
                           self.startXPoint: self.endXPoint]
        if self.averageOutput:
            meanData = np.zeros( ( self.nYOut, self.nXOut))
            for y in xrange( self.nYOut):
                for x in xrange( self.nXOut):
                    ii = localData[ y * 2: y * 2 + 2,\
                                    x * 2: x * 2 + 2]<= 255
                    if ii.sum() > 0:
                        meanData[ y, x] = localData[ y * 2: y * 2 + 2,\
                                                 x * 2: x * 2 + 2][ii].mean()
            return meanData
        else:
##            return localData
            return np.flipud(localData)        
##
#
##    
    def writeCDF(self):
        self.fidOut.createDimension( 'y', self.nYOut )
        self.fidOut.createDimension( 'x', self.nXOut )
        self.fidOut.createDimension( 't', self.nTimesIn )
        
        self.fidOut.createVariable( 'time', np.float32, ( 't') )
        self.fidOut.variables['time'].units = "Days since 01-01-2007"
        self.fidOut.variables['time'][:] = np.arange( self.nTimesIn )
        
        self.fidOut.createVariable( 'latitude', np.float32, ( 'y') )
        self.fidOut.variables['latitude'][:] = np.arange( self.y0Out, self.y0Out + \
                                                     self.nYOut * self.dXYOut , self.dXYOut )    
        
        self.fidOut.createVariable( 'longitude', np.float32, ( 'x') )
        self.fidOut.variables['longitude'][:] = np.arange( self.x0Out, self.x0Out + self.nXOut \
                                                      * self.dXYOut , self.dXYOut )    
        
        self.fidOut.createVariable( 'ssm', np.float32, ( 't', 'y', 'x' ) )
        
        self.fidOut.variables[ 'ssm'][:] =  self.outputGrid
        self.fidOut.close()
##
##
    def doStuff(self):
        
        self.outputGrid = np.zeros( ( self.nTimesIn, self.nYOut, \
                                      self.nXOut ), np.uint8 )
        count = 0
        for self.year in self.years:
            self.leap = isLeap(self.year)
            for self.month in self.months:
                for self.day in daysAsNumbers( self.month, self.leap ):

                    self.inputGrid = self.readInput()

                    print( self.outputGrid[ count, :, : ].shape)
                    print( self.takeASlice().shape)

                    self.outputGrid[ count, :, : ] = self.takeASlice()

                    count += 1
        self.writeCDF()
##
##
##
if __name__ == "__main__":


    a = mkAscat()

    a.doStuff()

