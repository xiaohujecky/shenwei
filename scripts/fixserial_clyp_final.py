#!/usr/bin/python
#! __*__ encoding=utf-8 __*__
import os
import sys
import math


def read2map(file_name):
    len_bin=100
    data_bin={}
    with open(file_name) as f:
        dline=f.readline()
        print dline
        dline=f.readline()
        while(dline):
            itms=dline.strip().split(',')
            if len(itms) < 7 :
                print('Data format wrong!')
                dline=f.readline()
                continue
            idx=0
            start_time = -200
            for bin_id in xrange(-2,16):
                # 起始位置在bin右边届以左，结束位置在bin左边界以右
                # 即：该注视点在当前bin中
                end_time = start_time + len_bin
                if int(itms[4]) < end_time and \
                   int(itms[5]) > start_time :
                       bin_idx="%d"%idx
                       if bin_idx not in data_bin:
                           data_bin[bin_idx]=[itms]
                       else:
                           data_bin[bin_idx].append(itms)
                start_time = end_time
                idx+=1
            dline=f.readline()
    # for the bins:
    return data_bin

def searchProportion(infile,outfile):
    data_bin=read2map(infile)
    fout=open(outfile,'w')
    print "bin,a,b,c,d,rest,rate_a,rate_b,rate_c,rate_d,rate_rest"
    fout.write("bin,a,b,c,d,rest,rate_a,rate_b,rate_c,rate_d,rate_rest\n")
    for b in sorted(data_bin.keys(), key=lambda x:int(x)):
        num_a = 0
        num_b = 0
        num_c = 0
        num_d = 0
        num_null = 0
        data=data_bin[b]
        #print len(data)
        if len(data) <= 0 :
            print "%d,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0\n"%(int(b)+1)
            continue
        for idx in xrange(len(data)):
            itm = data[idx]
            if itm[-1] == 'a':
                num_a += 1
            elif itm[-1] == 'b':
                num_b += 1
            elif itm[-1] == 'c':
                num_c += 1
            elif itm[-1] == 'd':
                num_d += 1
            else:
                num_null += 1
        #num_null = len(data) - (num_a+num_b+num_c+num_d)
        print "%d,%d,%d,%d,%d,%d,"\
                "%.4f,%.4f,%.4f,%.4f,%.4f"\
                %(int(b)+1,num_a,num_b,num_c,num_d,num_null,\
                float(num_a)/len(data),float(num_b)/len(data),\
                float(num_c)/len(data),float(num_d)/len(data),\
                float(num_null)/len(data))
        fout.write("%d,%d,%d,%d,%d,%d,"\
                "%.4f,%.4f,%.4f,%.4f,%.4f\n"\
                %(int(b)+1,num_a,num_b,num_c,num_d,num_null,\
                float(num_a)/len(data),float(num_b)/len(data),\
                float(num_c)/len(data),float(num_d)/len(data),\
                float(num_null)/len(data)))
    fout.close()
        


if __name__ == "__main__":
    searchProportion(sys.argv[1],sys.argv[2])
    
