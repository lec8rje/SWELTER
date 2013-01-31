import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from usefulFunctions import printUsual
from scipy.stats import mstats as stats
class corrPoint():
    def __init__(self):
        
        self.fidAscat = Dataset( "../newDomain/ascatAmQuartBigEurope.nc", 'r')
        self.fidEra = Dataset( "../newDomain/euroHalfDegWFDEITemp.nc", 'r')
        self.fidModis = Dataset( '../newDomain/modisQuartBigEurope.nc', 'r')        
## Define the point to be plotted
## East Anglian point of refernce with CMT

        self.latY = 52.125        
        self.lonX = 0.125

##        self.latY = 46.125
##        self.lonX = 28.125

##        self.latY = 48.25
##        self.lonX = -4.25        

## Define the domain for analysis lon lat for llcorner
        self.lat0 = 60.125
##        self.lat0 = 35.125        
        self.lon0 = -10.375
        self.dxy = 0.25
        self.nYOut = 100
        self.nXOut = 162
##        self.y = int( ( self.latY - self.lat0 )\
        self.y = int( ( self.lat0 - self.latY )\
                      / self.dxy )

##        self.y = self.nYOut = 100 - 4
##        self.x = 10
        self.x = int( (  self.lonX - self.lon0 ) / self.dxy )
##
##
        print( self.x, self.y)

        self.years = [ '2007', '2008', '2009', '2010']

        self.months = [ (  91, 120), ( 121, 150), ( 151, 180),\
                        ( 181, 211), ( 212, 242), ( 243, 272) ]

        self.strMonths = [ "Apr", "May", "Jun", "Jul", "Aug", "Sep"]
        self.pVal = 0.05


        self.ascat2Plot = []
        self.diffs2Plot = []        


        self.verbose = True
        
    def readVars(self):
## Initialise the arrays we will read the
        self.eraInt = np.array( (), ndmin = 1)
        self.modis = np.array( (), ndmin = 1)
        self.ascat = np.array( (), ndmin = 1)        
##        
        yearCount = 0
        tStart = 0
        print( self.months[self.month], \
               self.months[self.month][0],\
               self.months[self.month][1])
        for year in xrange( len(self.years)):

            self.eraInt = np.append( self.eraInt, self.fidEra.variables['tAir']\
                                     [ tStart + self.months[self.month][0]: \
                                       tStart + self.months[self.month][1], self.y/2-1, self.x/2] )

            self.modis = np.append( self.modis, self.fidModis.variables[ "lst"]\
                                    [ tStart + self.months[self.month][0]: \
                                      tStart + self.months[self.month][1], self.y-1, self.x] )
            
            self.ascat = np.append( self.ascat,  self.fidAscat.variables['ssm']\
                                    [ tStart + self.months[self.month][0]: \
                                      tStart + self.months[self.month][1], self.y-1, self.x] )
##
##
            self.eraInt = np.append( self.eraInt, self.fidEra.variables['tAir']\
                                     [ tStart + self.months[self.month][0]: \
                                       tStart + self.months[self.month][1], self.y/2-1, self.x/2] )
            
            self.modis = np.append( self.modis, self.fidModis.variables[ "lst"]\
                                    [ tStart + self.months[self.month][0]: \
                                      tStart + self.months[self.month][1], self.y-1, self.x+1] )
            
            self.ascat = np.append( self.ascat,  self.fidAscat.variables['ssm']\
                                    [ tStart + self.months[self.month][0]: \
                                      tStart + self.months[self.month][1], self.y-1, self.x+1] )
            
            
            self.eraInt = np.append( self.eraInt, self.fidEra.variables['tAir']\
                                     [ tStart + self.months[self.month][0]: \
                                       tStart + self.months[self.month][1], self.y/2, self.x/2] )
            
            self.modis = np.append( self.modis, self.fidModis.variables[ "lst"]\
                                    [ tStart + self.months[self.month][0]: \
                                      tStart + self.months[self.month][1], self.y-2, self.x] )

            self.ascat = np.append( self.ascat,  self.fidAscat.variables['ssm']\
                                    [ tStart + self.months[self.month][0]: \
                                      tStart + self.months[self.month][1], self.y-2, self.x] )


            self.eraInt = np.append( self.eraInt, self.fidEra.variables['tAir']\
                                     [ tStart + self.months[self.month][0]: \
                                       tStart + self.months[self.month][1], self.y/2-1, self.x/2] )
            
            self.modis = np.append( self.modis, self.fidModis.variables[ "lst"]\
                                    [ tStart + self.months[self.month][0]: \
                                      tStart + self.months[self.month][1], self.y-2, self.x+1] )

            self.ascat = np.append( self.ascat,  self.fidAscat.variables['ssm']\
                                    [ tStart + self.months[self.month][0]: \
                                      tStart + self.months[self.month][1], self.y-2, self.x+1] )

                
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

        self.ascat2Plot.append(localAscat) 
        self.diffs2Plot.append(localDiff)

##
## How many points are going into the corcoeff calculation
##
        self.regPoints = ii.sum()
        self.calcCorCoef( localAscat, localDiff)
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
    def calcCorCoef( self, var1, var2):
        result = stats.linregress( var1, var2)
        self.slope = result[0]
        self.intercept = result[1]
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
            self.corrCoeffs[ self.month] = result[2]
##
##
    def closeFiles(self):
        self.fidAscat.close()
        self.fidEra.close()
        self.fidModis.close()
##
##
    def plotStuff(self):
        nX = 2
        nY = 3
        plot = 0
        f, axn = plt.subplots(nY,nX,sharex=True,sharey=True)

        for x in xrange(nX):
            for y in xrange( nY):
                axn[y,x].plot( self.ascat2Plot[plot], \
                               self.diffs2Plot[plot], 'k+')

                axn[y,x].annotate( "R = " + \
                                   str( self.corrCoeffs[plot]),\
                                   xy=(0.4,10), xycoords="data")

##                axn[x,y].set_title( "Lon " + str( self.lonX) +\
##                                "Lat " + str( self.latY) +\
##                                "month " + self.strMonths[ self.month])

                axn[y,x].set_title( "Month " + \
                                    self.strMonths[plot])
                if ( plot == 2) | ( plot == 5):
                    print("Woooohoooo!")
                    axn[y,x].set_xlabel( "Ascat soil moisture")



##                if ( plot != 2) & ( plot != 5):
##                    print("Woooohoooo!")
##                    axn[y,x].set_xticks( [],[])

                if ( plot == 1):
                    print("Woooohoooo!")
                    axn[y,x].set_ylabel( "lst-T2m K")
                    
                plot += 1
        plt.savefig("scatterPlot.png", orientation = "landscape")
        plt.clf()                

    def doStuff(self):
##
## Read the tTable in
        self.tTable = self.readTable()
        self.pIndex = self.tTable[ 0 ].index( str( 1.0 - self.pVal ) )
##
        self.corrCoeffs = np.zeros( len( self.months))
##


        for self.month in xrange( len(self.months)):
            self.readVars()
            self.filterUndefs()


        self.closeFiles()

        self.plotStuff()

        plt.plot( self.corrCoeffs)
        plt.savefig("seasonCoeff.png", orientation = "landscape")
        plt.show()


##
##
if __name__ == "__main__":    

    p = corrPoint()

    p.doStuff()
##            plt.xlim( 0.0, 0.9)
##            plt.ylim( 0, 16)





