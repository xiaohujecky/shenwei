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
            idx=bin_start
            start_time = bin_start*100
            for bin_id in range(bin_start, bin_end):
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
            print "%d,0,0,0,0,0,0.0,0.0,0.0,0.0,0.0\n"%(int(b))
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
                %(int(b),num_a,num_b,num_c,num_d,num_null,\
                float(num_a)/len(data),float(num_b)/len(data),\
                float(num_c)/len(data),float(num_d)/len(data),\
                float(num_null)/len(data))
        fout.write("%d,%d,%d,%d,%d,%d,"\
                "%.4f,%.4f,%.4f,%.4f,%.4f\n"\
                %(int(b),num_a,num_b,num_c,num_d,num_null,\
                float(num_a)/len(data),float(num_b)/len(data),\
                float(num_c)/len(data),float(num_d)/len(data),\
                float(num_null)/len(data)))
    fout.close()
        

def searchMix(infile, outfile, bin_start, bin_end, output_bins=[], output_bins_name=[]):
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
            print "%d,sub,item,0,0,0,0,0\n"%(int(b))
            continue
        #record = {'sub':sub, 'item' : item, 'num_a':num_a, 'num_b':num_b, 'num_c':num_c, 'num_d':num_d}
        record = record_bin['{}'.format(int(b))] ={}
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
    sub_keys_sort = sorted(sub_keys, key=lambda x:int(x.replace('sub','')))
    itm_keys_sort = sorted(itm_keys, key=lambda x:int(x))
    bin_keys_sort = sorted(bin_keys, key=lambda x:int(x))
    print "sub : ",
    print sub_keys_sort
    print "item : ",
    print itm_keys_sort
    print "bin : ",
    print bin_keys_sort
    fout=open(outfile,'w')
    info_title = "sub,item,bin,a,b,c,d,rest"
    fout.write(info_title + '\n')
    print(info_title)
    total_lines = 0
    dump_lines = 0
    # save bins info to extra file.
    output_bins_name_f = {}
    print 'Single bin output : ', output_bins, 'in file ', output_bins_name
    for b_idx, bins_ in enumerate(output_bins):
        output_bins_name_f[bins_] = open(output_bins_name[b_idx], 'w')
        output_bins_name_f[bins_].write(info_title + '\n')

    for p_sub in  sub_keys_sort :
        for p_item in  itm_keys_sort :
            info_stack_temp = []
            dump_bin_temp = list()
            bin_range_data_valid = False
            for p_bin in bin_keys_sort :
                #print "p_bin : {}, p_sub : {}, p_itm : {}".format(p_bin,p_sub,p_item)
                num_a, num_b, num_c, num_d, num_null = 0, 0, 0, 0, 0
                info = "{},{},{},{},{},{},{},{}".format(
                        p_sub,p_item,p_bin,num_a,num_b,num_c,num_d,num_null)
                if p_sub not in record[p_bin] or p_item not in record[p_bin][p_sub]:
                    #pass
                    if not bin_range_data_valid : 
                        info_stack_temp.append(info)
                        dump_bin_temp.append(p_bin)
                        if p_bin == bin_keys_sort[-1]:
                            dump_lines += len(dump_bin_temp)
                            #print dump_bin_temp
                            #print "dumpline:{}, p_sub:{}, p_itm:{}, p_bin:{}".format(dump_lines,
                            #        p_sub, p_item, p_bin)
                            info_stack_temp = []
                            dump_bin_temp = list()
                        #print "WARNING : sub : {},item : {} got no data in bin {}".format(p_sub, p_item, p_bin)
                        continue
                else:
                    bin_range_data_valid = True
                    # 为了保证bin的长度一致，对有效数据前，没有数据的bin做补0操作
                    for p_bin_idx,placeholder in enumerate(info_stack_temp) :
                        total_lines += 1
                        #print "WARNING-add all 0 data: {}".format(placeholder)
                        fout.write(placeholder + '\n')
                        p_bin_former = dump_bin_temp[p_bin_idx]
                        if p_bin_former in output_bins:
                            #print "WARNING-add all 0 data: {}".format(placeholder)
                            output_bins_name_f[p_bin_former].write(placeholder + '\n')
                    info_stack_temp = []
                    dump_bin_temp = list()
                    num_a, num_b, num_c, num_d, num_null = \
                        record[p_bin][p_sub][p_item]['num_a'],\
                        record[p_bin][p_sub][p_item]['num_b'],\
                        record[p_bin][p_sub][p_item]['num_c'],\
                        record[p_bin][p_sub][p_item]['num_d'],\
                        record[p_bin][p_sub][p_item]['num_null']
                    info = "{},{},{},{},{},{},{},{}".format(
                        p_sub,p_item,p_bin,num_a,num_b,num_c,num_d,num_null)
                total_lines += 1
                if total_lines < 10: 
                    print(info)
                fout.write(info + '\n')

                # save info into sub bin file
                if p_bin in output_bins:
                    output_bins_name_f[p_bin].write(info + '\n')
    print "Total lines : {}".format(total_lines)
    print "Removed 0 value(wrong trials) lines : {}".format(dump_lines)
    fout.close()
    for b_idx, bins_ in enumerate(output_bins):
        output_bins_name_f[bins_].close()

def usage():
    """
    Usage : 
    """
    print('Usage : \n python fix_total_mix.py file_in file_out bin_start bin_end mod [needed_bin_id1,id2... needed_bin_name1,name2...]')
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
    output_bins = []
    output_bins_name = []
    if len(sys.argv) > 6:
        if len(sys.argv) != 8 or mod != 'mix':
            print "Warning : sub bins output is only for mix!"
            usage()
        needed_bins = sys.argv[6]
        needed_bins_name = sys.argv[7]
        output_bins = [bin_ for bin_ in needed_bins.strip().split(',')]
        output_bins_name = [bin_name for bin_name in needed_bins_name.strip().split(',')]

    if mod == 'total':
        searchProportion(file_in, file_out, bin_start, bin_end)
    if mod == 'mix':
        searchMix(file_in, file_out, bin_start, bin_end, output_bins, output_bins_name)
