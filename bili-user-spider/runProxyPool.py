# @echo off
# cd D:/Redis/
# redis-server redis.windows.conf

# cd F:/Sources/git/SciAni/bili-user-spider/proxy_pool-1.11/Run/
# D:/Anaconda/python.exe main.py

# http://127.0.0.1:5010/get_all/

# cd F:/Sources/git/SciAni/bili-user-spider/proxy_pool-1.11/Api/
# D:/Anaconda/python.exe ProxyApi.py
# cd F:/Sources/git/SciAni/bili-user-spider/proxy_pool-1.11/Schedule/
# D:/Anaconda/python.exe ProxyRefreshSchedule.py
# cd F:/Sources/git/SciAni/bili-user-spider/proxy_pool-1.11/Schedule/
# D:/Anaconda/python.exe ProxyValidSchedule.py


import os

cmd_cd_redis  = 'cd D:/Redis/'
cmd_run_redis = 'redis-server redis.windows.conf'

cmd_cd_main   = 'cd F:/Sources/git/SciAni/bili-user-spider/proxy_pool-1.11/Run/'
cmd_run_main  = 'D:/Anaconda/python.exe main.py'

# cmd_cd_api = 'cd F:/Sources/git/SciAni/bili-user-spider/proxy_pool-1.11/Api/'
# cmd_run_api = 'D:/Anaconda/python.exe ProxyApi.py'
# cmd_cd_sch = 'cd F:/Sources/git/SciAni/bili-user-spider/proxy_pool-1.11/Schedule/'
# cmd_run_refresh = 'D:/Anaconda/python.exe ProxyRefreshSchedule.py'
# cmd_run_valid = 'D:/Anaconda/python.exe ProxyValidSchedule.py'


os.system(cmd_cd_redis)
os.system(cmd_run_redis)
os.system(cmd_cd_main)
os.system(cmd_run_main)