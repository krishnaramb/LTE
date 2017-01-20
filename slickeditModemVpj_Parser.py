#!/usr/bin/python

#script to recursively create the absolute unix path for all the .c, .cpp and .h files of each of lte,mcs and wcdma tech
#script.py -i <build_path_in linux_format> -o <outputfile>

#example
#C:\Users\kbudhath>E:\Python_Practice\reader\slickeditModem_6.py -i <input file path> -o MeroOutput.vpj
#Author: Krishna Ram Budhathoki

import os
import sys, getopt
import re

class ModemPrj(object):
    def __init__(self,walk_dir,outputfile):
        self.walk_dir= walk_dir
        self.outputfile = outputfile
    def creatFile(self):
        fo = open(self.outputfile,"a+")
        for root,dirs,files in os.walk(self.walk_dir):
            for fileNames in files:
                list_file_path = os.path.join(root,fileNames)
                if (re.match('.*[.](c|cpp|h)$',fileNames)):
                    fo.write("\t"+"\t"+"\t"+"<F N="+'"' + list_file_path.replace(os.path.sep,'/')+'"'+"/>" + "\n") #window has default backward slash, so we converted to forward slash('/') before writing to file
        fo.close()

                    #print('list_file_path= '+ list_file_path)

                
        


def main (argv):

    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError as err:
        print ('slickeditModem.py -i <inputpath> -o <outputfile>')
        sys.exit(2)

    for opt,arg in opts:
        if opt == '-h':
            print("slickeditModem.py -i <inputfle_path_in_linux_format_which_is_forward_slash> -o <outputfile.vpj>")
            sys.exit()
        elif opt in ("-i","--ifile"):
            inputpath = arg
            print('Input file is: '+ inputpath)
        elif opt in ("-o","--ofile"):
            outputfile = arg
            print("Output file is: "+ outputfile)
    InitalfilePart(outputfile)
    
          
    componets = ['lte','mcs','wcdma','mmcp','geran'] #add the other components if you want;'mcs','wcdma','mmcp','geran'
    for tech in componets :
        
        walk_dir_root = os.path.join(inputpath,'modem_proc')
        walk_dir = walk_dir_root
        walk_dir = os.path.join(walk_dir,tech)
        print(walk_dir)
        fileObj = ModemPrj(walk_dir,"tmp_file1.vpj")
        fileObj.creatFile()
    FinalfilePart() #append the final part of the file
    os.remove(outputfile) 
    os.rename("tmp_file1.vpj",outputfile)
    os.remove("tmp_file.vpj") 
    os.remove("tmp_file2.vpj") 




def InitalfilePart(outputfile):
    fo_tmp = open("tmp_file.vpj","w+")

    with open(outputfile,'r') as fo:
        for line in fo:
            if(re.match('^((?!modem_proc).)*$',line)): #thiswill match a line which doesn't contain a word modem_proc
                fo_tmp.write(line)
        fo_tmp.close()


    fo_tmp1 = open("tmp_file1.vpj","w+")
    fo_tmp2 = open("tmp_file2.vpj","w+")
    Flag =1;
    with open("tmp_file.vpj","r+") as fo:
        for line in fo:
            if(Flag):
                fo_tmp1.write(line)
            else:
                fo_tmp2.write(line)
            
            if (re.match('.*Filters',line)):
                Flag =0
    fo_tmp1.close()
    fo_tmp2.close()


def FinalfilePart():
    fo_tmpfile1 = open("tmp_file1.vpj","a+")
    with open("tmp_file2.vpj","r") as fo:
        for line in fo:
            fo_tmpfile1.write(line)

    fo_tmpfile1.close()

  

            






if __name__ == "__main__":
    main(sys.argv[1:])

