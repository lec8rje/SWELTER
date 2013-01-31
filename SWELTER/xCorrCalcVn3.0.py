import numpy as np
import matplotlib.pyplot as plt
from numpy.ma import MaskedArray, masked, nomask
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset
import sys
from usefulFunctions import printUsual
import scipy.special as special
###
class params():
    def __init__(self):
        self.quartDeg = True
##
## Define the European 0.25 deg grid
##        
        if self.quartDeg:
            self.lat0 = 35.125
            self.dxy = 0.25
            self.lon0 = -10.375
            self.nYOut = 100
            self.nXOut = 162
        else:
            self.lat0 = 39.875
            self.dxy = 0.5
            self.lon0 = -10.375
            self.nYOut = 40
            self.nXOut = 61

        self.years = [ '2007' ]
##        self.years = [ '2007', '2008', '2009', '2010', '2011']        
##
## Ascat data begins in Jan 2007
        self.tStartAscat = 90
##
## Era file begins in Jan 2000
##        self.tStartEra = ( 366 * 2 + 365 * 5 ) + self.tStartAscat
        self.tStartEra = self.tStartAscat        
##
        self.undefVal = -999.0
        self.pVal = 0.05
        self.tTable = []
        self.pixelThreshold = 0.1
##
##        self.modisVar = 'Other'
##        self.modisVar = 'Forest'
        self.modisVar = 'Crop'
##        self.modisVar = 'All'                
##
##        self.season = 'all'
        self.season = 'Early'        
##        self.season = 'Mid'        
##        self.season = 'Late'        
##
        if self.season == 'Early':
            self.nTYear = 60
            self.seasonOffset = 0
        elif self.season == 'Mid':
            self.nTYear = 60            
            self.seasonOffset = 60
        elif self.season == 'Late':
            self.nTYear = 120      
            self.seasonOffset = 60
        else:
## Number of days in the April to September period
            self.season == 'all'            
            self.nTYear = 183
            self.seasonOffset = 0
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
##
## We thought that adding the pm values from the day before
##  might give us better correlations as we would have more
##  Dofs but it turns out this is wiped out by the additional
##  noise. One day we might revisit this with a filter for
##  rainfall between the pm and am sm measurements but we would
##  need a reliable rainfall product at a sub diurnal scale for
##  the European domain.            
        self.addPM = False
##
## this is a standard t test table for confidence testing        
def readTable():
    table = []
    fid = open( '../tTable.txt', 'r')
    for line in xrange( 102 ):
        table.append( fid.readline().split() )
    fid.close()
    return table
##
##
def linregressOwn(*args):
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
        if (r > 1.0):
            r = 0.99999 # from numerical error
##
    sigT, regPoints = findSigT(x,y)
##
    slope = Sxy / Sxx
    intercept = ymean - slope*xmean
    sterrest = np.ma.sqrt(1.-r*r) * y.std()
##
    if float( sigT ) > np.abs( slope / sterrest):
        r = p.undefVal
        slope = p.undefVal
    return slope, intercept, r, sterrest, Syy/Sxx, regPoints
##
##
def findSigT(xIn,yIn):
##
## Added to check their sig test. Yes I know it is paranoid rjel
##   regPoints are the number of points going into the
##    regression calculation.
## Check that there are some points not masked out first. Else you
##        get horrible errors.
    if np.any( np.isreal( ( ( xIn <= 1.0) & ( np.isreal( yIn )) ) ) ):
        rPoints = int( ( ( xIn <= 1.0) & np.isreal( yIn )).sum())
    else:
        rPoints = 0
##    print( 'There are ', regPoints,' points in the calculation')
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
    pIndex = tTable[ 0 ].index( str( 1.0 - p.pVal ) )
    sigLocal = tTable[ nIndex][pIndex]

    return sigLocal, rPoints
##
##
def readMask():
    f = Dataset( "../newDomain/modisQuartBigEMask.nc", "r")
    v = f.variables['mask'][:]
    f.close()
    return v
##
##
def readPointSeries( xIn, yIn):
    ascat = np.array( (), ndmin = 1)
    ascatb = np.array( (), ndmin = 1)
    era = np.array( (), ndmin = 1)
    modis = np.array( (), ndmin = 1)
    nPoints = np.array( (), ndmin = 1)    
##
## Adjust the start point depending on the season chosen in init
    tEra = p.tStartEra + p.seasonOffset
    tAscat = p.tStartAscat + p.seasonOffset
    tModis = p.tStartAscat + p.seasonOffset
##
##
    for year in xrange( len( p.years )):
        nPoints = np.append( nPoints, fidModis.variables[ p.cdfN ][ tModis: tModis + p.nTYear, yIn, xIn] )

        ascat = np.append( ascat,  fidAscat.variables['ssm'][ tAscat : tAscat + p.nTYear, yIn, xIn] )
    
        ascatb = np.append( ascatb, fidAscatB.variables['ssm'][tAscat : tAscat + p.nTYear, yIn, xIn] )
    
        era = np.append( era, fidEra.variables['tAir'][ tEra: tEra + p.nTYear, yIn/2, xIn/2] )
##        era = np.append( era, fidEra.variables['t2m'][ tEra: tEra + p.nTYear, yIn, xIn] )        
        
        modis = np.append( modis, fidModis.variables[ p.cdfVar][ tModis: tModis + p.nTYear, yIn, xIn] )
        
        if np.mod( p.years[ year], 4 ) == 0:
            nDays = 366
        else:
            nDays = 365
        tEra += nDays
        tAscat += nDays
        tModis += nDays 

    if p.addPM:
        ii = ( ascat[1:] > 254.0 ) & ( ascatb[:-1] < 255.0 )
        ascat[1:][ii ] = ascatb[:-1][ ii]
    return ascat, modis, era, nPoints
##
##
def calcCorr():
    for y in xrange( p.nYOut ):        
        print( 'Row ', y )
        for x in xrange( p.nXOut ):            
            if mask[ y, x] < 0.0:
                continue
##
## read in the values for teh linear reg based on season and
##  landcover            
##
            ascat, modis, era, n = readPointSeries( x, y)
##
## Calculate the difference between t2m and tStar but only where
##   there are more pixels than the threshold            
##            
            diff = np.ma.masked_array( modis, ( n < p.pixelThreshold * n.max() ) \
                                       | ( modis < 0.0)  ) \
                                       - era 
##
## calculate the linear regression stats
##
            result = linregressOwn( np.ma.masked_array( ascat, \
                                ascat > 254.0 ) / 200.0, \
                                       diff )
##
##
            corrGrid[ y, x ] = result[2]
            slopeGrid[ y, x] =result[0]
            nGrid[ y, x ] = result[5]
            if nGrid[ y, x] < 0:
                print( x, y, nGrid[ y, x] )
                sys.exit( -1)
##
##
def drawMap(varName, var):                

    if varName == "slope":
        vMin = -15.0
        vMax = 5.0
    elif varName == "corCoef":
        vMin = -0.9
        vMax = 0.0
    elif varName == "nPoints":
        vMin = 0.0
        vMax = var.max()       
    else:
        vMin = var.min()
        vMax = var.max()
    m = Basemap( projection = 'cyl',llcrnrlon = p.lon0, \
                 llcrnrlat = p.lat0, urcrnrlon = p.lon0 + p.dxy * p.nXOut,\
                 urcrnrlat = p.lat0 + p.dxy * p.nYOut, resolution='l')

    im = m.imshow( np.flipud( np.ma.masked_array( var, ( var < - 900.0 ) | ( corrGrid >= 0.0 ) ) ), vmin = vMin, vmax = vMax, interpolation = 'nearest' )    

    m.drawmeridians(np.arange( -10.0, 20, 5), labels = [1,0,0,1], fontsize = 10, rotation = 20)
    m.drawparallels(np.arange( 40.0, 60.0, 5), labels = [1,0,0,1], fontsize = 10, rotation = 20)

    m.drawcoastlines()
    m.drawcountries()
##    m.drawrivers()
    plt.colorbar(im, orientation = 'horizontal' , pad = 0.05 )
    plt.title( varName + ' dT against  Ascat' + p.modisVar + ' ' + p.season )
    plt.savefig( varName + p.modisVar + p.season + '0p5.png', orientation = 'landscape')
    plt.clf()
##
##
def laggedResponse():
    print( "calculating lagged response" )
    lag = 5
    diff = np.where( ( n >= p.modisThresh * n.max() ) \
                     & ( modis > 0.0), modis - era, -999.0 )

    print( era.shape, 'is the number of days')
    aDiff = np.zeros( era.shape[0]) -999.0
    tDiff = np.zeros( era.shape[0]) -999.0    
    maxLag = 5
    for point in xrange( maxLag, era.shape[0] ):
        if ( ascat[point] < 255.0 ) & \
               ( diff[ point] > -900.0 ):
            for lagP in xrange( 1, maxLag, 1):
                if ( ascat[point - lagP] < 255.0 ) & \
                       ( diff[ point - lagP] > -900.0 ):
                
                    aDiff[point] = ascat[point] - ascat[point-lagP]

                    tDiff[point] = diff[ point] - diff[ point - lagP]
                    break
    return 
##
## Stop defining get running
##
if __name__ == "__main__":
##
##
    p = params()
    mask = readMask()
    tTable = readTable()
##
##
    fidAscat = Dataset( "../newDomain/ascatAmQuartBigEurope.nc", 'r')
    fidAscatB = Dataset( "../newDomain/ascatAmQuartBigEurope.nc", 'r')
    fidEra = Dataset( "../newDomain/euroHalfDegWFDEITemp.nc", 'r')
    fidModis = Dataset( '../newDomain/modisQuartBigEurope.nc', 'r')
 
##
    corrGrid = np.zeros( ( p.nYOut, p.nXOut) ) + p.undefVal
    slopeGrid = np.zeros( ( p.nYOut, p.nXOut) ) + p.undefVal
    nGrid = np.zeros( ( p.nYOut, p.nXOut) ) + p.undefVal
##
##
    calcCorr()
##
##
    drawMap( 'corCoef', corrGrid )
    drawMap( 'slope',  slopeGrid)
    drawMap( 'nPoints',  nGrid)    
##
    fidAscat.close()
    fidAscatB.close()
    fidEra.close()
    fidModis.close()


