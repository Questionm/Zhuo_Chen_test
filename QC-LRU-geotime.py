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



import time
import socket
import os
import random
import select
from ICMP import ICMPPacket, ext_icmp_header

from collections import OrderedDict


def single_ping_request(s, addr=None):

    # Random Packet Id
    pkt_id = random.randrange(10000,65000)
    
    # Create ICMP Packet
    packet = ICMPPacket(icmp_id=pkt_id).raw

    # Send ICMP Packet
    while packet:
        sent = s.sendto(packet, (addr, 1))
        packet = packet[sent:]

    return pkt_id


def catch_ping_reply(s, ID, time_sent, timeout=1):

    while True:
        starting_time = time.time()     # Record Starting Time

        # to handle timeout function of socket
        process = select.select([s], [], [], timeout)
        
        # check if timeout
        if process[0] == []:
            return

        # receive packet
        rec_packet, addr = s.recvfrom(1024)

        # extract icmp packet from received packet 
        icmp = rec_packet[20:28]

        # extract information from icmp packet
        _id = ext_icmp_header(icmp)['id']

        # check identification
        if _id == ID:
            return ext_icmp_header(icmp)
    return


def main():
    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    
    # take Input
    addr = raw_input("[+] Enter Domain Name : ") or "www.google.com"
    
    # Request sent
    ID = single_ping_request(s, addr)

    # Catch Reply
    reply = catch_ping_reply(s, ID, time.time())

    if reply:
        print reply

    # close socket
    s.close()
    return


if __name__=='__main__':
    main() 



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
                

               
                
                
                
  

#-------------------------------
# The idea for this question is do a network cache with geo-search-time-expiration characteristic
#-------------------------------

              
