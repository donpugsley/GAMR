# Decode a binary file of data from George Valdes' AMR sensor
# Data for one channel is a status byte and 24 bits (3 bytes) of data, 4 bytes total
# A data packet is 4 channels plus one flag byte, so 17 bytes

import sys
import numpy as np
from plotters import oneplot,threeplot
import gamrlib as gamr

SR = 2000 

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = 'test.bin'

with open(filename,'rb') as f:
    D = gamr.decode(f.read())
    if len(D)==0: # Empty means EOF
        f.close()
    
n = len(D[0])

print (f'{n} points with {gamr.dataskip} skips over {n/SR} seconds, {(n/SR)/60} minutes...')

# Decode status

# Grab data and convert to floats
x = np.array(D[0])
x = x.astype(float)
y = np.array(D[1])
y = y.astype(float)
z = np.array(D[2])
z = z.astype(float)
temp = np.array(D[3])
temp = temp.astype(float)
flag = D[4]

# Create time, assuming no skips
t = np.array(list(range(1,x.size+1)))/SR # Seconds
t = t.astype(float)

threeplot(t,x,y,z,'Count',filename)
 