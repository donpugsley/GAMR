# Pugsley tweaks 11/25
import serial
import io
import numpy as np
#import matplotlib

SR = 2000

def decode(data):
    p = 1 # Pointer to current position
    x=[]
    xs=[]
    y=[]
    ys=[]
    z=[]
    zs=[]
    t=[]
    ts=[]
    f=[]

    while p < len(data):
        # Find next 0x10
        d1 = data.find(b'\x10',p)
        if d1 > 0:
            d2 = data.find(b'\x11',d1)
            if d2 == d1+4:
                d3 = data.find(b'\x12',d2)
                if d3 == d2+4:
                    d4 = data.find(b'\x13',d3)
                    if d4 == d3+4: # Correct spacing - decode this packet

                        p = d4 # Update pointer

                        xs.append(data[d1])
                        x.append(int.from_bytes(bytearray(data[d1+1:d2]),byteorder='big'))
                        ys.append(data[d2])
                        y.append(int.from_bytes(bytearray(data[d2+1:d3]),byteorder='big'))
                        zs.append(data[d3])
                        z.append(int.from_bytes(bytearray(data[d3+1:d4]),byteorder='big'))
                        ts.append(data[d4])
                        t.append(int.from_bytes(bytearray(data[d4+1:d4+4]),byteorder='big'))
                        f.append(data[d4+5])
                        
#                        print('Indices: ',d1,d2,d3,d4)
                    else: # No more 0x13
                        return x,xs,y,ys,z,zs,t,ts,f
                else: # No more 0x12
                    return x,xs,y,ys,z,zs,t,ts,f
            else: # No more 0x11
                return x,xs,y,ys,z,zs,t,ts,f
        else: # No more 0x10
            return x,xs,y,ys,z,zs,t,ts,f

ser = serial.Serial(
    port = "/dev/ttyS4",
    baudrate = 500000,
    bytesize = serial.EIGHTBITS,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    timeout = 0.01
)

# Set up buffered reader
BUFSEC = 5 # Delay at startup is to fill this entirely
READSEC = 0.2
buffered_reader = io.BufferedReader(ser,buffer_size=int(BUFSEC*2000*17)) # Hold 

while (1):
    try:
-        
        b = buffered_reader.read(int(READSEC*2000*17)) # First call reads a buffer full
        D = decode(b)
        x = np.array(D[0])
        y = np.array(D[2])
        z = np.array(D[4])
        temp = np.array(D[6])
        t = np.array(list(range(1,x.size+1)))/SR # Seconds  

        print('X ',f'{np.mean(x):.6}', '\tY ',f'{np.mean(y):.6}', '\tZ ',f'{np.mean(z):.6}')
        
    except KeyboardInterrupt:
        ser.close()
        buffered_reader.close()
    except:
        ser.close()
        buffered_reader.close()


## parse input arguments 
#parser = argparse.ArgumentParser()
#parser.add_argument("filename",nargs='?',default='gamr.bin')
#args = parser.parse_args()
#output_file = args.filename
#
## create buffer object
#buffer = io.BytesIO()
#
## lock for thread safe access to buffer
#buffer_lock = threading.Lock()
#
## flag to signal threads to stop
#stop_threads = threading.Event()
#
#def read_from_serial():
#    global buffer
#    while not stop_threads.is_set():
#        if ser.in_waiting > 0:
#            with buffer_lock:
#                buffer.write(ser.read(ser.in_waiting))
#
#        
#def save_data_to_file():
#    global buffer
#    with open(output_file,'wb') as f:
#        while not stop_threads.is_set():
#            with buffer_lock:
#                buffer.seek(0)
#                data = buffer.read() # read all available bytes
#                f.write(data)
#                buffer.seek(0) # go back to beginning of buffer
#                buffer.truncate(0) # clear buffer
##                time.sleep(0.01)
#
#def decode_data():
#    global buffer
##    with open(output_file,'wb') as f:
#    while not stop_threads.is_set():
#        with buffer_lock:
#            buffer.seek(0)
#            data = buffer.read() # read all available bytes
#                  
#            buffer.seek(0) # go back to beginning of buffer
#            buffer.truncate(0) # clear buffer
#
#try:
#    # create and start threads
#    read_thread = threading.Thread(target = read_from_serial)
##    save_thread = threading.Thread(target = decode_data)
#    read_thread.start()
# #   save_thread.start()
#    
#    # Allow threads to run indefinitely
#    read_thread.join()
#  #  save_thread.join()
#
#except KeyboardInterrupt:
#    print("exiting")
#    stop_threads.set()
#    read_thread.join()
#   # save_thread.join()
#finally:
#    ser.close()
#    print("port closed")

