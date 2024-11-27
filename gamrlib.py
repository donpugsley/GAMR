# Support functions for George Valdes AMR sensors

from dataclasses import dataclass

global dataskip

@dataclass
class AMR: 
    """Class to hold decoded GAMR sensor status bytes"""
    filter_saturated: bool
    filter_type_FIR: bool
    repeated_data: bool
    filter_not_settled: bool
    error: bool

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

def decode(data):
    """Extract magnetic field readings from binary GAMR data"""
    global dataskip # Count number of data skips
    p = 1 # Pointer to current position
    dataskip = 0 

    x,y,z,t,f = ([] for _ in range(5))

    while p < len(data):
        # 0x10 is the status byte for channel zero with all status bits zero, (00010000)=0x10/0x11/0x12/0x13 are the same for channels 1,2,3
        # We will search for four good status bytes with the correct separation 
        # If any status bit is set this search will fail, so FIR filtering on would require (00000001)=0x01/0x02/0x03/0x04
        # Find next 0x10
        d1 = data.find(b'\x10',p)
#        print ('1',end="")
        if d1==0:
            return x,y,z,t,f
        if d1 > 0:
            d2 = data.find(b'\x11',d1)
#            print ('2',end="")
            if d2==0:
                return x,y,z,t,f
            if d2 == d1+4:
                d3 = data.find(b'\x12',d2)
#                print ('3',end="")
                if d3==0:
                    return x,y,z,t,f
                if d3 == d2+4:
                    d4 = data.find(b'\x13',d3)
#                    print ('4',end="")
                    if d4==0:
                        return x,y,z,t,f
                    if d4 == d3+4: # Correct spacing - decode this packet
                        if d4+5 >= len(data):
                            return x,y,z,t,f
                        
                        p = d4 # Update pointer

                        x.append(int.from_bytes(bytearray(data[d1+1:d2])))
                        y.append(int.from_bytes(bytearray(data[d2+1:d3])))
                        z.append(int.from_bytes(bytearray(data[d3+1:d4])))
                        t.append(int.from_bytes(bytearray(data[d4+1:d4+4])))
                        f.append(data[d4+5])
                        
#                        print(': ',d1,d2,d3,d4)
                    else: # bad spacing... d4 was not preceded by d1, d2, and d3
                        p = d4
                        dataskip = dataskip + 1
                else: # bad spacing... d3 was not preceded by d1 and d2
                    p = d3
                    dataskip = dataskip + 1
            else: # bad spacing... d1 was not preceded by d1
                p = d2
                dataskip = dataskip + 1
