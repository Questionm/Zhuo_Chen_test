#Question C


#-------------------------------
# The core idea for this cache is:
# 1. can quickly pull/push data : the near real-time requirement
# 2. geo-near-fetch :close data get
# 3. time expiration : release space
#-------------------------------



#-------------------------------
# Design it by:
# 1. key-value data structure;

# 2. geo idea:
#    check the near ip by sending + gathering ping request
##
# 3. Regarding time expiration:
#    after every set/get operation, clean the overtime and earliest key
#    (based on recording each key's timeframe)  
#-------------------------------



## It is designed by imaging a network scenario like:
## The core is "-LRU cache-", its 'key-value' used to store network host information, cache contains the time control characteristics
## The nearest availability can be filtered by ping listening (light while consistent)   


import os
import socket
import struct
import array

from collections import OrderedDict

class Pinger(object):
    
   
    def __init__(self,timeout=3):
        self.timeout = timeout
        self.__id = os.getpid()
        self.__data = struct.pack('h',1)

        
    @property
    def __icmpSocket(self):
        icmp = socket.getprotobyname("icmp")
        sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,icmp)
        return sock


    def __doCksum(self,packet)
        words = array.array('h',packet)
        sum = 0
        for word in words:
            sum += (word & 0xffff)
        sum = (sum >> 16) + (sum & 0xffff)
        sum += (sum >> 16) 
        return (~sum) & 0xffff

    
    @property
    def __icmpPacket(self):                                                    # construct icmp packet
        header = struct.pack('bbHHh',8,0,0,self.__id,0)
        packet = header + self.__data
        cksum = self.__doCksum(packet)
        header = struct.pack('bbHHh',8,0,cksum,self.__id,0)
        return header + self.__data 


    def sendPing(self,target_host):
        
        try:
            socket.gethostbyname(target_host)

            sock = self.__icmpSocket
            sock.settimeout(self.timeout)

            packet = self.__icmpPacket

            sock.sendto(packet,(target_host,1))                                # send the icmp packet to the host 

            ac_ip = sock.recvfrom(1024)[1][0]
            print '[+] %s active'%(ac_ip)
            return ac_ip
        except Exception,e:
            sock.close()

            
# s = Pinger()
# s.sendPing('192.168.1.103')



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
                

               
# test 

import ipaddress

subnet = ipaddress.ip_network('192.168.1.0/24', strict=False)
for i in subnet.hosts():
    i = str(i)
    i = Pinger().sendPing(i)
    print (LRUCacheDict(index(subnet.hosts(i),i))
    
                
                
              
