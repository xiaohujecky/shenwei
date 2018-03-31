# shenwei projects

# 程序说明
1.fixserial_clyp_final.m  matlab版本统计程序  
2.fixserial_clyp_final.py python版本统计程序-未完待续  
3.修改fixserial_clyp_final.m为最终版本   
4.将一些代码段放到scripts文件夹, 包含：  
    ```
    data_transform.py
    random_b1b2.py
    fix_total_mix.py
    ```
    等程序
    其中, fix_total_mix.py功能:
    1. 去掉bin_range末尾的零值数据点;    
    2. bin_range中间缺少的数据点填0;  
    3. bin_range的数值改为了[bin_start, bin_end - 1];  
