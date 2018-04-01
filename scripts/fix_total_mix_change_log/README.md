fix_total_mix.py 改动记录(change log)
fix_total_mix_v0.0.0.py ==> 实现原始matlab版本功能：统计bin的注视点个数；
fix_total_mix_v0.0.1.py ==> 在v0.0.0基础上将sub/item的某一个bin_range全部为零的数据点删除，并且将bin_range尾部的零值数据点删除，同时，bin_range中间眼跳的数据点填入零值；
fix_total_mix_v0.0.2.py ==> 在v0.0.1基础上,只进行sub/item的某一个bin_range全部为零的数据点删除，其他bin_range内缺少的数据点上都填入0, 这样所有sub/item的bin_range个数都相同;
