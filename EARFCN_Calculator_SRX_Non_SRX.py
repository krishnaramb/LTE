#############################################################
#### Developed by: Krishna RAM Budhathoki  ##################
#############################################################



import getopt, sys
import ConfigParser
import json
import math
#Define Dictionary as Global parameters:
EARFCN_DICT = {'1':('2110','0','0','599'),
               '2':('1930','600','600','1199'),
               '3':('1805','1200','1200','1949'),
               '4':('2110','1950','1950','2399'),
               '5':('869','2400','2400','2649'),
               '6':('875','2650','2650','2749'),
               '7':('2620','2750','2750','3449'),
               '8':('925','3450','3450','3799'),
               '9':('1844.9','3800','3800','4149'),
               '10':('2110','4150','4150','4749'),
               '11':('1475.9','4750','4750','4999'),
               '12':('728','5000','5000','5179'),
               '13':('746','5180','5180','5279'),
               '14':('758,5280','5280','5379'),
               '17':('734','5730','5730','5849'),
               '18':('860','5850','5850','5999'),
               '19':('875','6000','6000','6149'),
               '20':('791','6150','6150','6449'),
               '21':('1495.9','6450','6450','6599'),
               '33': ('1900','36000','36000','36199'),
               '34':('2010','36200','36200','36349'),
               '35': ('1850','36350','36350','36949'),
               '36': ('1930','36950','36950','37549'),
               '37':('1910','37550','37550','37749'),
               '38':('2570','37750','37750','38249'),
               '39':('1880','38250','38250','38649'),
               '40':('2300','38650','38650','39649'),
               '41':('2496','39650','39650','41589')
               }




class calculator(object):
        Fdownlink = 0 #initialization
        def __init__(self,band,base_earfcn,FDL_Low,NDL_Offset,BW,max_earfcn,DLFreq_Lower):
                self.band = band
                self.base_earfcn = base_earfcn
                self.FDL_Low = FDL_Low
                self.NDL_Offset = NDL_Offset
                self.BW = BW
                self.max_earfcn = max_earfcn
                self.DLFreq_Upper = DLFreq_Lower + BW
                self.Fdownlink =DLFreq_Lower+ self.BW/2.0
                self.earfcn = (self.Fdownlink - self.FDL_Low)/0.1 + self.NDL_Offset
                self.Fdownlink_upper_limit = self.FDL_Low + 0.1*(self.max_earfcn - self.NDL_Offset)
               # print "value of BW is %s"%self.BW

        def EARFCN(self):
                return self.earfcn
        def DL_FREQ(self):
                return self.Fdownlink
        def FDL_UPPER_LIMIT(self):
                return self.Fdownlink_upper_limit
        def FDL_UPPER (self):
            return self.DLFreq_Upper
        def BAND(self):
            return self.band



        def check_bound(self):
                if self.DLFreq_Upper > self.Fdownlink_upper_limit:
                        print '\t The earfcn %s is out of range'%self.earfcn 
                        sys.exit()
                #else:
                #        print '\t The earfcn %s is within the range' %self.earfcn 

def delta_calculator (BW1,BW2):
        srx_bw = math.floor((float(BW1) + float(BW2) -0.1*abs(float(BW1)-float(BW2)))/0.6)*0.3
        normal_bw = (float(BW1) + float(BW2))/2.0
        delta = normal_bw - srx_bw
        return delta
        
        





def main():
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        #BW= json.loads(config.get("DRDSDS","Bandwidth_1"))# json is very useful tool for parsing items as a list
        #Band = config.get('DRDSDS', 'Band_1') #get the value of band as the string
        band_bandwith_pair = []#array for storing band followed by BW and so on
        band_bandwith_pair_srx = []#array for storing the band followed by BW for SRX combo
        OBJ_EARFCN = [] #list of objects
        OBJ_EARFCN_SRX = []
        counter_nonSRX = 0 
        counter_SRX = 0
        for name in config.options('NonSRX'):#name is the key
            band_bandwith_pair.append(json.loads(config.get('NonSRX', name)))
            #print ("%s has %s"%(name,config.get('DRDSDS', name)))
            counter_nonSRX+=1
        #print "value of band_bandwith_pair is %s"%band_bandwith_pair

        for name in config.options('SRX'):
            band_bandwith_pair_srx.append(json.loads(config.get('SRX',name)))
            counter_SRX+=1
       # print "value of band_bandwith_pair_srx is %s"%band_bandwith_pair_srx

        for loop in range(0,counter_nonSRX,2): #loop is for Band and next is for Bandwidth
            next = loop + 1
            print"------------------------------------------------------------------------"
            print"The values of Non-Contiguous EARFCN for LTE non-SRX Band %s are:"%band_bandwith_pair[loop]
            
            if str(band_bandwith_pair[loop]) in EARFCN_DICT:
                
                FDL_Low,NDL_Offset,base_earfcn,max_earfcn = EARFCN_DICT[str(band_bandwith_pair[loop])]#extraction
                DLFreq_Lower = FDL_Low #initialization once for each unique band
                for i in range(len(band_bandwith_pair[next])):
                    #print "\n the value of next is %s and value of band_bandwith_pair is %s"%(next,band_bandwith_pair[next])
                    OBJ_EARFCN.append( calculator(float (band_bandwith_pair[loop]),float(base_earfcn),float(FDL_Low),float(NDL_Offset),float(band_bandwith_pair[next][i]),float(max_earfcn),float(DLFreq_Lower)))
                    DLFreq_Lower = OBJ_EARFCN[-1].FDL_UPPER()#work on the lastly appeneded OBJ
                    print'EARFCN => %s for Bandwith of %s MHz'%(OBJ_EARFCN[-1].EARFCN(),OBJ_EARFCN[-1].BW)
                    OBJ_EARFCN[-1].check_bound()
                    

            else:
                    print '\tERROR: keyword %s is not found'%band_bandwith_pair[loop]
                    sys.exit()



    
        for loop in range (0,counter_SRX,2) :
            next = loop +1
            print"------------------------------------------------------------------------"
            print "The values of Contiguous EARFCN for LTE SRX Band %s are:"%band_bandwith_pair_srx[loop]
            if str(band_bandwith_pair_srx[loop] in EARFCN_DICT):
                
                FDL_Low,NDL_Offset,base_earfcn,max_earfcn = EARFCN_DICT[str(band_bandwith_pair_srx[loop])]#extraction
                tmp_DLFreq_Upper = 0 #initialization

                for obj in range (len(OBJ_EARFCN)) : #traverse accross whole object list
                   # print 'krishna: value of obj is %s and Band is %s'%(obj,OBJ_EARFCN[obj].BAND())
                    if OBJ_EARFCN[obj].BAND() == band_bandwith_pair_srx[loop]:
                        if OBJ_EARFCN[obj].FDL_UPPER()> tmp_DLFreq_Upper:
                            tmp_DLFreq_Upper = OBJ_EARFCN[obj].FDL_UPPER()
                #print '\n the value of tmp_DLFreq_Upper is %s'%tmp_DLFreq_Upper

                #after above for loop,  we have determined if the same band exits in the non-srx combo or not
                if tmp_DLFreq_Upper == 0:
                    DLFreq_Lower = FDL_Low #initialization once for each unique band
                else:
                    DLFreq_Lower = tmp_DLFreq_Upper


                
                for i in range(len(band_bandwith_pair_srx[next])):
                    #calculation of the delta BW
                    OBJ_EARFCN_SRX.append( calculator(float (band_bandwith_pair_srx[loop]),float(base_earfcn),float(FDL_Low),float(NDL_Offset),float(band_bandwith_pair_srx[next][i]),float(max_earfcn),float(DLFreq_Lower)))
                    if i+1 < len(band_bandwith_pair_srx[next]) : #this is for skipping the last value of srx BW
                        delta = delta_calculator(band_bandwith_pair_srx[next][i],band_bandwith_pair_srx[next][i+1])
                   
                    DLFreq_Lower = OBJ_EARFCN_SRX[-1].FDL_UPPER()-float(delta)#working on lastly appended obj
                    print'EARFCN => %s for Bandwith of %s MHz'%(OBJ_EARFCN_SRX[-1].EARFCN(),OBJ_EARFCN_SRX[-1].BW)
                    OBJ_EARFCN_SRX[-1].check_bound()

            else:
                 print '\tERROR: keyword %s is not found'%band_bandwith_pair_srx[loop]
                 sys.exit()


                
                

















            



if __name__ == "__main__":
        main()

        


        
