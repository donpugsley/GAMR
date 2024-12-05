# Support functions for George Valdes AMR sensors
import re
import regex
import numpy as np

def test_bit(byte, bit_position):
  """
  Tests if a specific bit is set in a byte.

  Args:
    byte: The byte to test.
    bit_position: The position of the bit to test (0-indexed, right to left).

  Returns:
    True if the bit is set, False otherwise.
  """

  return (byte & (1 << bit_position)) != 0

def nanotesla(i3): # Convert GAMR 24 bit binary to numpy float nT
    nt = np.array(i3) # this is signed 24 bit turned into signed 32 bit int
    nt = (nt.astype(float)*2*5)/(2**24)
    nt = (nt/(5e-3*182.8181818181))*1e5
    return nt

def temperature(i3): # Convert GAMR 24 bit binary to numpy float degrees C
    temp = np.array(i3)
    mv = ((temp.astype(float)*2*5)/(2**24))*1e3 # millivolts, ~-825
    # T=   ((5.506 -    sqrt((-5.506)^2+4*0.00176*(870.6-mv)))/(2*(-0.00176)))+30;
    temp = ((5.506 - np.sqrt((-5.506)**2+4*0.00176*(870.6-mv)))/(2*(-0.00176)))+30
    return temp

def decode(data):
    """Extract magnetic field readings from binary GAMR data"""
    p1 = re.compile(b'\x10(.{3})\x11(.{3})\x12(.{3})\x13(.{3})(.)') # plain
    m1 = re.findall(p1,data)
    sign = np.array([-1 if int.from_bytes(a[4]) & 0x80 > 0 else 1 for a in m1]) # x = [a * b for a, b in zip(dx,sign)]
    x = nanotesla([int.from_bytes(bytearray(a[0]),byteorder="big",signed=True) for a in m1])    
    y = nanotesla([int.from_bytes(bytearray(a[1]),byteorder="big",signed=True) for a in m1])
    z = nanotesla([int.from_bytes(bytearray(a[2]),byteorder="big",signed=True) for a in m1])
    t = temperature([int.from_bytes(bytearray(a[3]),byteorder="big",signed=True) for a in m1])
    pps = [True if int.from_bytes(a[4]) & 0x01 > 0 else False for a in m1]

    return x,y,z,t,pps,sign


def olddecode(data):
    #
    #    m3 = re.finditer(p1,data)
    #    p2 = re.compile(b'\x10(?P<X>.{3})\x11(?P<Y>.{3})\x12(?P<Z>.{3})\x13(?P<F>.{4})') # named
    #    m2 = re.findall(p2,data)

    # Alternate brute force method
    p = 1 # Pointer to current position
    x,y,z,t,f,dataskip = ([] for _ in range(6))
    while p < len(data):
        # 0x10 is the status byte for channel zero with all status bits zero, (00010000)=0x10/0x11/0x12/0x13 are the same for channels 1,2,3
        # We will search for four good status bytes with the correct separation 
        # If any status bit is set this search will fail, so FIR filtering on would require (00000001)=0x01/0x02/0x03/0x04
        # Find next 0x10

        d1 = data.find(b'\x10',p)
#        print ('1',end="")
        if d1==0:
            return x,y,z,t,f,dataskip
        if d1 > 0:
            d2 = data.find(b'\x11',d1)
#            print ('2',end="")
            if d2==0:
                return x,y,z,t,f,dataskip
            if d2 == d1+4:
                d3 = data.find(b'\x12',d2)
#                print ('3',end="")
                if d3==0:
                    return x,y,z,t,f,dataskip
                if d3 == d2+4:
                    d4 = data.find(b'\x13',d3)
#                    print ('4',end="")
                    if d4==0:
                        return x,y,z,t,f,dataskip
                    if d4 == d3+4: # Correct spacing - decode this packet
                        if d4+5 >= len(data):
                            return x,y,z,t,f,dataskip
                        
                        p = d4 # Update pointer

                        x.append(int.from_bytes(bytearray(data[d1+1:d2]),byteorder="big",signed=True))
                        y.append(int.from_bytes(bytearray(data[d2+1:d3]),byteorder="big",signed=True))
                        z.append(int.from_bytes(bytearray(data[d3+1:d4]),byteorder="big",signed=True))
                        t.append(int.from_bytes(bytearray(data[d4+1:d4+4]),byteorder="big",signed=True))
                        f.append(data[d4+5])
                        
#                        print(': ',d1,d2,d3,d4)
                    else: # bad spacing... d4 was not preceded by d1, d2, and d3
                        print(f'Bad d4 at d1 = ',d1)
                        p = d4
                        dataskip.append(p) 
                else: # bad spacing... d3 was not preceded by d1 and d2
                    print(f'Bad d3 at d1 = ',d1)
                    p = d3
                    dataskip.append(p) 
            else: # bad spacing... d2 was not preceded by d1
                print(f'Bad d2 at d1 = ',d1)
                p = d2
                dataskip.append(p) 
        else: # No more 0x10
            return x,y,z,t,f,dataskip
    # Fall through
    return x,y,z,t,f,dataskip