import matplotlib.pyplot as plt
import numpy as np

from usefulFunctions import yearsAsStrList, isLeap,\
     monthsAsNumbers, daysAsNumbers


class writeJamonFiles():

    def __init__(self):

        self.years = yearsAsStrList( 2000, 2010)

        self.rainFile = "eobsRain2000-2009.gra"
        
        self.lstFile ="terraLst2000-2009.gra"

        self.months = monthsAsNumbers
        
        self.nP = 2940

        self.accumDays = 11

    def readBinary(self, fName):
        fid = open( fName, 'rb')
        var = np.fromfile( fid, dtype = np.float32)
        fid.close()
        return var

    def mkTimeStamp(self):

        self.timeStamp = []

        for year in self.years:
            if isLeap( year): 
                nDaysYear = 366.0
            else:
                nDaysYear = 365.0
            daysSoFar = 1.0
            for month in self.months():
                if month in [ '01', '02', '11', '12']:
                    daysSoFar += \
                              len(daysAsNumbers(month,isLeap( year)))
                else:
                    for day in xrange( len( \
                        daysAsNumbers(month, isLeap( int(year)) ))):
                        self.timeStamp.append( year + str( daysSoFar / nDaysYear)[1:7])
                        daysSoFar += 1.0
##
##                    
    def accumulateRain(self):
        ii = self.lst >=0

        print( ii.sum())


        fid = open( "lstAccumRain"+ str( self.accumDays) + "Test.dat", "w")

        localStamp = np.asarray( self.timeStamp)

        for day in xrange( ii.sum()):
            print( localStamp[ii][day], self.rain[ii][day], self.lst[ii][day])

            iiTotal = np.argmax( localStamp == localStamp[ii][day])

            print( self.rain[ iiTotal - self.accumDays:iiTotal+1])

            
            totalRain = self.rain[ iiTotal - self.accumDays:iiTotal+1].sum()


##            if totalRain == 105:
##                sys.exit(-10)

            print( totalRain, self.rain[ iiTotal - self.accumDays:iiTotal+1].sum())

            fid.write( '%10s' '%2s' '%5s' '%2s' '%7s' '%2s' % (str( localStamp[ii][day]),'  ', str( totalRain),'  ',  \
                       str( self.lst[ii][day] ) , '\n'))


        fid.close()

        
    def doStuff(self):
        self.rain = self.readBinary( self.rainFile )
        self.lst = self.readBinary( self.lstFile )

        self.mkTimeStamp()

        self.accumulateRain()

##        self.plotStuff()

        
    def plotStuff(self):

        plt.subplot( 2,1,1)
        plt.plot( self.rain, 'k')
        plt.plot(  np.ma.masked_array(self.rain, self.lst < 0), 'r')
        plt.subplot( 2,1,2)
        plt.plot( np.ma.masked_array( self.lst, self.lst < 0))
        plt.show()

if __name__ == "__main__":



    wJ = writeJamonFiles()
    wJ.doStuff()
    
