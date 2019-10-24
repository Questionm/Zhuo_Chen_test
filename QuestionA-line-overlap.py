#Question A


#code
class Solution(object):
  
    # @param {list} line1
    # @param {list} line2
    # @return {bool}
    
    def isLineOverlap(self, line1, line2):
        A, B = line1[0], line1[1]
        E, F = line2[0], line2[1]
        if A > F or B < E:
            return False
        return True		        
        

        
#test        
print(Solution().isLineOverlap([1,5], [2,6]))
True


print(Solution().isLineOverlap([1,5], [5,6]))
True


print(Solution().isLineOverlap([1,5], [8,10]))
False
