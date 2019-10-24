#Question C


#-------------------------------
# The idea for this question is do a network cache with geo-search-time-expiration characteristic
#-------------------------------



#-------------------------------
# The core idea for this cache is:
# 1. can quickly pull/push data : the near real-time requirement
# 2. geo-near-fetch :close data get
# 3. time expiration : release space
#-------------------------------



#-------------------------------
# Design it by:
# 1. key-value data structure;
# 2. Regarding time expiration:
#    after every set/get operation, clean the overtime and earliest key
#    (based on recording each key's timeframe)  
##
# 3. geo idea!!!
#    listen to the host 
#    checking the nearest one by sending pin request. 
#-------------------------------



## It is designed by image the network scenario like:
## The core "-LRU cache-" contain the time control characteristics, while its 'key-value' store the network host information
##           



import time
from collections import OrderedDict


class LRUCacheDict(object):
    def __init__(self, expiration=15*60, maxsize=128):
        self.expiration = expiration
        self.maxsize = maxsize
        self.__expire_times = OrderedDict()
        self.__access_times = OrderedDict()
        self.__values = {}

        
    def __setitem__(self, key, value):
        t = int(time.time())
        self.__delitem__(key)
        self.__values[key] = value
        self.__access_times[key] = t
        self.__expire_times[key] = t + self.expiration
        self.cleanup()

        
    def __getitem__(self, key):
        t = int(time.time())
        del self.__access_times[key]
        self.__access_times[key] = t
        self.cleanup()
        return self.__values[key]

      
    def __delitem__(self, key):
        if key in self.__values:
            del self.__values[key]
            del self.__access_times[key]
            del self.__expire_times[key]


            
    def size(self):
        return len(self.__values)

 

    def clear(self):
        self.__values.clear()
        self.__access_times.clear()
        self.__expire_times.clear()

        
        
    def cleanup(self):
        t = int(time.time())
        for key, expire in self.__expire_times.iteritems():
            if expire < t:
                self.__delitem__(key)

                
        while self.size() > self.maxsize:
            for key in self.__access_times:
                self.__delitem__(key)
                break
                
                
                
                
