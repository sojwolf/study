###
#   Initialisierung:
#       N(i,i) = 0
#       N(i,j) = 0 ... i<j<=i+3
#
#   Berechnung:
#                     ---
#                     | N(i+1,j) ...   i=ungepaart
#       N(i,j) = max <
#                     |   max   N(i+1,k-1) + N(k+1,j) + F(i,k)
#                     | i+3<k<=j
#                     ---
#
#                 ---
#                 | 1 wenn i,k in (AU,GC,GU)
#   mit F(i,k) = <
#                 | 0
#                 ---
###

