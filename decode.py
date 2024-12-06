# Decode a binary file of data from George Valdes' AMR sensor

import os
import sys
import numpy as np
import gamrlib as gamr

SR = 2000 

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = 'short.bin'
    filename = '/home/pugsley/Data/gamr/20241119-201730_2G_linearity.bin'

with open(filename,'rb') as f:
    D = gamr.decode(f.read())
    f.close()
        
x = D[0]
y = D[1]
z = D[2]
temp = D[3]
pps = D[4]
sign = D[5]

gamr.pplot(x,y,z,SR)

#print(f'X {np.mean(x):.0f} {np.ptp(x):.0f} pkpk\t',end="")
#print(f'Y {np.mean(y):.0f} {np.ptp(y):.0f} pkpk\t',end="")
#print(f'Z {np.mean(z):.0f} {np.ptp(z):.0f} pkpk')
#threeplot(t,x,y,z,'nT',filename)
#oneplot(t,temp,"C",filename)

 
