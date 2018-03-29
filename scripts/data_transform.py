# _*_ encoding=utf-8 _*_
import sys

def readfile(filename, outputfile='data_transform_output.csv', fixed_c=[0,1,2], trans_c=[3,4,5]):
    print("Input : {}".format(filename))
    print("Output : {}".format(outputfile))
    fout=open(outputfile, 'w')
    pre_line=fixed_c
    with open(filename) as f:
        lines=f.readlines()
        itms_title = lines[0].strip().split(',')
        # write the title
        fout.write(','.join(itms_title[0:len(fixed_c)]+['condition']) + '\n')
        for line in lines[1:]:
            itms = line.strip().split(',')
            if len(itms) != len(fixed_c) + len(trans_c):
                print('coloum is wrong!')
                exit(0)
            for fc in xrange(len(fixed_c)):
                if itms[fc] is '':
                    itms[fc]= pre_line[fc]
                else:
                    pre_line[fc]=itms[fc]
            for tc in trans_c:
                fout.write(','.join(itms[:len(fixed_c)]+[itms[tc], itms_title[tc]]) + '\n')
    fout.close()
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage : You should specify the input file! Like this : \n \
                python data_transform.py input_file.csv")
    elif len(sys.argv) == 2: 
        readfile(sys.argv[1])
    elif len(sys.argv) == 3: 
        readfile(sys.argv[1], sys.argv[2])
