# 修改记录   
fix_total_mix.py 改动记录(change log)   
fix_total_mix_v0.0.0.py ==> 实现原始matlab版本功能：统计bin的注视点个数；   
fix_total_mix_v0.0.1.py ==> 在v0.0.0基础上将sub/item的某一个bin_range全部为零的数据点删除，并且将bin_range尾部的零值数据点删除，同时，bin_range中间眼跳的数据点填入零值；   
fix_total_mix_v0.0.2.py ==> 在v0.0.1基础上,只进行sub/item的某一个bin_range全部为零的数据点删除，其他bin_range内缺少的数据点上都填入0, 这样所有sub/item的bin_range个数都相同;    

    
    
2020.8.8   
fix_total_mix.py 改动记录(change log)   
fix_total_mix_v0.0.0.py ==> 实现原始matlab版本功能：统计bin的注视点个数；
fix_total_mix_v0.0.1.py ==> 在v0.0.0基础上将sub/item的某一个bin_range全部为零的数据点删除，并且将bin_range尾部的零值数据点删除，同时，bin_range中间眼跳的数据点填入零值；   
fix_total_mix_v0.0.2.py ==> 在v0.0.1基础上,只进行sub/item的某一个bin_range（譬如：-2到15bin之间全部为0，才表示当前这个trial是错误的trial）全部为零的数据点删除，其他bin_range内缺少的数据点上都填入0, 这样所有sub/item的bin_range个数都相同;   
fix_total_mix_v0.0.3.py ==> 在v0.0.2基础上改动：a.计算mix的时候，不用删除csv文件中的'sub'; b.增加单个bin数据输出到一个文件中的操作；   
fix_total_mix_v0.0.4.py ==> 在v0.0.3基础上改动：对"b.增加单个bin数据输出到一个文件中的操作；", 为了保证所有sub/item的bin_range个数都相同，因此，对有效数据中bin_range内缺失数据的bin上填0时，没有对单个bin数据输出的文件进行补零操作(比如：一个trail，中间有数据，前面没有数据的地方需要补零)      


# 操作示例   
提取第8个bin的数据：   
`python2 fix_total_mix_v0.0.4.py all_python.csv file_out.csv -2 15 mix 8 bin8.csv` 
