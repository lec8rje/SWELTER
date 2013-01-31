import numpy as np

MAPPING_FILE = "/users/global/ppha/swelter/wfd-ei/wfdei_map.asc"

NC_WFDEI = 720
NR_WFDEI = 360
NP_WFDEI = NC_WFDEI*NR_WFDEI
NL_WFDEI = 67209

DLON_WFDEI =  0.5
DLAT_WFDEI =  0.5
LON0_WFDEI = -180.0 + 0.5*DLON_WFDEI
LAT0_WFDEI =  -90.0 + 0.5*DLAT_WFDEI

NC_EURO = 81
NR_EURO = 50
NP_EURO = NC_EURO*NR_EURO

DLON_EURO = 0.5
DLAT_EURO = 0.5
LON0_EURO = -10.25
LAT0_EURO = 35.25
##    def __init__(self):
class euroPdef:
    def readWfdeiLand(self):
        """Return the WFD-EI domain mapping file info as a NumPy array of
        void objects, one void per WFD-EI land point.
        """
        self.globalMapping = np.genfromtxt(MAPPING_FILE,
            dtype=(int, int, int, int, float, float, int, int, int),
                                           skip_header=1, delimiter=',')
    def readEuroLand(self):
        """Return the Euro sub domain mapping as a dictionary of
        WFD-EI index: (Euro column, Euro row) values.
        """
        wfd = self.readWfdeiLand()
        self.euroMapping = {}

        for p in self.globalMapping:
            if p[-3] > 0:
                self.euroMapping[p[-3]] = ( p[-2], p[-1])
        print( len( self.euroMapping))
    def mkPdef(self):

        self.pdefGrid = np.zeros( ( NR_EURO, NC_EURO ) ) - 999.0
        self.wt = np.zeros( ( NR_EURO, NC_EURO ) ) - 999.0        
        self.rot = np.zeros( ( NR_EURO, NC_EURO ) )
        
        for p in self.euroMapping:
##            print( p, self.euroMapping[p][1], self.euroMapping[p][0])
            self.pdefGrid[ self.euroMapping[p][1]-1,\
                           self.euroMapping[p][0]-1 ] = \
                           p
            self.wt[ self.euroMapping[p][1]-1,\
                           self.euroMapping[p][0]-1 ] = 1.0
    def writePdefFile(self):

        fid = open( 'euroNewDomainPdef.gra', 'wb')

        self.pdefGrid.astype( np.int32).tofile( fid) 
        self.wt.astype( np.float32).tofile( fid)
        self.rot.astype( np.float32).tofile( fid)        

        fid.close()

    def writePointsList(self):
        f = open( "euroPoints2839.dat", "w")

        for p in self.globalMapping:
            if p[-3] > 0:
                f.write( str( p[0]) + '\n')
        f.close()
    def doStuff(self):

        self.readWfdeiLand()
        self.readEuroLand()
##        self.mkPdef()
##        self.writePdefFile()
        self.writePointsList()
if __name__ == "__main__":
    ep = euroPdef()
    ep.doStuff()
