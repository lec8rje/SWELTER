import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from netCDF4 import Dataset
from usefulFunctions import printUsual
from scipy.stats import mstats as stats
import sys
##
class pointCalc():
    def __init__(self):
##
## The files to read data in from
        self.fidAscat = Dataset( "../newDomain/ascatAmQuartBigEurope.nc", 'r')
        self.fidAscatB = Dataset( "../newDomain/ascatAmQuartBigEurope.nc", 'r')
        self.fidEra = Dataset( "../newDomain/euroHalfDegWFDEITemp.nc", 'r')
        self.fidModis = Dataset( '../newDomain/modisQuartBigEurope.nc', 'r')
## Define the point to be plotted
## East Anglian point of refernce with CMT
        self.latY = 52.625
        self.lonX = 1.125
##        self.latY = 51.125
##
## Define the domain for analysis lon lat for llcorner
        self.lat0 = 30.125
        self.lon0 = -10.375
##
        self.dxy = 0.25
        self.nYOut = 100
        self.nXOut = 162
        
##
        self.y = self.nYOut - int( ( self.latY - self.lat0 )\
                                   / self.dxy )
        self.x = int( ( self.lonX - ( self.lon0 ) ) / self.dxy )
##
##        self.years = [ '2007']
##        self.years = [ '2007', '2008', '2009', '2010', '2011']
        self.years = [ '2007', '2008', '2009', '2010']                

## Number of days in the April to September period
##
        self.nTYear = 183
##
## Ascat data begins in Jan 2007
        self.tStartAscat = 90
##
## Era file begins in Jan 2000
        self.tStartEra = self.tStartAscat
##        self.tStartEra = ( 366 * 2 + 365 * 5 ) + self.tStartAscat        
##
##
        self.modisThresh = 0.1
        self.pVal = 0.05
        self.tTable = []
##
##        self.modisVar = 'Other'
##        self.modisVar = 'Forest'
##        self.modisVar = 'Crop'
        self.modisVar = 'All'                
##
        self.seasons = [ {'Early':{ 0: 60}}, {'Mid':{ 60: 60}}, \
                         {'Late':{ 120: 60}}]
##
        if self.modisVar == 'Crop':
            self.cdfVar = 'lstC'
            self.cdfN = 'nC'
        elif self.modisVar == 'Forest':
            self.cdfVar = 'lstF'
            self.cdfN = 'nF'
        elif self.modisVar == 'Other':
            self.cdfVar = 'lstO'
            self.cdfN = 'nO'
        else:
            self.modisVar = 'All'
            self.cdfVar = 'lst'
            self.cdfN = 'n'                    
        self.symbols =  [ 'r', 'k', 'g']
##
        self.unDef = -999.0
##
## These values define the output options        
        self.diffPlot = False ## dt vs ascat or dt2/dascat
        self.savePlot = True ## Plot to screen or file
        self.addPm = False
##
## These are the vaiables we may plot depending on the options above
##   as they take no time to declare I just declare them all        
        self.diff = []
        self.aDiff = []
        self.tDiff = []
        self.ascat = []
        self.ascatb = []    
        self.allPointsA = np.array( [],ndmin = 1)
        self.allPointsT = np.array( [],ndmin = 1)
##
## For debugging and checking it is sometimes useful to export
##        the values to another analysis tool
## This writes out a csv file with ascat, modis and era data in it
##        
        self.writeText = False
##
## Likewise it can be useful to print extra stuff if you are debugging
        self.verbose = True
##
##        
    def runFunctions(self):
        self.tTable = self.readTable()
        self.pIndex = self.tTable[ 0 ].index( str( 1.0 - self.pVal ) )
        print( 'x is ',self.x, ' y is ',self.y)        
##
        self.sCount = 0
##
        for season in p.seasons:
            self.readInData()
##
            if self.addPm:
                self.ascat[ sCount ] = self.addPmData()
            if self.writeText:
                self.writeTetxFile()
##
            self.diff.append( np.where( ( self.nP >= self.modisThresh *\
                                          self.nP.max()) & ( self.modis > 0.0),\
                                        self.modis  - self.eraInt, self.unDef ) )

            self.ascat[ self.sCount] = np.where( self.ascat[ self.sCount] \
                < 255, self.ascat[ self.sCount] / 200.0, self.unDef )


            var1 = self.ascat[ self.sCount]
            var2 = self.diff[ self.sCount]

            self.regPoints = ( ( self.ascat[ self.sCount]!= self.unDef)\
                               & ( self.diff[ self.sCount ] \
                                   != self.unDef )).sum()

            print( 'There are ', self.regPoints,\
                   ' points in the calculation')            

            self.calcCorCoef( np.ma.masked_array( self.ascat[ self.sCount], \
                                                  self.ascat[ self.sCount] == self.unDef),\
                              np.ma.masked_array( self.diff[ self.sCount], self.diff[ self.sCount]\
                                                  == self.unDef))


            self.sCount += 1
        self.finishPLot( self.savePlot)
##
## Close the files for tidyness sake
##
        self.fidAscat.close()
        self.fidAscatB.close()
        self.fidEra.close()
        self.fidModis.close()

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
    def readInData(self):    

        ast = np.array( (), ndmin = 1)
        astb = np.array( (), ndmin = 1)
        self.eraInt = np.array( (), ndmin = 1)
        self.modis = np.array( (), ndmin = 1)
        self.nP = np.array( (), ndmin = 1)
##
        nTSeason = self.seasons[self.sCount].values()[0].values()[0]
        seasonOffset = self.seasons[self.sCount].values()[0].keys()[0]
##
        tEra = self.tStartEra + seasonOffset
        tAscat = self.tStartAscat + seasonOffset
        tModis = self.tStartAscat + seasonOffset
        print( 'Data from these times are being read ', tModis, tModis + nTSeason )
        for year in xrange( len( self.years )):        
            
            self.nP = np.append( self.nP, self.fidModis.variables[ self.cdfN ]\
                                 [ tModis: tModis + nTSeason, self.y, self.x] )
            
            self.modis = np.append( self.modis, self.fidModis.variables[ self.cdfVar]\
                                  [ tModis: tModis + nTSeason, self.y, self.x] )
            ast = np.append( ast,  self.fidAscat.variables['ssm']\
                                  [ tAscat : tAscat + nTSeason, self.y, self.x] )
            astb = np.append( astb, self.fidAscatB.variables['ssm']\
                                   [tAscat : tAscat + nTSeason, self.y, self.x] )
            
            self.eraInt = np.append( self.eraInt, self.fidEra.variables['tAir']\
                                     [ tEra: tEra + nTSeason, self.y/2, self.x/2] )

            

            if np.mod( self.years[ year], 4 ) == 0:
                tEra += 366
                tAscat += 366
                tModis += 366
            else:
                tEra += 365
                tAscat += 365
                tModis += 365
        self.ascat.append( ast)
        self.ascatb.append( astb)


        plt.plot( self.eraInt)
        plt.show()
##
##
    def writeTextFile(self):
        f = open( 'pythonPointData' + season + '.csv', 'w')
        for line in xrange( era.shape[0]):
            if ( n[line] > self.modisThresh * n.max() ) & ( self.modis[line] > 0.0) & ( self.ascat[line] <= 255 ):
                f.write( str( self.era[line] ) + ', ' + str( self.modis[line])  + ', ' + str( self.ascat[line] ) + '\n'  )
            
        f.close()
##
##
    def addPmData(self):
        asNew = self.ascat[ self.sCount].copy()
        asNew[ 1: ] = np.where( self.ascat[self.sCount][1:] \
                                < 255.0, ascat[self.sCount][1:], 
                                self.ascatb[ self.sCount][:-1] )
        self.ascat[self.sCount] = asNew
    
    def calcCorCoef( self, var1, var2):
##
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
##
##
    def finishPLot(self, save):

        markers = [ 'ro', 'ko', 'go']

        allPointsA = np.array( [],ndmin = 1)
        allPointsT = np.array( [],ndmin = 1)    

        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)
        sCount = 0
        for season in p.seasons:
            print( season )
            if self.diffPlot:
                ax1.plot(  aDiff[ sCount][aDiff[ sCount] != p.unDef],\
                           tDiff[ sCount][tDiff[ sCount] != p.unDef],\
                           markers[ sCount], label = season.keys()[0])

                calcCorCoef( \
                    aDiff[sCount][aDiff[ sCount] != p.unDef],\
                    tDiff[sCount][tDiff[ sCount] != p.unDef])

                plotX = np.arange( -0.6, 0.6, 0.1)
                plotY = intercept + plotX * slope
                ax1.plot( plotX, plotY, markers[ sCount][0])
            else:
##                print( len( self.ascat))
##                print( len(self.diff))
##                print( 'sCount b is ',sCount)
##                print( self.ascat[ sCount][ self.ascat[ sCount] != self.unDef].shape)
##                print( self.diff[ sCount][ self.diff[ sCount] != self.unDef].shape)
                ii = ( self.ascat[ sCount] != self.unDef) & ( self.diff[ sCount] != self.unDef) 
                ax1.plot(  self.ascat[ sCount][ii],\
                           self.diff[ sCount][ ii],\
                           markers[ sCount], label = season.keys()[0])

##                ax1.plot(  self.ascat[ sCount][ self.ascat[ sCount] != self.unDef],\
##                           self.diff[ sCount][ self.diff[ sCount] != self.unDef],\
##                           markers[ sCount], label = season.keys()[0])                

                self.calcCorCoef( \
                    self.ascat[sCount][ii], self.diff[sCount][ii])

                plotX = np.arange( 0.0, 1.0, 0.1)
                plotY = self.intercept + plotX * self.slope
                ax1.plot( plotX, plotY, markers[ sCount][0], linewidth=2)
            sCount += 1
##
        plt.legend()
        if self.diffPlot:
            plotX = np.arange( -0.6, 0.6, 0.1)
            plotY = intercept + plotX * slope
            ax1.plot( plotX, plotY, 'c-')

            plt.title( 'Site Lon' + str( self.lonX) + ' Lat ' + str( self.latY ) )
            plt.ylabel( 'd lst - T2m dt K')
            plt.xlabel( 'd Ascat SM index dt')

##            ax1.annotate( 'r     ' + str( corcoef ), xy= ( -0.5, -4.0) )
##            ax1.annotate( 'slope ' + str( slope ), xy= ( -0.5, -4.6) )


            plt.savefig( 'SiteLon' + str( self.lonX) + 'Lat' + str( self.latY ) + \
                         'dTDAscat.png')
        else:
            plt.xlim( ( 0.0, 1.0))
##            plt.ylim(( -7.0, 12.5))
##            plt.ylim(( 0.0, 15.5))
            plt.yticks( np.arange( 0.0, 15.0, 2.0))
##            plt.yticks( np.arange( -6.0, 14.0, 2.0))            
            mpl.rcParams.update({'font.size': 18})
            plt.legend()
            plt.title( 'lst-T2m vs SM Index Lon ' + str( self.lonX ) + \
                       ' Lat ' + str( self.latY ))
            plt.ylabel( 'lst - T2m K')
            plt.xlabel( 'Ascat SM index')
            plt.grid(True)
            if save:
                plt.savefig('scatterLon' + str( self.lonX ) + 'Lat' +  str( self.latY ) + \
                            p.modisVar + str( self.modisThresh) + '.png', \
                            orientation = 'landscape') 
            else:
                plt.show()
##
##
def laggedResponse():
    print( "calculating lagged response" )

    print( era.shape, 'is the number of days')
    aD = np.zeros( era.shape[0]) -999.0
    tD = np.zeros( era.shape[0]) -999.0    
    maxLag = 7
##
    for point in xrange( maxLag, era.shape[0] ):
        if ( ascat[ sCount][point] != p.unDef ) & \
               ( diff[ sCount][ point] != p.unDef ):
##
            for lagP in xrange( 1, maxLag, 1):
                if ( ascat[ sCount][point - lagP] != p.unDef ) & \
                       ( diff[ sCount][ point - lagP] != p.unDef ):
##
                    aD[point] = ascat[ sCount][point] - \
                                ascat[ sCount][point-lagP]
                    tD[point] = diff[ sCount][ point] - \
                                diff[ sCount][ point - lagP]
                    break
    return aD, tD



##
##    
if __name__ == "__main__":    
    p = pointCalc()

    p.runFunctions()
    ##
    ##    ad, td = laggedResponse()
    ##    aDiff.append( ad)
    ##    tDiff.append( td)
    ##
    ##
    ## regPoints = (( aDiff[ sCount] != p.unDef) &\
    ##                  ( tDiff[ sCount] != p.unDef )).sum()
    ## print( 'There are ', regPoints,' points in the calculation')
    ## corcoef, slope, intercept, diff = calcCorCoef( aDiff[ sCount]
    ##                                                    , tDiff[ sCount])
    ## allPointsA = np.append( allPointsA, \
    ##                             aDiff[sCount][aDiff[ sCount] != p.unDef])
    ## allPointsT = np.append( allPointsT, \
    ##                             tDiff[sCount][tDiff[ sCount] != p.unDef])


    ## iiP2 = allPointsA >= 0.0
    ## iiP = allPointsA < 0.0

    ## print('Long ',lonX,' Lat ',latY )
    ## print( 'Da > 0.2 ', allPointsA[ iiP2 ].mean(), 'Dt > 0.2 ',allPointsT[ iiP2].mean() )
    ## print( 'Da < 0.2 ',allPointsA[ iiP ].mean(), 'Dt < 0.2 ',allPointsT[ iiP].mean() )

