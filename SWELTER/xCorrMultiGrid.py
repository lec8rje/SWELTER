###from loadUsual import loadUsual
from numpy.ma import MaskedArray, masked, nomask
from scipy.stats import mstats as stats
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
import sys
class corrPoint():
    def __init__(self):
##
## We carry out the analysis with a number of data sets
##    these switches change the input streams        
##
        self.aqua = True

        self.ascat = True
##
        self.fromScratch = True
##
##
        self.fidAscat = Dataset( "../newDomain/ascatAmQuartBigEurope.nc", 'r')        

        if self.aqua:
            self.fidModis = Dataset( '../newDomain/aquaQuartBigEurope.nc', 'r')        
            self.fidEra = Dataset( "../newDomain/euroHalfDegWFDEITemp1200.nc", 'r')
        else:
            self.fidModis = Dataset( '../newDomain/terraQuartBigEurope.nc', 'r')                
            self.fidEra = Dataset( "../newDomain/euroHalfDegWFDEITemp0900.nc", 'r')
## Define the point to be plotted
## East Anglian point of refernce with CMT
        self.latY = 48.125
##        self.latY = 52.125        
        self.lonX = 0.125

## Define the domain for analysis lon lat for llcorner
        self.lat0 = 60.125
##        self.lat0 = 35.125        
        self.lon0 = -10.375
        self.dxy = 0.25
        self.nYOut = 100
        self.nXOut = 162

        self.nXEra = 81
        self.nYEra = 50

        
##        self.y = int( ( self.lat0 - self.latY  )\
##                      / self.dxy )

##        self.x = int( (  self.lonX - self.lon0 ) / self.dxy )
##
##
        self.years = [ '2007', '2008', '2009', '2010']

        self.months = [ ( 59, 90 ), ( 91, 120), ( 121, 150), \
                        ( 151, 180),( 181, 211),( 212, 242), \
                        ( 243, 272), (273, 303) ]

##        self.months = [ (  91, 120), ( 121, 150), ( 151, 180),\
##                        ( 181, 211), ( 212, 242), ( 243, 272) ]

        self.pVal = 0.01

        self.verbose = False
##
##
        self.undef = -999.0

    def readMask(self):
        fid = Dataset( "../newDomain/bigEuroMask.nc", "r")
        self.mask = fid.variables['lsm'][:].copy()
        fid.close()

    def loopOverGrid(self):

        self.corrCoeffGrid = np.zeros( ( len( self.months), self.nYEra, self.nXEra)) + self.undef
        self.slopeGrid = np.zeros( ( len( self.months), self.nYEra, self.nXEra)) + self.undef
        self.nPGrid = np.zeros( ( len( self.months), self.nYEra, self.nXEra)) + self.undef                

        for self.yEra in xrange( 1, self.nYEra):
            for self.xEra in xrange( 1, self.nXEra):

##                if np.any(self.mask[self.yEra-1:self.yEra+2,\
##                                 self.xEra-1:self.xEra+2 ] < 1.0):
                if self.mask[self.yEra,self.xEra] < 1.0:
                    continue

                self.y = self.yEra * 2
                self.x = self.xEra * 2
                for self.month in xrange( len(self.months)):
                    self.readVars()
                    self.filterUndefs()            
##
##
    def readVars(self):
## Initialise the arrays we will read the
        self.eraInt = np.array( (), ndmin = 1)
        self.modis = np.array( (), ndmin = 1)
        self.ascat = np.array( (), ndmin = 1)        
##        
        yearCount = 0
        tStart = 0
        for year in xrange( len(self.years)):

            self.eraInt = np.append( self.eraInt, self.fidEra.variables['tAir']\
                                     [ tStart + self.months[self.month][0]: \
                                       tStart + self.months[self.month][1], self.yEra, self.xEra] )

            self.modis = np.append( self.modis, self.fidModis.variables[ "lst"]\
                                    [ tStart + self.months[self.month][0]: \
                                      tStart + self.months[self.month][1], self.y, self.x] )
            
            self.ascat = np.append( self.ascat,  self.fidAscat.variables['ssm']\
                                    [ tStart + self.months[self.month][0]: \
                                      tStart + self.months[self.month][1], self.y, self.x] )
##
##
            self.eraInt = np.append( self.eraInt, self.fidEra.variables['tAir']\
                                     [ tStart + self.months[self.month][0]: \
                                       tStart + self.months[self.month][1], self.yEra, self.xEra] )
            
            self.modis = np.append( self.modis, self.fidModis.variables[ "lst"]\
                                    [ tStart + self.months[self.month][0]: \
                                      tStart + self.months[self.month][1], self.y, self.x+1] )
            
            self.ascat = np.append( self.ascat,  self.fidAscat.variables['ssm']\
                                    [ tStart + self.months[self.month][0]: \
                                      tStart + self.months[self.month][1], self.y, self.x+1] )
            
            
            self.eraInt = np.append( self.eraInt, self.fidEra.variables['tAir']\
                                     [ tStart + self.months[self.month][0]: \
                                       tStart + self.months[self.month][1], self.yEra, self.xEra] )
            
            self.modis = np.append( self.modis, self.fidModis.variables[ "lst"]\
                                    [ tStart + self.months[self.month][0]: \
                                      tStart + self.months[self.month][1], self.y+1, self.x] )

            self.ascat = np.append( self.ascat,  self.fidAscat.variables['ssm']\
                                    [ tStart + self.months[self.month][0]: \
                                      tStart + self.months[self.month][1], self.y+1, self.x] )


            self.eraInt = np.append( self.eraInt, self.fidEra.variables['tAir']\
                                     [ tStart + self.months[self.month][0]: \
                                       tStart + self.months[self.month][1], self.yEra, self.xEra] )
            
            self.modis = np.append( self.modis, self.fidModis.variables[ "lst"]\
                                    [ tStart + self.months[self.month][0]: \
                                      tStart + self.months[self.month][1], self.y+1, self.x+1] )

            self.ascat = np.append( self.ascat,  self.fidAscat.variables['ssm']\
                                    [ tStart + self.months[self.month][0]: \
                                      tStart + self.months[self.month][1], self.y+1, self.x+1] )

                
            if np.mod( int( self.years[ year]), 4 ) == 0:
                tStart += 366
            else:
                tStart += 365
##
##
    def filterUndefs(self):
##
## Find the number of times that have measurements for
##  ascat and modis        
##
        ii = ( self.ascat < 255) &\
             ( self.modis > -254)

        localAscat = self.ascat[ii] / 200.0
        localDiff = self.modis[ii] - self.eraInt[ii]
##
## How many points are going into the corcoeff calculation
##
        if ii.sum() >=3:
            self.regPoints = ii.sum()
            self.nPGrid[ self.month, self.yEra, self.xEra] = ii.sum()
            self.calcCorCoef( localAscat, localDiff)

##        print( self.yEra, self.xEra, self.month, ii.sum(), self.corrCoeffGrid[ self.month, self.yEra, self.xEra])

            
        
##
##
    def readTable(self):
        table = []
        fid = open( '../tTable.txt', 'r')
        for line in xrange( 102 ):
            table.append( fid.readline().split() )
        fid.close()
        return table
##
##
    def linregressOwn(self,*args):
        if len(args) == 1:  # more than 1D array?
            args = np.ma.array(args[0], copy=True)
            if len(args) == 2:
                x = args[0]
                y = args[1]
            else:
                x = args[:,0]
                y = args[:,1]
        else:
            x = np.ma.array(args[0]).flatten()
            y = np.ma.array(args[1]).flatten()
        m = np.ma.mask_or(np.ma.getmask(x), np.ma.getmask(y))
        if m is not nomask:
            x = np.ma.array(x,mask=m)
            y = np.ma.array(y,mask=m)
##
##
        (xmean, ymean) = (x.mean(), y.mean())
        (xm, ym) = (x-xmean, y-ymean)
        (Sxx, Syy) = (np.ma.add.reduce(xm*xm), np.ma.add.reduce(ym*ym))
        Sxy = np.ma.add.reduce(xm*ym)
        r_den = np.ma.sqrt(Sxx*Syy)
        if r_den == 0.0:
            r = 0.0
        else:
            r = Sxy / r_den
##            if (r > 1.0):
##                plt.plot( x,y)
##                plt.show()
##                r = 0.99999 # from numerical error
##
        sigT, regPoints = self.findSigT(x,y)
##
        slope = Sxy / Sxx
        intercept = ymean - slope*xmean
        sterrest = np.ma.sqrt(1.-r*r) * y.std()
##
        if float( sigT ) > np.abs( slope / sterrest):
            r = self.undef
            slope = self.undef
        return slope, intercept, r, sterrest, Syy/Sxx, regPoints
##
##
    def findSigT(self,xIn,yIn):
##
## Added to check their sig test. Yes I know it is paranoid rjel
##   regPoints are the number of points going into the
##    regression calculation.
## Check that there are some points not masked out first. Else you
##        get horrible errors.
        if np.any( np.isreal( ( ( xIn <= 1.0) & ( np.isreal( yIn )) ) )):
            rPoints = int( ( ( xIn <= 1.0) & np.isreal( yIn )).sum())
        else:
            rPoints = 0
##
## Find the value in the ttest table corresponding to n and
##    the p value of interest. The table I downloaded had 1-100
##        points then more than 100
        if ( rPoints < 103 ) & ( rPoints > 2 ) :
            nIndex = rPoints -2
##
## if there are less than 2 points don't bother
        elif ( rPoints <= 2):
            return 3000.0, rPoints
        else:
            nIndex = 101
## The first line of the t-table file has the p values in it
##  so we can search a split first line for the column
##   that contains a given p-value        
##        
        pIndex = self.tTable[ 0 ].index( str( 1.0 - p.pVal ) )
        sigLocal = self.tTable[ nIndex][pIndex]

        return sigLocal, rPoints
    
    def calcCorCoef( self, var1, var2):
            
        result = self.linregressOwn( var1, var2)

        self.slope = result[0]

        self.intercept = result[1]
##        print( self.month, self.yEra, self.xEra)
##        print( var1.shape, var2.shape)

        self.corrCoeffGrid[ self.month, self.yEra, self.xEra] = result[2]
        self.slopeGrid[ self.month, self.yEra, self.xEra] = result[0]

        if self.verbose:
            print("******************************************")
            print( "slope = ", self.slope )
            print( "intercept = ", self.intercept )
            print( "r_value = ",result[2])
            print( "std_err = ", result[4] )
            print( "t value = ", np.abs( result[0] ) /  result[4] )
            print( "tCrit = ", self.tTable[ min( self.regPoints, 101)]\
                   [ self.pIndex])
            print("************************************************")

##
##
    def writeCorCoeffCdf(self):
        if self.aqua:
            fidOut = Dataset("corCoefMonthlyAqua.nc", "w",\
                             format = "NETCDF3_CLASSIC")
        else:
            fidOut = Dataset("corCoefMonthlyTerra.nc", "w",\
                             format = "NETCDF3_CLASSIC")            
            fidOut.createDimension( 't', len( self.months))
            fidOut.createDimension( 'y', self.nYEra)
            fidOut.createDimension( 'x', self.nXEra)
            fidOut.createVariable( 'r', np.float32, [ 't', 'y', 'x'])
##            print(fidOut.variables['r'][:].shape, self.corrCoeffGrid[:].shape)
            fidOut.variables['r'][:] = self.corrCoeffGrid[:]
            fidOut.close()


    def writeSlopeCdf(self):
        if self.aqua:
            fidOut = Dataset("slopeMonthlyAqua.nc", "w",\
                             format = "NETCDF3_CLASSIC")
        else:
            fidOut = Dataset("slopeMonthlyTerra.nc", "w",\
                             format = "NETCDF3_CLASSIC")
        fidOut.createDimension( 't', len( self.months))
        fidOut.createDimension( 'y', self.nYEra)
        fidOut.createDimension( 'x', self.nXEra)
        fidOut.createVariable( 'slope', np.float32, [ 't', 'y', 'x'])
        fidOut.variables['slope'][:] = self.slopeGrid[:]
        fidOut.close()


    def writeNPCdf(self):
        if self.aqua:
            fidOut = Dataset("nPMonthlyAqua.nc", "w",\
                             format = "NETCDF3_CLASSIC")
        else:
            fidOut = Dataset("nPMonthlyTerra.nc", "w",\
                             format = "NETCDF3_CLASSIC")  
        fidOut.createDimension( 't', len( self.months))
        fidOut.createDimension( 'y', self.nYEra)
        fidOut.createDimension( 'x', self.nXEra)
        fidOut.createVariable( 'np', np.float32, [ 't', 'y', 'x'])
        fidOut.variables['np'][:] = self.nPGrid[:]
        fidOut.close()        
                             
    def closeFiles(self):
        self.fidAscat.close()
        self.fidEra.close()
        self.fidModis.close()
##
##
    def doStuff(self):
##
## Read the tTable in

        if self.fromScratch:
            self.tTable = self.readTable()
            self.pIndex = self.tTable[ 0 ].index( \
                str( 1.0 - self.pVal ) )
##
            self.readMask()
##
            self.loopOverGrid()


            self.writeCorCoeffCdf()
            self.writeSlopeCdf()
            self.writeNPCdf()                

            self.closeFiles()
        else:
            pass
##
##
if __name__ == "__main__":    

    p = corrPoint()

    p.doStuff()
