import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from usefulFunctions import printUsual
import sys

class plotCVH():

    def __init__(self):
        self.rootDir = "/prj/SWELTER/rjel/catherineVHFiles/"
### This is the best showing soil moisture dependence
##        self.inputFile = "Daily_Precip_Tsurf_SM_EF_Bug_2007_2008.txt"


##        self.inputFile = "Daily_Precip_Tsurf_SM_EF_Bug_longSeries.txt"
        self.inputFile = "Daily_Precip_Tsurf_SM_EF_Tha_2007_2009.txt"



#### These show little dependence

##        self.inputFile = "Daily_Precip_Tsurf_SM_EF_Loo_2007_2009.txt"
##        self.inputFile = "Daily_Precip_Tsurf_SM_EF_Wet_2007_2008.txt"
##        self.inputFile = "Daily_Precip_Tsurf_SM_EF_Cab_2007_2008.txt"
##        self.inputFile = "Daily_Precip_Tsurf_SM_EF_Hes_2007_2008.txt"
### This looks bad soil moisture looks unreliable
##
##        
##        self.inputFile = "Daily_Precip_Tsurf_SM_EF_Vie_2007_2009.txt"
    def plotHist(self):
## Params for Bug
##        xMin = 3.0/300.0
##        xMax = 13.0/30.0
##        yMin = 0.0
##        yMax = 1.5

        ## Params for Bug
        xMin = 0.0
        xMax = 40.0/10.0
        yMin = 0.0
        yMax = 1.5

        hist, xedges, yedges = np.histogram2d( \
            self.sm, self.ef, bins = 40,\
            range=[[ xMin, xMax],[ yMin, yMax]])
        
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

        print( hist.T.max())
        nMin = 1.0
        
        histT = np.ma.masked_array( hist.T, hist.T <= nMin) 
        
        norm = mpl.colors.Normalize( nMin, histT.max())
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(1,1,1, aspect = "auto")
        
    
        ax1.pcolor( xedges, yedges, np.log(histT))
        plt.plot( self.sm, self.ef, "+k")

        plt.ylim( 0.0, 1.0)
        plt.ylabel( "Evaporative fraction")
        plt.xlabel( "Soil moisture")
        
        plt.savefig( self.inputFile[ 25: 28] + \
                     "EFvsSM.eps", orientation = "landscape")
    
##        plt.show()
### Precip, LST, VolSM EF


    def readFile(self):
    
        fid = open( self.rootDir + self.inputFile, "r")
        
        inputData = fid.readlines()
        
        fid.close()

        precip = []
        lst = []
        sm = []
        ef = []
        count = 0
        for line in inputData:

            splitLine = line.split()


            if splitLine[2].find( 'NaN') > -1:
                sm.append( -9990.0)
            else:
                sm.append( splitLine[2] )

            if  splitLine[3].find( 'NaN') > -1:
                ef.append( -999.0)
            else:
                ef.append( float( splitLine[3]))

            precip.append( float(splitLine[0]))
            lst.append( float(splitLine[1]))


            count += 1

        sm = np.asarray( sm, np.float32)
        ef = np.asarray( ef, np.float32)

        ii = ( sm > -990.0) & ( ef > -990.0)
        self.sm = sm[ii] / 10.0
## For Bug
##        self.sm = sm[ii] / 30.0

        self.ef = ef[ii]

    def plotScatter(self):

        plt.plot( self.sm, self.ef, "+k")
        plt.show()


    def doStuff(self):


        

        self.readFile()

##        self.plotScatter()

        self.plotHist()


if __name__ == "__main__":

    plc = plotCVH()

    plc.doStuff()
