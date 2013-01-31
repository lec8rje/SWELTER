from usefulFunctions import monthsAsNumbers
from usefulFunctions import daysAsNumbers
from usefulFunctions import yearsAsStrList
from usefulFunctions import isLeap
from usefulFunctions import printUsual
class params():


    def __init__(self):
##
## Parameters defining the input grid and file structure
##
        self.nXIn = 162
        self.x0In = -10.375
##        self.x0In = -9.875        
        self.nYIn = 100
        self.y0In = 35.125
        self.nTimesIn = 1826
        self.startYear = 2007
        self.endYear = 2011 + 1
        self.months = monthsAsNumbers()
        self.years = yearsAsStrList( self.startYear, self.endYear )
        self.rootDir =\
                     '/users/global/cmt/SWELTER/lst/SWELTER_terra_025deg_files/'
##                     '/users/global/cmt/SWELTER/lst/SWELTER_aqua_025deg_files/'


        self.averageInput = False
## Parameters defining the output grid and netcdf file
##
        if self.averageInput:
## Half degree grid
            self.nXOut = 81
            self.nYOut = 50
            self.x0Out = -10.375
            self.y0Out = 35.125
        else:
            self.nXOut = 162
            self.nYOut = 100
            self.x0Out = -10.375
            self.y0Out = 35.125
##
##
def readInput():
    fileName = p.rootDir + 'lst_025deg_'  + year + month + day + '.gra'


    if ( month == '01' ) | ( month == '02' ) |\
           ( month == '11' ) | ( month == '12' ):
        return np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0, \
               np.zeros( ( p.nYOut, p.nXOut ) ), \
               np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0, \
               np.zeros( ( p.nYOut, p.nXOut ) ),\
               np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0, \
               np.zeros( ( p.nYOut, p.nXOut ) ),\
               np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0, \
               np.zeros( ( p.nYOut, p.nXOut ) ),\
               np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0, \
               np.zeros( ( p.nYOut, p.nXOut ) )
    else:
        try:
            fidIn = open( fileName, 'rb' )
            print( 'Found file ' + fileName)
            inData = np.fromfile( fidIn, count = p.nYIn * p.nXIn, \
                                  dtype = np.float32 ).byteswap()\
                                  .reshape( ( p.nYIn, p.nXIn ) )
            inN = np.fromfile( fidIn, count = p.nYIn * p.nXIn, \
                               dtype = np.float32 ).byteswap()\
                               .reshape( ( p.nYIn, p.nXIn ) )
            inData2 = np.fromfile( fidIn, count = p.nYIn * p.nXIn, \
                                   dtype = np.float32 ).byteswap()\
                                   .reshape( ( p.nYIn, p.nXIn ) )
            inN2 = np.fromfile( fidIn, count = p.nYIn * p.nXIn, \
                                dtype = np.float32 ).byteswap()\
                                .reshape( ( p.nYIn, p.nXIn ) )
            inData3 = np.fromfile( fidIn, count = p.nYIn * p.nXIn, \
                                   dtype = np.float32 ).byteswap()\
                                   .reshape( ( p.nYIn, p.nXIn ) )
            inN3 = np.fromfile( fidIn, count = p.nYIn * p.nXIn, \
                                dtype = np.float32 ).byteswap()\
                                .reshape( ( p.nYIn, p.nXIn ) )
            inData4 = np.fromfile( fidIn, count = p.nYIn * p.nXIn, \
                                   dtype = np.float32 ).byteswap()\
                                   .reshape( ( p.nYIn, p.nXIn ) )
            inN4 = np.fromfile( fidIn, count = p.nYIn * p.nXIn, \
                                dtype = np.float32 ).byteswap()\
                                .reshape( ( p.nYIn, p.nXIn ) )
            inData5 = np.fromfile( fidIn, count = p.nYIn * p.nXIn, \
                                   dtype = np.float32 ).byteswap()\
                                   .reshape( ( p.nYIn, p.nXIn ) )
            inN5 = np.fromfile( fidIn, count = p.nYIn * p.nXIn, \
                                dtype = np.float32 ).byteswap()\
                                .reshape( ( p.nYIn, p.nXIn ) )
            fidIn.close()
        except:
            return np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0, \
               np.zeros( ( p.nYOut, p.nXOut ) ), \
               np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0, \
               np.zeros( ( p.nYOut, p.nXOut ) ),\
               np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0, \
               np.zeros( ( p.nYOut, p.nXOut ) ),\
               np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0, \
               np.zeros( ( p.nYOut, p.nXOut ) ),\
               np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0, \
               np.zeros( ( p.nYOut, p.nXOut ) )
##
##
##
    if p.averageInput:
        outData = np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0
        outData2 = np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0
        outData3 = np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0
        outData4 = np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0
        outData5 = np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0

        outN = np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0
        outN2 = np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0
        outN3 = np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0
        outN4 = np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0
        outN5 = np.zeros( ( p.nYOut, p.nXOut ) ) - 999.0

        for y in xrange( p.nYOut):
            for x in xrange( p.nXOut):
                ii = inN[ y * 2: y * 2 + 2,\
                          x * 2: x * 2 + 2] > 62
                if ii.sum() > 0:
                    outData[ y, x] = inData[ y * 2: y * 2 + 2,\
                                             x * 2: x * 2 + 2][ii].mean()
                    outN[ y, x] = inN[ y * 2: y * 2 + 1,\
                          x * 2: x * 2 + 1].sum()

                ii = inN2[ y * 2: y * 2 + 1,\
                          x * 2: x * 2 + 1] > 62
                if ii.sum() > 0:
                    outData2[ y, x] = inData2[ y * 2: y * 2 + 1,\
                                             x * 2: x * 2 + 1][ii].mean()

                    outN2[ y, x] = inN2[ y * 2: y * 2 + 1,\
                          x * 2: x * 2 + 1].sum()

                ii = inN3[ y * 2: y * 2 + 1,\
                          x * 2: x * 2 + 1] > 62
                if ii.sum() > 0:
                    outData3[ y, x] = inData3[ y * 2: y * 2 + 1,\
                                             x * 2: x * 2 + 1][ii].mean()

                    outN3[ y, x] = inN3[ y * 2: y * 2 + 1,\
                          x * 2: x * 2 + 1].sum()

                ii = inN4[ y * 2: y * 2 + 1,\
                          x * 2: x * 2 + 1] > 62
                if ii.sum() > 0:
                    outData4[ y, x] = inData4[ y * 2: y * 2 + 1,\
                                             x * 2: x * 2 + 1][ii].mean()

                    outN4[ y, x] = inN4[ y * 2: y * 2 + 1,\
                          x * 2: x * 2 + 1].sum()

                ii = inN5[ y * 2: y * 2 + 1,\
                          x * 2: x * 2 + 1] > 62
                if ii.sum() > 0:
                    outData5[ y, x] = inData5[ y * 2: y * 2 + 1,\
                                             x * 2: x * 2 + 1][ii].mean()                    

                    outN5[ y, x] = inN5[ y * 2: y * 2 + 1,\
                          x * 2: x * 2 + 1].sum()

        return np.flipud( outData ), np.flipud( outN ), \
               np.flipud( outData2 ), np.flipud( outN2 ),\
               np.flipud( outData3 ), np.flipud( outN3 ),\
               np.flipud( outData4 ), np.flipud( outN4 ),\
               np.flipud( outData5 ), np.flipud( outN5 )
    else:
        return np.flipud( inData ), np.flipud( inN ), \
               np.flipud( inData2 ), np.flipud( inN2 ),\
               np.flipud( inData3 ), np.flipud( inN3 ),\
              np.flipud( inData4 ), np.flipud( inN4 ),\
               np.flipud( inData5 ), np.flipud( inN5 )
##
##
##
def writeCDF():
##    fidOut = Dataset( 'aquaQuartBigEurope.nc', 'w', format = \    
    fidOut = Dataset( 'terraQuartBigEurope.nc', 'w', format = \
                      'NETCDF3_CLASSIC')
    fidOut.createDimension( 'y', p.nYOut )
    fidOut.createDimension( 'x', p.nXOut )
    fidOut.createDimension( 't', p.nTimesIn )
##
    fidOut.createVariable( 'lst', np.float32, ( 't', 'y', 'x' ) )
    fidOut.variables[ 'lst'][:] = outputGrid
    fidOut.createVariable( 'n', np.float32, ( 't', 'y', 'x' ) )
    fidOut.variables[ 'n'][:] = outputCount
##
    fidOut.createVariable( 'lstF', np.float32, ( 't', 'y', 'x' ) )
    fidOut.variables[ 'lstF'][:] = forestGrid
    fidOut.createVariable( 'nF', np.float32, ( 't', 'y', 'x' ) )
    fidOut.variables[ 'nF'][:] = forestCount
##
    fidOut.createVariable( 'lstU', np.float32, ( 't', 'y', 'x' ) )
    fidOut.variables[ 'lstU'][:] = urbanGrid
    fidOut.createVariable( 'nU', np.float32, ( 't', 'y', 'x' ) )
    fidOut.variables[ 'nU'][:] = urbanCount
##
    fidOut.createVariable( 'lstC', np.float32, ( 't', 'y', 'x' ) )
    fidOut.variables[ 'lstC'][:] = cropGrid
    fidOut.createVariable( 'nC', np.float32, ( 't', 'y', 'x' ) )
    fidOut.variables[ 'nC'][:] = cropCount
##
    fidOut.createVariable( 'lstO', np.float32, ( 't', 'y', 'x' ) )
    fidOut.variables[ 'lstO'][:] = otherGrid
    fidOut.createVariable( 'nO', np.float32, ( 't', 'y', 'x' ) )
    fidOut.variables[ 'nO'][:] = otherCount
##
    fidOut.close()
##
##
##
if __name__ == "__main__":
    import sys
    import numpy as np
    import matplotlib.pyplot as plt
    from netCDF4 import Dataset

    p = params()

    outputGrid = np.zeros( ( p.nTimesIn, p.nYOut, p.nXOut ), np.float32 )
    outputCount = np.zeros( ( p.nTimesIn, p.nYOut, p.nXOut ), np.float32 )
    forestGrid = np.zeros( ( p.nTimesIn, p.nYOut, p.nXOut ), np.float32 )
    forestCount = np.zeros( ( p.nTimesIn, p.nYOut, p.nXOut ), np.float32 )

    urbanGrid = np.zeros( ( p.nTimesIn, p.nYOut, p.nXOut ), np.float32 )
    urbanCount = np.zeros( ( p.nTimesIn, p.nYOut, p.nXOut ), np.float32 )

    cropGrid = np.zeros( ( p.nTimesIn, p.nYOut, p.nXOut ), np.float32 )
    cropCount = np.zeros( ( p.nTimesIn, p.nYOut, p.nXOut ), np.float32 )

    otherGrid = np.zeros( ( p.nTimesIn, p.nYOut, p.nXOut ), np.float32 )
    otherCount = np.zeros( ( p.nTimesIn, p.nYOut, p.nXOut ), np.float32 )
    
    count = 0
    for year in p.years:

        leap = isLeap(year)
        for month in p.months:
            for day in daysAsNumbers( month, leap ):
##
##

                print( count, p.nTimesIn)
                
                outputGrid[ count, :, : ], outputCount[ count, :, : ],\
                forestGrid[ count, :, : ], forestCount[ count, :, : ],\
                urbanGrid[ count, :, : ], urbanCount[ count, :, : ],\
                cropGrid[ count, :, : ], cropCount[ count, :, : ],\
                otherGrid[ count, :, : ], otherCount[ count, :, : ]\
                            = readInput()


                if  outputGrid[ count, :, : ].max() > 0.0:
                    printUsual( outputGrid[ count, :, : ] )
                count += 1

    writeCDF()
