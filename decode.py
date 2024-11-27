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
    filename = 'short.bin'

with open(filename,'rb') as f:
    D = gamr.decode(f.read())
    if len(D)==0: # Empty means EOF
        f.close()
    
n = len(D[0])
skips = D[5] # byte offsets of data skips

print (f'{n} points with {len(skips)} skips over {n/SR} seconds, {(n/SR)/60} minutes...')

# Decode status

# Grab data and convert to floats
x = np.array(D[0])
x = (x.astype(float)*2*5)/(2**24) # voltage
x = (x/(5e-3*182.8181818181))*1e5 # nT
y = np.array(D[1]) # this is signed 24 bit turned into signed 32 bit int
y = (y.astype(float)*2*5)/(2**24)
y = (y/(5e-3*182.8181818181))*1e5
z = np.array(D[2])
z = (z.astype(float)*2*5)/(2**24)
z = (z/(5e-3*182.8181818181))*1e5
temp = np.array(D[3])
temp = ((temp.astype(float)*2*5)/(2**24))*1e3*-1
temp = ((5.506-np.sqrt((-5.506)**2+4*0.00176*(870.6-temp)))/(2*(-0.00176)))+30
temp = temp/10 # Bullshit approximate fix, not sure whats wrong with previous line
flag = D[4]

# Create time, assuming no skips
t = np.array(list(range(1,x.size+1)))/SR # Seconds
t = t.astype(float)

threeplot(t,x,y,z,'Count',filename)
oneplot(t,temp,"C",filename)

 
