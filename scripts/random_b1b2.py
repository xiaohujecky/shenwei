import os,sys
import random

def randomb1b2(file_input, file_output):
    fout=open(file_output, 'w')
    line_temp=''
    with open(file_input, 'r') as f:
        line_index=0
        for line in f.readlines():
            line = line.strip()
            if line_index == 0:
                fout.write('{}\n'.format(line))
                line_index=line_index+1
                continue
            if line_index%3 == 1:
                fout.write('{}\n'.format(line))
            if line_index%3 == 2:
                line_temp = line
            if line_index%3 == 0:
                itm_b1 = line_temp.strip().split(',')
                itm_b2 = line.strip().split(',')
                if random.randint(0,1) == 0:
                    fout.write('{},{},{},d1\n'.format(itm_b1[0],itm_b1[1],itm_b1[2]))
                    fout.write('{},{},{},d2\n'.format(itm_b2[0],itm_b2[1],itm_b2[2]))
                else: 
                    fout.write('{},{},{},d2\n'.format(itm_b1[0],itm_b1[1],itm_b1[2]))
                    fout.write('{},{},{},d1\n'.format(itm_b2[0],itm_b2[1],itm_b2[2]))
            line_index=line_index+1

if __name__ == '__main__':
    randomb1b2(sys.argv[1], sys.argv[2])



