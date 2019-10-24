#Question B


#code

class Solution(object):
    def compareVersion(self, version1, version2):
        
        # @param {string} version1
        # @param {string} version2
        # @return {int}
        
        if '..' in (version1 and version2):
            print ('fake version string exist!')
            
        else:
            
            v1 = version1.split(".") 
            v2 = version2.split(".") 

            i = 0    

            while(i < len(v1)):    

                if int(v2[i]) > int(v1[i]): 
                    return -1                             # version2 is greater

                if int(v1[i]) > int(v2[i]): 
                    return 1                              # version1 is greater

                i += 1

            return 0                                      # those two are equal version
      

#test

#general case

#'0.1' < '1.1'
#'13.2' > '1.15'



#corner case

#'01' = '1'
#'1.0' = '1'
#'1.15' > '1.5'



#extreme case
#'2..............333', '23............223.32'   should not be considered into comparison



