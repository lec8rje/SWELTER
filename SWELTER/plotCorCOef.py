from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
####
##
class plotR():


    def __init__(self):
        


        self.lon0 = -10.25
        self.lat0 = 35.25
        
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


        self.months = ["Apr", "May", "Jun", "Jul", "Aug", "Sep"]


    def readR(self):
        f = Dataset("/prj/SWELTER/rjel/newDomain/corCoefMonthly.nc","r")
        self.R = f.variables['r'][:]
        f.close()
##
##        
    def drawMap(self, var, strMonth):                

        m = Basemap( projection = 'cyl',llcrnrlon = p.lon0, \
                     llcrnrlat = self.lat0, urcrnrlon = self.lon0 + self.dxy * self.nX,\
                 urcrnrlat = self.lat0 + self.dxy * self.nY, resolution='i')

        var = np.flipud( np.ma.masked_array( var, var >= -0.2) )

        var = np.ma.masked_array( var, var < -10)

        levels = [ -0.1, -0.3, -0.5, -0.7, -0.9]

        im = m.pcolormesh( self.longitude, self.latitude,var, vmin = -0.9, vmax = 0.1)

        m.drawmeridians(np.arange( -10.0, 30, 5), labels = [1,0,0,1], fontsize = 10, rotation = 20)
        m.drawparallels(np.arange( 30.0, 60.0, 5), labels = [1,0,0,1], fontsize = 10, rotation = 20)
        
        m.drawcoastlines()
        m.drawcountries()
        plt.colorbar(im, orientation = 'vertical' , pad = 0.05 )


        plt.title( "CorrCoeff for month " + strMonth)


        plt.savefig( "corrCoeff" + strMonth + ".png", orientation = "landscape")
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


    def doStuff(self):
        self.readR()

##        self.strongestMonth()

        
        for month in xrange( self.R.shape[0]):
#####        for month in xrange( 1):
            self.drawMap( self.R[month, :, :], self.months[month] )
            
        
if __name__ == "__main__":

    p = plotR()
    p.doStuff()
