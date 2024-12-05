# Decode a binary file of data from George Valdes' AMR sensor
# Data for one channel is a status byte and 24 bits (3 bytes) of data, 4 bytes total
# A data packet is 4 channels plus one flag byte, so 17 bytes

import os
import sys
import numpy as np
from plotters import oneplot,threeplot,plot
import plotille
import gamrlib as gamr

SR = 2000 

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = 'short.bin'
    filename = '/home/pugsley/Data/gamr/20241119-201730_2G_linearity.bin'

with open(filename,'rb') as f:
    D = gamr.decode(f.read())
    if len(D)==0: # Empty means EOF
        f.close()
    
x = D[0]
y = D[1]
z = D[2]
temp = D[3]
pps = D[4]
sign = D[5]

# Create time, assuming no skips
t = np.array(list(range(1,len(x)+1)))/SR # Seconds
t = t.astype(float)

n = len(D[0])
# skips = D[5] # byte offsets of data skips
# print (f'{n} points with {len(skips)} skips over {n/SR} seconds, {(n/SR)/60} minutes...')
print (f'{n} points over {n/SR:.1f} seconds, {(n/SR)/60:.1f} minutes...')

# Decode status

# # Grab data and convert to floats
# x = np.array(D[0])
# x = (x.astype(float)*2*5)/(2**24) # voltage
# x = (x/(5e-3*182.8181818181))*1e5 # nT
# y = np.array(D[1]) # this is signed 24 bit turned into signed 32 bit int
# y = (y.astype(float)*2*5)/(2**24)
# y = (y/(5e-3*182.8181818181))*1e5
# z = np.array(D[2])
# z = (z.astype(float)*2*5)/(2**24)
# z = (z/(5e-3*182.8181818181))*1e5
# temp = np.array(D[3])
# mv = ((temp.astype(float)*2*5)/(2**24))*1e3*-1 # millivolts, ~-825

# # T=   ((5.506 -    sqrt((-5.506)^2+4*0.00176*(870.6-mv)))/(2*(-0.00176)))+30;

# temp = ((5.506 - np.sqrt((-5.506)**2+4*0.00176*(870.6-mv)))/(2*(-0.00176)))+30
# temp = temp/10 # Bullshit approximate fix, not sure whats wrong with previous line
# flag = D[4]


#os.system('clear')
# f = plotille.Figure()
# f.width = 100
# f.height = 40
# f.set_x_limits(min_=min(t),max_=max(t))
# mmax = max(max(x),max(y),max(z))
# mmin = min(min(x),min(y),min(z))
# f.set_y_limits(min_=mmin*1.05,max_=mmax*1.05)
# f.color_mode = 'names'
# f.scatter(t,x,lc='red',label='X')
# f.scatter(t,y,lc='green',label='Y')
# f.scatter(t,z,lc='blue',label='Z')
# print(f.show(legend=True))

# print(f'X {np.mean(x):.0f} {np.ptp(x):.0f} pkpk\t',end="")
# print(f'Y {np.mean(y):.0f} {np.ptp(y):.0f} pkpk\t',end="")
# print(f'Z {np.mean(z):.0f} {np.ptp(z):.0f} pkpk')


threeplot(t,x,y,z,'nT',filename)
oneplot(t,temp,"C",filename)

 
