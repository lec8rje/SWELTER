import numpy as np
from usefulFunctions import monthsAsNumbers, daysAsNumbers, \
     isLeap, yearsAsStrList
from netCDF4 import Dataset

nceuro = 80
nreuro = 50
npeuro = nceuro*nreuro

mapping_file = "/users/global/ppha/swelter/wfd-ei/wfdei_map.asc"

nc_wfdei = 720
nr_wfdei = 360
np_wfdei = nc_wfdei*nr_wfdei
nl_wfdei = 67209

dloneuro = 0.5
dlateuro = 0.5
lon0euro = -9.75
lat0euro = 35.25
months = monthsAsNumbers()
years = yearsAsStrList( 2000, 2012)

rootDir = "/prj/SWELTER/rjel/EIHDEC-land/"
prefix = "Tair_EIHDEC_land_"
suffix = ".nc"

firstTstep = 3

class dailyEra():
    __author__ = "RichE"
    __email__ = "rjel@ceh.ac.uk"
    __date__ = "12-11-2-12"
    '''
    A class to read in t2m data from annual files and
    extract the 0900-1200 value.

    The original files are global and teh output file is
    just for the extended SWELTER array.
    

    The resulting array is then written out to a netcdf
    file.
    '''
    def readMapping(self):
        self.globalMapping = \
                           np.genfromtxt( mapping_file,
                                         dtype=(int, int, int, int, float, float, int, int, int),
                                         skip_header=1, delimiter=',')
    def readEuroLand(self):
        """Return the Euro sub domain mapping as a dictionary of
        WFD-EI index: (Euro column, Euro row) values.
        """

        self.euroMapping = [p[0] for p in self.globalMapping if p[-3] > 0]
    def readT2m(self):

        self.t2M = np.array( [],ndmin=2)


        for year in years[:1]:
            for month in months[:1]:
                print( rootDir +\
                               prefix + year + month + suffix)
                fid = Dataset( rootDir +\
                               prefix + year + month + suffix,\
                               "r")
                for day in xrange( 1):
                    print( np.squeeze( fid.variables[ 'Tair'][(day*8)+firstTstep, self.euroMapping]).shape)
                    np.append( self.t2M, np.squeeze( fid.variables[ 'Tair'][(day*8)+firstTstep, self.euroMapping]), axis = 0)

##                    for day in xrange( len( \
##                    daysAsNumbers( month, isLeap(year)))):

                fid.close()

##
    def doStuff(self):

        self.readMapping()
        self.readEuroLand()

        self.readT2m()

if __name__ == "__main__":
    dE = dailyEra()
    dE.doStuff()        
