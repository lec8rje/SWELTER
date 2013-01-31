import numpy as np
from netCDF4 import Dataset
import matplotlib.pyplot as plt
import pickle
import os
import sys
from usefulFunctions import printUsual, yearsAsStrList,\
     monthsAsNumbers, daysAsNumbers, isLeap

class regridEra():
    '''
    A class to extract the relevant t2m temperature values
    from the global file and create a 0.5 deg domain for greater
    Europe.
    
    Author: RichE
    Date: Oct 16 2012
    Email: rjel@ceh.ac.uk
    
    '''  
    def __init__(self):
##define the output grid
        self.x0Out = -10.25
        self.y0Out = 59.75
        self.nXOut = 81
        self.nYOut = 50
        self.dxyOut = 0.5
##
## Only use True on first go as it adds to the time taken to run
##        
        self.fromScratch = False
        self.pickleFile = "mappingPickle.pl"
##
## Directory where we get the mapping file from        
        self.wfdEIRoot = "/prj/nceo/WFD-EI-Forcing/"
##
## Directory where we get the tAir data from        
        self.dataRoot = "../EIHDEC-land/"
## Years of interest
        self.years = yearsAsStrList( 2007, 2011)
##        self.years = yearsAsStrList( 2003, 2004)        
        self.months = monthsAsNumbers()
##
## this list will contain all the arrays to be written out at the end
        self.griddedData = {}
##        self.griddedData = []        
##
##
    def readWFDMApping(self):
##
        pointFile = self.wfdEIRoot + "swelterEuroPoints2.dat"
        fid = open( pointFile, "r")
        points = fid.read().split()
        fid.close()
##
## Turn the string into an integer list
##
        for point in xrange( len( points)):
            points[point] = int( points[ point ]) - 1
##
##
        longLatFile = self.wfdEIRoot + "EI-Halfdeg-land-elevation.nc"
        fidLL = Dataset( longLatFile, "r")
##
## Make the output grid
##        
        outLong = np.arange( self.x0Out, self.x0Out + \
                             self.nXOut * self.dxyOut, self.dxyOut)
        outLat = np.arange( self.y0Out, self.y0Out - \
                             self.nYOut * self.dxyOut, -self.dxyOut)

        self.mapping = []
        count = 0
        for point in points:

            print( point+1, (fidLL.variables['latitude'][point+1]\
                   == outLat).argmax(), \
                   fidLL.variables['latitude'][point+1])

            self.mapping.append( [\
                int((fidLL.variables['latitude'][point+1]\
                   == outLat).argmax()),
                int((fidLL.variables['longitude'][point+1]\
                   == outLong).argmax()),\
                fidLL.variables['latitude'][point+1],\
                fidLL.variables['longitude'][point+1],\
                int(point)+1])

        fP = open( self.pickleFile, "w")
        pickle.dump( self.mapping, fP)
        fP.close()
        fidLL.close()
##
##        
    def getFileList(self):
        fileList = os.listdir( self.dataRoot)
        self.nFiles = len( fileList )
##
##
    def gridData(self):
##
##  All Graham's files have the same start and end with
##  a combination of year and month in the middle        
        prefix = "Tair_EIHDEC_land_"
        suffix = ".nc"
##
        self.nDaysTotal = 0
        for year in self.years:
            self.griddedData[year] = {}
            for month in xrange(len(self.months)):
##            for month in xrange( 1):                
                self.griddedData[year][month] = []
                fName = self.dataRoot + \
                       prefix + year + self.months[month] + suffix
                print( fName)
## Does the file exist?
                try:
                    fid = Dataset( fName, "r")
##
## This will go in the try when it works
##                    
                    nDays = len(daysAsNumbers( self.months[month],\
                                       isLeap( int(year))))
                    localArray = np.zeros( (nDays, self.nYOut, self.nXOut)) - 999.0
##
                    for day in xrange( nDays):
                        self.nDaysTotal += 1
## there are eight timesteps in a day
## 0000 0300 0600 0900 1200 1500 1800 2100
###  0    1    2    3    4    5    6   7                        
##          and we are interested in the
##
##    0600, 0900 and 1200 steps.                    
                        startTime = day * 8 + 3
                        for point in xrange( len(self.mapping)):
##
## read the values in locally to make it explicit
                            inputVar = fid.variables["Tair"][ startTime: startTime + 3,self.mapping[point][4]]
##
## every three hours (the timestep of the input data) corresponds to 45 deg Longitude
## if the longitude is 0.0E then the required value is the mean of the 0900 and 1200
##  values                        

                            weight = 0.5 + self.mapping[point][3] / 45.0
                        
                            if self.mapping[point][3] <= 22.5:

                                localArray[ day, self.mapping[point][0],\
                                            self.mapping[point][1]] = \
                                            inputVar[1] *  weight + \
                                            inputVar[2] *  (1.0 - weight)
                            else:

                                weight = weight - np.fix( weight)
                            

                                localArray[ day, self.mapping[point][0],\
                                            self.mapping[point][1]] = \
                                            inputVar[1] *  ( 1.0- weight ) + \
                                            inputVar[0] *  weight

                    self.griddedData[year][month] = np.flipud(localArray)
  ##                  print( year, month, self.griddedData[year][month].shape)
                    fid.close()
                except:
                    print( "file not found")


##
##
    def writeCDFFile(self):
        fidOut = Dataset( "euroHalfDegWFDEITemp0900.nc", "w",\
                          format = 'NETCDF3_CLASSIC')
        fidOut.createDimension( 'y', self.nYOut )
        fidOut.createDimension( 'x', self.nXOut )
        fidOut.createDimension( 't', self.nDaysTotal )
        fidOut.createVariable( 'tAir',np.float32, ('t', 'y', 'x' ))
        time = 0
        for year in self.years:
            for month in xrange(len(self.months)):

                try:
                    dT = len(self.griddedData[year][month][:])
                    fidOut.variables["tAir"][time:time + dT, :, :] = \
                                                       self.griddedData[year][month]
                    time += dT
                except:
                    break
        fidOut.close()

##
##        
    def doStuff(self):
        if self.fromScratch:
            self.readWFDMApping()
        else:
            fP = open( self.pickleFile, "r")
            self.mapping = pickle.load( fP)
            fP.close()

##        self.getFileList()

        self.gridData()
        self.writeCDFFile()

##
##
if __name__ == "__main__":

    re = regridEra()
    re.doStuff()
