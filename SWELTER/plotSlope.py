from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
####
##
class plotR():


    def __init__(self):
        


##        self.lon0 = -10.25
##        self.lat0 = 35.25
        self.lon0 = -10.5
        self.lat0 = 35.0       
        
        self.nX = 81
        self.nY = 50

        self.dxy = 0.5

        self.longitude = np.tile( np.arange( self.lon0, \
                                        self.lon0 + self.dxy * self.nX, self.dxy)\
                             , self.nY )\
                             .reshape( ( self.nY, self.nX ))

        self.latitude = np.repeat( np.arange( self.lat0, \
                                        self.lat0 + self.dxy * self.nY, self.dxy)\
                             , self.nX )\
                             .reshape( ( self.nY, self.nX ))


        self.months = ["Mar", "Apr", "May", "Jun", "Jul", \
                       "Aug", "Sep", "Oct"]


    def readR(self):
        f = Dataset("/prj/SWELTER/rjel/newDomain/slopeMonthlyAqua.nc","r")
        self.R = f.variables['slope'][:]
        f.close()

    def readN(self):
        f = Dataset("/prj/SWELTER/rjel/newDomain/nPMonthlyAqua.nc","r")
        self.n = f.variables['np'][:]
        f.close()

    def readMask(self):
        f = Dataset("/prj/SWELTER/rjel/newDomain/bigEuroMask.nc","r")
        self.mask = np.flipud(f.variables['lsm'][:])
        f.close()
        
##
##        
    def drawMap(self, var, strMonth):                

        m = Basemap( projection = 'cyl',llcrnrlon = p.lon0, \
                     llcrnrlat = self.lat0, urcrnrlon = self.lon0 + self.dxy * self.nX,\
                     urcrnrlat = self.lat0 + self.dxy * self.nY, resolution='l')

        var = np.flipud( np.ma.masked_array( var, var >= -0.2) )
        var = np.ma.masked_array( var, var < -100)

##        im = m.pcolormesh( self.longitude, self.latitude,var, \
#                           vmin = -30, vmax = 0.0, cmap = "bone")

        var1 = np.flipud(self.n[ self.month,:,:])

        grey = np.where( ( var1 < 10) & ( self.mask > 0), 1, 0)


##        grey = np.where( ( var1 < 0) & ( self.mask > 0), 1, 0)                        
##        grey = np.ma.masked_array( grey, grey < 1.0)

        g = m.pcolormesh( self.longitude, self.latitude, grey)##,\
##                          cmap = "bone", vmin=0.0, vmax = 2.0)

##        g = m.contourf( self.longitude, self.latitude, grey,\
##                        vmin=0.0, vmax = 1.0,\
##                        hatches = ['/'],\
##                        cmap=plt.get_cmap('gray'),
##                        extend='both', alpha=0.5)

        m.drawmeridians(np.arange( -10.0, 30, 5), labels = [1,0,0,1], fontsize = 10, rotation = 20)
        m.drawparallels(np.arange( 30.0, 60.0, 5), labels = [1,0,0,1], fontsize = 10, rotation = 20)
        
        m.drawcoastlines()
        m.drawcountries()
##        plt.colorbar(im, orientation = 'vertical' , pad = 0.05,\
##                     shrink = 0.6, aspect = 20)


##        plt.title( "Slope for month " + strMonth)


        plt.savefig( "slope" + strMonth + ".png", orientation = "landscape")
        plt.clf()
##        plt.show()
##        m.drawrivers()




    def strongestMonth(self):
        strong = np.flipud( self.R.argmax( axis=0))
        strong = np.ma.masked_array( strong, strong < 1)

        levels = [ 0, 1, 2, 3, 4, 5, 6]

        m = Basemap( projection = 'cyl',llcrnrlon = p.lon0, \
                     llcrnrlat = self.lat0, \
                     urcrnrlon = self.lon0 + self.dxy * self.nX,\
                     urcrnrlat = self.lat0 + self.dxy * self.nY, \
                     resolution='c')
        
        im = m.contourf( self.longitude, self.latitude, strong, levels = levels )

        m.drawmeridians(np.arange( -10.0, 30, 5), labels = [1,0,0,1], fontsize = 10, rotation = 20)
        m.drawparallels(np.arange( 30.0, 60.0, 5), labels = [1,0,0,1], fontsize = 10, rotation = 20)
        
        m.drawcoastlines()
        m.drawcountries()
##        m.drawrivers()
        plt.colorbar(im, orientation = 'vertical' , pad = 0.05 )
        plt.title( "Month with strongest correlation")
        plt.show()

    def drawMinN(self):
        minN = np.flipud( np.min( self.n, axis = 0))

        minN = np.ma.masked_array( minN, minN < 0)

        minN = np.ma.masked_array( minN, minN > 20)
        
        m = Basemap( projection = 'cyl',llcrnrlon = p.lon0, \
                     llcrnrlat = self.lat0, \
                     urcrnrlon = self.lon0 + self.dxy * self.nX,\
                     urcrnrlat = self.lat0 + self.dxy * self.nY, \
                     resolution='c')
        im = m.pcolor( self.longitude, self.latitude, minN)##, levels = levels )
        
        m.drawmeridians(np.arange( -10.0, 30, 5), labels = [1,0,0,1], fontsize = 10, rotation = 20)
        m.drawparallels(np.arange( 30.0, 60.0, 5), labels = [1,0,0,1], fontsize = 10, rotation = 20)
        
        m.drawcoastlines()
        m.drawcountries()
##        m.drawrivers()
        plt.colorbar(im, orientation = 'vertical' , pad = 0.05 )
        plt.title( "Month with strongest correlation")
        plt.show()
##
##        
    def doStuff(self):
        self.readR()
        self.readN()
        self.readMask()        

##        self.strongestMonth()

        
##        for month in xrange( self.R.shape[0]):
        for self.month in xrange( 7,8):
##            self.drawMap( self.R[self.month, :, :],\
##                          self.months[self.month] )
            self.drawMinN()
        
if __name__ == "__main__":

    p = plotR()
    p.doStuff()
