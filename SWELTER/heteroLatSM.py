import numpy as np
import matplotlib.pyplot as plt
from usefulFunctions import printUsual
import pickle
import sys
class hLSM():


    def __init__(self):
##
## This defines the grid of the 1km modis grid
        self.nXModis = 4800
        self.nYModis = 3600
##
##
        self.nXReduced = 3981
        self.nYReduced = 3000
        self.xOffset = 168      ### 169 in cmt f90 code
        self.yOffset = 0        ### 1 in cmt code
##
## This describes the ASCAT grid at 0.25deg
        self.nXAscat = 162
        self.nYAscat = 100
        self.y0Ascat = 35.125
        self.x0Ascat = -10.375
        self.dXYAscat = 0.25
##
## The initial mapping takes an age so we pickle the
##    list after we get  it right. Then we can turn
## fromScratch to false and read the pickled map in        
        self.fromScratch = False
##
## This is for debugging the code and outputs a load
##   of information you may want then but is superfluous
##      in general  
##
        self.verbose = True
##
##
    def readModisLL(self):
        modisDir = "/prj/SWELTER/lst/modis/"
        modisLong = "mosaic_long_1km.dat"
        modisLat = "mosaic_lat_1km.dat"


        fid = open( modisDir + modisLong,  "rb")
        self.modisLong = np.fromfile( fid, dtype = np.float32,\
                                      count = self.nXModis * \
                                      self.nYModis)\
                                      .reshape(( self.nYModis,\
                                                 self.nXModis))
        fid.close()

        fid = open( modisDir + modisLat,  "rb")
        self.modisLat = np.fromfile( fid, dtype = np.float32,\
                                      count = self.nXModis * \
                                      self.nYModis)\
                                      .reshape(( self.nYModis,\
                                                 self.nXModis))
        fid.close()

    def reduceGrid(self):
##
## For some reason CMT reduced the grid of the modis data
### i am guessing to match the agreed swelter grid        
##        


        gridLong = self.modisLong[ self.yOffset:\
                                   self.yOffset+self.nYReduced,\
                                   self.xOffset:\
                                   self.xOffset+self.nXReduced]
        gridLat = self.modisLat[ self.yOffset:\
                                  self.yOffset+self.nYReduced,\
                                  self.xOffset:\
                                  self.xOffset+self.nXReduced]

        self.redLong = gridLong.reshape( self.nYReduced * \
                                         self.nXReduced)
        self.redLat = gridLat.reshape( self.nYReduced * \
                                       self.nXReduced)
        

        if self.verbose:
            print("****************************")        
            printUsual( self.redLong)
            print( self.x0Ascat - self.dXYAscat / 2.0,\
                   self.x0Ascat + self.dXYAscat / 2.0\
                   + self.nXAscat * self.dXYAscat)
            print("****************************")
            printUsual( self.redLat)
            print( self.y0Ascat - self.dXYAscat / 2.0,\
                   self.y0Ascat + self.dXYAscat / 2.0\
                   + self.nYAscat * self.dXYAscat)
            print("****************************")        
##
## We now need to map the modis 1km grid to the Ascat 0.25 deg
##   grid            
    def  makeMappingGrid(self):
##
## Create a list of lists for the mapping
##
        self.lMap = [[[] for i in range(self.nXAscat)] \
                     for j in range(self.nYAscat)]

        aYMin = self.y0Ascat - self.dXYAscat / 2.0
        aYMax = self.y0Ascat + self.dXYAscat / 2.0 +\
               + self.nYAscat * self.dXYAscat

        aXMin = self.x0Ascat - self.dXYAscat / 2.0
        aXMax = self.x0Ascat + self.dXYAscat / 2.0 +\
               + self.nXAscat * self.dXYAscat        


        for p in xrange( self.redLong.shape[0]):            
            if ( self.redLat[p] > aYMin) & \
               ( self.redLat[p] < aYMax) & \
               ( self.redLong[p]> aXMin) & \
               ( self.redLong[p]< aXMax):          
                
                y = ( self.redLat[p] - aYMin ) / \
                    self.dXYAscat
                y = np.floor( y).astype( np.int16)
                x = ( self.redLong[p] - aXMin )/ \
                    self.dXYAscat
                x = np.floor( x).astype( np.int16)                
                print( len( self.lMap), len( self.lMap[0]),\
                       len( self.lMap[0]))
                print( y, x)
                self.lMap[ y-1][ x-1].append( p)

##
        self.pickleStuff( self.lMap, "modisMapping.pi")
##
##
    def pickleStuff( self, var2Pick, pickleFile):
        fid = open( pickleFile, "w")
        pickle.dump( var2Pick, fid)
        fid.close()

    def readMappingGrid(self,pickleFile):
        print( "Reading mapping")
        fid = open( pickleFile, "r")
        var2Read = pickle.load( fid)
        fid.close()
        print( "Read mapping")        
        return var2Read
##
##
    def readModisFile(self, fileN):
        fid = open( fileN, "rb")
        self.inputGrid = np.fromfile( fid, dtype = \
                                 np.int16).byteswap()
        fid.close()
##
##
    def regridModis(self):
        print( "Regridding output")
        lstMean = np.zeros( (  self.nYAscat,\
                               self.nXAscat))

        lstStd = np.zeros( (  self.nYAscat,\
                               self.nXAscat))        
        
        for y in xrange( self.nYAscat):
            for x in xrange( self.nXAscat):


                lstMean[y,x] = self.inputGrid[ self.lMap[y][x]].mean()
##                print( y, x, lstMean[ y, x] )
##                print( self.inputGrid[ self.lMap[y][x]].shape)
        plt.imshow( lstMean)
        plt.show()
##
##
##
    def doStuff(self):
        if self.fromScratch:
            self.readModisLL()
            self.reduceGrid()
            self.makeMappingGrid()
        else:
            self.lMap = self.readMappingGrid("modisMapping.pi")


        fileName = \
                 "/prj/SWELTER/lst/modis/terra/screened_lst/2000/cmt_screened_vn4_lst_20000521.gra"

        self.readModisFile(fileName)
        self.regridModis()
            
if __name__ == "__main__":

    h = hLSM()
    h.doStuff()
