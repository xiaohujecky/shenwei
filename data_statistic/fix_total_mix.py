#!/usr/bin/python
#! __*__ encoding=utf-8 __*__
import os
import sys
import math


def read2map(file_name, bin_start=-2, bin_end=16):
    len_bin=100
    data_bin={}
    with open(file_name) as f:
        dline=f.readline()
        print dline,
        dline=f.readline()
        while(dline):
            itms=dline.strip().split(',')
            if len(itms) < 5 :
                print('Data format wrong!')
                dline=f.readline()
                continue
            idx=0
            start_time = bin_start*100
            for bin_id in xrange(bin_start, bin_end):
                # 起始位置在bin右边届以左，结束位置在bin左边界以右
                # 即：该注视点在当前bin中
                end_time = start_time + len_bin
                if int(itms[2]) < end_time and \
                   int(itms[3]) > start_time :
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

def searchProportion(infile, outfile, bin_start, bin_end):
    data_bin=read2map(infile, int(bin_start), int(bin_end))
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
        

def searchMix(infile, outfile, bin_start, bin_end):
    data_bin=read2map(infile, int(bin_start), int(bin_end))
    record_bin={}
    for b in sorted(data_bin.keys(), key=lambda x:int(x)):
        num_a = 0
        num_b = 0
        num_c = 0
        num_d = 0
        num_null = 0
        data=data_bin[b]
        #print len(data)
        if len(data) <= 0 :
            print "%d,sub,item,0,0,0,0,0\n"%(int(b)+1)
            continue
        #record = {'sub':sub, 'item' : item, 'num_a':num_a, 'num_b':num_b, 'num_c':num_c, 'num_d':num_d}
        record = record_bin['{}'.format(int(b) + 1)] ={}
        len_data = len(data)
        for idx in xrange(len_data):
            [sub, item, t_start, t_end, mark] = data[idx]
            if sub not in record:
                record[sub] = {}
                num_a, num_b, num_c, num_d, num_null = 0, 0, 0, 0, 0
                if mark == 'a':
                    num_a += 1 
                elif mark == 'b':
                    num_b += 1
                elif mark == 'c':
                    num_c += 1
                elif mark == 'd':
                    num_d += 1
                else:
                    num_null += 1
                record[sub][item] = {'num_a':num_a, 'num_b':num_b,
                        'num_c':num_c, 'num_d':num_d, 'num_null' : num_null} 
            else:
                if item not in record[sub]:
                    num_a, num_b, num_c, num_d, num_null = 0, 0, 0, 0, 0
                    if mark == 'a':
                        num_a += 1 
                    elif mark == 'b':
                        num_b += 1
                    elif mark == 'c':
                        num_c += 1
                    elif mark == 'd':
                        num_d += 1
                    else:
                        num_null += 1
                    record[sub][item] = {'num_a':num_a, 'num_b':num_b,
                            'num_c':num_c, 'num_d':num_d, 'num_null' : num_null} 
                else:
                    num_a, num_b, num_c, num_d, num_null = \
                            record[sub][item]['num_a'],\
                            record[sub][item]['num_b'],\
                            record[sub][item]['num_c'],\
                            record[sub][item]['num_d'],\
                            record[sub][item]['num_null']
                    if mark == 'a':
                        num_a += 1 
                    elif mark == 'b':
                        num_b += 1
                    elif mark == 'c':
                        num_c += 1
                    elif mark == 'd':
                        num_d += 1
                    else:
                        num_null += 1
                    record[sub][item] = {'num_a':num_a, 'num_b':num_b,
                            'num_c':num_c, 'num_d':num_d, 'num_null' : num_null} 
    
    bin_keys = set()
    sub_keys = set()
    itm_keys = set()
    record = record_bin
    for p_bin in record.keys() :
        bin_keys.add(p_bin)
        for p_sub in record[p_bin].keys() : 
            sub_keys.add(p_sub)
            for p_item in record[p_bin][p_sub].keys() :
                itm_keys.add(p_item)
    print("Total sub : {}, total item : {}, total bin : {}".format(
        len(sub_keys), len(itm_keys), len(bin_keys)))
    fout=open(outfile,'w')
    info_title = "sub,item,bin,a,b,c,d,rest"
    fout.write(info_title + '\n')
    print(info_title)
    total_lines = 0
    for p_sub in sorted(sub_keys, key=lambda x:int(x)) :
        for p_item in sorted(itm_keys, key=lambda x:int(x)) :
            for p_bin in sorted(bin_keys, key=lambda x:int(x)) :
                #print "p_bin : {}, p_sub : {}, p_itm : {}".format(p_bin,p_sub,p_item)
                num_a, num_b, num_c, num_d, num_null = 0, 0, 0, 0, 0
                if p_sub not in record[p_bin] or p_item not in record[p_bin][p_sub]:
                    pass;
                    #print "WARNING : sub : {},item : {} got no data in bin {}".format(p_sub, p_item, p_bin)
                else:
                    num_a, num_b, num_c, num_d, num_null = \
                        record[p_bin][p_sub][p_item]['num_a'],\
                        record[p_bin][p_sub][p_item]['num_b'],\
                        record[p_bin][p_sub][p_item]['num_c'],\
                        record[p_bin][p_sub][p_item]['num_d'],\
                        record[p_bin][p_sub][p_item]['num_null']
                #num_null = len(data) - (num_a+num_b+num_c+num_d)
                #info = "{},{},{},{},{},{},{},{},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(
                #        int(b)+1,p_sub,p_item,num_a,num_b,num_c,num_d,num_null,
                #        float(num_a)/len_data,float(num_b)/len_data,
                #        float(num_c)/len_data,float(num_d)/len_data,
                #        float(num_null)/len_data)
                info = "{},{},{},{},{},{},{},{}".format(
                        p_sub,p_item,p_bin,num_a,num_b,num_c,num_d,num_null)
                total_lines += 1
                if total_lines < 10: 
                    print(info)
                fout.write(info + '\n')
    print "Total lines : {}".format(total_lines)
    fout.close()

def usage():
    """
    Usage : 
    """
    print('Usage : \n python fix_total_mix.py file_in flie_out bin_start bin_end mod')
    exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == '-h' or sys.argv[1] == '--help' or\
            len(sys.argv) < 5:
        usage()

    file_in = sys.argv[1]
    file_out = sys.argv[2]
    bin_start = sys.argv[3]
    bin_end = sys.argv[4]
    mod = sys.argv[5]
    if mod == 'total':
        searchProportion(file_in, file_out, bin_start, bin_end)
    if mod == 'mix':
        searchMix(file_in, file_out, bin_start, bin_end)
